import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import text
from database import engine, SessionLocal
from models.user import User
from models.jeweler import Jeweler
from models.category import Category
from models.payment import PaymentMethod
from models.product import Product, ProductImage, product_categories
from models.cart import Cart, CartItem
from models.order import Order, OrderItem
from models.design import UserGeneratedDesign, DesignRequest
from utils.security import get_password_hash


def clear_database():
    print("Clearing existing data...")
    db = SessionLocal()
    try:
        tables = [
            "design_requests",
            "user_generated_designs",
            "order_items",
            "orders",
            "cart_items",
            "carts",
            "product_categories",
            "product_images",
            "products",
            "categories",
            "payment_methods",
            "jewelers",
            "users",
        ]
        for table in tables:
            db.execute(text(f"SET FOREIGN_KEY_CHECKS = 0"))
            db.execute(text(f"TRUNCATE TABLE {table}"))
            db.execute(text(f"SET FOREIGN_KEY_CHECKS = 1"))
        db.commit()
        print("Database cleared successfully!")
    except Exception as e:
        print(f"Error clearing database: {e}")
        db.rollback()
    finally:
        db.close()


def seed_users(db):
    print("Seeding users...")
    users = [
        User(
            username="admin",
            email="admin@jewelry.com",
            password=get_password_hash("admin123"),
            first_name="Admin",
            last_name="User",
            phone="+1234567890",
            address="123 Admin Street, Admin City",
        ),
        User(
            username="john_doe",
            email="john@example.com",
            password=get_password_hash("password123"),
            first_name="John",
            last_name="Doe",
            phone="+1987654321",
            address="456 Main Street, New York, NY",
        ),
        User(
            username="jane_smith",
            email="jane@example.com",
            password=get_password_hash("password123"),
            first_name="Jane",
            last_name="Smith",
            phone="+1555666777",
            address="789 Oak Avenue, Los Angeles, CA",
        ),
        User(
            username="mohammed_ali",
            email="mohammed@example.com",
            password=get_password_hash("password123"),
            first_name="Mohammed",
            last_name="Ali",
            phone="+966501234567",
            address="King Fahd Road, Riyadh, Saudi Arabia",
        ),
        User(
            username="sarah_wilson",
            email="sarah@example.com",
            password=get_password_hash("password123"),
            first_name="Sarah",
            last_name="Wilson",
            phone="+1444555666",
            address="321 Pine Street, Chicago, IL",
        ),
    ]
    db.add_all(users)
    db.commit()
    return users


def seed_jewelers(db):
    print("Seeding jewelers...")
    jewelers = [
        Jeweler(
            name="Ahmed Goldsmith",
            shop_name="Golden Dreams Jewelry",
            bio="Master goldsmith with 20 years of experience in crafting exquisite gold jewelry. Specializing in traditional Arabic designs with modern touches.",
            address="Gold Souk, Deira, Dubai, UAE",
            phone="+971501234567",
            email="ahmed@goldendreams.com",
            rating=4.9,
        ),
        Jeweler(
            name="Maria Silva",
            shop_name="Elegance Jewelers",
            bio="Award-winning designer specializing in diamond jewelry and custom engagement rings. GIA certified gemologist.",
            address="Fifth Avenue, New York, NY 10001",
            phone="+12125551234",
            email="maria@elegancejewelers.com",
            rating=4.8,
        ),
        Jeweler(
            name="Omar Hassan",
            shop_name="Heritage Gold",
            bio="Third-generation jeweler preserving traditional Middle Eastern craftsmanship. Expert in 21k and 22k gold pieces.",
            address="Al-Balad, Jeddah, Saudi Arabia",
            phone="+966512345678",
            email="omar@heritagegold.com",
            rating=4.7,
        ),
    ]
    db.add_all(jewelers)
    db.commit()
    return jewelers


