from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import crud, schemas, database
from typing import List

router = APIRouter()

@router.post("/Create-Product")
def create_product(product: schemas.ProductCreate, db: Session = Depends(database.get_db)):
    new_product = crud.create_product(db=db, product=product)
    return {
        'id': new_product.id,
        'name': new_product.name,
        'price': new_product.price
    }

@router.get("/Check-Products-Created")
def read_products(skip: int = 0, limit: int = 10, db: Session = Depends(database.get_db)):
    products = crud.get_products(db, skip=skip, limit=limit)
    return [
        {
            'id': product.id,
            'name': product.name,
            'price': product.price
        }
        for product in products
    ]

@router.get("/Get-Product-By-Id/{product_id}")
def read_product(product_id: int, db: Session = Depends(database.get_db)):
    db_product = crud.get_product_by_id(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Get all sales related to this product
    sales = crud.get_sales_by_product_id(db, product_id=product_id)

    sales_details = []
    for sale in sales:
        user = crud.get_user_by_id(db, sale.user_id)
        sales_details.append({
            "sale_id": sale.id,
            "user_id": sale.user_id,
            "user_name": user.name if user else "Unknown",
            "created_at": sale.created_at
        })
    
    return {
        'id': db_product.id,
        'name': db_product.name,
        'price': db_product.price,
        'total_sales_count': len(sales),
        'sales_details': sales_details
    }

@router.get("/Get-Product-By-Name/{name}")
def read_product_by_name(name: str, db: Session = Depends(database.get_db)):
    db_product = crud.get_product_by_name(db, name=name)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Get all sales related to this product
    sales = crud.get_sales_by_product_id(db, product_id=db_product.id)

    sales_details = []
    for sale in sales:
        user = crud.get_user_by_id(db, sale.user_id)
        sales_details.append({
            "sale_id": sale.id,
            "user_id": sale.user_id,
            "user_name": user.name if user else "Unknown",
            "created_at": sale.created_at
        })
    
    return {
        'id': db_product.id,
        'name': db_product.name,
        'price': db_product.price,
        'total_sales_count': len(sales),
        'sales_details': sales_details
    }

@router.get("/Get-Products-By-User-Id/{user_id}")
def read_products_by_user_id(user_id: int, db: Session = Depends(database.get_db)):
    # Get all sales made by this user
    sales = crud.get_sales_by_user_id(db, user_id=user_id)
    
    product_details = []
    for sale in sales:
        product = crud.get_product_by_id(db, sale.product_id)
        if product:
            product_details.append({
                "product_id": product.id,
                "product_name": product.name,
                "product_price": product.price,
                "sale_id": sale.id,
                "created_at": sale.created_at
            })
    
    if not product_details:
        raise HTTPException(status_code=404, detail="No products found for this user")
    
    return {
        "user_id": user_id,
        "total_product_count": len(product_details),
        "product_details": product_details
    }
