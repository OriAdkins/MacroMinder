from models import User, CoachingGroups
from app import db, bcrypt

class CoachingService:
    @staticmethod
    def get_paired_users(coach_id):
        # Query the database to get the list of users paired with the coach
        paired_users = db.session.query(User).join(CoachingGroups, CoachingGroups.user_id == User.id).filter(CoachingGroups.life_coach_id == coach_id).all()
        return paired_users
    
    @staticmethod
    def delete_link(user_id):
        link = CoachingGroups.query.filter_by(user_id=user_id).first()
        if link:
            db.session.delete(link)
            db.session.commit()
