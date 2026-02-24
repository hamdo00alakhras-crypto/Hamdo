import enum
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Text, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


class OrderStatus(enum.Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    payment_method_id = Column(Integer, ForeignKey("payment_methods.id"), nullable=True)
    order_date = Column(DateTime, server_default=func.now())
    status = Column(Enum(OrderStatus), default=OrderStatus.PENDING)
    total_amount = Column(Float, default=0.0)
    shipping_address = Column(Text, nullable=True)
    transfer_receipt = Column(String(255), nullable=True)

    user = relationship("User", backref="orders")
    payment_method = relationship("PaymentMethod")
    items = relationship(
        "OrderItem",
        back_populates="order",
        cascade="all, delete-orphan",
    )


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, default=1)
    unit_price = Column(Float, nullable=False)
    subtotal = Column(Float, nullable=False)

    order = relationship("Order", back_populates="items")
    product = relationship("Product")