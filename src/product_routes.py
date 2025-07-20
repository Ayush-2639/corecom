from fastapi import APIRouter,status, Query
from .models import Item, serialize_product
from .db import product_collection
from typing import List, Optional
from pymongo import ASCENDING
from bson import ObjectId, Regex

productRouter = APIRouter()

@productRouter.post("/products", status_code=status.HTTP_201_CREATED)
def create_product(item: Item):
    result = product_collection.insert_one(item.dict())
    new_item = product_collection.find_one({"_id": result.inserted_id})
    return {"id:"+str(new_item["_id"])}

@productRouter.get("/products")
def get_filtered_products(
        name: Optional[str] = Query(None),
        size: Optional[str] = Query(None),
        limit: int = Query(10, gt=0, le=100),
        offset: int = Query(0, ge=0)
):
    query = {}

    if name:
        query["name"] = {"$regex": name, "$options": "i"}
    if size:
        query["sizes"] = {"$elemMatch": {"size": size}}
    total = product_collection.count_documents(query)
    cursor = (
        product_collection.find(query)
        .sort("_id", ASCENDING)
        .skip(offset)
        .limit(limit)
    )
    products = [serialize_product(p) for p in cursor]
    next_offset = offset + limit if offset + limit < total else None
    prev_offset = max(offset - limit, 0) if offset > 0 else None
    return {
        "data": products,
        "page": {
            "next": next_offset,
            "previous": prev_offset,
            "limit": limit
        }
    }