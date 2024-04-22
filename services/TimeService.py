from models import Habits
from app import db
from datetime import date, datetime
from flask import request, session

class TimeService:

    @staticmethod
    def set_current_date(date):
        session['current_date'] = date

    @staticmethod
    def get_current_date():
        return session.get('current_date', datetime.date.today())

    @staticmethod
    def set_next_date():
        current_date = TimeService.get_current_date()
        next_date = current_date + datetime.timedelta(days=1)
        TimeService.set_current_date(next_date)

    @staticmethod
    def set_previous_date():
        current_date = TimeService.get_current_date()
        previous_date = current_date - datetime.timedelta(days=1)
        TimeService.set_current_date(previous_date)

    #you need to call this when doing session.get[current_time] so that it is a date object
    #only date obj (YYYY-MM-DD) can be passed into the db, it doesnt understand other values
    @staticmethod
    def parse_session_date(session_date_str):
        parsed_date = datetime.strptime(session_date_str, '%a, %d %b %Y %H:%M:%S %Z')
        return parsed_date.date()
