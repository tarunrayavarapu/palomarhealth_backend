from __init__ import db

class FoodReview123(db.Model):
    """
    FoodReview123 Model

    This model represents a food review with information about the food name, review text, and rating.
    """
    __tablename__ = 'food_reviews1234'
    __table_args__ = {'extend_existing': True}  # Allow redefining the table


    id = db.Column(db.Integer, primary_key=True)
    food= db.Column(db.String(255), nullable=False)
    review= db.Column(db.String(255), nullable=False)
    rating= db.Column(db.String(255), nullable=False)

    def __init__(self, food, review, rating):
        """
        Initialize the FoodReview123 object.

        Args:
            food (str): Name of the food item.
            review (str): Review text.
            rating (float): Rating (1 to 5).
        """
        self.food = food
        self.review = review
        self.rating = rating

    def create(self):
        """
        Add the food review to the database and commit the transaction.
        """
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    def read(self):
        """
        Retrieve the food review's data as a dictionary.

        Returns:
            dict: A dictionary containing the food review data.
        """
        return {
            "id": self.id,
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
        try:
            self.food = data.get('food', self.food)
            self.review = data.get('review', self.review)
            self.rating = data.get('rating', self.rating)
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
        Restore food reviews from a list of dictionaries.

        Args:
            data (list): A list of dictionaries containing food review data.

        Returns:
            dict: A dictionary of restored food reviews keyed by food name.
        """
        restored_reviews = {}
        for review_data in data:
            food = review_data.get("food", None)
            food_review = FoodReview123.query.filter_by(food=food).first()
            if food_review:
                food_review.update(review_data)
            else:
                food_review = FoodReview123(**review_data)
                food_review.create()
        return restored_reviews

def initFoodReviews():
    """
    Initialize the FoodReview123 table with default data.
    """
    reviews = [
        FoodReview123("Pizza", "Delicious and cheesy!", "5"),
        FoodReview123("Burger", "Juicy and filling.", "4"),
        FoodReview123("Sushi", "Fresh and tasty.", "5"),
        FoodReview123("Pasta", "Creamy and delightful.", "4.5"),
        FoodReview123("Salad", "Healthy but could use more flavor.", "3")
    ]

    for review in reviews:
        try:
            review.create()
        except Exception as e:
            db.session.rollback()
            print(f"Error adding review for {review.food}: {e}")