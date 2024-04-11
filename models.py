from app import db
from sqlalchemy import ForeignKey

class User(db.Model):
    # Replace 'User' with the name of your database table containing these exact things - Ori
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    role = db.Column(db.String(80), nullable=False)

#table linked to user to define their habits
class Habits(db.Model):
    __tablename__ = 'Habits'
    habit_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)
    habit_description = db.Column(db.String(255), nullable=False)
    #user = db.relationship('User', backref='habits')


# Db table for tracking the macro for the day, tasks_completed is for habits
class CompletionLog(db.Model):
    __tablename__ = 'CompletionLog'
    tracking_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    protein = db.Column(db.Integer, default=0)
    calories = db.Column(db.Integer, default=0)
    tasks_completed = db.Column(db.Integer, default=0)
    weightlbs = db.Column(db.DECIMAL(4, 2), default=150)