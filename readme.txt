This is a FastAPI-based backend project that connects to MongoDB using `MongoDB Atlas`.
It provides APIs for managing products and orders with pagination, filtering, and error handling.


#Secure connection with `.env` configuration
#Ready for deployment on Railway (Free tier)
#Uses MongoDB Atlas M0 Free Tier

----------------- Environment Variables ---------------

Create a `.env` file in the root directory and add:

## Running Locally

1. Install dependencies:
```bash
pip install -r requirements.txt

2. Start server
uvicorn src.main:app --reload


------------ Endpoints
Product APIs
GET	/products
POST /products

Order APIs
POST /orders
GET	/orders/{user_id}

------------------- Railway base url ---------------
https://web-production-4d323.up.railway.app/




