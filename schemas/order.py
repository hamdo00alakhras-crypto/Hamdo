from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from models.order import OrderStatus


class OrderItemBase(BaseModel):
    product_id: int
    quantity: int = Field(..., ge=1)
    unit_price: float = Field(..., ge=0)


class OrderItemResponse(OrderItemBase):
    id: int
    order_id: int
    subtotal: float

    class Config:
        from_attributes = True


class OrderBase(BaseModel):
    payment_method_id: Optional[int] = None
    shipping_address: Optional[str] = None
    transfer_receipt: Optional[str] = None


class OrderCreate(OrderBase):
    pass


class OrderResponse(OrderBase):
    id: int
    user_id: int
    order_date: Optional[datetime] = None
    status: OrderStatus = OrderStatus.PENDING
    total_amount: float = 0.0
    items: List[OrderItemResponse] = []

    class Config:
        from_attributes = True


class OrderStatusUpdate(BaseModel):
    status: OrderStatus