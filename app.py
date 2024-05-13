# app.py

from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import requests

app = Flask(__name__)
app.secret_key = 'your_secret_key'

conn = sqlite3.connect('book_catalogue.db', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS users (
             id INTEGER PRIMARY KEY,
             username TEXT NOT NULL,
             password TEXT NOT NULL
             )''')
c.execute('''CREATE TABLE IF NOT EXISTS books (
             id INTEGER PRIMARY KEY,
             title TEXT NOT NULL,
             author TEXT NOT NULL,
             page_count INTEGER,
             average_rating REAL,
             thumbnail_url TEXT,
             user_id INTEGER,
             FOREIGN KEY (user_id) REFERENCES users(id)
             )''')
conn.commit()


@app.route('/')
def login():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login_user():
    username = request.form.get('username')
    password = request.form.get('password')

    c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = c.fetchone()
    if user:
        session['user_id'] = user[0]
        session['username'] = user[1]
        return redirect(url_for('dashboard'))
    else:
        return render_template('login.html', error='Invalid username or password')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        c.execute("SELECT * FROM users WHERE username = ?", (username,))
        existing_user = c.fetchone()
        if existing_user:
            return render_template('register.html', error='Username already exists')

        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()

        return redirect(url_for('login', message='Registration successful!'))

    return render_template('register.html')


@app.route('/dashboard')
def dashboard():
    user_id = session.get('user_id')
    username = session.get('username')

    if user_id:
        page = request.args.get('page', 1, type=int)
        per_page = 10
        offset = (page - 1) * per_page

        c.execute("SELECT * FROM books WHERE user_id = ? LIMIT ? OFFSET ?", (user_id, per_page, offset))
        books = c.fetchall()

        return render_template('dashboard.html', books=books, username=username)
    else:
        return redirect(url_for('login'))


@app.route('/search', methods=['POST'])
def search():
    search_type = request.form.get('search_type')
    search_query = request.form.get('search_query')

    if search_type == 'isbn':
        response = requests.get(f'https://www.googleapis.com/books/v1/volumes?q=isbn:{search_query}')
    elif search_type == 'title':
        response = requests.get(f'https://www.googleapis.com/books/v1/volumes?q=intitle:{search_query}')

    data = response.json()

    if 'items' in data:
        return render_template('search_results.html', books=data['items'])
    else:
        return render_template('dashboard.html', error='No results found for the given query')


@app.route('/save_book', methods=['POST'])
def save_book():
    user_id = session.get('user_id')
    if user_id:
        title = request.form.get('title')
        author = request.form.get('author')
        page_count = request.form.get('page_count')
        average_rating = request.form.get('average_rating')
        thumbnail_url = request.form.get('thumbnail_url')

        c.execute(
            "INSERT INTO books (title, author, page_count, average_rating, thumbnail_url, user_id) VALUES (?, ?, ?, ?, ?, ?)",
            (title, author, page_count, average_rating, thumbnail_url, user_id))
        conn.commit()

        return redirect(url_for('dashboard'))
    else:
        return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    return redirect(url_for('login'))


@app.route('/delete_book/<int:book_id>', methods=['POST'])
def delete_book(book_id):
    user_id = session.get('user_id')

    c.execute("DELETE FROM books WHERE id = ? AND user_id = ?", (book_id, user_id))
    conn.commit()

    return redirect(url_for('dashboard'))


if __name__ == '__main__':
    app.run(debug=True)
