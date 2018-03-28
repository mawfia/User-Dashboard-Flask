from flask import Blueprint, Flask, render_template, request, redirect, session, flash
from mysqlconnection import MySQLConnector
from user import *
from message import *

comments = Blueprint('comments', __name__, template_folder='templates')
comment = Blueprint('comment', __name__, template_folder='templates')

def showComments(message_id, comments_id=None):
    query = "SELECT comments.id, comments.user_id, comments.message_id, comments.comment, users.first_name, users.last_name, DATE_FORMAT(comments.created_at, '%M %D %Y') AS date FROM users, comments WHERE comments.message_id = :message_id AND users.id = comments.user_id"
    data = { 'message_id': message_id }
    return mysql.query_db(query, data)

@comment.route('/<comment_id>/<user_id>/delete', methods=['POST'])
@comment.route('/<comment_id>/delete', methods=['POST'])
def destroy(comment_id, user_id=None):
    if session.get('user_id') == None: return redirect('/')

    query = "DELETE FROM comments WHERE id = :comment_id"
    data = { 'comment_id': comment_id, }
    mysql.query_db(query, data)

    if user_id == None: return redirect('/wall')
    else: return redirect('/user/'+user_id)

@comment.route('/<message_id>/<user_id>', methods=['POST'])
@comment.route('/<message_id>', methods=['POST'])
def create(message_id, user_id=None):
    if session.get('user_id') == None: return redirect('/')

    query = "INSERT INTO comments (user_id, message_id, comment, created_at) VALUES (:user_id, :message_id, :comment, NOW())"
    data = { 'user_id': session['user_id'], 'message_id': message_id, 'comment': request.form['comment'], }
    mysql.query_db(query, data)

    if user_id == None: return redirect('/wall')
    else: return redirect('/user/'+user_id)
