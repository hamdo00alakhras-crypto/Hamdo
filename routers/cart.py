from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models.user import User
from models.product import Product
from models.cart import Cart, CartItem
from schemas.cart import CartResponse, CartItemCreate, CartItemWithProduct
from utils.auth import get_current_user

router = APIRouter(prefix="/api/cart", tags=["Cart"])


def get_or_create_cart(db: Session, user_id: int) -> Cart:
    cart = db.query(Cart).filter(Cart.user_id == user_id).first()
    if not cart:
        cart = Cart(user_id=user_id)
        db.add(cart)
        db.commit()
        db.refresh(cart)
    return cart


def calculate_cart_total(cart: Cart) -> float:
    total = 0.0
    for item in cart.items:
        if item.product:
            total += item.product.price * item.quantity
    return total


def format_cart_response(cart: Cart) -> CartResponse:
    items = []
    for item in cart.items:
        items.append(
            CartItemWithProduct(
                id=item.id,
                cart_id=item.cart_id,
                product_id=item.product_id,
                quantity=item.quantity,
                product_name=item.product.name if item.product else None,
                product_price=item.product.price if item.product else None,
                product_image=item.product.image_path if item.product else None,
            )
        )
    total = calculate_cart_total(cart)
    return CartResponse(
        id=cart.id,
        user_id=cart.user_id,
        updated_at=cart.updated_at,
        items=items,
        total_amount=total,
    )


@router.get("/", response_model=CartResponse)
def get_cart(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    cart = get_or_create_cart(db, current_user.id)
    return format_cart_response(cart)


@router.post("/add", response_model=CartResponse, status_code=status.HTTP_201_CREATED)
def add_to_cart(
    item_data: CartItemCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    product = db.query(Product).filter(Product.id == item_data.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    if product.stock_quantity < item_data.quantity:
        raise HTTPException(status_code=400, detail="Not enough stock")

    cart = get_or_create_cart(db, current_user.id)

    existing_item = (
        db.query(CartItem)
        .filter(CartItem.cart_id == cart.id, CartItem.product_id == item_data.product_id)
        .first()
    )

    if existing_item:
        existing_item.quantity += item_data.quantity
    else:
        new_item = CartItem(
            cart_id=cart.id,
            product_id=item_data.product_id,
            quantity=item_data.quantity,
        )
        db.add(new_item)

    db.commit()
    db.refresh(cart)
    return format_cart_response(cart)


@router.put("/update/{item_id}", response_model=CartResponse)
def update_cart_item(
    item_id: int,
    quantity: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    cart = db.query(Cart).filter(Cart.user_id == current_user.id).first()
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")

    item = db.query(CartItem).filter(CartItem.id == item_id, CartItem.cart_id == cart.id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Cart item not found")

    if quantity <= 0:
        db.delete(item)
    else:
        item.quantity = quantity

    db.commit()
    db.refresh(cart)
    return format_cart_response(cart)


@router.delete("/remove/{item_id}", response_model=CartResponse)
def remove_from_cart(
    item_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    cart = db.query(Cart).filter(Cart.user_id == current_user.id).first()
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")

    item = db.query(CartItem).filter(CartItem.id == item_id, CartItem.cart_id == cart.id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Cart item not found")

    db.delete(item)
    db.commit()
    db.refresh(cart)
    return format_cart_response(cart)


@router.delete("/clear", response_model=CartResponse)
def clear_cart(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    cart = db.query(Cart).filter(Cart.user_id == current_user.id).first()
    if cart:
        db.query(CartItem).filter(CartItem.cart_id == cart.id).delete()
        db.commit()
        db.refresh(cart)
    return format_cart_response(cart) if cart else CartResponse(id=0, user_id=current_user.id, items=[], total_amount=0.0)