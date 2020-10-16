from firebase_admin import credentials, firestore, initialize_app, auth
from functools import wraps
from flask import Flask, request, jsonify
from app.services.user_service import UserService
from app.services.team_service import TeamService
from app.services.authentication_service import AuthenticationService
import pyrebase
import json
import sys

app = Flask(__name__) 

# Firebase variables initializers
cred = credentials.Certificate("conf/key.json")
firebase = initialize_app(cred)
db = firestore.client()
pb = pyrebase.initialize_app(json.load(open("conf/init.json")))

# Services initializers
user_service = UserService(db)
team_service = TeamService(db)
authentication_service = AuthenticationService(pb)

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

@app.route("/login", methods=['POST']) 
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    if email is None or password is None:
        return {'message': 'Error missing email or password'}, 400
    try:
        tokens = authentication_service.login(email, password)
        return tokens, 200
    except:
        return {'message': 'Error logging in'}, 400

@app.route("/reset_password", methods=['GET'])
@check_token
def reset_password():
    email = request.form.get('email')
    if email is None:
        return {'message': 'Error missing email or password'}, 400
    try:
        _ = authentication_service.reset_password(email)
        return {'message': 'Password reset email sent'}, 200
    except:
        return {'message': 'Error resseting password from email'}, 400

@app.route("/refresh_token", methods=['GET'])
@check_token
def refresh_token():
    try:
        user = authentication_service.refresh_token(request.form.get('refresh_token'))
        return {'user': user}, 200
    except:
        return {'message': 'Error refreshing token'}, 400

@app.route("/users", methods=['GET'])
@check_token
def get_users():
    try:
        user_list = user_service.get_all_users()
        return {'users': user_list}, 200
    except:
        return {'message': 'Error retrieving users'}, 400

@app.route("/users/update/<string:user_id>", methods=['POST'])
@check_token
def update_user_status(user_id):
    try:
        user_service.update_user_status(user_id, request.form.get('status'))
        return {'users': "user_list"}, 200
    except:
        return {'message': 'Error retrieving users'}, 400

@app.route("/teams", methods=['GET']) 
@check_token
def get_teams():
    try:
        user_list = user_service.get_all_users()
        team_list = team_service.get_all_teams(user_list)
        return {'teams': team_list}, 200
    except:
        return {'message': 'Error retrieving teams'}, 400
    
