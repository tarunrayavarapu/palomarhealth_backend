from sqlalchemy import Integer
from __init__ import app, db
import logging
from sqlite3 import IntegrityError
from sqlalchemy import Text, JSON
from sqlalchemy.exc import IntegrityError
from model.user import User
from model.post import Post

class Weather(db.Model):
    
    __tablename__ = 'packing_checklists'
    
    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String(3), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __init__(self, item, user_id=None, ):
        self.item = item
        self.user_id = user_id

    def __repr__(self):

        return f"Weather(id={self.id}, user={self.user_id}, item={self.item})"
    
    def create(self):

        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
        return self

    def read(self):

        return {
            "id": self.id,
            "item": self.item,
            "user_id": self.user_id
            
        }
        
    def update(self, data):

        self.item = data.get('item', self.item)
        self.user = data.get('user_id', self.user_id)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
        
    def delete(self):

        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
        
    @staticmethod
    def restore(data):
        for packing_item in data:
            _ = packing_item.pop('id', None)  # Remove 'id' from post_data
            packing_checklist_item = packing_item.get("item", None)
            item = Weather.query.filter_by(item=packing_checklist_item).first()
            if item:
                item.update(packing_item)
            else:
                item = Weather(**packing_item)
                item.update(packing_item)
                item.create()
                

def initPackingChecklist():

    with app.app_context():

        db.create_all()

        test_data = [
            Weather(user_id=1, item="Hat"),
            Weather(user_id=1, item="Sunglasses"),
            Weather(user_id=1, item="French Dictionary"),
        ]
        
        for data in test_data:
            try:
                db.session.add(data)
                db.session.commit()
                print(f"Record created: {repr(data)}")
            except Exception as e:
                db.session.rollback()
                print(f"Error creating record for user {data.user_id}: {e}")