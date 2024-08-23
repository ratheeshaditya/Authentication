from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime 
from response_types import AuthenticationToken, UserCreateSuccess, UserCreate, UserLogin, UserUpdate
from db import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from dotenv import load_dotenv
import jwt
from jwt.exceptions import InvalidTokenError
import os

#This function is to load all environment variables
load_dotenv()

#Load private keys via environment variables
SECRET_KEY = os.environ.get("SECRET_KEY")

ALGORITHM = os.environ.get("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES")


router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")



def verify_password(plain_password, hashed_password):
    """
    Function to verify the password
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    """
    Function to hash the plain-text password
    """
    return pwd_context.hash(password)


def get_user(email, db):
    """
    Function to get a user object given an email. Returns 404
    in the case of user not found.
    """
    from oauth.model import UserAccount
    user_obj = db.query(UserAccount).filter(UserAccount.email==email).first()
    db.close()
    if user_obj:
        #If there is a user found with the email
        return user_obj
    else:
        return False
    

@router.post("/create",response_model=UserCreateSuccess)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    from oauth.model import UserAccount
    """
    Function to create a user
    """
    lookup_user = get_user(email=user.email,db=db)
    if not lookup_user:
        #Check if the user already exists.
        password_hash = get_password_hash(user.password)
        new_user = UserAccount(name=user.name,last_name=user.last_name,
                                                email=user.email,password_hash=password_hash,
                                                phone_number=user.phone_number,
                                                country=user.country)
        db.add(new_user)
        db.commit()
        return new_user
    else:
        #Raise exception
        raise HTTPException(status_code=400, detail="Email already exists")


def authenticate(user:UserLogin,db):
    """
    Performs the entire authentication process for the given user ranging from
    -> Fetching the user
    -> Verifying the password
    """
    user_obj = get_user(user.email,db)
    if not verify_password(user.password, user_obj.password_hash): #Return 
        #Returning same exception for both
        raise HTTPException(status_code=404, detail="User not found or invalid username or password")
    return user_obj #Returns a user object
