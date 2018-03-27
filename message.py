
from flask import Blueprint, Flask, render_template, request, redirect, session, flash
from mysqlconnection import MySQLConnector
from user import *


messages = Blueprint('messages', __name__, template_folder='templates')
message = Blueprint('message', __name__, template_folder='templates')

@message.route('/create/<user_id>', methods=['POST'])
@message.route('/create', methods=['POST'])
def create(user_id=None):
    if session.get('user_id') == None: return redirect('/')

    data = { 'message': request.form['message'], }
    message_id = mysql.query_db("INSERT INTO messages (message, created_at) VALUES (:message, NOW())", data)
    query = "INSERT INTO users_messages (user_id, message_id) VALUES (:user_id, :message_id)"
    data = { 'user_id': session['user_id'], 'message_id': message_id }
    mysql.query_db(query, data)
    if user_id == None: return redirect('/wall')
    else:
        query = "INSERT INTO users_messages (user_id, message_id) VALUES (:user_id, :message_id)"
        data = { 'user_id': user_id, 'message_id': message_id }
        mysql.query_db(query, data)
        return redirect('/wall/' + user_id)



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
