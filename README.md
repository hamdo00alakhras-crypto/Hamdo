# Jewelry E-commerce & AI Design Platform

A complete backend for a jewelry e-commerce platform with AI-powered design generation using Google Gemini API.

## Technology Stack

- **Framework**: FastAPI (Python)
- **Database**: MySQL (XAMPP)
- **ORM**: SQLAlchemy with Pydantic
- **Authentication**: JWT (python-jose)
- **AI Integration**: Google Gemini API (`gemini-3-pro-image-preview`)

## Setup Instructions

### 1. Install XAMPP and Setup MySQL

1. Download and install [XAMPP](https://www.apachefriends.org/)
2. Start Apache and MySQL from XAMPP Control Panel
3. Open phpMyAdmin (http://localhost/phpmyadmin)
4. Create a new database named `jewelry_db`

### 2. Clone and Setup Project

```bash
# Navigate to project directory
cd G:\Hamdo

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure Environment Variables

```bash
# Copy example env file
copy .env.example .env

# Edit .env file with your settings
# Add your Gemini API Key
GEMINI_API_KEY=your_actual_gemini_api_key_here
```

### 4. Initialize Database

```bash
# Run the seeder to populate database with sample data
python seeder.py
```

### 5. Start the Server

```bash
# Start development server
uvicorn main:app --reload

# Server will be available at:
# http://localhost:8000
# API Documentation: http://localhost:8000/docs
# ReDoc: http://localhost:8000/redoc
```

## API Endpoints

### Authentication (`/api/auth`)
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/register` | Register new user |
| POST | `/login` | Login and get JWT token |
| GET | `/me` | Get current user info |

### Products (`/api/products`)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Get all products (with filters) |
| GET | `/{product_id}` | Get single product |
| GET | `/categories/` | Get all categories |

### Cart (`/api/cart`)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | View cart |
| POST | `/add` | Add item to cart |
| PUT | `/update/{item_id}` | Update item quantity |
| DELETE | `/remove/{item_id}` | Remove item |
| DELETE | `/clear` | Clear cart |

### Orders (`/api/orders`)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Get user orders |
| GET | `/{order_id}` | Get order details |
| POST | `/checkout` | Create order from cart |

### Admin (`/api/admin`)
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/products` | Create product |
| PUT | `/products/{id}` | Update product |
| DELETE | `/products/{id}` | Delete product |
| POST | `/categories` | Create category |
| POST | `/payment-methods` | Create payment method |
| GET | `/orders` | Get all orders |
| PUT | `/orders/{id}/status` | Update order status |
| GET | `/design-requests` | Get design requests |
| PUT | `/design-requests/{id}` | Update design request |

### AI Design (`/api/ai`)
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/generate-design` | Generate AI jewelry design |
| GET | `/my-designs` | Get user's generated designs |

## Frontend Integration Guide

### Authentication Example

```javascript
// Register User
async function register(userData) {
    const response = await fetch('http://localhost:8000/api/auth/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(userData)
    });
    return await response.json();
}

// Login
async function login(username, password) {
    const response = await fetch('http://localhost:8000/api/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
    });
    const data = await response.json();
    // Store token in localStorage
    localStorage.setItem('token', data.access_token);
    return data;
}

// Get current user (authenticated request)
async function getCurrentUser() {
    const token = localStorage.getItem('token');
    const response = await fetch('http://localhost:8000/api/auth/me', {
        headers: {
            'Authorization': `Bearer ${token}`
        }
    });
    return await response.json();
}
```

### AI Design Generation Example

```javascript
async function generateDesign(designOptions) {
    const token = localStorage.getItem('token');
    const response = await fetch('http://localhost:8000/api/ai/generate-design', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
            type: 'Ring',           // Ring, Necklace, Bracelet, Earrings
            color: 'Gold',          // Gold, Silver, Rose Gold, White Gold
            shape: 'Round',         // Round, Oval, Square, Heart
            material: 'Gold',       // Gold, Silver, Platinum
            karat: '18k',          // 18k, 21k, 22k, 24k, 925
            gemstone_type: 'Diamond', // Diamond, Ruby, Emerald, Sapphire, None
            gemstone_color: 'White'   // White, Red, Green, Blue, etc.
        })
    });
    return await response.json();
}

// Usage
const design = await generateDesign({
    type: 'Ring',
    color: 'Gold',
    shape: 'Round',
    material: 'Gold',
    karat: '21k',
    gemstone_type: 'Ruby',
    gemstone_color: 'Red'
});
console.log('Generated Image URL:', design.generated_image_url);
```

### Cart Management Example

```javascript
// Add to cart
async function addToCart(productId, quantity = 1) {
    const token = localStorage.getItem('token');
    const response = await fetch('http://localhost:8000/api/cart/add', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ product_id: productId, quantity })
    });
    return await response.json();
}

// Get cart
async function getCart() {
    const token = localStorage.getItem('token');
    const response = await fetch('http://localhost:8000/api/cart/', {
        headers: { 'Authorization': `Bearer ${token}` }
    });
    return await response.json();
}

// Checkout
async function checkout(shippingAddress, paymentMethodId) {
    const token = localStorage.getItem('token');
    const response = await fetch('http://localhost:8000/api/orders/checkout', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
            shipping_address: shippingAddress,
            payment_method_id: paymentMethodId
        })
    });
    return await response.json();
}
```

## Project Structure

```
G:\Hamdo\
├── main.py                 # FastAPI application entry point
├── config.py               # Configuration settings
├── database.py             # Database connection setup
├── requirements.txt        # Python dependencies
├── .env.example            # Environment variables template
├── seeder.py               # Database seeder script
├── models/                 # SQLAlchemy models
│   ├── __init__.py
│   ├── user.py
│   ├── jeweler.py
│   ├── product.py
│   ├── category.py
│   ├── cart.py
│   ├── order.py
│   ├── design.py
│   └── payment.py
├── schemas/                # Pydantic schemas
│   ├── __init__.py
│   ├── user.py
│   ├── product.py
│   ├── cart.py
│   ├── order.py
│   ├── design.py
│   ├── category.py
│   ├── payment.py
│   └── jeweler.py
├── routers/                # API route handlers
│   ├── __init__.py
│   ├── auth.py
│   ├── products.py
│   ├── cart.py
│   ├── orders.py
│   ├── admin.py
│   └── ai.py
├── utils/                  # Utility functions
│   ├── __init__.py
│   ├── auth.py             # JWT authentication
│   └── security.py         # Password hashing
└── static/                 # Static files
    └── generated_designs/  # AI-generated designs
```

## Default Credentials (After Seeding)

| Username | Password | Role |
|----------|----------|------|
| admin | admin123 | Admin |
| john_doe | password123 | User |
| jane_smith | password123 | User |
| mohammed_ali | password123 | User |
| sarah_wilson | password123 | User |

## Getting Gemini API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the key and add it to your `.env` file

## License

MIT License