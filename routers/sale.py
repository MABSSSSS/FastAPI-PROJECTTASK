from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import crud, schemas, database
from typing import List

router = APIRouter()

@router.post("/Create-Sale")
def create_sale(sale: schemas.SaleCreate, db: Session = Depends(database.get_db)):
    new_sale = crud.create_sale(db=db, sale=sale)
    return {
        'id': new_sale.id,
        'user_id': new_sale.user_id,
        'product_id': new_sale.product_id,
        'created_at': new_sale.created_at
    }

@router.get("/Check-Sales-Created")
def read_sales(skip: int = 0, limit: int = 10, db: Session = Depends(database.get_db)):
    sales = crud.get_sales(db, skip=skip, limit=limit)
    for sale in sales:
        print("This is sales id", sale.id)
    return [
        {
            'id': sale.id,
            'user_id': sale.user_id,
            'product_id': sale.product_id,
            'created_at': sale.created_at
        }
        for sale in sales
    ]

@router.get("/Enter-Product-Id/{product_id}")
def read_sales_by_product_id(product_id: int, db: Session = Depends(database.get_db)):
    # Fetch sales associated with the product ID
    sales = crud.get_sales_by_product_id(db, product_id)
    if not sales:
        raise HTTPException(status_code=404, detail="No sales found for this product")
    
    # Fetch product details
    product = crud.get_product_by_id(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Compile sales details
    sales_details = []
    for sale in sales:
        user = crud.get_user_by_id(db, sale.user_id)
        sales_details.append({
            "sales_id":sale.id,
            "user_id": sale.user_id,
            "user_name": user.name if user else "Unknown",
            "user_email": user.email,
            "created_at": sale.created_at
        })
    
    # Return the response
    return {
        "product_id": product_id,
        "product_name": product.name,
        "product_price":product.price,
        "total_sales_count": len(sales),
        "sales_details": sales_details
    }

@router.get("/Enter-User-Id/{user_id}")
def read_sales_by_user_id(user_id: int, db: Session = Depends(database.get_db)):
    sales = crud.get_sales_by_user_id(db, user_id)
    if not sales:
        raise HTTPException(status_code=404, detail="No sales found for this user")
    
    user = crud.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    sales_details = []
    for sale in sales:
        product = crud.get_product_by_id(db, sale.product_id)
        sales_details.append({
            "sale_id": sale.id,
            "product_name": product.name if product else "Unknown",
            "product_price": product.price if product else "Unknown",
            "created_at": sale.created_at
        })
    
    return {
        "user_id": user_id,
        "user_name": user.name,
        "total_sales_count": len(sales),
        "sales_details": sales_details
    }

@router.get("/Enter-Sales-Id/{sale_id}")
def read_sale(sale_id: int, db: Session = Depends(database.get_db)):
    db_sale = crud.get_sale_by_id(db, sale_id=sale_id)
    if db_sale is None:
        raise HTTPException(status_code=404, detail="Sale not found")
    
    product = crud.get_product_by_id(db, db_sale.product_id)
    user = crud.get_user_by_id(db, db_sale.user_id)
    
    related_sales = crud.get_sales_by_user_and_product(db, user_id=db_sale.user_id, product_id=db_sale.product_id)
    total_sales_count = len(related_sales)
    
    response = {
        "current_sale_id": db_sale.id,
        "product_id": db_sale.product_id,
        "product_name": product.name if product else "Unknown",
        "user_id": db_sale.user_id,
        "user_name": user.name if user else "Unknown",
        "created_at": db_sale.created_at,
        "total_sales_count_of_current_sale_id": total_sales_count,
        "sales": [
            {
                "sale_id": sale.id,
                "product_id": sale.product_id,
                "user_id": sale.user_id,
                "created_at": sale.created_at
            }
            for sale in related_sales
        ]
    }
    return response
