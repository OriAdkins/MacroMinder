from models import Habits
from app import db
import datetime
from services.TimeService import TimeService
from flask import request, session


class HabitService:

    @staticmethod
    def delete_all_user_habits(user_id):
        habits = Habits.query.filter_by(user_id=user_id).all()
        for habit in habits:
            db.session.delete(habit)
        db.session.commit()

    @staticmethod
    def check_for_existing_habits(userid, date):
        previous_date = date - HabitService.current_date.timedelta(days=1)

        prev_habit_list = Habits.query.filter_by(date = previous_date)

        #for i in prev_habit_list:
            #call add_habit()???


    @staticmethod
    def list_habits(user_id, current_date): #change to take in date???
        #current_date = TimeService.get_current_date()
        #print("Type of current_date:", type(current_date))  # Debug print
        habits = Habits.query.filter_by(user_id=user_id, date=current_date).all()
        return habits
    
    @staticmethod
    def get_habit(habit_id):
        habit = Habits.query.filter_by(habit_id = habit_id).first()
        return habit
    
    @staticmethod
    def mark_completed(habit, completed):
        habit.is_completed = completed
        db.session.commit()

    @staticmethod
    def add_habit(user_id, description, current_date):
        existing_habit = Habits.query.filter_by(user_id=user_id, habit_description=description).first()
        if existing_habit:
            return False, 'This habit already exists'
    
        # Create a new Habits object with the current date
        new_habit = Habits(user_id=user_id, habit_description=description, date=current_date)
        db.session.add(new_habit)
        db.session.commit()
        return True, new_habit.habit_id
    
    @staticmethod
    def edit_habit(habit_id, new_description):
        #set date variable to the date of the habit i wanna edit
        #date = request.form.get('date')
        habit = Habits.query.filter_by(habit_id=habit_id).first()
        if habit:
            habit.habit_description = new_description
            db.session.commit()
            return True
        else:
            return False
        
    @staticmethod
    def delete_habit(habit_id, date):
        # Query the habit using both habit_id and date
        habit = Habits.query.filter_by(habit_id=habit_id, date=date).first()
        if habit:
            db.session.delete(habit)
            db.session.commit()
            return True
        else:
            return False

