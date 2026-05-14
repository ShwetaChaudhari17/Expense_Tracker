from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from schemas.budget_schema import BudgetCreate
from databse.db import get_db
from service.auth_service import get_current_user

from service.budget_service import create_budget_service, get_all_budget_service, get_budget_vs_spending_service
router = APIRouter(prefix="/budget", tags=["Budget"])

@router.post("/")
def create_budget(budget: BudgetCreate, db : Session = Depends(get_db), user = Depends(get_current_user)):
    return create_budget_service(budget, db, user)


@router.get("/")
def get_budget(db : Session = Depends(get_db), user = Depends(get_current_user)):
    return get_all_budget_service(db, user)


@router.get("/compare")
def get_budget_vs_spending(db : Session = Depends(get_db), user = Depends(get_current_user)):
    return get_budget_vs_spending_service(db, user)