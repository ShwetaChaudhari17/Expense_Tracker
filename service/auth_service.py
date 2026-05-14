from models.task_models import User
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from passlib.context import CryptContext
import os
from datetime import datetime, timedelta
from databse.db import get_db
from sqlalchemy.orm import Session

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated = "auto")

def hash_password(password):
    return pwd_context.hash(password)

def verify_password(password, hash_password):
    return pwd_context.verify(password, hash_password)    


def create_user_token(user):
    to_encode = user.copy()
    to_encode["exp"] = datetime.utcnow() + timedelta(minutes=30)

    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return token

def verify_token(token):
        
    try:    
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        user_id = payload.get("user_id")

        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token??")
        
        return payload
    
    except JWTError:
        raise HTTPException(status_code=401, detail="Token is invalid or expired")

security = HTTPBearer()

def get_current_user(credentials : HTTPAuthorizationCredentials = Depends(security), db : Session =  Depends(get_db)):
    token = credentials.credentials
    payload = verify_token(token)

    user = db.query(User).filter(User.id == payload.get("user_id")).first()
    
    return user

    

def signup_auth_service(user, db):
    exi_user = db.query(User).filter(User.email == user.email).first()

    if exi_user:
        raise HTTPException(status_code=401, detail="user already exists")
    
    new_user = User(
        email = user.email,
        name = user.name,
        password = hash_password(user.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "user signed up"}

def loginuser_auth_service(user, db):
    exi_user = db.query(User).filter(User.email == user.email).first()

    if not exi_user:
        raise HTTPException(status_code=401, detail="user doesn't exists")
    
    if not verify_password(user.password, exi_user.password):
        raise HTTPException(status_code=401, detail="password is not correct")
    
    token = create_user_token({"user_id": exi_user.id})

    return {"token " :token}


    