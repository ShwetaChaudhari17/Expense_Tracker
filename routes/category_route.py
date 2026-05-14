from schemas.category_schema import CategoryCreate
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from databse.db import get_db
from service.auth_service import get_current_user
from service.category_service import create_category_service, get_category_service, delete_category_service

router = APIRouter(prefix="/categories", tags=["Categories"])

@router.post("/")
def create_category(category : CategoryCreate, db : Session = Depends(get_db), user = Depends(get_current_user)):

    return create_category_service(category, db, user)

@router.get("/")
def get_category(db : Session = Depends(get_db), user = Depends(get_current_user)):

    return get_category_service(db, user)


@router.delete("/{category_id}")
def delete_category(category_id : int, db : Session = Depends(get_db), user = Depends(get_current_user)):
    return delete_category_service(category_id, db, user)
