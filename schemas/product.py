from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class ProductImageBase(BaseModel):
    image_path: str
    display_order: int = 0


class ProductImageCreate(ProductImageBase):
    pass


class ProductImageResponse(ProductImageBase):
    id: int
    product_id: int

    class Config:
        from_attributes = True


class ProductBase(BaseModel):
    name: str
    material: Optional[str] = None
    karat: Optional[str] = None
    weight: Optional[float] = None
    price: float = Field(..., ge=0)
    stock_quantity: int = Field(default=0, ge=0)
    description: Optional[str] = None
    image_path: Optional[str] = None


class ProductCreate(ProductBase):
    jeweler_id: int
    category_ids: List[int] = []


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    material: Optional[str] = None
    karat: Optional[str] = None
    weight: Optional[float] = None
    price: Optional[float] = Field(None, ge=0)
    stock_quantity: Optional[int] = Field(None, ge=0)
    description: Optional[str] = None
    image_path: Optional[str] = None
    category_ids: Optional[List[int]] = None


class ProductResponse(ProductBase):
    id: int
    jeweler_id: int
    images: List[ProductImageResponse] = []

    class Config:
        from_attributes = True


class ProductFilter(BaseModel):
    category_id: Optional[int] = None
    material: Optional[str] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    karat: Optional[str] = None