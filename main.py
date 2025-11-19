import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from bson import ObjectId

from database import db, create_document, get_documents
from schemas import JewelryProduct, Order, OrderItem, User, Product

app = FastAPI(title="Gothic Jewellery Store API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "Gothic Jewellery Store Backend"}


@app.get("/api/hello")
def hello():
    return {"message": "Welcome to the Gothic Jewellery API"}


@app.get("/test")
def test_database():
    """Test endpoint to check if database is available and accessible"""
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }
    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Configured"
            response["database_name"] = getattr(db, 'name', '✅ Connected')
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"

    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"
    return response


# API models for queries
class ProductFilter(BaseModel):
    category: Optional[str] = None
    featured: Optional[bool] = None
    limit: Optional[int] = 50


@app.post("/api/products", response_model=List[dict])
def list_products(filter: ProductFilter):
    try:
        query = {}
        if filter.category:
            query["category"] = filter.category
        if filter.featured is not None:
            query["featured"] = filter.featured
        items = get_documents("jewelryproduct", query, limit=filter.limit or 50)
        # Convert ObjectId to string
        for it in items:
            if isinstance(it.get("_id"), ObjectId):
                it["_id"] = str(it["_id"])
        return items
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class CreateProduct(BaseModel):
    title: str
    description: Optional[str] = None
    price: float
    category: str
    images: List[str] = []
    material: Optional[str] = None
    color: Optional[str] = None
    size: Optional[str] = None
    stock: int = 0
    rating: Optional[float] = None
    featured: bool = False


@app.post("/api/product")
def create_product(payload: CreateProduct):
    try:
        model = JewelryProduct(**payload.model_dump())
        inserted_id = create_document("jewelryproduct", model)
        return {"_id": inserted_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/orders")
def create_order(order: Order):
    try:
        order_id = create_document("order", order)
        return {"order_id": order_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
