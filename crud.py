from sqlalchemy.orm import Session
import models, schemas
from utils.hashing import Hash

# User CRUD Operations
def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = Hash.bcrypt(user.password)
    db_user = models.User(name=user.name, email=user.email, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.User).offset(skip).limit(limit).all()

# Product CRUD Operations
def create_product(db: Session, product: schemas.ProductCreate):
    db_product = models.Product(name=product.name, price=product.price)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def get_product_by_id(db: Session, product_id: int):
    return db.query(models.Product).filter(models.Product.id == product_id).first()

def get_product_by_name(db: Session, name: str):
    return db.query(models.Product).filter(models.Product.name == name).first()

def get_products(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Product).offset(skip).limit(limit).all()

# Sale CRUD Operations
def create_sale(db: Session, sale: schemas.SaleCreate):
    db_sale = models.Sale(user_id=sale.user_id, product_id=sale.product_id)
    db.add(db_sale)
    db.commit()
    db.refresh(db_sale)
    return db_sale

def get_sale_by_id(db: Session, sale_id: int):
    return db.query(models.Sale).filter(models.Sale.id == sale_id).first()

def get_sales_by_product_id(db: Session, product_id: int):
    return db.query(models.Sale).filter(models.Sale.product_id == product_id).all()

def get_sales_by_user_id(db: Session, user_id: int):
    return db.query(models.Sale).filter(models.Sale.user_id == user_id).all()

def get_sales_by_user_and_product(db: Session, user_id: int, product_id: int):
    return db.query(models.Sale).filter(models.Sale.user_id == user_id, models.Sale.product_id == product_id).all()

def get_users_by_product_id(db: Session, product_id: int):
    return db.query(models.User).join(models.Sale).filter(models.Sale.product_id == product_id).all()

def get_products_by_user_id(db: Session, user_id: int):
    return db.query(models.Product).join(models.Sale).filter(models.Sale.user_id == user_id).all()

def get_product_sales_count(db: Session, product_id: int):
    return db.query(models.Sale).filter(models.Sale.product_id == product_id).count()

def get_user_product_count(db: Session, user_id: int):
    return db.query(models.Sale).filter(models.Sale.user_id == user_id).count()
