import logging
from sqlite3 import IntegrityError
from sqlalchemy.exc import IntegrityError
from __init__ import app, db

class FoodReview1234(db.Model):
    __tablename__ = 'food_reviews_1234'
    __table_args__ = {'extend_existing': True}  # Allow redefining the table

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Assuming you have a `User` model
    food = db.Column(db.String(255), nullable=False)
    review = db.Column(db.String(255), nullable=False)
    rating = db.Column(db.String(255), nullable=False)

    def __init__(self, user_id, food, review, rating):
        """
        Initialize the FoodReview1234 object.

        Args:
            user_id (int): The user ID who made the review.
            food (str): Name of the food item.
            review (str): Review text.
            rating (float): Rating (1 to 5).
        """
        self.user_id = user_id
        self.food = food
        self.review = review
        self.rating = rating

    def __repr__(self):
        return f"FoodReview1234(id={self.id}, user_id={self.user_id}, food={self.food}, review={self.review}, rating={self.rating})"

    def create(self):
        """
        Add the food review to the database and commit the transaction.
        """
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logging.warning(f"Error saving review for '{self.food}': {str(e)}")
            raise e

    def read(self):
        """
        Retrieve the food review's data as a dictionary.

        Returns:
            dict: A dictionary containing the food review data.
        """
        return {
            "id": self.id,
            "user_id": self.user_id,
            "food": self.food,
            "review": self.review,
            "rating": self.rating
        }

    def update(self, data):
        """
        Update the food review's data with the provided dictionary.

        Args:
            data (dict): A dictionary containing the fields to update.
        """
        self.food = data.get('food', self.food)
        self.review = data.get('review', self.review)
        self.rating = data.get('rating', self.rating)

        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    def delete(self):
        """
        Remove the food review from the database and commit the transaction.
        """
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def restore(data):
        """
        Restore or update food reviews in the database from the provided data.
        """
        for food_data in data:
            _ = food_data.pop('id', None)  # Remove 'id' from post_data
            food_name = food_data.get("food", None)
            food = FoodReview1234.query.filter_by(food=food_name).first()
            if food:
                food.update(food_data)
            else:
                food = FoodReview1234(**food_data)
                food.create()

def initFoodReviews1234():
    """
    Initialize the FoodReview12345 table with default data.
    """
    reviews = [
        FoodReview1234(user_id=1, food="Pizza", review="Delicious and cheesy!", rating="5"),
        FoodReview1234(user_id=2, food="Burger", review="Juicy and filling.", rating="4"),
        FoodReview1234(user_id=3, food="Sushi", review="Fresh and tasty.", rating="5"),
        FoodReview1234(user_id=4, food="Pasta", review="Creamy and delightful.", rating="4.5"),
        FoodReview1234(user_id=5, food="Salad", review="Healthy but could use more flavor.", rating="3")
    ]

    for review in reviews:
        try:
            review.create()
        except Exception as e:
            db.session.rollback()
            print(f"Error adding review for {review.food}: {e}")
