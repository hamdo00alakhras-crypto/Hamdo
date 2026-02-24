from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class CartItemBase(BaseModel):
    product_id: int
    quantity: int = Field(default=1, ge=1)


class CartItemCreate(CartItemBase):
    pass


class CartItemUpdate(BaseModel):
    quantity: int = Field(..., ge=1)


class CartItemResponse(CartItemBase):
    id: int
    cart_id: int

    class Config:
        from_attributes = True


class CartItemWithProduct(CartItemResponse):
    product_name: Optional[str] = None
    product_price: Optional[float] = None
    product_image: Optional[str] = None


class CartResponse(BaseModel):
    id: int
    user_id: int
    updated_at: Optional[datetime] = None
    items: List[CartItemWithProduct] = []
    total_amount: float = 0.0

    class Config:
        from_attributes = True