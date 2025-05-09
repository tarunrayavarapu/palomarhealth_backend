# post.py
import logging
from sqlite3 import IntegrityError
from sqlalchemy.exc import IntegrityError
from __init__ import app, db


class Hotel(db.Model):

    __tablename__ = 'hotels'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    hotel = db.Column(db.String(3), nullable=False)
    city = db.Column(db.String(3), nullable=False)
    country = db.Column(db.String(3), nullable=False)
    rating = db.Column(db.String(3), nullable=False)
    note = db.Column(db.String(3), nullable=False)

    def __init__(self, user_id, hotel, city, country, rating, note):

        self.user_id = user_id
        self.hotel = hotel
        self.city = city
        self.country = country
        self.rating = rating
        self.note = note

    def __repr__(self):

        return f"Hotel(id={self.id}, user_id={self.user_id}, hotel={self.hotel}, city={self.city}, country={self.country}, rating={self.rating}, note={self.note})"

    def create(self):

        try:
            db.session.add(self)
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            logging.warning(f"IntegrityError: Could not save '{self.user_id}', '{self.hotel}', '{self.city}', '{self.country}', '{self.rating}', and '{self.note} due to {str(e)}.")
            return None
        return self
        
    def read(self):

        return {
            "id": self.id,
            "user_id": self.user_id,
            "hotel": self.hotel,
            "city": self.city,
            "country": self.country,
            "rating": self.rating,
            "note": self.note
        }
    
    def delete(self):

        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
        
    def update(self, data):

        self.user_id = data.get('user_id', self.user_id)
        self.hotel = data.get('hotel', self.hotel)
        self.city = data.get('city', self.city)
        self.country = data.get('country', self.country)
        self.rating = data.get('rating', self.rating)
        self.note = data.get('note', self.note)
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
            Hotel(user_id=1, hotel='Hilton', city='Paris', country='France', rating=5, note="Beautiful hotel! Amazing pool and view!"),
            Hotel(user_id=2, hotel='Holiday Inn', city='San Diego', country='USA', rating=2, note="Not the best hotel, but it was cheap."),
            Hotel(user_id=3, hotel='Motel 12345', city='Los Angeles', country='USA', rating=1, note="Terrible hotel. Do not stay here!"),
        ]
        
        for entry in test_data:
            try:
                entry.create()
                print(f"Record created: {repr(entry)}")
            except IntegrityError:
                db.session.remove()
                print(f"Record exists or error: {entry.hotel}, {entry.city}, {entry.country} and {entry.rating}")