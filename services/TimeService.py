from models import Habits
from app import db
from datetime import date, datetime, timedelta
from flask import request, session

class TimeService:

    @staticmethod
    def set_current_date(date):
        # Convert date to string before storing in session
        session['current_date'] = date.isoformat()

    @staticmethod
    def get_current_date():
        session_date_str = session.get('current_date')
        try:
            # Try parsing the date string in the expected format
            return datetime.strptime(session_date_str, '%a, %d %b %Y %H:%M:%S %Z').date()
        except ValueError:
            # If parsing fails, assume the date string is in ISO format
            return datetime.strptime(session_date_str, '%Y-%m-%d').date()
    
    @staticmethod
    def set_next_date():
        current_date = TimeService.get_current_date()
        next_date = current_date + timedelta(days=1)
        TimeService.set_current_date(next_date)

    @staticmethod
    def set_previous_date():
        current_date = TimeService.get_current_date()
        previous_date = current_date - timedelta(days=1)
        TimeService.set_current_date(previous_date)

    @staticmethod
    def parse_session_date(session_date_str):
        try:
            # Try parsing the date string in the expected format
            parsed_date = datetime.strptime(session_date_str, '%a, %d %b %Y %H:%M:%S %Z')
        except ValueError:
            # If parsing fails, try parsing in ISO format
            parsed_date = datetime.strptime(session_date_str, '%Y-%m-%d')
        return parsed_date.date()