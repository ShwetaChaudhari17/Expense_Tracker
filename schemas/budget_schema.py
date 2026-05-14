from pydantic import BaseModel

class BudgetCreate(BaseModel):
    month : str
    amount : int
    category_id : int