def seed_categories(db):
    print("Seeding categories...")
    
    rings = Category(name="Rings")
    db.add(rings)
    db.commit()
    
    rings_sub = [
        Category(name="Engagement Rings", parent_id=rings.id),
        Category(name="Wedding Bands", parent_id=rings.id),
        Category(name="Fashion Rings", parent_id=rings.id),
    ]
    db.add_all(rings_sub)
    
    necklaces = Category(name="Necklaces")
    db.add(necklaces)
    db.commit()
    
    necklaces_sub = [
        Category(name="Pendants", parent_id=necklaces.id),
        Category(name="Chains", parent_id=necklaces.id),
        Category(name="Chokers", parent_id=necklaces.id),
    ]
    db.add_all(necklaces_sub)
    
    bracelets = Category(name="Bracelets")
    db.add(bracelets)
    db.commit()
    
    db.commit()
    
    return {
        "rings": rings,
        "necklaces": necklaces,
        "bracelets": bracelets,
        "engagement_rings": rings_sub[0],
        "wedding_bands": rings_sub[1],
        "fashion_rings": rings_sub[2],
        "pendants": necklaces_sub[0],
        "chains": necklaces_sub[1],
    }


def seed_payment_methods(db):
    print("Seeding payment methods...")
    payment_methods = [
        PaymentMethod(
            method_name="Bank Transfer",
            qr_code_image="/static/payment/qr_bank.png",
            is_active=True,
            notes="Please transfer to: Bank Account XXXX-XXXX-XXXX. Send receipt to orders@jewelry.com",
        ),
        PaymentMethod(
            method_name="PayPal",
            qr_code_image="/static/payment/qr_paypal.png",
            is_active=True,
            notes="Send payment to: payments@jewelry.com",
        ),
    ]
    db.add_all(payment_methods)
    db.commit()
    return payment_methods


