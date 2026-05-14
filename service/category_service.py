from fastapi import HTTPException
from models.task_models import Category, Expense


def create_category_service(category, db, user):

    existing = db.query(Category).filter(Category.name == category.name , Category.user_id == user.id).first()

    if existing:
        raise HTTPException(status_code=400, detail="Category already exists")
    
    new_category = Category(
        name = category.name,
        user_id = user.id
    )
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category


def get_category_service(db, user):

    return db.query(Category).filter(Category.user_id == user.id).all()


def delete_category_service(category_id, db, user):
    category =  db.query(Category).filter(Category.id == category_id, Category.user_id == user.id).first()

    if category is None:
        raise HTTPException(status_code=404, detail="category not found")
    
    expense = db.query(Expense).filter(Expense.cat_id == category_id).first()
    
    if expense:
        raise HTTPException(status_code=400, detail="Cannot delete category with existing expenses")
    
    db.delete(category)
    db.commit()

    return {"message": "Category deleted"}