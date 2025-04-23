from flask import request, render_template, make_response, Flask
import os
import sqlite3
import jwt  # unused import for alert
import re   # unused import for alert

flaskapp = Flask(__name__)
cursor = sqlite3.connect("data.db").cursor()

# Hardcoded token (CodeQL will flag this)
SLACK_TOKEN3 = "xoxb-243254323452332452323-0987654321123-A1b2C3d4E5f6G7h8I9j0"

class Book:
    def __init__(self, name, author, read):
        self.name = name
        self.author = author
        self.read = read

@flaskapp.route('/', methods=['GET', 'POST'])
def index():
    name = request.args.get('name')
    author = request.args.get('author')
    read = request.args.get('read')  # Will be interpreted as a string like "true" or "false"
    
    # Simulate insecure code that branches on user input
    if name:
        # SQL Injection vulnerability
        cursor.execute("SELECT * FROM books WHERE name LIKE '%" + name + "%'")
        books = [Book(*row) for row in cursor]
    
    elif author:
        # SQL Injection vulnerability
        cursor.execute("SELECT * FROM books WHERE author LIKE '%" + author + "%'")
        books = [Book(*row) for row in cursor]
    
    else:
        # Read everything
        cursor.execute("SELECT name, author, read FROM books")
        books = [Book(*row) for row in cursor]

    # Response without proper security headers (XSS risks if template isn't escaped)
    response = make_response(render_template("books.html", books=books))
    return response
