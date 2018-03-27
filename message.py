from flask import Blueprint, Flask, render_template, request, redirect, session, flash
from mysqlconnection import MySQLConnector
from user import *

app = Flask(__name__)
app.secret_key = 'SecretKey'
mysql = MySQLConnector(app,'RESTlite_Users_db')

messages = Blueprint('messages', __name__, template_folder='templates')
message = Blueprint('message', __name__, template_folder='templates')


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

@message.route('/create', methods=['POST'])
def create():
    if session.get('user_id') == None: return redirect('/')

    query = "INSERT INTO messages (user_id, message, created_at) VALUES (:user_id, :message, NOW())"
    data = { 'user_id': session['user_id'], 'message': request.form['message'], }
    mysql.query_db(query, data)
    return redirect('/wall')

@message.route('/<message_id>/delete', methods=['POST'])
def destroy(message_id):
    if session.get('user_id') == None: return redirect('/')

    query = "DELETE FROM comments WHERE message_id = :message_id"
    data = { 'message_id': message_id, }
    mysql.query_db(query, data)

    query = "DELETE FROM messages WHERE id = :message_id"
    data = { 'message_id': message_id, }
    mysql.query_db(query, data)
    return redirect('/wall')
