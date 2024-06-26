from app import db
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy import ForeignKey, Column, Integer, String, Boolean, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import PrimaryKeyConstraint
from sqlalchemy.orm import relationship

Base = declarative_base

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
    is_completed = db.Column(db.Boolean, default=False, nullable=False)
    date = db.Column(db.Date, nullable = False)
    user = relationship("User", backref="habits")
    __table_args__ = (
        PrimaryKeyConstraint('habit_id', 'date'),
        {},
    )


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
    user = relationship("User", backref="completionlogs")

# Db table for keeping life coaches linked with their standard users
class CoachingGroups(db.Model):
    __tablename__ = 'CoachingGroups'
    life_coach_id = db.Column(db.Integer, db.ForeignKey('User.id'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), primary_key=True)
    life_coach = relationship("User", foreign_keys=[life_coach_id])
    user = relationship("User", foreign_keys=[user_id])
