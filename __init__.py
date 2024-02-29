from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:CockBalls6!@localhost:3306/user_info'
db = SQLAlchemy(app)

from app import routes, models
socketio = SocketIO(app)  # Move this line to the end
