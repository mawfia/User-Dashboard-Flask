import re
import time
import datetime

import os, binascii

from flask import Flask, render_template, request, redirect, session, flash
from mysqlconnection import MySQLConnector
from hashlib import md5
from User import *
from Car import Car

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'^[a-zA-Z-]{2,20}$')
PASSWORD_REGEX = re.compile(r'^(?=.*[0-9])(?=.*[A-Z])([a-zA-Z0-9!@#$%^&*()]{8,16})$')

app = Flask(__name__)
app.secret_key = 'SecretKey'
mysql = MySQLConnector(app,'RESTlite_Users_db')

@app.route('/')
def index():
  # Authenticate user session
  if session.get('user_id') == None:
      session['permission_level'] = permissions(None)
      return render_template('index.html')
  else: return render_template('user.html', user=User(session['user_id']))

@app.route('/register', methods=['POST'])
def register():
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
    account = User(session['user_id'])
    session['permission_level'] = permissions(account['permission_level']).permissions_level
    return render_template('user.html', user=account)
  else: return render_template('index.html', fname=request.form['fname'], lname=request.form['lname'], email=request.form['email'], bdate=request.form['bdate'])

def authenticate(destination):
    if session.get('user_id') == None: return redirect('/')
    elif destination: return redirect(destination)

def validateEmail(email):
    errors = 0
    if not EMAIL_REGEX.match(email):
       flash("Invalid Email Address!")
       errors = 1
    elif len(verifyUser(email)) != 0:
       flash("Username/email '{}', already exists.".format(email))
       return errors + 1
    else: return errors

def validatePassword(password, cpassword):
    errors = 0
    if password != cpassword:
        flash("Passwords do not match.")
        errors = 1
    elif not PASSWORD_REGEX.match(request.form['password']):
        flash("Password must be 8-16 characters and contain at least one upper case letter and one number.")
        errors += 1

    return errors

def validateBirthdate(ubdate): # takes unicoded birthdate as input
    date = datetime.datetime.fromtimestamp(time.time()).strftime('%m/%d/%Y').split('/') # todays date
    ebdate = ubdate.split('-') #encoded birthdate

    errors = 0
    if datetime.datetime(int(date[2])-18,int(date[0]),int(date[1])) <= datetime.datetime(int(ebdate[0]), int(ebdate[1]), int(ebdate[2])):
      flash("You must be 18 years or older to register.")
      errors = 1
    elif datetime.datetime(int(date[2])-130,int(date[0]),int(date[1])) > datetime.datetime(int(ebdate[0]), int(ebdate[1]), int(ebdate[2])):
      flash("Birthdate selected {}, out of range 18-130.".format(ubdate))
      errors += 1

    return errors

def verifyUser(email):
    query = "SELECT id, email, password, salt, permission_level FROM users WHERE email = :email"
    data = {'email':email}
    result = mysql.query_db(query, data)
    if len(result) != 0 : return result[0]
    else: return []

# Salt and Hash password
def SHPassword(password):
    salt = binascii.b2a_hex(os.urandom(15))
    shpassword = md5((password + salt).encode('utf-8')).hexdigest()
    return {'shpassword':shpassword, 'salt': salt}

# Compate Salt and Hash password with password given
def deSHPassword(password, shpassword, salt):
    if shpassword == md5((password + salt).encode('utf-8')).hexdigest() : return True
    else: return False

@app.route('/user/<user_id>')
def showOtherUser(user_id):
    if session.get('user_id') == None: return redirect('/')

    return render_template('user.html', user=User(user_id))

@app.route('/users')
def showUsers():
    if session.get('user_id') == None: return redirect('/')

    return render_template('users.html', users=Users())

@app.route('/user/create', methods=['GET'])
def createUser1():

    if session.get('user_id') == None: return redirect('/')

    return render_template('index.html', create=1)

@app.route('/user/create', methods=['POST'])
def createUser2():
    if session.get('user_id') == None: return redirect('/')

    errors = validateName(request.form['fname'], request.form['lname'])
    errors += validateEmail(request.form['email'])
    errors += validatePassword(request.form['password'], request.form['cpassword'])
    errors += validateBirthdate(request.form['bdate'])

    if errors == 0:
      flash("Successfully created acount for {} {}.".format(request.form['fname'], request.form['lname']))

      SHP = SHPassword(request.form['password'])

      if session['permission_level'][0] > 2:
          query = "INSERT INTO users (first_name, last_name, email, password, salt, birthdate, permission_level, created_at) VALUES (:first_name, :last_name, :email, :password, :salt, :birthdate, :permission_level, NOW())"
          data = { 'first_name':request.form['fname'], 'last_name':request.form['lname'], 'email':request.form['email'], 'password':SHP['shpassword'], 'salt':SHP['salt'], 'birthdate':request.form['bdate'], 'permission_level':request.form['permission_level'], }
      elif session['permission_level'] > 1:
          query = "INSERT INTO users (first_name, last_name, email, password, salt, birthdate, created_at) VALUES (:first_name, :last_name, :email, :password, :salt, :birthdate, NOW())"
          data = { 'first_name':request.form['fname'], 'last_name':request.form['lname'], 'email':request.form['email'],'password':SHP['shpassword'], 'salt':SHP['salt'], 'birthdate':request.form['bdate'], }

      mysql.query_db(query, data)
      return redirect('/users')
    return redirect('/?create=1')



