from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text, Table
from sqlalchemy.orm import relationship
from database import Base

product_categories = Table(
    "product_categories",
    Base.metadata,
    Column("product_id", Integer, ForeignKey("products.id"), primary_key=True),
    Column("category_id", Integer, ForeignKey("categories.id"), primary_key=True),
)


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    jeweler_id = Column(Integer, ForeignKey("jewelers.id"), nullable=False)
    name = Column(String(200), nullable=False)
    material = Column(String(50), nullable=True)
    karat = Column(String(10), nullable=True)
    weight = Column(Float, nullable=True)
    price = Column(Float, nullable=False)
    stock_quantity = Column(Integer, default=0)
    description = Column(Text, nullable=True)
    image_path = Column(String(255), nullable=True)

    jeweler = relationship("Jeweler", backref="products")
    categories = relationship(
        "Category",
        secondary=product_categories,
        backref="products",
    )
    images = relationship(
        "ProductImage",
        back_populates="product",
        cascade="all, delete-orphan",
    )


class ProductImage(Base):
    __tablename__ = "product_images"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    image_path = Column(String(255), nullable=False)
    display_order = Column(Integer, default=0)

    product = relationship("Product", back_populates="images")