from models import CompletionLog
from models import User
from flask_login import current_user
from app import db

class CompletionLogService:
    @staticmethod
    def delete_all_user_completion_logs(user_id):
        logs = CompletionLog.query.filter_by(user_id=user_id).all()
        for log in logs:
            db.session.delete(log)
        db.session.commit()

    @staticmethod
    def add_completion_log(user_id, date, protein=0, calories=0, tasks_completed=0, weightlbs=150):
        new_log = CompletionLog(
            user_id=user_id,
            date=date,
            protein=protein,
            calories=calories,
            tasks_completed=tasks_completed,
            weightlbs=weightlbs
        )
        db.session.add(new_log)
        db.session.commit()
        return new_log.tracking_id
    
    @staticmethod
    def edit_completion_log(log_id, protein=None, calories=None, tasks_completed=None, weightlbs=None):
        log = CompletionLog.query.get(log_id)
        if log:
            if protein is not None:
                log.protein = protein
            if calories is not None:
                log.calories = calories
            if tasks_completed is not None:
                log.tasks_completed = tasks_completed
            if weightlbs is not None:
                log.weightlbs = weightlbs
            db.session.commit()
            return True
        else:
            return False

    @staticmethod
    def delete_completion_log(log_id):
        log = CompletionLog.query.get(log_id)
        if log:
            db.session.delete(log)
            db.session.commit()
            return True
        else:
            return False
        
    @staticmethod
    def fetch_macros_for_current_user(user_id):
        macros = CompletionLog.query.filter_by(user_id=user_id).all()
        return macros