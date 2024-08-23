from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine
from oauth.base import Base
from dotenv import load_dotenv
import os

load_dotenv()

file_path = os.environ.get("DB_PATH")
engine = create_engine(f"sqlite+pysqlite:///{file_path}", echo=True, future=True)
Base.metadata.create_all(engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """
        This function returns a DB instance which can be used through dependency injection.
        This instance can be used perform CRUD operations on the DB based on the oauth.model
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()