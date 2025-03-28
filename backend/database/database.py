import os
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Engine, create_engine
from dotenv import load_dotenv

load_dotenv()

def get_db():
    SessionLocal = sessionmaker(bind=__get_engine())
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def __get_engine() -> Engine:
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        raise ValueError(f"{'DATABASE_URL'} environment variable is not set.")
    return create_engine(database_url)