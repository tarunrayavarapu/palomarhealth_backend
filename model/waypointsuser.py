# waypointsuser.py
import logging
from sqlite3 import IntegrityError
from sqlalchemy import Text, JSON
from sqlalchemy.exc import IntegrityError
from __init__ import app, db
from model.user import User

class WaypointsUser(db.Model):
    """
    WaypointsUser Model
    
    The WaypointsUser class represents an individual contribution or discussion within a channel.
    
    Attributes:
        id (db.Column): The primary key, an integer representing the unique identifier for the waypointsuser.
        _injury (db.Column): A string representing the injury of the waypointsuser.
        _location (db.Column): A string representing the location of the waypointsuser.
        _rating (db.Column): An integer representing the user rating on the hospital treatment.
        _user_id (db.Column): An integer representing the user who created the waypointsuser.
    """
    __tablename__ = 'waypointsuser'

    id = db.Column(db.Integer, primary_key=True)
    _injury = db.Column(db.String(255), nullable=False)
    _location = db.Column(db.String(255), nullable=False)
    _address = db.Column(db.String(255), nullable=False)
    _rating = db.Column(db.Integer, nullable=True)
    _user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __init__(self, injury, location, address, rating, user_id=None):
        """
        Constructor, 1st step in object creation.
        
        Args:
            injury (str): The injury of the waypointsuser.
            location (str): The location of the waypointsuser.
            address (json): The extra address of the waypointsuser.
            user_id (int): The user who created the waypointsuser.
        """
        self._injury = injury
        self._location = location
        self._address = address
        self._rating = rating
        self._user_id = user_id

    def to_dict(self):
        return {
            "id": self.id,
            "injury": self._injury,
            "location": self._location,
            "address": self._address,
            "rating": self._rating,
            "user_id": self._user_id,
        }

    def __repr__(self):
        """
        The __repr__ method is a special method used to represent the object in a string format.
        Called by the repr(waypointsuser) built-in function, where waypointsuser is an instance of the waypointsuser class.
        
        Returns:
            str: A text representation of how to create the object.
        """
        return f"WaypointsUser(id={self.id}, injury={self._injury}, location={self._location}, address={self._address}, rating={self._rating}, user_id={self._user_id})"

    def create(self):
        """
        Creates a new waypointsuser in the database.
        
        Returns:
            WaypointsUser: The created waypointsuser object, or None on error.
        """
        try:
            db.session.add(self)
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            logging.warning(f"IntegrityError: Could not create waypointsuser with injury '{self._injury}' due to {str(e)}.")
            return None
        return self
        
    def read(self):
        """
        The read method retrieves the object data from the object's attributes and returns it as a dictionary.
        
        Uses:
            The Channel.query and User.query methods to retrieve the channel and user objects.
        
        Returns:
            dict: A dictionary containing the waypointsuser data, including user and channel names.
        """
        user = User.query.get(self._user_id)
        data = {
            "id": self.id,
            "injury": self._injury,
            "location": self._location,
            "address": self._address,
            "rating": self._rating,
            "user_id": user.id if user else None,
        }
        return data
    

    def update(self, data):
        self._injury = data.get('_injury', self._injury)

        self._location = data.get('_location', self._location)
        self._address = data.get('_address', self._address)
        self._rating = data.get('_rating', self._rating)
        self._user_id = data.get('_user_id', self._user_id)

        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
       
    
    def delete(self):
        """
        The delete method removes the object from the database and commits the transaction.
        
        Uses:
            The db ORM methods to delete and commit the transaction.
        
        Raises:
            Exception: An error occurred when deleting the object from the database.
        """    
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
        
    @staticmethod
    def restore(data):
        for waypoints_data in data:
            _ = waypoints_data.pop('id', None)  # Remove 'id' from waypoints_data
            injury = waypoints_data.get("injury", None)
            waypointsuser = WaypointsUser.query.filter_by(_injury=injury).first()
            if waypointsuser:
                waypointsuser.update(waypoints_data)
            else:
                waypointsuser = WaypointsUser(**waypoints_data)
                waypointsuser.update(waypoints_data)
                waypointsuser.create()
        
def initWaypointsUser():
    """
    The initWaypoints function creates the WaypointsUser table and adds tester data to the table.
    
    Uses:
        The db ORM methods to create the table.
    
    Instantiates:
        WaypointsUser objects with tester data.
    
    Raises:
        IntegrityError: An error occurred when adding the tester data to the table.
    """        
    with app.app_context():
        """Create database and tables"""
        db.create_all()
        """Tester data for table"""
        waypointsuser = [
                    WaypointsUser(injury='Fractures', location='Hospital', address="Scripps, La Jolla, CA", rating=5, user_id=1),
                    WaypointsUser(injury='Minor Cuts', location='Pharmacy', address="Scripps, La Jolla, CA", rating=5,user_id=1),
                    WaypointsUser(injury='Muscle Strains', location='Recovery', address="Scripps, La Jolla, CA", rating=5, user_id=1),
        ]
        
        for waypointsuser in waypointsuser:
            try:
                waypointsuser.create()
                print(f"Record created: {repr(waypointsuser)}")
            except IntegrityError:
                '''fails with bad or duplicate data'''
                db.session.remove()
                print(f"Records exist, duplicate email, or error: {waypointsuser._injury}")