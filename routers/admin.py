from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models.user import User
from models.product import Product, ProductImage, product_categories
from models.category import Category
from models.payment import PaymentMethod
from models.jeweler import Jeweler
from models.order import Order, OrderStatus
from models.design import DesignRequest, DesignRequestStatus
from schemas.product import ProductCreate, ProductUpdate, ProductResponse
from schemas.category import CategoryCreate, CategoryResponse
from schemas.payment import PaymentMethodCreate, PaymentMethodResponse
from schemas.jeweler import JewelerCreate, JewelerResponse
from schemas.order import OrderStatusUpdate, OrderResponse
from schemas.design import DesignRequestResponse, DesignRequestUpdate
from utils.auth import get_current_user

router = APIRouter(prefix="/api/admin", tags=["Admin"])


@router.post("/products", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(product_data: ProductCreate, db: Session = Depends(get_db)):
    jeweler = db.query(Jeweler).filter(Jeweler.id == product_data.jeweler_id).first()
    if not jeweler:
        raise HTTPException(status_code=404, detail="Jeweler not found")

    new_product = Product(
        jeweler_id=product_data.jeweler_id,
        name=product_data.name,
        material=product_data.material,
        karat=product_data.karat,
        weight=product_data.weight,
        price=product_data.price,
        stock_quantity=product_data.stock_quantity,
        description=product_data.description,
        image_path=product_data.image_path,
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    if product_data.category_ids:
        for category_id in product_data.category_ids:
            db.execute(
                product_categories.insert().values(
                    product_id=new_product.id, category_id=category_id
                )
            )
        db.commit()
        db.refresh(new_product)

    return new_product


@router.put("/products/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int,
    product_data: ProductUpdate,
    db: Session = Depends(get_db),
):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    update_data = product_data.dict(exclude_unset=True, exclude={"category_ids"})
    for key, value in update_data.items():
        setattr(product, key, value)

    if product_data.category_ids is not None:
        db.execute(
            product_categories.delete().where(product_categories.c.product_id == product_id)
        )
        for category_id in product_data.category_ids:
            db.execute(
                product_categories.insert().values(
                    product_id=product_id, category_id=category_id
                )
            )

    db.commit()
    db.refresh(product)
    return product


@router.delete("/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(product)
    db.commit()
    return {"message": "Product deleted successfully"}


@router.post("/categories", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
def create_category(category_data: CategoryCreate, db: Session = Depends(get_db)):
    if category_data.parent_id:
        parent = db.query(Category).filter(Category.id == category_data.parent_id).first()
        if not parent:
            raise HTTPException(status_code=404, detail="Parent category not found")

    new_category = Category(
        name=category_data.name,
        parent_id=category_data.parent_id,
    )
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category


@router.delete("/categories/{category_id}")
def delete_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    db.delete(category)
    db.commit()
    return {"message": "Category deleted successfully"}


@router.post("/payment-methods", response_model=PaymentMethodResponse, status_code=status.HTTP_201_CREATED)
def create_payment_method(payment_data: PaymentMethodCreate, db: Session = Depends(get_db)):
    new_payment = PaymentMethod(**payment_data.dict())
    db.add(new_payment)
    db.commit()
    db.refresh(new_payment)
    return new_payment


@router.get("/payment-methods", response_model=List[PaymentMethodResponse])
def get_payment_methods(db: Session = Depends(get_db)):
    payments = db.query(PaymentMethod).all()
    return payments


@router.put("/payment-methods/{payment_id}", response_model=PaymentMethodResponse)
def update_payment_method(
    payment_id: int,
    payment_data: PaymentMethodCreate,
    db: Session = Depends(get_db),
):
    payment = db.query(PaymentMethod).filter(PaymentMethod.id == payment_id).first()
    if not payment:
        raise HTTPException(status_code=404, detail="Payment method not found")
    for key, value in payment_data.dict().items():
        setattr(payment, key, value)
    db.commit()
    db.refresh(payment)
    return payment


@router.delete("/payment-methods/{payment_id}")
def delete_payment_method(payment_id: int, db: Session = Depends(get_db)):
    payment = db.query(PaymentMethod).filter(PaymentMethod.id == payment_id).first()
    if not payment:
        raise HTTPException(status_code=404, detail="Payment method not found")
    db.delete(payment)
    db.commit()
    return {"message": "Payment method deleted successfully"}


@router.get("/orders", response_model=List[OrderResponse])
def get_all_orders(db: Session = Depends(get_db)):
    orders = db.query(Order).all()
    return orders


@router.put("/orders/{order_id}/status", response_model=OrderResponse)
def update_order_status(
    order_id: int,
    status_data: OrderStatusUpdate,
    db: Session = Depends(get_db),
):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    order.status = status_data.status
    db.commit()
    db.refresh(order)
    return order


@router.get("/design-requests", response_model=List[DesignRequestResponse])
def get_all_design_requests(db: Session = Depends(get_db)):
    requests = db.query(DesignRequest).all()
    return requests


@router.put("/design-requests/{request_id}", response_model=DesignRequestResponse)
def update_design_request(
    request_id: int,
    request_data: DesignRequestUpdate,
    db: Session = Depends(get_db),
):
    design_request = db.query(DesignRequest).filter(DesignRequest.id == request_id).first()
    if not design_request:
        raise HTTPException(status_code=404, detail="Design request not found")

    update_data = request_data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(design_request, key, value)

    db.commit()
    db.refresh(design_request)
    return design_request


@router.post("/jewelers", response_model=JewelerResponse, status_code=status.HTTP_201_CREATED)
def create_jeweler(jeweler_data: JewelerCreate, db: Session = Depends(get_db)):
    new_jeweler = Jeweler(**jeweler_data.dict())
    db.add(new_jeweler)
    db.commit()
    db.refresh(new_jeweler)
    return new_jeweler