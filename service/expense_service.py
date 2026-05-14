from fastapi import HTTPException
from models.task_models import Category, Expense
from sqlalchemy import func

import logging
logger = logging.getLogger(__name__)

def create_expense_service(expense, db, user):
    exi_cat = db.query(Category).filter(Category.id == expense.category_id, Category.user_id == user.id).first()
    
    if exi_cat is None:
        logger.warning(
            f"Category {exi_cat.id} not found"
        )
        raise HTTPException(status_code=400, detail="Category doesn't exists")
    
    new_exp = Expense(
        amount = expense.amount,
        description = expense.description,
        is_recurring = expense.is_recurring,
        recurring_type = expense.recurring_type,
        category_id = expense.category_id,
        user_id = user.id)
    
    db.add(new_exp)
    db.commit()
    db.refresh(new_exp)
    logger.info("Expense Added")
    return new_exp


def update_expense_service(expense_id, expense, db, user):
    exi_expense = db.query(Expense).filter(Expense.id == expense_id, Expense.user_id == user.id).first()
    
    if exi_expense is None:
        logger.error("Expense doeesn't exists")
        raise HTTPException(status_code=400, detail="Expense doeesn't exists")
    
    exi_expense.amount = expense.amount
    exi_expense.description = expense.description 
    exi_expense.category_id = expense.category_id

    db.commit()
    logger.info(f"{user.id} updated expense")
    return exi_expense


def get_expense_service(id, db, user):
    expense = db.query(Expense).filter(Expense.id == id, Expense.user_id == user.id).first()
    if expense is None:
        
        raise HTTPException(status_code=404, detail="Expense not found")

    return expense

def delete_expenses_service(expense_id, db, user):
    expense =  db.query(Expense).filter(Expense.id == expense_id, Expense.user_id == user.id).first()

    if expense is None:
        raise HTTPException(status_code=404, detail="Expense not found")
    
    db.delete(expense)
    db.commit()

    return {"message": "Expense deleted"}

def get_category_summary_service(db, user):
    summary = db.query(Category.name, func.sum(Expense.amount).label("total")
    ).join(Category, Expense.category_id == Category.id
    ).filter(Expense.user_id == user.id).group_by(Category.name).all()

    result = []

    for row in summary:
        result.append({"category" : row.name, "total exp" : row.total } )

    return result

def get_monthly_summary_service(db, user):
    summary = db.query(func.to_char(Expense.created_at, 'YYYY').label("month"), func.sum(Expense.amount).label("total")
                       ).filter(Expense.user_id == user.id).group_by(func.to_char(Expense.created_at, 'YYYY')).all()
    result = []

    for row in summary:
        result.append(
            {
                "month": row.month,
                "total": row.total
            }
        )
      
    return result
    

def get_all_expenses_service(category_id, max_amount, search, db, user):

    query = db.query(Expense).filter(
        Expense.user_id == user.id
    )

    if category_id is not None:

        query = query.filter(
            Expense.category_id == category_id
        )
    if max_amount is not None:
        
        query = query.filter(
            Expense.amount <= max_amount
        )
    if search is not None:
        query = query.filter(
            Expense.description.ilike(f"%{search}%")
        )

    return query.all()    