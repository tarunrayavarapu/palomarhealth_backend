# user.py
from flask import current_app
from flask_login import UserMixin
from datetime import date
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash
import os
import json

from __init__ import app, db

""" Helper Functions """

def default_year():
    """
    Returns the default year for user enrollment based on the current month.
    
    If the current month is between August (8) and December (12), the enrollment year is the next year.
    Otherwise, it is the current year.
    
    Returns:
        int: The default year for user enrollment.
    """
    current_month = date.today().month
    current_year = date.today().year
    if 7 <= current_month <= 12:
        current_year += 1
    return current_year 

""" Database Models """

''' Tutorial: https://www.sqlalchemy.org/library.html#tutorials, try to get into Python shell and follow along '''

class User(db.Model, UserMixin):
    """
    User Model

    This class represents the User model, which is used to manage actions in the 'users' table of the database. It is an
    implementation of Object Relational Mapping (ORM) using SQLAlchemy, allowing for easy interaction with the database
    using Python code. The User model includes various fields and methods to support user management, authentication,
    and profile management functionalities.

    Attributes:
        __tablename__ (str): Specifies the name of the table in the database.
        id (Column): The primary key, an integer representing the unique identifier for the user.
        _name (Column): A string representing the user's name. It is not unique and cannot be null.
        _uid (Column): A unique string identifier for the user, cannot be null.
        _password (Column): A string representing the hashed password of the user. It is not unique and cannot be null.
        _role (Column): A string representing the user's role within the application. Defaults to "User".
        _pfp (Column): A string representing the path to the user's profile picture. It can be null.
        _grade_data (Column): A JSON column storing assessment data for the user including grades, attendance, etc.
        _ap_exam (Column): A JSON column storing AP exam data including predicted and manual scores.
    """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    _name = db.Column(db.String(255), unique=False, nullable=False)
    _uid = db.Column(db.String(255), unique=True, nullable=False)
    _email = db.Column(db.String(255), unique=False, nullable=False)
    _password = db.Column(db.String(255), unique=False, nullable=False)
    _role = db.Column(db.String(20), default="User", nullable=False)
    _pfp = db.Column(db.String(255), unique=False, nullable=True)
    _car = db.Column(db.String(255), unique=False, nullable=True)
    _grade_data = db.Column(db.JSON, unique=False, nullable=True)
    _ap_exam = db.Column(db.JSON, unique=False, nullable=True)
   
    posts = db.relationship('Post', backref='author', lazy=True)
                                 
    
    def __init__(self, name, uid, password="", role="User", pfp='', car='', email='?', grade_data=None, ap_exam=None):
        """
        Constructor, 1st step in object creation.
        
        Args:
            name (str): The name of the user.
            uid (str): The unique identifier for the user.
            password (str): The password for the user.
            role (str): The role of the user within the application. Defaults to "User".
            pfp (str): The path to the user's profile picture. Defaults to an empty string.
            car (str): The path to the user's car picture. Defaults to an empty string.
            email (str): The user's email. Defaults to '?'.
            grade_data (dict): JSON data containing assessment information. Defaults to None.
            ap_exam (dict): JSON data containing AP exam scores. Defaults to None.
        """
        self._name = name
        self._uid = uid
        self._email = email
        self.set_password(password)
        self._role = role
        self._pfp = pfp
        self._car = car
        self._grade_data = grade_data if grade_data else {}
        self._ap_exam = ap_exam if ap_exam else {}

    # UserMixin/Flask-Login requires a get_id method to return the id as a string
    def get_id(self):
        """
        Returns the user's ID as a string.
        
        Returns:
            str: The user's ID.
        """
        return str(self.id)

    # UserMixin/Flask-Login requires is_authenticated to be defined
    @property
    def is_authenticated(self):
        """
        Indicates whether the user is authenticated.
        
        Returns:
            bool: True if the user is authenticated, False otherwise.
        """
        return True

    # UserMixin/Flask-Login requires is_active to be defined
    @property
    def is_active(self):
        """
        Indicates whether the user is active.
        
        Returns:
            bool: True if the user is active, False otherwise.
        """
        return True

    # UserMixin/Flask-Login requires is_anonymous to be defined
    @property
    def is_anonymous(self):
        """
        Indicates whether the user is anonymous.
        
        Returns:
            bool: True if the user is anonymous, False otherwise.
        """
        return False
    
    @property
    def email(self):
        """
        Gets the user's email.
        
        Returns:
            str: The user's email.
        """
        return self._email
    
    @email.setter
    def email(self, email):
        """
        Sets the user's email.
        
        Args:
            email (str): The new email for the user.
        """
        if email is None or email == "":
            self._email = "?"
        else:
            self._email = email
        
    def set_email(self):
        """
        Sets the email of the user based on the UID 
        """
        self.email = "?"

    @property
    def name(self):
        """
        Gets the user's name.
        
        Returns:
            str: The user's name.
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the user's name.
        
        Args:
            name (str): The new name for the user.
        """
        self._name = name

    @property
    def uid(self):
        """
        Gets the user's unique identifier.
        
        Returns:
            str: The user's unique identifier.
        """
        return self._uid

    @uid.setter
    def uid(self, uid):
        """
        Sets the user's unique identifier.
        
        Args:
            uid (str): The new unique identifier for the user.
        """
        self._uid = uid

    def is_uid(self, uid):
        """
        Checks if the provided UID matches the user's UID.
        
        Args:
            uid (str): The UID to check.
        
        Returns:
            bool: True if the UID matches, False otherwise.
        """
        return self._uid == uid

    @property
    def password(self):
        """
        Gets the user's password (partially obscured for security).
        
        Returns:
            str: The user's password (first 10 characters followed by "...").
        """
        return self._password[0:10] + "..."  # because of security only show 1st characters

    def set_password(self, password):
        """
        Sets the user's password (hashed).
        
        Args:
            password (str): The new password for the user.
        """
        if not password or password == "":
            password=app.config["DEFAULT_PASSWORD"]
        self._password = generate_password_hash(password, "pbkdf2:sha256", salt_length=10)

    def is_password(self, password):
        """
        Checks if the provided password matches the user's stored password.
        
        Args:
            password (str): The password to check.
        
        Returns:
            bool: True if the password matches, False otherwise.
        """
        return check_password_hash(self._password, password)

    def __str__(self):
        """
        Returns a string representation of the user object (JSON format).
        
        Returns:
            str: A JSON string representation of the user object.
        """
        return json.dumps(self.read())

    @property
    def role(self):
        """
        Gets the user's role.
        
        Returns:
            str: The user's role.
        """
        return self._role

    @role.setter
    def role(self, role):
        """
        Sets the user's role.
        
        Args:
            role (str): The new role for the user.
        """
        self._role = role

    def is_admin(self):
        """
        Checks if the user is an admin.
        
        Returns:
            bool: True if the user is an admin, False otherwise.
        """
        return self._role == "Admin"
    
    @property
    def pfp(self):
        """
        Gets the user's profile picture path.
        
        Returns:
            str: The path to the user's profile picture.
        """
        return self._pfp

    @pfp.setter
    def pfp(self, pfp):
        """
        Sets the user's profile picture path.
        
        Args:
            pfp (str): The new profile picture path for the user.
        """
        self._pfp = pfp

    @property
    def car(self):
        return self._car
    
    @car.setter
    def car(self, car):
        self._car = car
        
    @property
    def grade_data(self):
        """
        Gets the user's grade data.
        
        Returns:
            dict: The user's grade data in JSON format.
        """
        return self._grade_data
    
    @grade_data.setter
    def grade_data(self, grade_data):
        """
        Sets the user's grade data.
        
        Args:
            grade_data (dict): The new grade data for the user.
        """
        self._grade_data = grade_data
    
    @property
    def ap_exam(self):
        """
        Gets the user's AP exam data.
        
        Returns:
            dict: The user's AP exam data in JSON format.
        """
        return self._ap_exam
    
    @ap_exam.setter
    def ap_exam(self, ap_exam):
        """
        Sets the user's AP exam data.
        
        Args:
            ap_exam (dict): The new AP exam data for the user.
        """
        self._ap_exam = ap_exam
    
    def create(self, inputs=None):
        """
        Adds a new record to the table and commits the transaction.
        
        Args:
            inputs (dict, optional): Additional data to update the user with.
        
        Returns:
            User: The created user object, or None on error.
        """
        try:
            db.session.add(self)  # add prepares to persist person object to Users table
            db.session.commit()  # SqlAlchemy "unit of work pattern" requires a manual commit
            if inputs:
                self.update(inputs)
            return self
        except IntegrityError:
            db.session.rollback()
            return None

    def read(self):
        """
        Converts the user object to a dictionary.
        
        Returns:
            dict: A dictionary representation of the user object.
        """
        data = {
            "id": self.id,
            "uid": self.uid,
            "name": self.name,
            "email": self.email,
            "role": self._role,
            "pfp": self._pfp,
            "car": self._car,
            "grade_data": self._grade_data,
            "ap_exam": self._ap_exam
        }
        return data
        
    def update(self, inputs):
        """
        Updates the user object with new data.
        
        Args:
            inputs (dict): A dictionary containing the new data for the user.
        
        Returns:
            User: The updated user object, or None on error.
        """
        if not isinstance(inputs, dict):
            return self

        name = inputs.get("name", "")
        uid = inputs.get("uid", "")
        password = inputs.get("password", "")
        pfp = inputs.get("pfp", None)
        grade_data = inputs.get("grade_data", None)
        ap_exam = inputs.get("ap_exam", None)

        # Update table with new data
        if name:
            self.name = name
        if uid:
            self.set_uid(uid)
        if password:
            self.set_password(password)
        if pfp is not None:
            self.pfp = pfp
        if grade_data is not None:
            self.grade_data = grade_data
        if ap_exam is not None:
            self.ap_exam = ap_exam

        # Check this on each update
        self.set_email()

        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return None
        return self
    
    def delete(self):
        """
        Removes the user object from the database and commits the transaction.
        
        Returns:
            None
        """
        try:
            db.session.delete(self)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
        return None   
    
    def save_pfp(self, image_data, filename):
        """
        Saves the user's profile picture.
        
        Args:
            image_data (bytes): The image data of the profile picture.
            filename (str): The filename of the profile picture.
        """
        try:
            user_dir = os.path.join(app.config['UPLOAD_FOLDER'], self.uid)
            if not os.path.exists(user_dir):
                os.makedirs(user_dir)
            file_path = os.path.join(user_dir, filename)
            with open(file_path, 'wb') as img_file:
                img_file.write(image_data)
            self.update({"pfp": filename})
        except Exception as e:
            raise e
        
    def delete_pfp(self):
        """
        Deletes the user's profile picture from the user record.
        """
        self.pfp = None
        db.session.commit()
        
    def save_car(self, image_data, filename):
        """
        Saves the user's car picture.
        
        Args:
            image_data (bytes): The image data of the car picture.
            filename (str): The filename of the car picture.
        """
        try:
            user_dir = os.path.join(app.config['UPLOAD_FOLDER'], self.uid)
            if not os.path.exists(user_dir):
                os.makedirs(user_dir)
            file_path = os.path.join(user_dir, filename)
            with open(file_path, 'wb') as img_file:
                img_file.write(image_data)
            self.update({"car": filename})
        except Exception as e:
            raise e
        
    def delete_car(self):
        """
        Deletes the user's profile picture from the user record.
        """
        self.car = None
        db.session.commit()
        
    def set_uid(self, new_uid=None):
        """
        Updates the user's directory based on the new UID provided.

        Args:
            new_uid (str, optional): The new UID to update the user's directory.
        
        Returns:
            User: The updated user object.
        """
        # Store the old UID for later comparison
        old_uid = self._uid
        # Update the UID if a new one is provided
        if new_uid and new_uid != self._uid:
            self._uid = new_uid
            # Commit the UID change to the database
            db.session.commit()

        # If the UID has changed, update the directory name
        if old_uid != self._uid:
            old_path = os.path.join(current_app.config['UPLOAD_FOLDER'], old_uid)
            new_path = os.path.join(current_app.config['UPLOAD_FOLDER'], self._uid)
            if os.path.exists(old_path):
                os.rename(old_path, new_path)
                
    @staticmethod
    def restore(data):
        users = {}
        for user_data in data:
            _ = user_data.pop('id', None)  # Remove 'id' from user_data and store it in user_id
            uid = user_data.get("uid", None)
            user = User.query.filter_by(_uid=uid).first()
            if user:
                user.update(user_data)
            else:
                user = User(**user_data)
                user.create()
        return users


