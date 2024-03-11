from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

# MySQL configurations
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'login'

mysql = MySQL(app)

# Create users table if it doesn't exist
with app.app_context():
    cur = mysql.connection.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(100) NOT NULL,
            pass VARCHAR(100) NOT NULL
        )
    ''')
    mysql.connection.commit()
    cur.close()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE username = %s AND pass = %s", (username, password))
    user = cur.fetchone()
    cur.close()

    if user:
        # Successful login
        return redirect(url_for('login_success', username=username))
    else:
        # Failed login
        return redirect(url_for('wrong_password'))

@app.route('/login_success/<username>')
def login_success(username):
    return render_template('login_success.html', username=username)

@app.route('/wrong_password')
def wrong_password():
    return render_template('wrong_password.html')

if __name__ == '__main__':
    app.run(debug=True)
