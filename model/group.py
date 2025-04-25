from sqlite3 import IntegrityError
from __init__ import app, db
from model.section import Section
from model.user import User

# Association table for the many-to-many relationship between Group and User (moderators)
group_moderators = db.Table('group_moderators',
    db.Column('group_id', db.Integer, db.ForeignKey('groups.id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True)
)

class Group(db.Model):
    """
    Group Model
    
    The Group class represents a specific community within a section.
    
    Attributes:
        id (db.Column): The primary key, an integer representing the unique identifier for the group.
        _name (db.Column): A string representing the name of the group.
        _section_id (db.Column): An integer representing the section to which the group belongs.
        moderators (relationship): A collection of users who are the moderators of the group.
    """
    __tablename__ = 'groups'

    id = db.Column(db.Integer, primary_key=True)
    _name = db.Column(db.String(255), unique=True, nullable=False)
    _section_id = db.Column(db.Integer, db.ForeignKey('sections.id'), nullable=False)

    channels = db.relationship('Channel', backref='group', lazy=True)
    moderators = db.relationship('User', secondary=group_moderators, lazy='subquery',
                                 backref=db.backref('moderated_groups', lazy=True))
    
    def __init__(self, name, section_id, moderators=None):
        """
        Constructor, 1st step in object creation.
        
        Args:
            name (str): The name of the group.
            section_id (int): The section to which the group belongs.
            moderators (list, optional): A list of users who are the moderators of the group. Defaults to None.
        """
        self._name = name
        self._section_id = section_id
        self.moderators = moderators or []
        
    @property
    def name(self):
        """
        Gets the group's name.
        
        Returns:
            str: The group's name.
        """
        return self._name

    def __repr__(self):
        """
        The __repr__ method is a special method used to represent the object in a string format.
        Called by the repr() built-in function.
        
        Returns:
            str: A text representation of how to create the object.
        """
        return f"Group(id={self.id}, name={self._name}, section_id={self._section_id}, moderators={[moderator.id for moderator in self.moderators]})"

    def create(self):
        """
        The create method adds the object to the database and commits the transaction.
        
        Uses:
            The db ORM methods to add and commit the transaction.
        
        Raises:
            Exception: An error occurred when adding the object to the database.
        """
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
    
    def read(self):
        """
        The read method retrieves the object data from the object's attributes and returns it as a dictionary.
        
        Returns:
            dict: A dictionary containing the group data.
        """
        return {
            'id': self.id,
            'name': self._name,
            'section_id': self._section_id,
            'moderators': [moderator.id for moderator in self.moderators]
        }
        
    def update(self, inputs):
        """
        Updates the group object with new data.
        
        Args:
            inputs (dict): A dictionary containing the new data for the group.
        
        Returns:
            Group: The updated group object, or None on error.
        """
        if not isinstance(inputs, dict):
            return self

        name = inputs.get("name", "")
        section_id = inputs.get("section_id", None)

        # Update table with new data
        if name:
            self._name = name
        if section_id:
            self._section_id = section_id

        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return None
        return self
        
    @staticmethod
    def restore(data, users):
        groups = {}
        for group_data in data:
            _ = group_data.pop('id', None)  # Remove 'id' from group_data
            name = group_data.get("name", None)
            group = Group.query.filter_by(_name=name).first()
            if group:
                group.update(group_data)
            else:
                group = Group(**group_data)
                group.create() 

        # Restore moderators relationship (TBD)
        """
        for group_data in data:
            group = groups[group_data['name']]
            if 'moderators' in group_data:
                for moderator_id in group_data['moderators']:
                    moderator = users[moderator_id]
                    group.moderators.append(moderator)
        db.session.commit()
        """
        return groups

def create_group(name, section_id, moderators):
    try:
        group = Group(name=name, section_id=section_id, moderators=moderators)
        db.session.add(group)  # Ensure the group is added to the session
        db.session.commit()
        print(f"Record created: Group(id={group.id}, name={group.name}, section_id={group.section_id}, moderators={moderators})")
    except AttributeError as e:
        print(f"An error occurred: {e}")
        db.session.rollback()  # Rollback the session in case of an error
    except Exception as e:
        print(f"Unexpected error: {e}")
        db.session.rollback()
            
def initGroups():
    """
    The initGroups function creates the Group table and adds tester data to the table.
    
    Uses:
        The db ORM methods to create the table.
    
    Instantiates:
        Group objects with tester data.
    
    Raises:
        IntegrityError: An error occurred when adding the tester data to the table.
    """
    with app.app_context():
        """Create database and tables"""
        db.create_all()
        """Tester data for table"""

        # Home Page Groups
        home_page_section = Section.query.filter_by(_name='Home Page').first()
        if not home_page_section:
            print("Error: 'Home Page' section not found.")
            return

        moderator = User.query.get(1)
        if not moderator:
            print("Error: User with ID 1 not found.")
            return

        groups = [
            Group(name='General', section_id=home_page_section.id, moderators=[moderator]),
            Group(name='Support', section_id=home_page_section.id, moderators=[moderator])
        ]
        
        for group in groups:
            try:
                db.session.add(group)
                db.session.commit()
                print(f"Record created: {repr(group)}")
            except IntegrityError:
                db.session.rollback()
                print(f"Records exist, duplicate email, or error: {group._name}")
            except Exception as e:
                db.session.rollback()
                print(f"Unexpected error: {e}")
