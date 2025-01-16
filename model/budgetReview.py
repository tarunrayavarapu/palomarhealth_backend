import logging
from sqlite3 import IntegrityError
from sqlalchemy import Text, Integer, String, DateTime
from sqlalchemy.exc import IntegrityError
from __init__ import app, db
from model.user import User
from model.channel import Channel
from datetime import datetime

class BudgetReview(db.Model):
    """
    BudgetReview Model
    
    The BudgetReview class represents an individual review of a budget by a user within a specific channel.
    
    Attributes:
        id (db.Column): The primary key, an integer representing the unique identifier for the review.
        _title (db.Column): A string representing the title of the review.
        _comment (db.Column): A string representing the comment of the review.
        _rating (db.Column): An integer representing the rating given to the review.
        _hashtag (db.Column): A string representing associated hashtags with the review.
        _date (db.Column): A datetime representing when the review was created.
        _user_id (db.Column): An integer representing the user who created the review.
        _channel_id (db.Column): An integer representing the channel to which the review belongs.
    """
    __tablename__ = 'budget_reviews'

    id = db.Column(db.Integer, primary_key=True)
    _title = db.Column(db.String(255), nullable=False)
    _comment = db.Column(db.String(255), nullable=False)
    _rating = db.Column(db.Integer, nullable=False)
    _hashtag = db.Column(db.String(255), nullable=True)
    _date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    _user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    _channel_id = db.Column(db.Integer, db.ForeignKey('channels.id'), nullable=False)

    def __init__(self, title, comment, rating, hashtag=None, date=None, user_id=None, channel_id=None):
        """
        Constructor for BudgetReview object creation.
        
        Args:
            title (str): The title of the review.
            comment (str): The comment describing the review.
            rating (int): The rating given to the budget review.
            hashtag (str): Optional field for hashtags.
            date (datetime): The date of the review (defaults to current time).
            user_id (int): The ID of the user who created the review.
            channel_id (int): The ID of the channel to which the review belongs.
        """
        self._title = title
        self._comment = comment
        self._rating = rating
        self._hashtag = hashtag
        self._date = date or datetime.utcnow()  # default to current time if not provided
        self._user_id = user_id
        self._channel_id = channel_id

    def __repr__(self):
        """
        The __repr__ method returns a string representation of the BudgetReview instance.
        
        Returns:
            str: A string representation of the BudgetReview object.
        """
        return f"BudgetReview(id={self.id}, title={self._title}, comment={self._comment}, rating={self._rating}, hashtag={self._hashtag}, date={self._date}, user_id={self._user_id}, channel_id={self._channel_id})"

    def create(self):
        """
        Creates a new budget review in the database.
        
        Returns:
            BudgetReview: The created review object, or None on error.
        """
        try:
            db.session.add(self)
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            logging.warning(f"IntegrityError: Could not create review with title '{self._title}' due to {str(e)}.")
            return None
        return self
        
    def read(self):
        """
        Retrieves the budget review data and returns it as a dictionary.
        
        Returns:
            dict: A dictionary containing the review data, including user and channel names.
        """
        user = User.query.get(self._user_id)
        channel = Channel.query.get(self._channel_id)
        data = {
            "id": self.id,
            "title": self._title,
            "comment": self._comment,
            "rating": self._rating,
            "hashtag": self._hashtag,
            "date": self._date,
            "user_name": user.name if user else None,
            "channel_name": channel.name if channel else None
        }
        return data

    def update(self):
        """
        Updates the budget review object with new data.
        
        Args:
            inputs (dict): A dictionary containing the new data for the review.
        
        Returns:
            BudgetReview: The updated review object, or None on error.
        """
        inputs = BudgetReview.query.get(self.id)
        
        title = inputs._title
        comment = inputs._comment
        rating = inputs._rating
        hashtag = inputs._hashtag
        date = inputs._date
        channel_id = inputs._channel_id
        user_id = inputs._user_id

        # Update fields if new data is provided
        if title:
            self._title = title
        if comment:
            self._comment = comment
        if rating:
            self._rating = rating
        if hashtag:
            self._hashtag = hashtag
        if date:
            self._date = date
        if channel_id:
            self._channel_id = channel_id
        if user_id:
            self._user_id = user_id

        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            logging.warning(f"IntegrityError: Could not update review with title '{title}'.")
            return None
        return self
    
    def delete(self):
        """
        Deletes the budget review from the database.
        
        Raises:
            Exception: An error occurred when deleting the review.
        """    
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

def initBudgetReviews():
    """
    Initializes the BudgetReview table and adds test data to the table.
    """
    with app.app_context():
        db.create_all()
        budget_reviews = [
            BudgetReview(title='Marketing Budget Review', comment='Reviewing the Q1 marketing budget allocation.', rating=4, hashtag='marketing', user_id=1, channel_id=1),
            BudgetReview(title='Sales Budget Review', comment='Reviewing the Q1 sales budget allocation.', rating=5, hashtag='sales', user_id=2, channel_id=1),
            BudgetReview(title='Tech Budget Review', comment='Reviewing the Q1 tech budget allocation.', rating=3, hashtag='tech', user_id=1, channel_id=2),
        ]
        
        for review in budget_reviews:
            try:
                review.create()
                print(f"Record created: {repr(review)}")
            except IntegrityError:
                db.session.remove()
                print(f"Records exist, duplicate data, or error: {review._title}")
