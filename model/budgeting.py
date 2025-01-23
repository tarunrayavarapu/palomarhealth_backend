import logging
from sqlite3 import IntegrityError
from sqlalchemy.exc import IntegrityError
from __init__ import app, db


class Budgeting(db.Model):

    __tablename__ = 'budgeting_data'

    id = db.Column(db.Integer, primary_key=True)
    expense = db.Column(db.String, nullable=False)  # Name of the expense (e.g., "Rent", "Groceries")
    cost = db.Column(db.Float, nullable=False)  # The cost for the expense
    category = db.Column(db.String, nullable=False)  # Expense category (e.g., "Housing", "Food")
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Linked to the user who created the budget

    user = db.relationship('User', backref='budgeting_entries')  # Assuming there is a 'User' model

    def __init__(self, expense, cost, category, user_id):
        self.expense = expense
        self.cost = cost
        self.category = category
        self.user_id = user_id

    def __repr__(self):
        return f"Budgeting(id={self.id}, expense={self.expense}, cost={self.cost}, category={self.category}, user_id={self.user_id})"

    def create(self):
        try:
            db.session.add(self)
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            logging.warning(f"IntegrityError: Could not save budgeting data for expense {self.expense}, cost {self.cost}, category {self.category}, user_id {self.user_id} due to {str(e)}.")
            return None
        return self
        
    def read(self):
        return {
            "id": self.id,
            "expense": self.expense,
            "cost": self.cost,
            "category": self.category,
            "user_id": self.user_id
        }
    
    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
        
    def update(self, data):
        self.expense = data.get('expense', self.expense)
        self.cost = data.get('cost', self.cost)
        self.category = data.get('category', self.category)
        self.user_id = data.get('user_id', self.user_id)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def restore(data):
        for budgeting_data in data:
            _ = budgeting_data.pop('id', None)  # Remove 'id' from budgeting_data
            expense = budgeting_data.get("expense", None)
            if expense:
                budgeting = Budgeting.query.filter_by(expense=expense, user_id=budgeting_data["user_id"]).first()
                if budgeting:
                    budgeting.update(budgeting_data)
                else:
                    budgeting = Budgeting(**budgeting_data)
                    budgeting.create()


def initBudgeting():
    with app.app_context():
        db.create_all()

        test_data = [
            Budgeting(expense="Rent", cost=1000, category="Housing", user_id=1),
            Budgeting(expense="Groceries", cost=300, category="Food", user_id=2),
            Budgeting(expense="Transport", cost=150, category="Transport", user_id=1),
        ]
        
        for entry in test_data:
            try:
                entry.create()
                print(f"Record created: {repr(entry)}")
            except IntegrityError:
                db.session.remove()
                print(f"Record exists or error: {entry.expense}, {entry.cost}, {entry.category}, {entry.user_id}")