from fastapi import FastAPI, Request
from databse.db import Base, engine
from routes import auth_route, category_route, expense_route, budget_route
import logging
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware  #Cross-Origin Resource Sharing

app = FastAPI()
app.add_middleware(
    CORSMiddleware, 
    allow_origins = ["*"],
    allow_credentials = True,
    allow_methods=["*"],
    allow_headers=["*"]
)

Base.metadata.create_all(bind= engine)

logging.basicConfig(
    level = logging.INFO,
    format= "%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unexpected error: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error"
        }
    )

app.include_router(auth_route.router)
app.include_router(expense_route.router)
app.include_router(budget_route.router)
app.include_router(category_route.router)

