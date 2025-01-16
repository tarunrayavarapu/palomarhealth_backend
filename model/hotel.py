# post.py
import logging
from sqlite3 import IntegrityError
from sqlalchemy.exc import IntegrityError
from __init__ import app, db


class Hotel(db.Model):

    __tablename__ = 'hotel_data'

    id = db.Column(db.Integer, primary_key=True)
    hotel = db.Column(db.String(3), nullable=False)
    location = db.Column(db.String(3), nullable=False)
    rating = db.Column(db.String(3), nullable=False)

    def __init__(self, hotel, location, rating):

        self.hotel = hotel
        self.location = location
        self.rating = rating

    def __repr__(self):

        return f"Hotel(id={self.id}, hotel={self.hotel}, location={self.location}, rating={self.rating})"

    def create(self):

        try:
            db.session.add(self)
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            logging.warning(f"IntegrityError: Could not save '{self.hotel}', '{self.location}', and '{self.rating}' due to {str(e)}.")
            return None
        return self
        
    def read(self):

        return {
            "id": self.id,
            "hotel": self.hotel,
            "location": self.location,
            "rating": self.rating
        }
    
    def delete(self):

        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
        
    def update(self, data):

        self.hotel = data.get('hotel', self.hotel)
        self.location = data.get('location', self.location)
        self.rating = data.get('rating', self.rating)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def restore(data):
        for hotel_data in data:
            _ = hotel_data.pop('id', None)  # Remove 'id' from post_data
            hotel_name = hotel_data.get("hotel", None)
            hotel = Hotel.query.filter_by(hotel=hotel_name).first()
            if hotel:
                hotel.update(hotel_data)
            else:
                hotel = Hotel(**hotel_data)
                hotel.update(hotel_data)
                hotel.create()

def initHotel():

    with app.app_context():

        db.create_all()

        test_data = [
            Hotel(hotel='Hilton', location='Paris', rating=5),
            Hotel(hotel='Holiday Inn', location='San Diego', rating=4),
            Hotel(hotel='Motel 12345', location='Los Angeles', rating=3),
        ]
        
        for entry in test_data:
            try:
                entry.create()
                print(f"Record created: {repr(entry)}")
            except IntegrityError:
                db.session.remove()
                print(f"Record exists or error: {entry.hotel}, {entry.location} and {entry.rating}")