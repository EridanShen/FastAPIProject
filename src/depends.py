from sqlalchemy.orm import Session
from src.main import SessionLocal

def get_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

