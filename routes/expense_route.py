from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from schemas.expense_schema import ExpenseCreate, ExpenseUpdate
from databse.db import get_db
from service.auth_service import get_current_user

from service.expense_service import create_expense_service, \
update_expense_service, get_all_expenses_service, get_expense_service,\
delete_expenses_service, get_category_summary_service, get_monthly_summary_service

router = APIRouter(prefix="/expenses", tags=["Expenses"])

@router.post("/")
def create_expense(expense: ExpenseCreate, db : Session = Depends(get_db), user = Depends(get_current_user)):
    return create_expense_service(expense, db, user)

@router.put("/{expense_id}")
def update_expense(expense_id : int, expense: ExpenseUpdate, db : Session = Depends(get_db), user = Depends(get_current_user)):
    return update_expense_service(expense_id, expense, db, user)

@router.get("/")
def get_all_expenses(category_id :int = None, max_amount : int = None, search : str = None, db : Session = Depends(get_db), user = Depends(get_current_user)):
    return get_all_expenses_service(category_id, max_amount, search , db, user)

@router.get("/MonthlySummary")
def get_monthly_summary(db : Session = Depends(get_db), user = Depends(get_current_user)):
    return get_monthly_summary_service(db, user)

@router.get("/summary")
def get_category_summary(db : Session = Depends(get_db), user = Depends(get_current_user)):
    return get_category_summary_service(db, user)

@router.get("/{id}")
def get_expense(id: int, db : Session = Depends(get_db), user = Depends(get_current_user)):
    return get_expense_service(id, db, user)


@router.delete("/{expense_id}")
def delete_expenses(expense_id : int, db : Session = Depends(get_db), user = Depends(get_current_user)):
    return delete_expenses_service(expense_id, db, user)


