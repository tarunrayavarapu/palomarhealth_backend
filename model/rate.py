from __init__ import db, app
from sqlalchemy.exc import IntegrityError
from model.post import Post
from model.user import User

class Rate(db.Model):
    """
    Rate Model

    The Rate class represents a rating on a post by a user.

    Attribut    es:
        id (db.Column): The primary key, an integer representing the unique identifier for the rating.
        value (db.Column): An integer representing the rating value (1-10).
        user_id (db.Column): An integer representing the ID of the user who gave the rating.
        post_id (db.Column): An integer representing the ID of the post that received the rating.
    """
    __tablename__ = 'rates'

    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Integer, nullable=False)  # Rating value (1-10)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)

    def __init__(self, value, user_id, post_id):
        self.value = value
        self.user_id = user_id
        self.post_id = post_id

    def create(self):
        """
        Add the rating to the database and commit the transaction.
        """
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    def read(self):
        """
        Retrieve the rating data as a dictionary.

        Returns:
        Dictionary with rating information.
        """
        return {
            "id": self.id,
            "value": self.value,
            "user_id": self.user_id,
            "post_id": self.post_id
        }

    def delete(self):
        """
        Remove the rating from the database and commit the transaction.
        """
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e


    def update(self, data):

        self.value = data.get('value', self.value)
        self.user_id = data.get('user_id', self.user_id)
        self.post_id = data.get('post_id', self.post_id)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
        
    @staticmethod
    def restore(data):
        for rate_data in data:
            _ = rate_data.pop('id', None)  # Remove 'id' from post_data
            title = rate_data.get("value", None)
            post = Rate.query.filter_by(value=title).first()
            if post:
                post.update(rate_data)
            else:
                post = Rate(**rate_data)
                post.update(rate_data)
                post.create()

def initRates():
    """
    Initialize the Rate table with any required starter data.
    """
    with app.app_context():
        # Create database tables if they don't exist
        db.create_all()

        # Optionally, add some test data (replace with actual values as needed)
        
        rates = [
            Rate(value=5, user_id=5, post_id=1),
            Rate(value=8, user_id=6, post_id=1),
            Rate(value=1, user_id=7, post_id=1),
            Rate(value=7, user_id=8, post_id=1),
            Rate(value=1, user_id=9, post_id=1),

            Rate(value=8, user_id=10, post_id=2),
            Rate(value=6, user_id=11, post_id=2),
            Rate(value=3, user_id=12, post_id=2),
            Rate(value=8, user_id=13, post_id=2),
            Rate(value=10, user_id=14, post_id=2),

            Rate(value=8, user_id=15, post_id=3),
            Rate(value=7, user_id=16, post_id=3),
            Rate(value=6, user_id=17, post_id=3),
            Rate(value=5, user_id=18, post_id=3),
            Rate(value=5, user_id=19, post_id=3),

            Rate(value=8, user_id=20, post_id=4),
            Rate(value=4, user_id=21, post_id=4),
            Rate(value=3, user_id=22, post_id=4),
            Rate(value=8, user_id=23, post_id=4),
            Rate(value=2, user_id=24, post_id=4),

            Rate(value=2, user_id=25, post_id=5),
            Rate(value=2, user_id=26, post_id=5),
            Rate(value=1, user_id=27, post_id=5),
            Rate(value=5, user_id=28, post_id=5),
            Rate(value=7, user_id=29, post_id=5)
        ]

        for rate in rates:
            try:
                db.session.add(rate)
                db.session.commit()
                print(f"Record created: {repr(rate)}")
            except IntegrityError:
                db.session.rollback()
                print(f"Duplicate or error: {repr(rate)}")