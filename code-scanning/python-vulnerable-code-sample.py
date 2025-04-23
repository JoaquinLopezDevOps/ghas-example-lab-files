from flask import request, render_template, make_response, Flask
import sqlite3

flaskapp = Flask(__name__)
conn = sqlite3.connect("data.db", check_same_thread=False)
cursor = conn.cursor()

# 🚨 Hardcoded sensitive token
SLACK_TOKEN3 = "xoxb-243254323452332452323-0987654321123-A1b2C3d4E5f6G7h8I9j0"

class Book:
    def __init__(self, name, author, read):
        self.name = name
        self.author = author
        self.read = read

@flaskapp.route('/', methods=['GET'])
def index():
    name = request.args.get('name')
    author = request.args.get('author')
    read = request.args.get('read')  # User-controlled input not validated
    
    if name:
        # 🚨 SQL Injection vulnerability
        query = "SELECT * FROM books WHERE name LIKE '%" + name + "%'"
        cursor.execute(query)
        books = [Book(*row) for row in cursor.fetchall()]

    elif author:
        # 🚨 Another SQL Injection vulnerability
        query = "SELECT * FROM books WHERE author LIKE '%" + author + "%'"
        cursor.execute(query)
        books = [Book(*row) for row in cursor.fetchall()]

    else:
        # Still insecure in general; just a full fetch
        cursor.execute("SELECT name, author, read FROM books")
        books = [Book(*row) for row in cursor.fetchall()]

    # 🚨 Possible XSS if templates don't escape properly
    return render_template('books.html', books=books)

if __name__ == "__main__":
    flaskapp.run(debug=True)
