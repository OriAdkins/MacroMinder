from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
# ALWAYS REPLACE THIS LINE WITH YOUR LOCAL DATABASE PATH - Ori
# For example: mysql://username:password@localhost/TableName
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://Ori:password@localhost/Users'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
socketio = SocketIO(app)

import routes 