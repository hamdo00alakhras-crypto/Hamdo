from sqlalchemy import Column, Integer, String, Boolean, Text
from database import Base


class PaymentMethod(Base):
    __tablename__ = "payment_methods"

    id = Column(Integer, primary_key=True, index=True)
    method_name = Column(String(100), nullable=False)
    qr_code_image = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True)
    notes = Column(Text, nullable=True)