from flask import Flask, jsonify, request, make_response, redirect, url_for
import uuid
from  werkzeug.security import generate_password_hash, check_password_hash
from db import User

from __main__ import app


# login route
@app.route("/login", methods =['POST'])
def login():
    auth = request.form
    if not auth or not auth.get('username') or not auth.get('password'):
        return make_response(
            'Could not verify',
            401,
            {'WWW-Authenticate' : 'Basic realm ="Login required !!"'}
        )
    user = User.objects(name = auth.get('username')).first()
    if not user:
        return make_response(
            'Could not verify',
            401,
            {'WWW-Authenticate' : 'Basic realm ="User does not exist !!"'}
        )

    if check_password_hash(user.password, auth.get('password')):
        return make_response(jsonify({"status":"SUCCESS", "output":"Logged in successfully"}), 201)
    
    return make_response(
        'Could not verify',
        403,
        {'WWW-Authenticate' : 'Basic realm ="Wrong Password !!"'}
    )
  
# signup route
@app.route("/signup", methods =['POST'])
def signup():
    name, email = request.form["username"], request.form["email"]
    password = request.form["password"]
    user = User.objects(email=email).first()
    if not user:
        # database ORM object
        User(
            public_id = str(uuid.uuid4()),
            name = name,
            email = email,
            password = generate_password_hash(password)
        ).save()
  
        # return redirect(url_for('home'))
        return make_response(jsonify({"status":"SUCCESS", "output":"Signed up successfully"}), 201)
    else:
        return make_response('User already exists. Please Log in.', 202)
