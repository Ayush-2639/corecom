from fastapi import FastAPI

from .product_routes import productRouter
from .order_routes import orderRouter

app = FastAPI()

# Include the API routes
app.include_router(productRouter)
app.include_router(orderRouter)