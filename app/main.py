from datetime import datetime
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import database
from .database import engine, Base

# Import routers
from .routers import phones, auth, orders

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Phone Ecommerce API",
    version="1.0.0",
    description="API for Phone Ecommerce Website"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(phones.router)
app.include_router(auth.router)
app.include_router(orders.router)

@app.get("/")
def read_root():
    return {"message": "Phone Ecommerce API", "docs": "/docs", "redoc": "/redoc"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow()}