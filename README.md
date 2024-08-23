The code is built through FastAPI using Python. Once you clone the project. 

1. First create a Python environment using the following command python -m venv env
2. Once its completed, you can run this script to activate the environment: ./env/scripts/activate (in windows) source /env/bin/activate (I'm not sure about this oen)
3. Run the command:- pip install -r requirements.txt
4. Navigate through the oauth_app folder, and run the command uvicorn main:app --reload. This will load up the APIs
5. With FastAPI we can access the list of APIs and execute them via http://127.0.0.1:8000/docs#/

 You should land in the API page:- 
![l;adning](https://github.com/user-attachments/assets/d81ee93c-0901-4436-a6dd-a22a4e5e259d)

auth_api.py - Contains all the methods API routes for the authentication
model.py - Contains the models (Users)
uitils.py - Utility function
main.py - Main python file.

The .env file contains :-
- SECRET_KEY
- ALGORITHM
- ACCESS_TOKEN_EXPIRE_MINUTES
- DB_PATH

