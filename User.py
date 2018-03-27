import re
import time
import datetime

from flask import Blueprint, Flask, render_template, request, redirect, session, flash
from mysqlconnection import MySQLConnector
from hashlib import md5

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'^[a-zA-Z-]{2,20}$')

app = Flask(__name__)
app.secret_key = 'SecretKey'
mysql = MySQLConnector(app,'RESTlite_Users_db')

users = Blueprint('users', __name__, template_folder='templates')
user = Blueprint('user', __name__, template_folder='templates')


@user.route('/')
def index():
    return render_template('user.html', messages=userMessages(session['user_id']), user=showUser(session['user_id']))

def userMessages(user_id):

    query = "SELECT messages.id, users.id AS user_id, users_messages.id AS um_id, messages.message, users.first_name, users.last_name, DATE_FORMAT(messages.created_at, '%M %D %Y') AS date FROM users, messages, users_messages, (SELECT messages.id, COUNT(*) AS count FROM users, messages, users_messages WHERE users.id = users_messages.user_id AND users_messages.message_id = messages.id GROUP BY messages.id HAVING count = 2) AS um WHERE messages.id = um.id AND users_messages.message_id = um.id AND users_messages.user_id = users.id;"
    results = mysql.query_db(query, data={"user_id":user_id})
    messages = []
    for m in range(0,len(results),2):
        if results[m+1]['user_id'] == int(user_id) and results[m+1]['um_id'] > results[m]['um_id']:
            messages.append(results[m])
            messages[len(messages)-1]['from_id'] = results[m]['user_id']
            messages[len(messages)-1]['to_id'] = results[m+1]['user_id']
    if len(messages) > 0:
        for message in messages:
            query = "SELECT comments.id, comments.user_id, comments.message_id, comments.comment, users.first_name, users.last_name, DATE_FORMAT(comments.created_at, '%M %D %Y') AS date FROM users, comments WHERE comments.message_id = :message_id AND users.id = comments.user_id"
            data = { 'message_id': message['id'] }
            comments = mysql.query_db(query, data)
            if len(comments) > 0: message['comments'] = comments
            else: message['comments'] = []
        return messages
    else: return []

def permissions(level):
  if level == None or level == 0: permissions_level = [0,'Guest']
  elif level == 1 or level == 'Basic': permissions_level = [1, 'Basic']
  elif level == 2 or level == 'Admin Level 1': permissions_level = [2, 'Admin Level 1']
  elif level == 3 or level == 'Admin Level 2': permissions_level = [3, 'Admin Level 2']
  else: permissions_level = [0, 'Guest']
  return permissions_level

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

def validateName(fname, lname):
  if not NAME_REGEX.match(fname) or not NAME_REGEX.match(lname):
      flash("First and last name must be 2-20 characters and contain only letters a-z.")
      return 1
  else: return 0

def showUser(user_id):
  query = "SELECT id, first_name, last_name, email, DATE_FORMAT(birthdate, '%Y-%m-%d') AS birthdate, permission_level, created_at, updated_at FROM users WHERE id = :id"
  data = {'id':user_id}
  result = mysql.query_db(query, data)

  if len(result) != 0 :
      result[0]['permission_level'] = permissions(result[0]['permission_level'])
      return result[0]
  else: return []

@user.route('/<user_id>')
def showOtherUser(user_id):
  if session.get('user_id') == None: return redirect('/')
  elif session['user_id'] == int(user_id): return redirect('/user')
  else: return render_template('user.html', messages=userMessages(user_id), user=showUser(user_id))

@users.route('/')
def showUsers():
    if session.get('user_id') == None: return redirect('/')

    query = "SELECT id, first_name, last_name, email, DATE_FORMAT(birthdate, '%Y-%m-%d') AS birthdate, permission_level, DATE_FORMAT(created_at, '%Y-%m-%d') AS created_at, DATE_FORMAT(updated_at, '%Y-%m-%d') AS updated_at FROM users"
    users = mysql.query_db(query, data=None)
    for user in users:
        user['permission_level'] = permissions(user['permission_level'])
    return render_template('users.html', users=users)

@user.route('/<user_id>/update', methods=['POST'])
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

    if session['user_id'] == user_id: return redirect('/user')
    else: return redirect('/user/' + user_id)

@user.route('/create', methods=['GET'])
def createUser1():

    if session.get('user_id') == None: return redirect('/')

    return render_template('index.html', create=1)

@user.route('/create', methods=['POST'])
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

@user.route('/<user_id>/delete')
def destroy(user_id):
    mysql.query_db("DELETE FROM users WHERE id = :id", {'id':user_id})

    if session['user_id'] == user_id: return redirect('/logout')
    else: return redirect('/users')

#vacuum = Product(200, "Tornado", 25, "Bissel")
#vacuum.addTax(.13).sell().display_info().Return("Box Open").display_info()
