from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3, logging
logging.basicConfig(level=logging.DEBUG)

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'Jesus7god'  # Secret key for session handling

# Dummy user data for login
USER_CREDENTIALS = {
    'username': 'admin',
    'password': 'password123'
}

# Connect to SQLite
def get_db_connection():
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row
    return conn

#Route for registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect('users.db')
        try:
            conn.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
            conn.commit()
        except sqlite3.IntegrityError:
            return "Username already exists. Please choose a different one."
        finally:
            conn.close()
        return redirect('/login')
    return render_template('register.html')
# Route: Home page
@app.route('/')
def home():
    if 'user' in session:
        return redirect(url_for('welcome'))
    return redirect(url_for('login'))

# Route: Login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        logging.debug(f"Attempting login for username: {username}")
        conn = sqlite3.connect('users.db')
        cursor = conn.execute('SELECT * FROM users WHERE username=? AND password=?', (username, password))
        user = cursor.fetchone()
        logging.debug(f"User found: {user}")
        conn.close()
        if user:
            session['username'] = username
            return redirect('/users')
        else:
            return "Invalid username or password. Please try again."
    return render_template('login.html')

# Route: Welcome page after login
@app.route('/welcome')
def welcome():
    if 'user' in session:
        return render_template('welcome.html', username=session['user'])
    return redirect(url_for('login'))

# Route: Logout
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

# Run the application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

# Route to view usernames (logged-in users only)
@app.route('/users', methods=['GET'])
@app.route('/users')
def users():
    logging.debug(f"Session data: {session}")
    if 'username' not in session:
        return redirect('/login')
    conn = sqlite3.connect('users.db')
    cursor = conn.execute('SELECT username FROM users')
    users = [{'username': row[0]} for row in cursor.fetchall()]
    conn.close()
    return render_template('users.html', users=users)

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'username' not in session:
        return redirect('/login')
    conn = sqlite3.connect('users.db')
    username = session['username']

    if request.method == 'POST':
        email = request.form['email']
        bio = request.form['bio']
        conn.execute('UPDATE users SET email = ?, bio = ? WHERE username = ?', (email, bio, username))
        conn.commit()

    cursor = conn.execute('SELECT email, bio FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    conn.close()
    if user:
        return render_template('profile.html', user={'email': user[0], 'bio': user[1]})
    return redirect('/login')
