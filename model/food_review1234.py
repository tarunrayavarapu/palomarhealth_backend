from __init__ import db

class FoodReview1234(db.Model):
    """
    FoodReview1234 Model

    This model represents a food review with information about the food name, review text, and rating.
    """
    __tablename__ = 'food1234'
    __table_args__ = {'extend_existing': True}  # Allow redefining the table

    id = db.Column(db.Integer, primary_key=True)
    food = db.Column(db.String(255), nullable=False)
    review = db.Column(db.String(255), nullable=False)
    rating = db.Column(db.String(255), nullable=False)

    def __init__(self, food, review, rating):
        """
        Initialize the FoodReview1 object.

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
            food_name = food_data.get("foods", None)
            food = FoodReview1234.query.filter_by(food=food_name).first()
            if food:
                food.update(food_data)
            else:
                food = FoodReview1234(**food_data)
                food.update(food_data)
                food.create()

def initFoodReviews1234 ():
    """
    Initialize the FoodReview1 table with default data.
    """
    reviews = [
        FoodReview1234("Pizza", "Delicious and cheesy!", "5"),
        FoodReview1234("Burger", "Juicy and filling.", "4"),
        FoodReview1234("Sushi", "Fresh and tasty.", "5"),
        FoodReview1234("Pasta", "Creamy and delightful.", "4.5"),
        FoodReview1234("Salad", "Healthy but could use more flavor.", "3")
    ]

    for review in reviews:
        try:
            review.create()
        except Exception as e:
            db.session.rollback()
            print(f"Error adding review for {review.food}: {e}")
