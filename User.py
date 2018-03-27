import re

from flask import Flask, render_template, request, redirect, session, flash
from mysqlconnection import MySQLConnector

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'^[a-zA-Z-]{2,20}$')

app = Flask(__name__)
app.secret_key = 'SecretKey'
mysql = MySQLConnector(app,'RESTlite_Users_db')


def permissions(level):
  if level == None or level == 0: permissions_level = [0,'Guest']
  elif level == 1 or level == 'Basic': permissions_level = [1, 'Basic']
  elif level == 2 or level == 'Admin Level 1': permissions_level = [2, 'Admin Level 1']
  elif level == 3 or level == 'Admin Level 2': permissions_level = [3, 'Admin Level 2']
  else: permissions_level = [0, 'Guest']
  return permissions_level

def validateName(fname, lname):
    if not NAME_REGEX.match(fname) or not NAME_REGEX.match(lname):
        flash("First and last name must be 2-20 characters and contain only letters a-z.")
        return 1
    else: return 0

def User(user_id):
    query = "SELECT id, first_name, last_name, email, DATE_FORMAT(birthdate, '%Y-%m-%d') AS birthdate, permission_level, created_at, updated_at FROM users WHERE id = :id"
    data = {'id':user_id}
    result = mysql.query_db(query, data)

    if len(result) != 0 :
        result[0]['permission_level'] = permissions(result[0]['permission_level'])
        return result[0]
    else: return []

def Users():
    query = "SELECT id, first_name, last_name, email, DATE_FORMAT(birthdate, '%Y-%m-%d') AS birthdate, permission_level, DATE_FORMAT(created_at, '%Y-%m-%d') AS created_at, DATE_FORMAT(updated_at, '%Y-%m-%d') AS updated_at FROM users"
    users = mysql.query_db(query, data=None)
    for user in users:
        user['permission_level'] = permissions(user['permission_level'])

    return users
#vacuum = Product(200, "Tornado", 25, "Bissel")
#vacuum.addTax(.13).sell().display_info().Return("Box Open").display_info()
