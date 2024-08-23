The code is built through FastAPI using Python. Once you clone the project. 

1. First create a Python environment using the following command python -m venv env
2. Once its completed, you can run this script to activate the environment: ./env/scripts/activate (in windows) source /env/bin/activate (I'm not sure about this oen)
3. Run the command:- pip install -r requirements.txt
4. Navigate through the oauth_app folder, and run the command uvicorn main:app --reload. This will load up the APIs
5. With FastAPI we can access the list of APIs and execute them via http://127.0.0.1:8000/docs#/
 
