import os
import base64
import json
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import google.generativeai as genai
from database import get_db
from models.user import User
from models.design import UserGeneratedDesign
from schemas.design import DesignInput, DesignResponse
from utils.auth import get_current_user
from config import settings

router = APIRouter(prefix="/api/ai", tags=["AI Design"])

DESIGNS_DIR = "static/generated_designs"

if settings.GEMINI_API_KEY:
    genai.configure(api_key=settings.GEMINI_API_KEY)


def ensure_designs_dir():
    if not os.path.exists(DESIGNS_DIR):
        os.makedirs(DESIGNS_DIR)


def construct_prompt(data: DesignInput) -> str:
    gemstone_desc = ""
    if data.gemstone_type and data.gemstone_type.lower() != "none":
        gemstone_desc = f"featuring a {data.gemstone_color or 'natural colored'} {data.gemstone_type}"
        if data.gemstone_color:
            gemstone_desc = f"featuring a {data.gemstone_color} {data.gemstone_type}"

    prompt = f"""
    Create a photorealistic image of an exquisite {data.type.lower()} jewelry piece.
    
    Design Specifications:
    - Type: {data.type}
    - Material: {data.material} ({data.karat})
    - Primary Color: {data.color}
    - Shape/Style: {data.shape}
    {f'- Gemstone: {gemstone_desc}' if gemstone_desc else '- No gemstones'}
    
    Requirements:
    - Professional jewelry photography style
    - Clean white or light gradient background
    - Proper lighting showing the {data.material}'s luster and shine
    - High detail showing craftsmanship
    - Realistic metallic reflections and shadows
    - The jewelry should be the focal point, centered in frame
    - Multiple angles view if possible
    
    Style: Elegant, luxurious, high-end jewelry catalog photography
    Quality: Ultra-high detail, 8K quality rendering
    """
    return prompt.strip()


def save_image(image_data: bytes, user_id: int) -> str:
    ensure_designs_dir()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"design_{user_id}_{timestamp}.png"
    filepath = os.path.join(DESIGNS_DIR, filename)

    with open(filepath, "wb") as f:
        f.write(image_data)

    return f"/static/generated_designs/{filename}"


@router.post("/generate-design", response_model=DesignResponse, status_code=status.HTTP_201_CREATED)
async def generate_design(
    design_input: DesignInput,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not settings.GEMINI_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Gemini API key not configured",
        )

    prompt = construct_prompt(design_input)

    try:
        model = genai.GenerativeModel("gemini-3-pro-image-preview")
        
        response = await model.generate_content_async(
            prompt,
            generation_config={
                "response_modalities": ["image", "text"],
            }
        )

        image_data = None
        for part in response.parts:
            if hasattr(part, "inline_data"):
                image_data = part.inline_data.data
                break

        if not image_data:
            text_response = response.text if hasattr(response, "text") else "No image generated"
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to generate image. Response: {text_response}",
            )

        if isinstance(image_data, str):
            image_bytes = base64.b64decode(image_data)
        else:
            image_bytes = image_data

        image_url = save_image(image_bytes, current_user.id)

        new_design = UserGeneratedDesign(
            user_id=current_user.id,
            selected_options=design_input.dict(),
            generated_image_url=image_url,
        )
        db.add(new_design)
        db.commit()
        db.refresh(new_design)

        return new_design

    except Exception as e:
        if "API key" in str(e) or "authentication" in str(e).lower():
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Invalid Gemini API key or authentication failed",
            )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating design: {str(e)}",
        )


@router.get("/my-designs", response_model=list[DesignResponse])
def get_my_designs(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    designs = (
        db.query(UserGeneratedDesign)
        .filter(UserGeneratedDesign.user_id == current_user.id)
        .order_by(UserGeneratedDesign.created_at.desc())
        .all()
    )
    return designs