import logging
from sqlite3 import IntegrityError
from sqlalchemy.exc import IntegrityError
from __init__ import app, db


class Budgeting(db.Model):

    __tablename__ = 'budgeting_data'

    id = db.Column(db.Integer, primary_key=True)
    total_budget = db.Column(db.Float, nullable=False) 
    percent_hotels = db.Column(db.Float, nullable=False)
    percent_transport = db.Column(db.Float, nullable=False) 
    overbudget = db.Column(db.Boolean, nullable=False) 

    def __init__(self, total_budget, percent_hotels, percent_transport, overbudget):

        self.total_budget = total_budget
        self.percent_hotels = percent_hotels
        self.percent_transport = percent_transport
        self.overbudget = overbudget

    def __repr__(self):

        return f"Budgeting(id={self.id}, total_budget={self.total_budget}, percent_hotels={self.percent_hotels}, percent_transport={self.percent_transport}, overbudget={self.overbudget})"

    def create(self):

        try:
            db.session.add(self)
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            logging.warning(f"IntegrityError: Could not save budgeting data for total budget {self.total_budget}, percent_hotels {self.percent_hotels}, percent_transport {self.percent_transport}, overbudget {self.overbudget} due to {str(e)}.")
            return None
        return self
        
    def read(self):

        return {
            "id": self.id,
            "total_budget": self.total_budget,
            "percent_hotels": self.percent_hotels,
            "percent_transport": self.percent_transport,
            "overbudget": self.overbudget
        }
    
    def delete(self):

        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
        
    def update(self, data):

        self.total_budget = data.get('total_budget', self.total_budget)
        self.percent_hotels = data.get('percent_hotels', self.percent_hotels)
        self.percent_transport = data.get('percent_transport', self.percent_transport)
        self.overbudget = data.get('overbudget', self.overbudget)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def restore(data):
        for budgeting_data in data:
            _ = budgeting_data.pop('id', None)  # Remove 'id' from budgeting_data
            total_budget = budgeting_data.get("total_budget", None)
            if total_budget:
                budgeting = Budgeting.query.filter_by(total_budget=total_budget).first()
                if budgeting:
                    budgeting.update(budgeting_data)
                else:
                    budgeting = Budgeting(**budgeting_data)
                    budgeting.create()

def initBudgeting():

    with app.app_context():

        db.create_all()

        test_data = [
            Budgeting(total_budget=10000, percent_hotels=40, percent_transport=20, overbudget=False),
            Budgeting(total_budget=5000, percent_hotels=30, percent_transport=25, overbudget=True),
            Budgeting(total_budget=8000, percent_hotels=35, percent_transport=15, overbudget=False),
        ]
        
        for entry in test_data:
            try:
                entry.create()
                print(f"Record created: {repr(entry)}")
            except IntegrityError:
                db.session.remove()
                print(f"Record exists or error: {entry.total_budget}, {entry.percent_hotels}, {entry.percent_transport}, {entry.overbudget}")
