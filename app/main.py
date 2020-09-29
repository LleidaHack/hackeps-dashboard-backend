from firebase_admin import credentials, firestore, initialize_app, auth
from flask import Flask, request, jsonify
import pyrebase
import json

app = Flask(__name__) 

cred = credentials.Certificate("conf/key.json")
initialize_app(cred)
db = firestore.client()
pb = pyrebase.initialize_app(json.load(open("conf/init.json")))


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
