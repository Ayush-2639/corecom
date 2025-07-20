from fastapi import APIRouter, HTTPException, Query
from bson import ObjectId
from .models import OrderCreate, serialize_order
from .db import order_collection, product_collection
from pymongo import ASCENDING


orderRouter = APIRouter()

@orderRouter.post("/orders", status_code=201)
def create_order(order: OrderCreate):
    if not order.items:
        raise HTTPException(status_code=400, detail="Order must contain at least one item")

    validated_items = []

    for item in order.items:
        if not ObjectId.is_valid(item.productId):
            raise HTTPException(status_code=400, detail=f"Invalid product_id: {item.productId}")

        product = product_collection.find_one({"_id": ObjectId(item.productId)})
        if not product:
            raise HTTPException(status_code=404, detail=f"Product not found: {item.productId}")

        if item.qty <= 0:
            raise HTTPException(status_code=400, detail=f"Quantity must be > 0 for product {item.productId}")

        validated_items.append({
            "product_id": ObjectId(item.productId),
            "quantity": item.qty
        })

    order_doc = {
        "user_id": order.user_id,
        "items": validated_items
    }

    result = order_collection.insert_one(order_doc)

    return {
        "id": str(result.inserted_id)
    }

@orderRouter.get("/orders/{user_id}")
def get_orders_for_user(
        user_id: str,
        limit: int = Query(5, gt=0, le=100),
        offset: int = Query(0, ge=0)
):
    query = {"user_id": user_id}
    total_orders = order_collection.count_documents(query)

    orders_cursor = (
        order_collection.find(query)
        .sort("_id", ASCENDING)
        .skip(offset)
        .limit(limit)
    )

    response_data = []

    for order in orders_cursor:
        order_items = []
        for item in order.get("items", []):
            product = product_collection.find_one({"_id": item["product_id"]}, {"name": 1})
            if not product:
                continue  # skip if product not found

            order_items.append({
                "quantity": item["quantity"],
                "productDetails": {
                    "product_id": str(item["product_id"]),
                    "name": product["name"]
                }
            })

        response_data.append({
            "id": str(order["_id"]),
            "total": sum(i["quantity"] for i in order.get("items", [])),
            "items": order_items
        })

    next_offset = offset + limit if offset + limit < total_orders else None
    prev_offset = max(offset - limit, 0) if offset > 0 else None

    return {
        "data": response_data,
        "page": {
            "next": next_offset,
            "previous": prev_offset,
            "limit": limit
        }
    }
