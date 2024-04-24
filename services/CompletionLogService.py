from models import CompletionLog
from models import User
from app import db

class CompletionLogService:
    
    @staticmethod
    def delete_all_user_completion_logs(user_id):
        logs = CompletionLog.query.filter_by(user_id=user_id).all()
        for log in logs:
            db.session.delete(log)
        db.session.commit()

    # Instead of having an edit button, we 'limit' the user to one log per day by checking against 
    # the date stored in the db 
    @staticmethod
    def add_completion_log(user_id, date, protein=0, calories=0, tasks_completed=0, weightlbs=150):
        # Check if there is already a log for the given user and date
        existing_log = CompletionLog.query.filter_by(user_id=user_id, date=date).first()

        if existing_log:
            # Update the existing log
            existing_log.protein = protein
            existing_log.calories = calories
            existing_log.tasks_completed = tasks_completed
            existing_log.weightlbs = weightlbs
        else:
            # Create a new log
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
        return existing_log.tracking_id if existing_log else new_log.tracking_id

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
    
    @staticmethod
    def fetch_weight_data(user_id):
        # Fetch weight and date data from CompletionLog table for the given user_id
        logs = CompletionLog.query.filter_by(user_id=user_id).all()

        # Extract dates and weights from the logs
        dates = [log.date for log in logs]
        weights = [log.weightlbs for log in logs]

        return dates, weights