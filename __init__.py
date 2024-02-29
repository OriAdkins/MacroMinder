from flask import Flask, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:CockBalls6!@localhost:3306/user_info'
# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Define routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return redirect(url_for('login_page'))

@app.route('/login_page')
def login_page():
    return render_template('LoginPage.html')

@app.route('/register')
def register():
    return redirect(url_for('register_page'))

@app.route('/register_page')
def register_page():
    return render_template('RegisterPage.html')


from . import models