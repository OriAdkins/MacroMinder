from models import CompletionLog
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