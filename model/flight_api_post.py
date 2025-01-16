# post.py
import logging
from sqlite3 import IntegrityError
from sqlalchemy.exc import IntegrityError
from __init__ import app, db


class Flight(db.Model):
    """
    Flight Model
    
    Represents a flight record with departure and arrival airport IATA codes.
    
    Attributes:
        id (db.Column): The primary key, an integer representing the unique identifier for the flight.
        departure_iata (db.Column): The IATA code for the departure airport.
        arrival_iata (db.Column): The IATA code for the arrival airport.
    """
    __tablename__ = 'flights'

    id = db.Column(db.Integer, primary_key=True)
    departure_iata = db.Column(db.String(3), nullable=False)
    arrival_iata = db.Column(db.String(3), nullable=False)

    def __init__(self, departure_iata, arrival_iata):
        """
        Constructor, initializes a flight record.
        
        Args:
            departure_iata (str): The IATA code for the departure airport.
            arrival_iata (str): The IATA code for the arrival airport.
        """
        self.departure_iata = departure_iata
        self.arrival_iata = arrival_iata

    def __repr__(self):
        """
        Represents the flight record in string format.
        
        Returns:
            str: A string representation of the flight record.
        """
        return f"Flight(id={self.id}, departure_iata={self.departure_iata}, arrival_iata={self.arrival_iata})"

    def create(self):
        """
        Creates a new flight record in the database.
        
        Returns:
            Flight: The created flight object, or None on error.
        """
        try:
            db.session.add(self)
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            logging.warning(f"IntegrityError: Could not create flight with departure '{self.departure_iata}' and arrival '{self.arrival_iata}' due to {str(e)}.")
            return None
        return self
        
    def read(self):
        """
        Retrieves the flight record as a dictionary.
        
        Returns:
            dict: A dictionary containing the flight data.
        """
        return {
            "id": self.id,
            "departure_iata": self.departure_iata,
            "arrival_iata": self.arrival_iata,
        }
        
    def update(self, data):
        self.departure_iata = data.get('dep_iata', self.departure_iata)
        self.arrival_iata = data.get('arr_iata', self.arrival_iata)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
    
    def delete(self):
        """
        Deletes the flight record from the database.
        
        Raises:
            Exception: An error occurred when deleting the flight record.
        """
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e


def initFlights():
    """
    Initializes the Flight table and adds some test data.
    """
    with app.app_context():
        # Create database and tables
        db.create_all()

        # Test data
        flights = [
            Flight(departure_iata='LAX', arrival_iata='JFK'),
            Flight(departure_iata='SFO', arrival_iata='ATL'),
            Flight(departure_iata='ORD', arrival_iata='MIA'),
        ]
        
        for flight in flights:
            try:
                flight.create()
                print(f"Record created: {repr(flight)}")
            except IntegrityError:
                db.session.remove()
                print(f"Record exists or error: {flight.departure_iata} to {flight.arrival_iata}")
