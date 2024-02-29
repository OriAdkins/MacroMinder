from flask import Flask, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime #use this to see when something was added to the db
from flask_bcrypt import Bcrypt #used to hash passwords so they are stored securely

#instance of the app
app = Flask(__name__)
#format: 'mysql://username:password@localhost/databasename'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:monkeyinhospital@localhost/users'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
#creating a table User that has a username, password, and role
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    role = db.Column(db.String(80), nullable=False)

#render the login page to start
@app.route('/')
def index():
    return render_template('LoginPage.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    #if there is a user in User table with the username, existingUser is that. Otherwise, it is None
    existingUser = User.query.filter_by(username=username).first()
    #if the user does exist and the hashed passwords match, go to their HomePage. Otherwise, stay on LoginPage
    if existingUser and bcrypt.check_password_hash(existingUser.password, password):
        return render_template('HomePage.html')
    else:
        return render_template('LoginPage.html')

@app.route('/gotoregister', methods=['POST'])
def goToRegister():
    return render_template('RegisterPage.html')

@app.route('/register', methods=['POST'])
def register():
    username = request.form.get('username')
    password = request.form.get('password')
    role = request.form.get('role')
    hashedPassword = bcrypt.generate_password_hash(password).decode('utf-8') #created hashed pw, convert to string to store in db

    #if there is a user in User table with the username, existingUser is that. Otherwise, it is None
    existingUser = User.query.filter_by(username=username).first()

    #username doesn't exist, add the new user
    if existingUser is None:
        #display success message
        #flash('Registration successful!')
        newUser = User(username=username, password=hashedPassword, role=role)
        db.session.add(newUser)
        db.session.commit()
        return render_template('LoginPage.html')
        #later, check if the password is valid (make up your own rules)
    else:
        #username already exists, display error message
        #flash('Username already exists. Please choose a different username.', 'error')
        return render_template('RegisterPage.html')

if __name__ == "__main__":
    with app.app_context():
        db.create_all() #creates the tables in the database that do not already exist
    app.run(debug=True)