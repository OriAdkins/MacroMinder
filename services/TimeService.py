from models import Habits
from app import db
import datetime
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