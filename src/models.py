from pydantic import BaseModel, Field
from typing import List
from bson import ObjectId

class Size(BaseModel):
    size: str
    quantity: int = 0

class Item(BaseModel):
    name: str
    price: float
    sizes: List[Size]

class OrderItem(BaseModel):
    productId: str
    qty: int = Field(..., gt=0, description="Quantity must be > 0")

class OrderCreate(BaseModel):
    user_id: str
    items: List[OrderItem]

def serialize_product(item):
    return {
        "id": str(item["_id"]),
        "name": item["name"],
        "price": item["price"]
    }

def serialize_order(order, total):
    return {
        "id": str(order["_id"]),
        "user_id": str(order["user_id"]),
        "total": str(total),
        "items": [
            {
                "product_id": str(item["product_id"]),
                "quantity": item["quantity"]
            }
            for item in order["items"]
        ]
    }
