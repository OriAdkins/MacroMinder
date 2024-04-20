from models import User
from app import db, bcrypt
from services.HabitService import HabitService
from services.CompletionLogService import CompletionLogService

class UserService:
    @staticmethod
    def create_user(username, password, role):
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(username=username, password=hashed_password, role=role)
        db.session.add(new_user)
        db.session.commit()
        return new_user
    
    @staticmethod
    def update_user(user_id, username=None, password=None, role=None):
        user = User.query.get(user_id)
        if not user:
            return None
        
        if username:
            user.username = username
        if password:
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            user.password = hashed_password
        if role:
            user.role = role
        
        db.session.commit()
        return user
    
    @staticmethod
    def delete_user(user_id):
        # Delete all habits associated with the user
        #HabitService.delete_all_user_habits(user_id)
        
        # Delete all completion logs associated with the user
        #CompletionLogService.delete_all_user_completion_logs(user_id)
        
        # Delete the user
        user = User.query.get(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
            return True
        else:
            return False
    
    @staticmethod
    def list_users():
        users = User.query.all()
        return users