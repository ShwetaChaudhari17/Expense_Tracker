from databse.db import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime

class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)
    
    category = relationship("Category", back_populates="user")
    expense = relationship("Expense", back_populates="user")
    budget = relationship("Budget", back_populates= "user")
    
class Category(Base):
    __tablename__ = "category"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    user_id = Column(Integer, ForeignKey("user.id"))

    user = relationship("User", back_populates="category")
    expense = relationship("Expense", back_populates="category")
    budget = relationship("Budget", back_populates= "category")
    

class Expense(Base):
    __tablename__ = "expense"
    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Integer)
    description = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_recurring = Column(Boolean, default=False)
    recurring_type = Column(String, nullable=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    category_id = Column(Integer, ForeignKey("category.id"))

    user = relationship("User", back_populates="expense")
    category = relationship("Category",back_populates="expense")

class Budget(Base):
    __tablename__ = "monthly_budget"
    id = Column(Integer, primary_key= True, index= True)
    user_id = Column(Integer, ForeignKey("user.id"))
    category_id = Column(Integer, ForeignKey("category.id"))
    month = Column(String, nullable= False)
    amount = Column(Integer)

    user = relationship("User", back_populates="budget")
    category = relationship("Category",back_populates="budget")

