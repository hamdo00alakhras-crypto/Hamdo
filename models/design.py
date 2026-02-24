import enum
import json
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text, Enum, Float, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


class DesignRequestStatus(enum.Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    COMPLETED = "completed"


class UserGeneratedDesign(Base):
    __tablename__ = "user_generated_designs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    selected_options = Column(JSON, nullable=True)
    generated_image_url = Column(String(255), nullable=True)
    created_at = Column(DateTime, server_default=func.now())

    user = relationship("User", backref="generated_designs")


class DesignRequest(Base):
    __tablename__ = "design_requests"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    jeweler_id = Column(Integer, ForeignKey("jewelers.id"), nullable=True)
    generated_design_id = Column(Integer, ForeignKey("user_generated_designs.id"), nullable=True)
    request_date = Column(DateTime, server_default=func.now())
    description = Column(Text, nullable=True)
    attachment_url = Column(String(255), nullable=True)
    estimated_budget = Column(Float, nullable=True)
    jeweler_price_offer = Column(Float, nullable=True)
    status = Column(Enum(DesignRequestStatus), default=DesignRequestStatus.PENDING)

    user = relationship("User", backref="design_requests")
    jeweler = relationship("Jeweler", backref="design_requests")
    generated_design = relationship("UserGeneratedDesign", backref="design_requests")