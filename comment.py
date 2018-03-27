from flask import Blueprint, Flask, render_template, request, redirect, session, flash
from mysqlconnection import MySQLConnector
from user import *
from message import *

app = Flask(__name__)
app.secret_key = 'SecretKey'
mysql = MySQLConnector(app,'RESTlite_Users_db')

comments = Blueprint('comments', __name__, template_folder='templates')
comment = Blueprint('comment', __name__, template_folder='templates')

@comment.route('/<comment_id>/delete', methods=['POST'])
def destroy(comment_id):
    if session.get('user_id') == None: return redirect('/')

    query = "DELETE FROM comments WHERE id = :comment_id"
    data = { 'comment_id': comment_id, }
    mysql.query_db(query, data)
    return redirect('/wall')

@comment.route('/<message_id>', methods=['POST'])
def create(message_id):
    if session.get('user_id') == None: return redirect('/')

    query = "INSERT INTO comments (user_id, message_id, comment, created_at) VALUES (:user_id, :message_id, :comment, NOW())"
    data = { 'user_id': session['user_id'], 'message_id': message_id, 'comment': request.form['comment'], }
    mysql.query_db(query, data)
    return redirect('/wall')
