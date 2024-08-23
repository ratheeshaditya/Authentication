from sqlalchemy import create_engine
from oauth import auth_api
# from models.db import SessionLocal
from sqlalchemy.orm import Session, sessionmaker
from fastapi import FastAPI, HTTPException,Depends


from fastapi.middleware.cors import CORSMiddleware



app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace "*" with specific origins if needed
    allow_credentials=True,
    allow_methods=["*"],  # Or specify the methods you want to allow
    allow_headers=["*"],  # Or specify the headers you want to allow
)

app.include_router(auth_api.router, prefix="/user", tags=["User Authentication"])

