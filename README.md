The code is built through FastAPI using Python. 
1. First create a Python environment using the following command python -m venv env
2. Once its completed, you can run this script to activate the environment: ./env/scripts/activate (in windows) source /env/bin/activate (I'm not sure about Mac/Linux)
3. Run the command:- pip install -r requirements.txt to install the required dependencies
4. Navigate through the oauth_app folder, and run the command uvicorn main:app --reload. This will load up the APIs
5. With FastAPI we can access the list of APIs and execute them via http://127.0.0.1:8000/docs#/

 You should land in the API page, where you can create, update, authenticate user:- 
![l;adning](https://github.com/user-attachments/assets/d81ee93c-0901-4436-a6dd-a22a4e5e259d)

## File structure

- auth_api.py - Contains all the methods API routes for the authentication and token verification
- model.py - Contains the models (Users)
- uitils.py - Utility function(to create access tokens)
- main.py - Main python file which contains the code to insantiate a FastAPI instance.
- response_types.py - Contains the schema of the request/response of the API
- auth_db - Empty database.

## Environment Variables
The .env file contains :-
- SECRET_KEY
- ALGORITHM
- ACCESS_TOKEN_EXPIRE_MINUTES
- DB_PATH

Note: The final proof of concept application is incomplete. Here’s an overview of what has been implemented and the intended functionality:

Update 24/08/2024. Just thought I'll add a bit more information to make things much more clear and my thought process. **No code changes was made in this update**.

## API Implementation and Logic
  What I was trying to do is to have an API to:-
  - Create a new user (user/create)
  
  - Update user information (user/update_user)
    
  - Authenticate user and provide an access token(JWT)(/authenticate).
    
  - Validate current user(user/validate_api). This basically checks whether the user is valid by performing checks such as token expiry or whether the user has changed the password.
    
    - For the logic to expire the sessions on password change, I basically added a field password_last_updated in the User model, and when the user is updated, the field gets updated. This field is also encoded in the access token when the token is generated, which will be used to expire all the tokens when if the password is updated(since the newly updated field in the User model > than the updated field in the access token).

## Proof of Concept application
For the proof of concept application, I wanted to create a log-in page, that authenticates the user. Once the user is authenticated and the token is provided. For every service that the user requests it calls the validate current user api(/validate_api) to see if the token is valid, and it returns invalid if the token is expired/invalid. So if the user changes the password from the SSO provider, it gets expired because the password_last_updated is updated. Hence, when the /validate_api is called when requesting a service, it rejects the user session.

This is achived using the Depends() function in FastAPI. So for every API call, it makes request on the /validate_api with the token.
