from flask import Blueprint, Flask, render_template, request, redirect, session, flash
from mysqlconnection import MySQLConnector
from message import *
from user import *

wall = Blueprint('wall', __name__, template_folder='templates')

@wall.route('/')
def index():
    if session.get('user_id') == None: return redirect('/')

    return render_template('wall.html', messages=showMessages(), user=showUser(session['user_id']))

def showMessages():
    query = "SELECT messages.id, users.id AS user_id, messages.message, users.first_name, users.last_name, DATE_FORMAT(messages.created_at, '%M %D %Y') AS date, COUNT(users.id) AS users FROM users, messages, users_messages WHERE users.id = users_messages.user_id AND users_messages.message_id = messages.id GROUP BY messages.id, users.id, messages.message, users.first_name, users.last_name HAVING users < 2;"
    messages = mysql.query_db(query, data=None)
    if len(messages) > 0:
        for message in messages:
            query = "SELECT comments.id, comments.user_id, comments.message_id, comments.comment, users.first_name, users.last_name, DATE_FORMAT(comments.created_at, '%M %D %Y') AS date FROM users, comments WHERE comments.message_id = :message_id AND users.id = comments.user_id"
            data = { 'message_id': message['id'] }
            comments = mysql.query_db(query, data)
            print("{} {}".format(message['id'], len(comments)))
            if len(comments) > 0: message['comments'] = comments
            else: message['comments'] = []
        return messages
    else: return []
