from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, Session
from sqlalchemy import create_engine, Column, DateTime, Date, String,ForeignKey,Enum as SQLAlchemyEnum
from .base import Base
from enum import Enum
from datetime import datetime 

class UserAccount(Base):

    """
        This schema defines the User database.
    """


    __tablename__ = "user_account"
    id: Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    name: Mapped[str] = mapped_column(String(30))
    last_name: Mapped[str] = mapped_column(String(30))
    email: Mapped[str] = mapped_column(String(50),unique=True)
    password_hash = Column(String, nullable=False)
    country = Column(String, nullable=False)
    phone_number: Mapped[str] = mapped_column(String(50))
    password_last_updated: Mapped[DateTime] = Column(DateTime, default=datetime.now)
    def __repr__(self):
        return f"<UserAccount(id={self.id}, name={self.name}, email={self.email})>"
    
