from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload
from typing import Optional, List
from database import get_db
from models.product import Product, ProductImage, product_categories
from models.category import Category
from schemas.product import ProductResponse, ProductCreate, ProductUpdate, ProductFilter

router = APIRouter(prefix="/api/products", tags=["Products"])


@router.get("/", response_model=List[ProductResponse])
def get_products(
    category_id: Optional[int] = Query(None),
    material: Optional[str] = Query(None),
    min_price: Optional[float] = Query(None),
    max_price: Optional[float] = Query(None),
    karat: Optional[str] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    query = db.query(Product).options(joinedload(Product.images))

    if category_id:
        query = query.join(product_categories).filter(product_categories.c.category_id == category_id)

    if material:
        query = query.filter(Product.material.ilike(f"%{material}%"))

    if min_price is not None:
        query = query.filter(Product.price >= min_price)

    if max_price is not None:
        query = query.filter(Product.price <= max_price)

    if karat:
        query = query.filter(Product.karat == karat)

    products = query.offset(skip).limit(limit).all()
    return products


@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = (
        db.query(Product)
        .options(joinedload(Product.images))
        .filter(Product.id == product_id)
        .first()
    )
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.get("/categories/", tags=["Categories"])
def get_categories(db: Session = Depends(get_db)):
    categories = db.query(Category).all()
    return categories