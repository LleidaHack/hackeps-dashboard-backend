from firebase_admin import credentials, firestore, initialize_app, auth
from functools import wraps
from flask import Flask, request, jsonify
from app.services.user_service import UserService
from app.services.team_service import TeamService
import pyrebase
import json

app = Flask(__name__) 

# Firebase variables initializers
cred = credentials.Certificate("conf/key.json")
firebase = initialize_app(cred)
db = firestore.client()
pb = pyrebase.initialize_app(json.load(open("conf/init.json")))

# Services initializers
user_service = UserService()
team_service = TeamService()

def check_token(f):
    @wraps(f)
    def wrap(*args,**kwargs):
        if not request.headers.get('token'):
            return {'message': 'No token provided'},400
        try:
            user = auth.verify_id_token(request.headers['token'])
            request.user = user
        except:
            return {'message':'Invalid token provided.'},400
        return f(*args, **kwargs)
    return wrap

@app.route("/login", methods=['GET']) 
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    if email is None or password is None:
        return {'message': 'Error missing email or password'}, 400
    try:
        user = pb.auth().sign_in_with_email_and_password(email, password)
        token = user['idToken']
        return {'token':token}, 200
    except:
        return {'message': 'Error logging in'}, 400

@app.route("/getUsers", methods=['GET'])
@check_token
def get_users():
    user_list = user_service.get_all_users(db)
    print(user_list)
    return {'users': user_list}, 200    

@app.route("/getTeams", methods=['GET']) 
@check_token
def get_teams():
    user_list = user_service.get_all_users(db)
    team_list = team_service.get_all_teams(db, user_list)
    return {'teams': team_list}, 200
    firebase.auth().signOut()