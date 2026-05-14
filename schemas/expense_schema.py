from pydantic import BaseModel
from enum import Enum

class RecurringType(str, Enum):
    daily = "daily"
    weekly = "weekly"
    monthly = "monthly"

class ExpenseCreate(BaseModel):
    amount : int
    description : str
    category_id : int
    is_recurring : bool = False
    recurring_type : RecurringType | None = None

class ExpenseUpdate(BaseModel):
    amount : int
    description : str
    category_id : int
