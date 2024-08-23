from datetime import datetime, timedelta, timezone
import os
import jwt
from oauth.auth_api import SECRET_KEY,ALGORITHM,ACCESS_TOKEN_EXPIRE_MINUTES

def create_access_token(data: dict):
    """
    Function to create the access token once the user is authenticated.
    """
    
    to_encode = data.copy()
    #Expiry is the current time + configured time. If no token expiry is provided, default is 15
    expire = datetime.now() + timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES) if ACCESS_TOKEN_EXPIRE_MINUTES else 15)
    print("Expiry is : ",expire)
    to_encode.update({"exp": expire}) #Add token expiry date
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt