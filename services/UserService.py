from models import User, CoachingGroups
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
    
    @staticmethod
    def get_life_coaches():
        return User.query.filter_by(role='LifeCoach').all()
    
    @staticmethod
    def link_user_and_coach(user_id, life_coach_id):
        try:
            # Check if the user is already linked to a coach
            existing_link = CoachingGroups.query.filter_by(user_id=user_id).first()
            if existing_link:
                # If a link already exists, update the coach_id
                existing_link.life_coach_id = life_coach_id
            else:
                # If no link exists, create a new entry in the CoachingGroups table
                new_link = CoachingGroups(user_id=user_id, life_coach_id=life_coach_id)
                db.session.add(new_link)

            db.session.commit()
            return True
        except Exception as e:
            print(e)
            db.session.rollback()
            return False