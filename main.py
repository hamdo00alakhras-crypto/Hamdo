from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import os

from database import engine, Base, init_db
from routers import (
    auth_router,
    products_router,
    cart_router,
    orders_router,
    admin_router,
    ai_router,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    os.makedirs("static/generated_designs", exist_ok=True)
    yield


app = FastAPI(
    title="Jewelry E-commerce & AI Design Platform",
    description="A complete backend for jewelry e-commerce with AI-powered design generation",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(auth_router)
app.include_router(products_router)
app.include_router(cart_router)
app.include_router(orders_router)
app.include_router(admin_router)
app.include_router(ai_router)


@app.get("/")
def root():
    return {
        "message": "Welcome to Jewelry E-commerce & AI Design Platform API",
        "docs": "/docs",
        "redoc": "/redoc",
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}