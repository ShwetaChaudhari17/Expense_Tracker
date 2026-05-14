from fastapi import HTTPException

from models.task_models import Budget, Category, Expense
from sqlalchemy import func

def create_budget_service(budget, db, user):
    category = db.query(Category).filter(budget.category_id == Category.id, Category.user_id == user.id).first()
    if category is None:
        raise HTTPException(status_code=400, detail="category not found")
    
    exi_budget = db.query(Budget).filter(Budget.category_id == budget.category_id, Budget.month == budget.month, Budget.user_id == user.id).first()

    if exi_budget:
        raise HTTPException(status_code=404, detail="Budget exists")
    
    new_budget = Budget(
        month = budget.month,
        amount = budget.amount,
        category_id = budget.category_id,
        user_id = user.id)
    
    db.add(new_budget)
    db.commit()
    db.refresh( new_budget)
    return  new_budget

def get_all_budget_service(db, user):    
    summary = db.query(Category.name, Budget.month, Budget.amount
             ).join(Budget, Budget.category_id == Category.id
             ).filter(Budget.user_id == user.id).all()
    result = []

    for row in summary:
        result.append({"category" : row[0], "month" : row[1], "amount" : row[2] } )

    return result


def get_budget_vs_spending_service(db, user):    

    summary = db.query(Category.name.label("category"), Budget.amount.label("budget"), func.to_char(Expense.created_at, 'YYYY-MM').label("month"), func.sum(Expense.amount).label("spent")
                       ).filter(Expense.user_id == user.id).join(Category, Expense.category_id == Category.id).join(Budget, (Category.id == Budget.category_id)
                & (Budget.month == func.to_char(Expense.created_at, 'YYYY-MM'))).group_by(
    Category.id,

    Category.name,

    Budget.amount, func.to_char(Expense.created_at, 'YYYY-MM')).all()

    result = []

    for row in summary:
        result.append(
            {
                "category": row.category,
                "month": row.month,
                "budget": row.budget,
                "spent": row.spent,
                "remaining": row.budget - row.spent
            }
        )
    return result
  

