import sqlite3
import datetime as dt
from backend.exercise_manager import ExerciseManager
from backend.weight_manager import WeightManager
from backend.step_manager import StepManager
from backend.calorie_manager import CalorieManager


class Database():
    def __init__(self):
        # today, last day/week/month/year current and previous
        self.today, self.dates, self.previous_dates = self.set_dates()

        self.get_data()

        self.exercise = ExerciseManager('exercise', self.exercise, self.today.strftime('%Y%m%d'), self.dates)
        self.weight = WeightManager('weight', self.weight, self.today.strftime('%Y%m%d'), self.dates)
        self.step = StepManager('steps', self.step, self.today.strftime('%Y%m%d'), self.dates, self.previous_dates)
        self.calorie = CalorieManager('calories', self.calorie, self.today.strftime('%Y%m%d'), self.dates, self.previous_dates)

    def get_data(self):
        conn = sqlite3.connect('user.db')

        self.exercise = self.load_exercise(conn)   
        self.weight = self.load_weight(conn)   
        self.step = self.load_step(conn)   
        self.calorie = self.load_calorie(conn)    

        conn.close()
    
    def load_exercise(self, conn):
        c = conn.cursor()

        table_create_query = """CREATE TABLE IF NOT EXISTS exercise (
                                date text,
                                name text,
                                weight1 int,
                                reps1 int,
                                weight2 int,
                                reps2 int,
                                weight3 int,
                                reps3 int
                                )"""
        
        c.execute(table_create_query)

        table_return_query = "SELECT * FROM exercise"
        c.execute(table_return_query)

        exercise = c.fetchall()

        return exercise

    def load_weight(self, conn):
        c = conn.cursor()

        table_create_query = """CREATE TABLE IF NOT EXISTS weight (
                                date text, 
                                weight float, 
                                goal float
                                )"""
        
        c.execute(table_create_query)

        table_return_query = "SELECT * FROM weight"
        c.execute(table_return_query)

        items = c.fetchall()

        return items

    def load_step(self, conn):
        c = conn.cursor()

        table_create_query = """CREATE TABLE IF NOT EXISTS steps (
                                date text, 
                                steps int, 
                                goal int
                                )"""
        
        c.execute(table_create_query)

        table_return_query = "SELECT * FROM steps"
        c.execute(table_return_query)

        items = c.fetchall()

        return items

    def load_calorie(self, conn):
        c = conn.cursor()

        table_create_query = """CREATE TABLE IF NOT EXISTS calories (
                                date text, 
                                calories int, 
                                goal int
                                )"""
        
        c.execute(table_create_query)

        table_return_query = "SELECT * FROM calories"
        c.execute(table_return_query)

        items = c.fetchall()

        return items

    def get_exercise(self):
        return self.exercise
    
    def get_weight(self):
        return self.weight
    
    def get_step(self):
        return self.step
    
    def get_calorie(self):
        return self.calorie

    def set_dates(self):
        today = dt.date.today()
        dates = []
        previous_dates = []

        day = today - dt.timedelta(days=1)
        week = today - dt.timedelta(days=today.weekday()+1)
        month = today - dt.timedelta(days=today.day)
        year = dt.date(today.year - 1, 12, 31)

        previous_day = day - dt.timedelta(days=1)
        previous_week = week - dt.timedelta(days=7)
        previous_month = month - dt.timedelta(days=month.day)
        previous_year = dt.date(year.year - 1, 12, 31)

        dates.append(day.strftime('%Y%m%d'))
        dates.append(week.strftime('%Y%m%d'))
        dates.append(month.strftime('%Y%m%d'))
        dates.append(year.strftime('%Y%m%d'))

        previous_dates.append(previous_day.strftime('%Y%m%d'))
        previous_dates.append(previous_week.strftime('%Y%m%d'))
        previous_dates.append(previous_month.strftime('%Y%m%d'))
        previous_dates.append(previous_year.strftime('%Y%m%d'))

        return today, dates, previous_dates   
    
    def save_all(self):
        pass