"""Database Creation and Testing """

def initUsers():
    """
    The initUsers function creates the User table and adds tester data to the table.
    
    Uses:
        The db ORM methods to create the table.
    
    Instantiates:
        User objects with tester data.
    
    Raises:
        IntegrityError: An error occurred when adding the tester data to the table.
    """
    with app.app_context():
        """Create database and tables"""
        db.create_all()
        """Tester data for table"""
        
        default_grade_data = {
            'grade': 'A',
            'attendance': 5,
            'work_habits': 5,
            'behavior': 5,
            'timeliness': 5,
            'tech_sense': 4,
            'tech_talk': 4,
            'tech_growth': 4,
            'advocacy': 4,
            'communication_collaboration': 5,
            'integrity': 5,
            'organization': 5
        }

        default_ap_exam = {
            'predicted_score': {
                'practice_based': {
                    'mcq_2018': 0,
                    'mcq_2020': 0,
                    'mcq_2021': 0,
                    'practice_frq': 0,
                    'predicted_ap_score': 0,
                    'confidence_level': 'Low'
                },
                'manual_calculator': {
                    'mcq_score': 60,
                    'frq_score': 6,
                    'composite_score': 90,
                    'predicted_ap_score': 5
                }
            },
            'last_updated': None
        }

        u1 = User(name='Thomas Edison', uid=app.config['ADMIN_USER'], password=app.config['ADMIN_PASSWORD'],
                pfp='toby.png', car='toby_car.png', role="Admin", grade_data=default_grade_data, ap_exam=default_ap_exam)
        u3 = User(name='Nicholas Tesla', uid='niko', password='123niko', pfp='niko.png', grade_data=default_grade_data, ap_exam=default_ap_exam)
        u4 = User(name='Arhaan Memon', uid='amemon', password=app.config['DEFAULT_PASSWORD'],
                pfp='toby.png', car='toby_car.png', role="Admin", grade_data=default_grade_data, ap_exam=default_ap_exam)
        u5 = User(name='David Brown', uid='david', password='123David!', grade_data=default_grade_data, ap_exam=default_ap_exam)
        u6 = User(name='Sarah Williams', uid='sarah', password='123Sarah!', grade_data=default_grade_data, ap_exam=default_ap_exam)
        u7 = User(name='James Wilson', uid='james', password='123James!', grade_data=default_grade_data, ap_exam=default_ap_exam)
        u8 = User(name='Olivia Taylor', uid='olivia', password='123Olivia!', grade_data=default_grade_data, ap_exam=default_ap_exam)
        u9 = User(name='Daniel Anderson', uid='daniel', password='123Daniel!', grade_data=default_grade_data, ap_exam=default_ap_exam)
        u10 = User(name='Sophia Thomas', uid='sophia', password='123Sophia!', grade_data=default_grade_data, ap_exam=default_ap_exam)
        u11 = User(name='Matthew Martinez', uid='matthew', password='123Matthew!', grade_data=default_grade_data, ap_exam=default_ap_exam)
        u12 = User(name='Charlotte Moore', uid='charlotte', password='123Charlotte!', grade_data=default_grade_data, ap_exam=default_ap_exam)
        u13 = User(name='William Jackson', uid='william', password='123William!', grade_data=default_grade_data, ap_exam=default_ap_exam)
        u14 = User(name='Ava Lee', uid='ava', password='123Ava!', grade_data=default_grade_data, ap_exam=default_ap_exam)
        u15 = User(name='Benjamin Harris', uid='benjamin', password='123Benjamin!', grade_data=default_grade_data, ap_exam=default_ap_exam)
        u16 = User(name='Isabella Clark', uid='isabella', password='123Isabella!', grade_data=default_grade_data, ap_exam=default_ap_exam)
        u17 = User(name='Lucas Lewis', uid='lucas', password='123Lucas!', grade_data=default_grade_data, ap_exam=default_ap_exam)
        u18 = User(name='Amelia Walker', uid='amelia', password='123Amelia!', grade_data=default_grade_data, ap_exam=default_ap_exam)
        u19 = User(name='Ethan Hall', uid='ethan', password='123Ethan!', grade_data=default_grade_data, ap_exam=default_ap_exam)
        u20 = User(name='Mia Young', uid='mia', password='123Mia!', grade_data=default_grade_data, ap_exam=default_ap_exam)
        u21 = User(name='Alexander King', uid='alexander', password='123Alexander!', grade_data=default_grade_data, ap_exam=default_ap_exam)
        u22 = User(name='Chloe Scott', uid='chloe', password='123Chloe!', grade_data=default_grade_data, ap_exam=default_ap_exam)
        u23 = User(name='Henry Adams', uid='henry', password='123Henry!', grade_data=default_grade_data, ap_exam=default_ap_exam)
        u24 = User(name='Ella Green', uid='ella', password='123Ella!', grade_data=default_grade_data, ap_exam=default_ap_exam)
        u25 = User(name='Jack Nelson', uid='jack', password='123Jack!', grade_data=default_grade_data, ap_exam=default_ap_exam)
        u26 = User(name='Lily Carter', uid='lily', password='123Lily!', grade_data=default_grade_data, ap_exam=default_ap_exam)
        u27 = User(name='Noah Mitchell', uid='noah', password='123Noah!', grade_data=default_grade_data, ap_exam=default_ap_exam)
        u28 = User(name='Grace Perez', uid='grace', password='123Grace!', grade_data=default_grade_data, ap_exam=default_ap_exam)
        u29 = User(name='Matthew Robinson', uid='matthew', password='123Matthew!', grade_data=default_grade_data, ap_exam=default_ap_exam)
        u30 = User(name='Hannah Garcia', uid='hannah', password='123Hannah!', grade_data=default_grade_data, ap_exam=default_ap_exam)


        users = [u1, u3, u4, u5, u6, u7, u8, u9, u10, u11, u12, u13, u14, u15, u16, u17, u18, u19, u20, u21, u22, u23, u24, u25, u26, u27, u28, u29, u30]

        
        for user in users:
            try:
                user.create()
            except IntegrityError:
                '''fails with bad or duplicate data'''
                db.session.remove()