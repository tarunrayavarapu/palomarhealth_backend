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
        _title (db.Column): A string representing the title of the waypoints.
        _comment (db.Column): A string representing the comment of the waypoints.
        _content (db.Column): A JSON blob representing the content of the waypoints.
        _user_id (db.Column): An integer representing the user who created the waypoints.
    """
    __tablename__ = 'waypoints'

    id = db.Column(db.Integer, primary_key=True)
    _title = db.Column(db.String(255), nullable=False)
    _comment = db.Column(db.String(255), nullable=False)
    _content = db.Column(JSON, nullable=False)
    _user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __init__(self, title, comment, user_id=None, content={}, user_name=None, channel_name=None):
        """
        Constructor, 1st step in object creation.
        
        Args:
            title (str): The title of the waypoints.
            comment (str): The comment of the waypoints.
            user_id (int): The user who created the waypoints.
            content (dict): The content of the waypoints.
        """
        self._title = title
        self._comment = comment
        self._user_id = user_id
        self._content = content

    def __repr__(self):
        """
        The __repr__ method is a special method used to represent the object in a string format.
        Called by the repr(waypoints) built-in function, where waypoints is an instance of the waypoints class.
        
        Returns:
            str: A text representation of how to create the object.
        """
        return f"Waypoints(id={self.id}, title={self._title}, comment={self._comment}, content={self._content}, user_id={self._user_id})"

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
            logging.warning(f"IntegrityError: Could not create waypoints with title '{self._title}' due to {str(e)}.")
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
        user = User.query.get(self._user_id)
        data = {
            "id": self.id,
            "title": self._title,
            "comment": self._comment,
            "content": self._content,
            "user_id": user.id if user else None,
        }
        return data
    

    def update(self, data):
        self._title = data.get('_title', self._title)
        self._content = data.get('_content', self._content)
        self._comment = data.get('_comment', self._comment)
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
            title = waypoints_data.get("title", None)
            waypoints = Waypoints.query.filter_by(_title=title).first()
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
            Waypoints(title='Broken Bone', comment='Hospital', content={'type': 'announcement'}, user_id=1),
            Waypoints(title='Bruise', comment='Pharmacy', content={'type': 'announcement'}, user_id=1),
            Waypoints(title='Sprained Ankle', comment='Recovery Center', content={'type': 'announcement'}, user_id=2),
        ]
        
        for waypoints in waypoints:
            try:
                waypoints.create()
                print(f"Record created: {repr(waypoints)}")
            except IntegrityError:
                '''fails with bad or duplicate data'''
                db.session.remove()
                print(f"Records exist, duplicate email, or error: {waypoints._title}")