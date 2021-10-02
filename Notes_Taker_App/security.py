import sqlite3
from flask import request,jsonify


def authenticate(username,password):
    user = User.find_by_username(username)
    if user and user.password == password:
        return user


def identity(payload):
    user_id = payload['identity']
    return User.find_by_id(user_id)




class User:
    def __init__(self,_id,username,password):
        self.id = _id,
        self.username = username,
        self.password = password

    @classmethod
    def find_by_username(cls,username):
        connection = sqlite3.connect('notes.db')
        cursor = connection.cursor()
        user_fetch_username = "SELECT * FROM users WHERE username= ?"
        user = cursor.execute(user_fetch_username, (username,)).fetchone()
        if user:
            user = User(user[0],user[1],user[2])
        else:
            user = None
        connection.close()
        return user

    @classmethod
    def find_by_id(cls,_id):
        connection = sqlite3.connect('notes.db')
        cursor = connection.cursor()
        user_fetch_id = "SELECT * FROM users WHERE id= ?"
        user = cursor.execute(user_fetch_id, (_id,)).fetchone()
        if user:
            user = User(user[0],user[1],user[2])
        else:
            user = None
        connection.close()
        return user