@app.route('/user/<user_id>/delete')
def deleteUser(user_id):
    mysql.query_db("DELETE FROM users WHERE id = :id", {'id':user_id})

    if session['user_id'] == user_id: return redirect('/logout')
    else: return redirect('/users')

@app.route('/user/<user_id>/update', methods=['POST'])
def updateUser(user_id):
    if session.get('user_id') == None: return redirect('/')

    errors = validateName(request.form['fname'], request.form['lname'])
    if not EMAIL_REGEX.match(request.form['email']): errors += 1
    errors += validateBirthdate(request.form['bdate'])

    if errors == 0:
        if session['permission_level'][0] >= 2:
            query = "UPDATE users SET first_name = :first_name, last_name = :last_name, email = :email, birthdate = :birthdate, permission_level = :permission_level WHERE id = :id"
            data = { 'first_name': request.form['fname'], 'last_name':  request.form['lname'], 'email': request.form['email'], 'birthdate': request.form['bdate'], 'permission_level': request.form['permission_level'], 'id': user_id, }
        else:
            query = "UPDATE users SET first_name = :first_name, last_name = :last_name, email = :email, birthdate = :birthdate WHERE id = :id"
            data = { 'first_name': request.form['fname'], 'last_name':  request.form['lname'], 'email': request.form['email'], 'birthdate': request.form['bdate'], 'id': user_id, }
        mysql.query_db(query, data)

    if session['user_id'] == user_id: return redirect('/')
    else: return redirect('/user/' + user_id)

@app.route('/login', methods=['POST'])
def login():

  errors = 0
  if not EMAIL_REGEX.match(request.form['email']):
    flash("Invalid Email Address!")
    errors = 1
  if not PASSWORD_REGEX.match(request.form['password']):
    flash("Password must be 8-16 characters and contain at least one upper case letter and one number.")
    errors = 1

  if errors == 0:
    user = verifyUser(request.form['email'])

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
    session['user_id'] = None
    session['permission_level'] = None
    return redirect('/')

@app.route('/wall')
def wall():
    if session.get('user_id') == None: return redirect('/')

    return render_template('wall.html', messages=showMessages(), user=User(session['user_id']))

def showMessages():
    query = "SELECT messages.id, messages.user_id, messages.message, users.first_name, users.last_name, DATE_FORMAT(messages.created_at, '%M %D %Y') AS date FROM users, messages WHERE users.id = messages.user_id"
    messages = mysql.query_db(query, data=None)
    if len(messages) > 0:
        for message in messages:
            query = "SELECT comments.id, comments.user_id, comments.comment, users.first_name, users.last_name, DATE_FORMAT(comments.created_at, '%M %D %Y') AS date FROM users, comments WHERE comments.message_id = :message_id AND users.id = comments.user_id"
            data = { 'message_id': message['id'] }
            comments = mysql.query_db(query, data)
            if len(comments) > 0: message['comments'] = comments
            else: message['comments'] = []
        return messages
    else: return []

@app.route('/message', methods=['POST'])
def createMessage():
    authenticate(None)

    query = "INSERT INTO messages (user_id, message, created_at) VALUES (:user_id, :message, NOW())"
    data = { 'user_id': session['user_id'], 'message': request.form['message'], }
    mysql.query_db(query, data)
    return redirect('/wall')

@app.route('/message/<message_id>/delete', methods=['POST'])
def deleteMessage(message_id):
    authenticate('/wall')

    query = "DELETE FROM comments WHERE message_id = :message_id"
    data = { 'message_id': message_id, }
    mysql.query_db(query, data)

    query = "DELETE FROM messages WHERE id = :message_id"
    data = { 'message_id': message_id, }
    mysql.query_db(query, data)
    return redirect('/wall')

@app.route('/comment/<comment_id>/delete', methods=['POST'])
def deleteComment(comment_id):
    authenticate('/wall')

    query = "DELETE FROM comments WHERE id = :comment_id"
    data = { 'comment_id': comment_id, }
    mysql.query_db(query, data)
    return redirect('/wall')

@app.route('/comment/<message_id>', methods=['POST'])
def createComment(message_id):
    authenticate(None)

    query = "INSERT INTO comments (user_id, message_id, comment, created_at) VALUES (:user_id, :message_id, :comment, NOW())"
    data = { 'user_id': session['user_id'], 'message_id': message_id, 'comment': request.form['comment'], }
    mysql.query_db(query, data)
    return redirect('/wall')

@app.route('/', defaults={'path':''})
@app.route('/<path:path>')
@app.route('/register/<path:path>')
def error(path):
    return redirect('/')
app.run(debug=True)