def seed_products(db, jewelers, categories):
    print("Seeding products...")
    products_data = [
        {
            "name": "Elegant Diamond Engagement Ring",
            "jeweler_id": jewelers[1].id,
            "material": "Gold",
            "karat": "18k",
            "weight": 5.2,
            "price": 2999.99,
            "stock_quantity": 10,
            "description": "A stunning 18k gold engagement ring featuring a brilliant 1-carat diamond surrounded by smaller accent diamonds. Perfect for your special moment.",
            "image_path": "/static/products/ring1.jpg",
            "categories": [categories["engagement_rings"].id, categories["rings"].id],
        },
        {
            "name": "Classic 21k Gold Wedding Band",
            "jeweler_id": jewelers[2].id,
            "material": "Gold",
            "karat": "21k",
            "weight": 8.5,
            "price": 1299.99,
            "stock_quantity": 25,
            "description": "Traditional 21k gold wedding band with a smooth polished finish. Handcrafted by master artisans.",
            "image_path": "/static/products/ring2.jpg",
            "categories": [categories["wedding_bands"].id, categories["rings"].id],
        },
        {
            "name": "Ruby Pendant Necklace",
            "jeweler_id": jewelers[0].id,
            "material": "Gold",
            "karat": "18k",
            "weight": 12.3,
            "price": 1899.99,
            "stock_quantity": 8,
            "description": "An exquisite 18k gold necklace featuring a natural Burmese ruby pendant surrounded by diamond accents.",
            "image_path": "/static/products/necklace1.jpg",
            "categories": [categories["pendants"].id, categories["necklaces"].id],
        },
        {
            "name": "Sterling Silver Chain",
            "jeweler_id": jewelers[1].id,
            "material": "Silver",
            "karat": "925",
            "weight": 15.0,
            "price": 199.99,
            "stock_quantity": 50,
            "description": "Classic sterling silver chain with a modern design. Perfect for everyday wear or layering.",
            "image_path": "/static/products/chain1.jpg",
            "categories": [categories["chains"].id, categories["necklaces"].id],
        },
        {
            "name": "Diamond Tennis Bracelet",
            "jeweler_id": jewelers[1].id,
            "material": "White Gold",
            "karat": "18k",
            "weight": 25.0,
            "price": 4999.99,
            "stock_quantity": 5,
            "description": "Stunning tennis bracelet featuring 3 carats of round brilliant diamonds set in 18k white gold.",
            "image_path": "/static/products/bracelet1.jpg",
            "categories": [categories["bracelets"].id],
        },
        {
            "name": "Emerald Fashion Ring",
            "jeweler_id": jewelers[0].id,
            "material": "Gold",
            "karat": "18k",
            "weight": 6.8,
            "price": 2299.99,
            "stock_quantity": 7,
            "description": "Beautiful Colombian emerald ring set in 18k yellow gold with diamond side stones.",
            "image_path": "/static/products/ring3.jpg",
            "categories": [categories["fashion_rings"].id, categories["rings"].id],
        },
        {
            "name": "Traditional Arabic Gold Necklace",
            "jeweler_id": jewelers[2].id,
            "material": "Gold",
            "karat": "22k",
            "weight": 35.0,
            "price": 3499.99,
            "stock_quantity": 4,
            "description": "Traditional Arabic design necklace in pure 22k gold. Features intricate filigree work inspired by heritage designs.",
            "image_path": "/static/products/necklace2.jpg",
            "categories": [categories["necklaces"].id],
        },
        {
            "name": "Sapphire Pendant",
            "jeweler_id": jewelers[1].id,
            "material": "Platinum",
            "karat": "950",
            "weight": 8.0,
            "price": 3299.99,
            "stock_quantity": 6,
            "description": "Elegant platinum pendant featuring a 2-carat Ceylon sapphire with diamond halo.",
            "image_path": "/static/products/pendant1.jpg",
            "categories": [categories["pendants"].id, categories["necklaces"].id],
        },
        {
            "name": "Gold Link Bracelet",
            "jeweler_id": jewelers[0].id,
            "material": "Gold",
            "karat": "21k",
            "weight": 28.0,
            "price": 2799.99,
            "stock_quantity": 12,
            "description": "Classic 21k gold link bracelet with a contemporary design. Perfect for both men and women.",
            "image_path": "/static/products/bracelet2.jpg",
            "categories": [categories["bracelets"].id],
        },
        {
            "name": "Rose Gold Fashion Ring",
            "jeweler_id": jewelers[1].id,
            "material": "Rose Gold",
            "karat": "18k",
            "weight": 4.5,
            "price": 899.99,
            "stock_quantity": 15,
            "description": "Trendy rose gold fashion ring with a unique twisted band design. Perfect for everyday elegance.",
            "image_path": "/static/products/ring4.jpg",
            "categories": [categories["fashion_rings"].id, categories["rings"].id],
        },
    ]

    products = []
    for product_data in products_data:
        category_ids = product_data.pop("categories")
        product = Product(**product_data)
        db.add(product)
        db.commit()
        db.refresh(product)

        for cat_id in category_ids:
            db.execute(
                product_categories.insert().values(
                    product_id=product.id, category_id=cat_id
                )
            )
        db.commit()

        product_image = ProductImage(
            product_id=product.id,
            image_path=product.image_path,
            display_order=1,
        )
        db.add(product_image)
        products.append(product)

    db.commit()
    return products


def run_seeder():
    print("=" * 50)
    print("Starting Database Seeding...")
    print("=" * 50)

    clear_database()

    db = SessionLocal()
    try:
        users = seed_users(db)
        print(f"Created {len(users)} users")

        jewelers = seed_jewelers(db)
        print(f"Created {len(jewelers)} jewelers")

        categories = seed_categories(db)
        print(f"Created categories")

        payment_methods = seed_payment_methods(db)
        print(f"Created {len(payment_methods)} payment methods")

        products = seed_products(db, jewelers, categories)
        print(f"Created {len(products)} products")

        print("=" * 50)
        print("Database seeding completed successfully!")
        print("=" * 50)
        print("\nDefault Users:")
        print("  - admin / admin123")
        print("  - john_doe / password123")
        print("  - jane_smith / password123")
        print("  - mohammed_ali / password123")
        print("  - sarah_wilson / password123")
        print("\nYou can now start the server with: uvicorn main:app --reload")

    except Exception as e:
        print(f"Error during seeding: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    run_seeder()