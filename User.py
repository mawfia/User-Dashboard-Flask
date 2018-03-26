import re

from flask import Flask, render_template, request, redirect, session, flash
from mysqlconnection import MySQLConnector

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'^[a-zA-Z-]{2,20}$')

app = Flask(__name__)
app.secret_key = 'SecretKey'
mysql = MySQLConnector(app,'RESTlite_Users_db')

class User(object):
    def __init__(self, ID=None, first_name=None, last_name=None, email=None, password=None, salt=None, birthdate=None, permission_level=[0,'Guest']):
      self.id = ID
      self.first_name = first_name
      self.last_name = last_name
      self.email = email
      self.password = password
      self.birthdate = birthdate
      self.permission_level = permission_level

    def register(self, first_name, last_name, email, password, salt, birthdate, permission_level):
      self.status = "Sold"
      return self

    def permissions(self, level):
      if level == None or level == 0: self.permissions_level = [0,'Guest']
      elif level == 1 or level == 'Basic': self.permissions_level = [1, 'Basic']
      elif level == 2 or level == 'Admin Level 1': self.permissions_level = [2, 'Admin Level 1']
      elif level == 3 or level == 'Admin Level 2': self.permissions_level = [3, 'Admin Level 2']
      else: self.permissions_level = [0, 'Guest']
      return self

    def validateName(fname, lname):
        if not NAME_REGEX.match(fname) or not NAME_REGEX.match(lname):
            flash("First and last name must be 2-20 characters and contain only letters a-z.")
            return 1
        else: return 0

    def showUser(self, user_id):
        query = "SELECT id, first_name, last_name, email, DATE_FORMAT(birthdate, '%Y-%m-%d') AS birthdate, permission_level, created_at, updated_at FROM users WHERE id = :id"
        data = {'id':user_id}
        result = mysql.query_db(query, data)

        if len(result) != 0 :
            result[0]['permission_level'] = self.permissions(result[0]['permission_level']).permissions_level
            return result[0]
        else: return []

    def showUsers():
        if session.get('user_id') == None: return redirect('/')

        query = "SELECT id, first_name, last_name, email, DATE_FORMAT(birthdate, '%Y-%m-%d') AS birthdate, permission_level, DATE_FORMAT(created_at, '%Y-%m-%d') AS created_at, DATE_FORMAT(updated_at, '%Y-%m-%d') AS updated_at FROM users"
        users = mysql.query_db(query, data=None)
        for user in users:
            new_user = User()
            user['permission_level'] = new_user.permissions(user['permission_level']).permissions_level

        return users
#vacuum = Product(200, "Tornado", 25, "Bissel")
#vacuum.addTax(.13).sell().display_info().Return("Box Open").display_info()
