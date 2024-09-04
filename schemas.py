from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class UserBase(BaseModel):
    name: str
    email: str

class UserCreate(UserBase):
    password: str

class SaleBase(BaseModel):
    user_id: int
    product_id: int

class SaleCreate(SaleBase):
    pass

class Sale(SaleBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True  # For Pydantic v1
        from_attributes = True  # For Pydantic v2

class User(UserBase):
    id: int
    sales: Optional[List[Sale]] = []
    products: Optional[List["Product"]] = []  # Relationship to products

    class Config:
        orm_mode = True  # For Pydantic v1
        from_attributes = True  # For Pydantic v2

class ProductBase(BaseModel):
    name: str
    price: float

class ProductCreate(ProductBase):
    pass  # Removed user_id from the creation schema

class Product(ProductBase):
    id: int
    sales: Optional[List[Sale]] = []

    class Config:
        orm_mode = True  # For Pydantic v1
        from_attributes = True  # For Pydantic v2

class ProductResponse(ProductBase):
    id: int
    sales: Optional[List[Sale]] = []

    class Config:
        orm_mode = True  # For Pydantic v1
        from_attributes = True  # For Pydantic v2

# New schema to show product count by user_id
class UserProductCount(BaseModel):
    user_id: int
    product_count: int

    class Config:
        orm_mode = True  # For Pydantic v1
        from_attributes = True  # For Pydantic v2
