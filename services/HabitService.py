from models import Habits
from app import db

class HabitService:
    @staticmethod
    def delete_all_user_habits(user_id):
        habits = Habits.query.filter_by(user_id=user_id).all()
        for habit in habits:
            db.session.delete(habit)
        db.session.commit()
        
    @staticmethod
    def delete_user_habit(habit_id):
        habit = Habits.query.get(habit_id)
        if habit:
            db.session.delete(habit)
            db.session.commit()
            return True
        else:
            return False

    @staticmethod
    def list_habits(user_id):
        habits = Habits.query.filter_by(user_id=user_id).all()
        return habits
    
    @staticmethod
    def get_habit(habit_id):
        habit = Habits.query.get(habit_id)
        return habit
    
    @staticmethod
    def mark_completed(habit, completed):
        habit.is_completed = completed
        db.session.commit()

    @staticmethod
    def add_habit(user_id, description):
        existing_habit = Habits.query.filter_by(user_id=user_id, habit_description=description).first()
        if existing_habit:
            return False, 'This habit already exists'
        
        new_habit = Habits(user_id=user_id, habit_description=description)
        db.session.add(new_habit)
        db.session.commit()
        return True, new_habit.habit_id
    
    @staticmethod
    def edit_habit(habit_id, new_description):
        habit = Habits.query.get(habit_id)
        if habit:
            habit.habit_description = new_description
            db.session.commit()
            return True
        else:
            return False
        
    @staticmethod
    def delete_habit(habit_id):
        habit = Habits.query.get(habit_id)
        if habit:
            db.session.delete(habit)
            db.session.commit()
            return True
        else:
            return False
