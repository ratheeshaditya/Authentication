from pydantic import BaseModel
from datetime import timedelta
from oauth.model import UserAccount

"""
These classes are essentially schema for the response, which basically 
maps the class variables to the model variables. 
"""

class UserCreate(BaseModel):
    """
        This schema will be used to create a new user.
    """
    name: str
    last_name: str
    email: str
    phone_number: str
    country: str
    password: str



class UserUpdate(BaseModel):
    """
        This schema will be used to for updating a new user.
    """
    name: str
    last_name: str
    phone_number: str
    country: str
    password: str



class UserCreateSuccess(BaseModel):
    """
        This schema will be used to return a new user after successful 
        user creation.
    """

    name: str
    last_name: str
    email: str
    phone_number: str
    country: str
    password_hash: str #optional for reference


class UserLogin(BaseModel):
    """
        This schema will be used for taking in fields for the user login-in
    """
    email: str
    password: str


class AuthenticationToken(BaseModel):
    """
        After logging in the user, we will return the encrypted token which
        will contain the user object. Main difference is that it does not contain the password hash 
    """
    token_session: str