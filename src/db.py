from pymongo import MongoClient
from .config import settings

client = MongoClient(settings.MONGO_URI)
db = client["corecom_db"]

product_collection = db["product"]
order_collection = db["orders"]

