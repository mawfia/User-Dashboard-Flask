import re
import time
import datetime
import os, binascii

from flask import Blueprint, Flask, render_template, request, redirect, session, flash
from mysqlconnection import MySQLConnector
from hashlib import md5
from user import *
from message import *
from comment import *
from wall import *

PASSWORD_REGEX = re.compile(r'^(?=.*[0-9])(?=.*[A-Z])([a-zA-Z0-9!@#$%^&*()]{8,16})$')

app = Flask(__name__)
app.secret_key = 'SecretKey'
mysql = MySQLConnector(app,'RESTlite_Users_db')

app.register_blueprint(users, url_prefix='/users')
app.register_blueprint(user, url_prefix='/user')
app.register_blueprint(wall, url_prefix='/wall')
app.register_blueprint(messages, url_prefix='/messages')
app.register_blueprint(message, url_prefix='/message')
app.register_blueprint(comments, url_prefix='/comments')
app.register_blueprint(comment, url_prefix='/comment')

@app.route('/')
def index():
  # Authenticate user session
  if session.get('user_id') == None:
      session['permission_level'] = permissions(None)
      return render_template('index.html')
  else: return redirect('/user')

@app.route('/register', methods=['POST'])
def register():
  if 'user_id' in session: return redirect('/user')

  errors = validateName(request.form['fname'], request.form['lname'])
  errors += validateEmail(request.form['email'])
  errors += validatePassword(request.form['password'], request.form['cpassword'])
  errors += validateBirthdate(request.form['bdate'])

  if errors == 0:
    flash("{} {}, successfully registered.".format(request.form['fname'], request.form['lname']))
    # we want to insert into our query.
    query = "INSERT INTO users (first_name, last_name, email, password, salt, birthdate, created_at) VALUES (:first_name, :last_name, :email, :password, :salt, :birthdate, NOW())"
    # We'll then create a dictionary of data from the POST data received.
    SHP = SHPassword(request.form['password'])
    data = { 'first_name': request.form['fname'], 'last_name': request.form['lname'], 'email': request.form['email'],'password': SHP['shpassword'], 'salt': SHP['salt'], 'birthdate':request.form['bdate'], }
    # Run query, with dictionary values injected into the query.
    session['user_id'] = mysql.query_db(query, data)
    account = showUser(session['user_id'])
    session['permission_level'] = permissions(account['permission_level']).permissions_level
    return render_template('user.html', user=account)
  else: return render_template('index.html', fname=request.form['fname'], lname=request.form['lname'], email=request.form['email'], bdate=request.form['bdate'])

def validatePassword(password, cpassword, login=False):
    errors = 0

    if not PASSWORD_REGEX.match(request.form['password']):
        flash("Password must be 8-16 characters and contain at least one upper case letter and one number.")
        errors = 1
    if login == True: return errors
    elif password != cpassword:
        flash("Passwords do not match.")
        errors += 1

    return errors

# Salt and Hash password
def SHPassword(password):
    salt = binascii.b2a_hex(os.urandom(15))
    shpassword = md5((password + salt).encode('utf-8')).hexdigest()
    return {'shpassword':shpassword, 'salt': salt}

# Compate Salt and Hash password with password given
def deSHPassword(password, shpassword, salt):
    if shpassword == md5((password + salt).encode('utf-8')).hexdigest() : return True
    else: return False

@app.route('/login', methods=['POST'])
def login():
  if 'user_id' in session: return redirect('/user')

  errors = validateEmail(request.form['email'], True)
  errors += validatePassword(request.form['password'], None, True)

  if errors == 0:
    user = validateUser(request.form['email'])

    if len(user) == 0: flash("Login unsuccessful. Username/email '{}', not found.".format(request.form['email']))
    elif deSHPassword(request.form['password'], user['password'], user['salt']) == False: flash("Login unsuccessful. Incorrect password.")
    else:
        mysql.query_db("UPDATE users SET updated_at = NOW() WHERE id = :id", {'id': user['id']}) # Updated time stamp for user in db
        if session.get('user_id') == None:          #  This line may be unnecessary
            session['user_id'] = user['id']
            session['permission_level'] = permissions(user['permission_level'])
        return redirect('/')

  return render_template('index.html', email=request.form['email'])

@app.route('/logout')
def logout():
    if 'user_id' in session:
        del session['user_id']
        del session['permission_level']
    return redirect('/')

@app.route('/', defaults={'path':''})
@app.route('/<path:path>')
@app.route('/register/<path:path>')
def error(path):
    return redirect('/')
app.run(debug=True)
