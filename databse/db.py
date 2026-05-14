from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine

import os
from dotenv import load_dotenv

load_dotenv()

DATABASE = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE)
sessionLocal = sessionmaker(
    autocommit = False,
    autoflush = False,
    bind = engine)

Base = declarative_base()

def get_db():
    db = sessionLocal()
    try:
        yield db

    finally:
        db.close()    
    

