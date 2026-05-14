from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from databse.db import get_db
from schemas.task_schema import UserCreate, UserLogin

from service.auth_service import signup_auth_service, loginuser_auth_service, get_current_user

router = APIRouter()

@router.post("/signup")
def signup(user: UserCreate, db : Session = Depends(get_db)):
    return signup_auth_service(user, db)

@router.post("/login")
def login(user: UserLogin, db : Session = Depends(get_db)):
    return loginuser_auth_service(user, db)

@router.get("/protected")
def validate_user(mesg : dict = Depends(get_current_user)):
    return mesg