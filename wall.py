from flask import Blueprint, Flask, render_template, request, redirect, session, flash
from mysqlconnection import MySQLConnector
from message import *
from user import *
from comment import *

wall = Blueprint('wall', __name__, template_folder='templates')

@wall.route('/')
def index():
    if session.get('user_id') == None: return redirect('/')

    return render_template('wall.html', messages=wallMessages(), user=showUser(session['user_id']))

def wallMessages():

    query = "SELECT messages.id, users.id AS user_id, users_messages.id AS um_id, messages.message, users.first_name, users.last_name, DATE_FORMAT(messages.created_at, '%M %D %Y') AS date FROM users, messages, users_messages, (SELECT messages.id, COUNT(*) AS count FROM users, messages, users_messages WHERE users.id = users_messages.user_id AND users_messages.message_id = messages.id GROUP BY messages.id HAVING count < 2) AS um WHERE messages.id = um.id AND users_messages.message_id = um.id AND users_messages.user_id = users.id ORDER BY um_id DESC;"
    messages = mysql.query_db(query, data=None)

    if len(messages) > 0:
        for message in messages:
            comments = showComments(message['id'])
            if len(comments) > 0: message['comments'] = comments
            else: message['comments'] = []
        return messages
    else: return []
