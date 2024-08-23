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
        return None
    

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


def validate_current_user(token:str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
    Validates the current user based on the provided token. If the token is valid, and if the time of the last updated password in the token
    is the same as the one present in the database, no changes is made, otherwise 
    it returns the user object, otherwise, it raises a 401 Unauthorized error.
    """

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    token_expiry = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="The token has been expired",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(payload)
        if datetime.fromtimestamp(payload.get("exp")) < datetime.now(): #Checking if the payload date is expired
            raise token_expiry
        user_obj: str = payload.get("user_obj")
        if not user_obj:
            raise credentials_exception
        user = get_user(user_obj["email"],db) 
        
        if not user or datetime.fromisoformat(user_obj["password_last_updated"]) < user.password_last_updated:
            #Checking if the password has been changed.
            raise credentials_exception
        return user
    except InvalidTokenError:
        raise credentials_exception

@router.post("/validate_api",response_model=UserCreateSuccess)
def validate_current_user_api(token:str = Depends(oauth2_scheme),db: Session = Depends(get_db)):
    """
    Function to validate the token.
    """
    validate_current_user(token,db)



@router.post("/update_user",response_model=UserCreateSuccess)
def update_user(user_input: UserUpdate, current_user: dict = Depends(validate_current_user),db: Session = Depends(get_db)):
    
    """
    Function to update the user
    """
    
    getUser = get_user(current_user.email,db)
    if getUser:
        getUser.name = user_input.name
        getUser.last_name = user_input.last_name
        getUser.email = getUser.email #Leave it as default for now
        getUser.password_hash = get_password_hash(user_input.password)
        getUser.phone_number = user_input.phone_number
        getUser.country = user_input.country
        getUser.password_last_updated = datetime.now()
        db.add(getUser)
        db.commit()

    return getUser




@router.post("/authenticate",response_model=AuthenticationToken)
def authenticate_user(user: UserLogin, db: Session = Depends(get_db)):
    from oauth.utils import create_access_token
    """
    Function to authenticate a user
    """
    user_obj = authenticate(user,db)  #This calls a series of functions to authenticate the user
    get_token = create_access_token({"user_obj":{
                "name" : user_obj.name,
                "email" : user_obj.email,
                "last_name": user_obj.last_name,
                "phone_number" : user_obj.phone_number,
                "country" : user_obj.country,
                "password_last_updated": user_obj.password_last_updated.isoformat() 
            }
        }
    )
    
    token = AuthenticationToken(token_session=get_token)
    return token
    
    