from flask import Flask, request
import sqlite3

from sqlite3 import Error

app = Flask(__name__)  # Flask constructor


def create_connection(path):
    connection = None

    try:
        connection = sqlite3.connect(path)

        print("Connection to SQLite DB successful")
    except Error as e:

        print(f"The error '{e}' occurred")

    return connection


def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query executed successfully")

        return cursor
    except Error as e:
        print(f"The error '{e}' occurred")


@app.route('/')
def create():
    db_conn = create_connection("Players.sqlite")

    create_query = """
CREATE TABLE IF NOT EXISTS Players (
Username INTEGER PRIMARY KEY AUTOINCREMENT,
Password TEXT NOT NULL
);
"""

    execute_query(db_conn, create_query)

    return "Successfully created table"

@app.route('/InsertUSer', methods=['POST'])
def insert():
    db_conn = create_connection("Players.sqlite")
    body = request.json

    insert_query = f"""
INSERT INTO Players(username, password) 
VALUES ("{body['username']}", {body['password']}" )
"""
    execute_query(db_conn, insert_query)

    return "Signup Success"

@app.route('/login', methods=['GET', 'POST'])
def login():
    db_conn = create_connection("chat.sqlite")
    get_query = """SELECT * FROM Players"""
    cursor = execute_query(db_conn, get_query)

    if request.method == 'POST':
        if request.form['username'] != get_query['username'] or request.form['password'] != get_query["password"]:
            return "Invalid username/password, please try again"
        else:
            return "logged in succesfully"