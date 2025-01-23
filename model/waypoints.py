# waypoints.py
import logging
from sqlite3 import IntegrityError
from sqlalchemy import Text, JSON
from sqlalchemy.exc import IntegrityError
from __init__ import app, db
from model.user import User

class Waypoints(db.Model):
    """
    Waypoints Model
    
    The Waypoints class represents an individual contribution or discussion within a channel.
    
    Attributes:
        id (db.Column): The primary key, an integer representing the unique identifier for the waypoints.
        _injury (db.Column): A string representing the injury of the waypoints.
        _location (db.Column): A string representing the location of the waypoints.
    """
    __tablename__ = 'waypoints'

    id = db.Column(db.Integer, primary_key=True)
    _injury = db.Column(db.String(255), nullable=False)
    _location = db.Column(db.String(255), nullable=False)
    _notes = db.Column(JSON, nullable=False)

    def __init__(self, injury, location, notes={}):
        """
        Constructor, 1st step in object creation.
        
        Args:
            injury (str): The injury of the waypoints.
            location (str): The location of the waypoints.
            notes (json): The extra notes of the waypoints.
        """
        self._injury = injury
        self._location = location
        self._notes = notes

    def to_dict(self):
        return {
            "id": self.id,
            "injury": self._injury,
            "location": self._location,
            "notes": self._notes,
        }

    def __repr__(self):
        """
        The __repr__ method is a special method used to represent the object in a string format.
        Called by the repr(waypoints) built-in function, where waypoints is an instance of the waypoints class.
        
        Returns:
            str: A text representation of how to create the object.
        """
        return f"Waypoints(id={self.id}, injury={self._injury}, location={self._location}, notes={self._notes}"

    def create(self):
        """
        Creates a new waypoints in the database.
        
        Returns:
            Waypoints: The created waypoints object, or None on error.
        """
        try:
            db.session.add(self)
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            logging.warning(f"IntegrityError: Could not create waypoints with injury '{self._injury}' due to {str(e)}.")
            return None
        return self
        
    def read(self):
        """
        The read method retrieves the object data from the object's attributes and returns it as a dictionary.
        
        Uses:
            The Channel.query and User.query methods to retrieve the channel and user objects.
        
        Returns:
            dict: A dictionary containing the waypoints data, including user and channel names.
        """
        data = {
            "id": self.id,
            "injury": self._injury,
            "location": self._location,
            "notes": self._notes,
        }
        return data
    

    def update(self, data):
        self._injury = data.get('_injury', self._injury)
        self._notes = data.get('_notes', self._notes)
        self._location = data.get('_location', self._location)

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
            waypoints = Waypoints.query.filter_by(_injury=injury).first()
            if waypoints:
                waypoints.update(waypoints_data)
            else:
                waypoints = Waypoints(**waypoints_data)
                waypoints.update(waypoints_data)
                waypoints.create()
        
def initWaypoints():
    """
    The initWaypoints function creates the Waypoints table and adds tester data to the table.
    
    Uses:
        The db ORM methods to create the table.
    
    Instantiates:
        Waypoints objects with tester data.
    
    Raises:
        IntegrityError: An error occurred when adding the tester data to the table.
    """        
    with app.app_context():
        """Create database and tables"""
        db.create_all()
        """Tester data for table"""
        waypoints = [
                    Waypoints(injury='Fractures', location='Hospital', notes={}),
                    Waypoints(injury='Broken Bones', location='Hospital', notes={}),
                    Waypoints(injury='Severe Bleeding', location='Hospital', notes={}),
                    Waypoints(injury='Head Injuries', location='Hospital', notes={}),
                    Waypoints(injury='Concussions', location='Hospital', notes={}),
                    Waypoints(injury='Heart Attack', location='Hospital', notes={}),
                    Waypoints(injury='Stroke', location='Hospital', notes={}),
                    Waypoints(injury='Appendicitis', location='Hospital', notes={}),
                    Waypoints(injury='Dehydration', location='Hospital', notes={}),
                    Waypoints(injury='Heatstroke', location='Hospital', notes={}),
                    Waypoints(injury='Allergic Reaction', location='Hospital', notes={}),
                    Waypoints(injury='Burns', location='Hospital', notes={}),
                    Waypoints(injury='Respiratory Issues', location='Hospital', notes={}),
                    Waypoints(injury='Infections', location='Hospital', notes={}),
                    Waypoints(injury='Snake Bite', location='Hospital', notes={}),
                    Waypoints(injury='Animal Bite', location='Hospital', notes={}),
                    Waypoints(injury='Minor Cuts', location='Pharmacy', notes={}),
                    Waypoints(injury='Motion Sickness', location='Pharmacy', notes={}),
                    Waypoints(injury='Mild Allergies', location='Pharmacy', notes={}),
                    Waypoints(injury='Upset Stomach', location='Pharmacy', notes={}),
                    Waypoints(injury='Diarrhea', location='Pharmacy', notes={}),
                    Waypoints(injury='Pain', location='Pharmacy', notes={}),
                    Waypoints(injury='Headaches', location='Pharmacy', notes={}),
                    Waypoints(injury='Coughs', location='Pharmacy', notes={}),
                    Waypoints(injury='Colds', location='Pharmacy', notes={}),
                    Waypoints(injury='Insect Bites', location='Pharmacy', notes={}),
                    Waypoints(injury='Stings', location='Pharmacy', notes={}),
                    Waypoints(injury='Sunburn', location='Pharmacy', notes={}),
                    Waypoints(injury='Blisters', location='Pharmacy', notes={}),
                    Waypoints(injury='Skin Irritation', location='Pharmacy', notes={}),
                    Waypoints(injury='Menstrual Pain', location='Pharmacy', notes={}),
                    Waypoints(injury='Muscle Strains', location='Recovery', notes={}),
                    Waypoints(injury='Sprains', location='Recovery', notes={}),
                    Waypoints(injury='Back Pain', location='Recovery', notes={}),
                    Waypoints(injury='Neck Pain', location='Recovery', notes={}),
                    Waypoints(injury='Post-Surgery Recovery', location='Recovery', notes={}),
                    Waypoints(injury='Joint Injuries', location='Recovery', notes={}),
                    Waypoints(injury='Exhaustion', location='Recovery', notes={}),
                    Waypoints(injury='Chronic Fatigue', location='Recovery', notes={}),
                    Waypoints(injury='Mental Health', location='Recovery', notes={}),
                    Waypoints(injury='Substance Overuse', location='Recovery', notes={}),
                    Waypoints(injury='Addiction', location='Recovery', notes={}),
                    Waypoints(injury='Rehabilitation', location='Recovery', notes={}),
                    Waypoints(injury='Mobility Issues', location='Recovery', notes={}),
        ]
        
        for waypoints in waypoints:
            try:
                waypoints.create()
                print(f"Record created: {repr(waypoints)}")
            except IntegrityError:
                '''fails with bad or duplicate data'''
                db.session.remove()
                print(f"Records exist, duplicate email, or error: {waypoints._injury}")