from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class PaymentMethodBase(BaseModel):
    method_name: str
    qr_code_image: Optional[str] = None
    is_active: bool = True
    notes: Optional[str] = None


class PaymentMethodCreate(PaymentMethodBase):
    pass


class PaymentMethodResponse(PaymentMethodBase):
    id: int

    class Config:
        from_attributes = True