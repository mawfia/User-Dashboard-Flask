import re
import time
import datetime

from flask import Flask, render_template, request, redirect, session, flash
from mysqlconnection import MySQLConnector
from hashlib import md5

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'^[a-zA-Z-]{2,20}$')

app = Flask(__name__)
app.secret_key = 'SecretKey'
mysql = MySQLConnector(app,'RESTlite_Users_db')




#vacuum = Product(200, "Tornado", 25, "Bissel")
#vacuum.addTax(.13).sell().display_info().Return("Box Open").display_info()
