import logging
from sqlite3 import IntegrityError
from sqlalchemy.exc import IntegrityError
from __init__ import app, db
from flask_cors import CORS


class Flight(db.Model):
   """
   Flight Model
  
   Represents a flight record with departure and arrival airport IATA codes and optional notes.
  
   Attributes:
       id (db.Column): The primary key, an integer representing the unique identifier for the flight.
       departure_iata (db.Column): The IATA code for the departure airport.
       arrival_iata (db.Column): The IATA code for the arrival airport.
       notes (db.Column): Stores notes associated with a flight (optional).
   """
   __tablename__ = 'flights'


   id = db.Column(db.Integer, primary_key=True)
   origin = db.Column(db.String(3), nullable=False)
   destination = db.Column(db.String(3), nullable=False)
   note = db.Column(db.String(255))  # Field to store optional notes


   def __init__(self, origin, destination, note=None):
       """
       Constructor, initializes a flight record with optional notes.
      
       Args:
           departure_iata (str): The IATA code for the departure airport.
           arrival_iata (str): The IATA code for the arrival airport.
           notes (str, optional): Any notes associated with the flight.
       """
       self.origin = origin
       self.destination = destination
       self.note = note


   def __repr__(self):
       """
       Represents the flight record in string format.
      
       Returns:
           str: A string representation of the flight record.
       """
       return f"Flight(id={self.id}, origin={self.origin}, destination={self.destination}, notes={self.note})"


   def create(self):
       """
       Creates a new flight record in the database, including optional notes.
      
       Returns:
           Flight: The created flight object, or None on error.
       """
       try:
           db.session.add(self)
           db.session.commit()
       except IntegrityError as e:
           db.session.rollback()
           logging.warning(f"IntegrityError: Could not create flight with departure '{self.origin}' and arrival '{self.destination}' due to {str(e)}.")
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
           "origin": self.origin,
           "destination": self.destination,
           "notes": self.note,
       }
      
   def update(self, data):
       """
       Updates the flight record based on the provided data, including optional notes.
      
       Args:
           data (dict): The updated data for the flight.
       """
       self.origin = data.get('origin', self.origin)
       self.destination = data.get('destination', self.destination)
       self.note = data.get('note', self.note)
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
  
   @staticmethod
   def restore(data):
       """
       Restore flight records, updating existing ones or creating new ones based on provided data.
      
       Args:
           data (list): List of flight data dictionaries.
       """
       for flight_data in data:
           _ = flight_data.pop('id', None)  # Remove 'id' from post_data
           title = flight_data.get("origin", None)
           flight = Flight.query.filter_by(origin=title).first()
           if flight:
               flight.update(flight_data)
           else:
               flight = Flight(**flight_data)
               flight.update(flight_data)
               flight.create()




def initFlights():
   """
   Initializes the Flight table and adds some test data.
   """
   with app.app_context():
       # Create database and tables
       db.create_all()


       # Test data
       flights = [
           Flight(origin='LAX', destination='JFK', note='Flight from Los Angeles to New York'),
           Flight(origin='SFO', destination='ATL', note='Flight from San Francisco to Atlanta'),
           Flight(origin='ORD', destination='MIA', note='Flight from Chicago to Miami'),
       ]
      
       for flight in flights:
           try:
               flight.create()
               print(f"Record created: {repr(flight)}")
           except IntegrityError:
               db.session.remove()
               print(f"Record exists or error: {flight.origin} to {flight.destination}")