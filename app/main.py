from firebase_admin import credentials, firestore, initialize_app, auth
from functools import wraps
from flask import Flask, request, jsonify
import pyrebase
import json

app = Flask(__name__) 

cred = credentials.Certificate("conf/key.json")
firebase = initialize_app(cred)
db = firestore.client()
pb = pyrebase.initialize_app(json.load(open("conf/init.json")))

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
    users = db.collection(u'hackeps-2019').document(u'dev').collection(u'users').get()
    user_list = list()
    for user in users:
        user_list.append(user.to_dict())
    
    return {'users': user_list}, 200    

@app.route("/getTeams", methods=['GET']) 
@check_token
def get_teams():
    users = db.collection(u'hackeps-2019').document(u'prod').collection(u'users').get()
    teams = db.collection(u'hackeps-2019').document(u'prod').collection(u'teams').get()
    team_list = list()
    
    for team in teams:
        team = team.to_dict()
        prov_members = list()
        for member in team['members']:
            if member is not None:
                rmv_index = -1
                for index, user in enumerate(users):
                    if user.id == member.id:
                        rmv_index = index
                        prov_members.append(user.to_dict())
                        break
                if rmv_index != -1:
                    users.pop(rmv_index)
                        
        prov_team = {
            'name': team['name'], 
            'uid': team['uid'],
            'members': prov_members}
        team_list.append(prov_team)
        
    
    return {'teams': team_list}, 200