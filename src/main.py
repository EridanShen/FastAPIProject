from fastapi import FastAPI
import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.db import Base
from src import apifile
import uvicorn


app = FastAPI()

app.include_router(apifile.router)

DATABASE_URL = "postgresql+psycopg2://postgres:posgtres@localhost/testapi"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    uvicorn.run('main:app', host="0.0.0.0", port=8000)
