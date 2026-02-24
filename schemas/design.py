from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime
from models.design import DesignRequestStatus


class DesignInput(BaseModel):
    type: str = Field(..., description="Jewelry type: Ring, Necklace, Bracelet, Earrings, etc.")
    color: str = Field(..., description="Primary color of the jewelry")
    shape: str = Field(..., description="Shape or style of the jewelry")
    material: str = Field(..., description="Material: Silver, Gold, Platinum, etc.")
    karat: str = Field(..., description="Karat: 18k, 21k, 22k, 24k, etc.")
    gemstone_type: str = Field(default="None", description="Gemstone type: Diamond, Ruby, Emerald, Sapphire, None, etc.")
    gemstone_color: Optional[str] = Field(default=None, description="Color of the gemstone if applicable")


class DesignResponse(BaseModel):
    id: int
    user_id: int
    selected_options: Optional[Dict[str, Any]] = None
    generated_image_url: Optional[str] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class DesignRequestBase(BaseModel):
    description: Optional[str] = None
    attachment_url: Optional[str] = None
    estimated_budget: Optional[float] = None


class DesignRequestCreate(DesignRequestBase):
    jeweler_id: Optional[int] = None
    generated_design_id: Optional[int] = None


class DesignRequestUpdate(BaseModel):
    jeweler_id: Optional[int] = None
    jeweler_price_offer: Optional[float] = None
    status: Optional[DesignRequestStatus] = None


class DesignRequestResponse(DesignRequestBase):
    id: int
    user_id: int
    jeweler_id: Optional[int] = None
    generated_design_id: Optional[int] = None
    request_date: Optional[datetime] = None
    jeweler_price_offer: Optional[float] = None
    status: DesignRequestStatus = DesignRequestStatus.PENDING

    class Config:
        from_attributes = True