from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import crud, schemas, database
from utils.hashing import Hash
from utils.authentication import create_access_token

router = APIRouter()

@router.post("/Register-User")
def register_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = crud.create_user(db=db, user=user)
    return {'detail': {'Id': new_user.id, 'Name': new_user.name, 'Email': new_user.email}}

@router.post("/User-login/")
def login(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if not db_user or not Hash.verify(db_user.password, user.password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    access_token = create_access_token(data={"sub": db_user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/Enter-User-Id/{user_id}")
def read_user(user_id: int, db: Session = Depends(database.get_db)):
    db_user = crud.get_user_by_id(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return {
        'Id': db_user.id,
        'Name': db_user.name,
        'Email': db_user.email
    }

@router.get("/Enter-User-email/{email}")
def read_user_by_email(email: str, db: Session = Depends(database.get_db)):
    db_user = crud.get_user_by_email(db, email=email)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return {
        'Id': db_user.id,
        'Name': db_user.name,
        'Email': db_user.email
    }
