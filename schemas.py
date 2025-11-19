"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field
from typing import Optional, List

# Example schemas (replace with your own):

class User(BaseModel):
    """
    Users collection schema
    Collection name: "user" (lowercase of class name)
    """
    name: str = Field(..., description="Full name")
    email: str = Field(..., description="Email address")
    address: str = Field(..., description="Address")
    age: Optional[int] = Field(None, ge=0, le=120, description="Age in years")
    is_active: bool = Field(True, description="Whether user is active")

class Product(BaseModel):
    """
    Generic products collection schema
    Collection name: "product" (lowercase of class name)
    """
    title: str = Field(..., description="Product title")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., ge=0, description="Price in dollars")
    category: str = Field(..., description="Product category")
    in_stock: bool = Field(True, description="Whether product is in stock")

# Gothic Jewellery specific schemas

class JewelryProduct(BaseModel):
    """
    Gothic jewellery products
    Collection name: "jewelryproduct" (lowercase of class name)
    """
    title: str = Field(..., description="Product title")
    description: Optional[str] = Field(None, description="Detailed description")
    price: float = Field(..., ge=0, description="Price in USD")
    category: str = Field(..., description="Category: rings, necklaces, earrings, bracelets")
    images: List[str] = Field(default_factory=list, description="Image URLs")
    material: Optional[str] = Field(None, description="Material, e.g., sterling silver, stainless steel")
    color: Optional[str] = Field(None, description="Primary color / finish")
    size: Optional[str] = Field(None, description="Size or adjustable")
    stock: int = Field(0, ge=0, description="Units in stock")
    rating: Optional[float] = Field(None, ge=0, le=5, description="Average rating")
    featured: bool = Field(False, description="Featured on homepage")

class OrderItem(BaseModel):
    product_id: str = Field(..., description="Referenced product _id as string")
    title: str
    price: float
    quantity: int = Field(..., ge=1)

class Order(BaseModel):
    """
    Orders collection
    Collection name: "order"
    """
    items: List[OrderItem]
    total: float = Field(..., ge=0)
    customer_name: Optional[str] = None
    customer_email: Optional[str] = None
    customer_address: Optional[str] = None
    status: str = Field("pending", description="Order status")

# Add your own schemas here:
# --------------------------------------------------

# Note: The Flames database viewer will automatically:
# 1. Read these schemas from GET /schema endpoint
# 2. Use them for document validation when creating/editing
# 3. Handle all database operations (CRUD) directly
# 4. You don't need to create any database endpoints!
