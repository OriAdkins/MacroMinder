from models import CompletionLog
from app import db

class CompletionLogService:
    @staticmethod
    def delete_all_user_completion_logs(user_id):
        logs = CompletionLog.query.filter_by(user_id=user_id).all()
        for log in logs:
            db.session.delete(log)
        db.session.commit()