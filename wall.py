from flask import Blueprint, Flask, render_template, request, redirect, session, flash
from mysqlconnection import MySQLConnector
from message import *
from user import *
from comment import *

wall = Blueprint('wall', __name__, template_folder='templates')

@wall.route('/')
def index(user_id=None):
    if session.get('user_id') == None: return redirect('/')

    return render_template('wall.html', messages=showMessages(user_id), user=showUser(session['user_id']))

def showMessages(user_id=None):

    if user_id == None:
        query = "SELECT messages.id, users.id AS user_id, users_messages.id AS um_id, messages.message, users.first_name, users.last_name, DATE_FORMAT(messages.created_at, '%M %D %Y') AS date FROM users, messages, users_messages, (SELECT messages.id, COUNT(*) AS count FROM users, messages, users_messages WHERE users.id = users_messages.user_id AND users_messages.message_id = messages.id GROUP BY messages.id HAVING count < 2) AS um WHERE messages.id = um.id AND users_messages.message_id = um.id AND users_messages.user_id = users.id;"
        messages = mysql.query_db(query, data=None)
    else:
        query = "SELECT messages.id, users.id AS user_id, users_messages.id AS um_id, messages.message, users.first_name, users.last_name, DATE_FORMAT(messages.created_at, '%M %D %Y') AS date FROM users, messages, users_messages, (SELECT messages.id, COUNT(*) AS count FROM users, messages, users_messages WHERE users.id = users_messages.user_id AND users_messages.message_id = messages.id GROUP BY messages.id HAVING count = 2) AS um WHERE messages.id = um.id AND users_messages.message_id = um.id AND users_messages.user_id = users.id ORDER BY um_id ASC;"
        results = mysql.query_db(query, data={"user_id":user_id})
        messages = []
        for m in range(0,len(results),2):
            if results[m+1]['user_id'] == user_id or results[m+1]['um_id'] > results[m]['um_id']:
                messages.append(results[m])
                messages[len(messages)-1]['user_from'] = results[m]['user_id']
                messages[len(messages)-1]['user_to'] = results[m+1]['user_id']
            print(messages)
    if len(messages) > 0:
        for message in messages:
            comments = showComments(message['id'])
            if len(comments) > 0: message['comments'] = comments
            else: message['comments'] = []
        return messages
    else: return []
