from flask import render_template, request, flash
from app import app, db, bcrypt
from models import User

# Render login page
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    existingUser = User.query.filter_by(username=username).first()

    if existingUser and bcrypt.check_password_hash(existingUser.password, password):
        return render_template('HomePage.html')
    else:
        return render_template('LoginPage.html')

# Route to render registration page
@app.route('/gotoregister', methods=['POST'])
def goToRegister():
    return render_template('RegisterPage.html')

# Registration route
@app.route('/register', methods=['POST'])
def register():
    username = request.form.get('username')
    password = request.form.get('password')
    role = request.form.get('role')
    hashedPassword = bcrypt.generate_password_hash(password).decode('utf-8')
    existingUser = User.query.filter_by(username=username).first()

    if existingUser is None:
        newUser = User(username=username, password=hashedPassword, role=role)
        db.session.add(newUser)
        db.session.commit()
        return render_template('LoginPage.html')
    else:
        return render_template('RegisterPage.html')
