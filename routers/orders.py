from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models.user import User
from models.order import Order, OrderItem, OrderStatus
from models.cart import Cart, CartItem
from schemas.order import OrderCreate, OrderResponse, OrderStatusUpdate
from utils.auth import get_current_user

router = APIRouter(prefix="/api/orders", tags=["Orders"])


@router.get("/", response_model=List[OrderResponse])
def get_orders(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    orders = db.query(Order).filter(Order.user_id == current_user.id).all()
    return orders


@router.get("/{order_id}", response_model=OrderResponse)
def get_order(
    order_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    order = db.query(Order).filter(Order.id == order_id, Order.user_id == current_user.id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@router.post("/checkout", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def checkout(
    order_data: OrderCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    cart = db.query(Cart).filter(Cart.user_id == current_user.id).first()
    if not cart or not cart.items:
        raise HTTPException(status_code=400, detail="Cart is empty")

    total_amount = 0.0
    order_items = []

    for cart_item in cart.items:
        if cart_item.product.stock_quantity < cart_item.quantity:
            raise HTTPException(
                status_code=400,
                detail=f"Not enough stock for product: {cart_item.product.name}",
            )

        unit_price = cart_item.product.price
        subtotal = unit_price * cart_item.quantity
        total_amount += subtotal

        order_item = OrderItem(
            product_id=cart_item.product_id,
            quantity=cart_item.quantity,
            unit_price=unit_price,
            subtotal=subtotal,
        )
        order_items.append(order_item)

        cart_item.product.stock_quantity -= cart_item.quantity

    new_order = Order(
        user_id=current_user.id,
        payment_method_id=order_data.payment_method_id,
        shipping_address=order_data.shipping_address,
        transfer_receipt=order_data.transfer_receipt,
        total_amount=total_amount,
        status=OrderStatus.PENDING,
    )
    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    for item in order_items:
        item.order_id = new_order.id
        db.add(item)

    db.query(CartItem).filter(CartItem.cart_id == cart.id).delete()

    db.commit()
    db.refresh(new_order)
    return new_order