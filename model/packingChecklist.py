from sqlalchemy import Integer
from __init__ import app, db

class packingChecklist(db.Model):
    
    __tablename__ = 'packing_checklists'
    
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(3), nullable=False)
    item = db.Column(db.String(3), nullable=False)

    def __init__(self, user, item):
        self.user = user
        self.item = item

    def __repr__(self):

        return f"packingChecklist(id={self.id}, user={self.user}, item={self.item})"
    
    def create(self):

        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    def read(self):

        return {
            "id": self.id,
            "user": self.user,
            "item": self.item,
        }

def initPackingChecklist():

    with app.app_context():

        db.create_all()

        test_data = [
            packingChecklist(user='Aaditya Taleppady', item="Hat"),
            packingChecklist(user='Toby', item="Sunglasses"),
            packingChecklist(user='Mr. Mort', item="French Dictionary"),
        ]
        
        for data in test_data:
            try:
                db.session.add(data)
                db.session.commit()
                print(f"Record created: {repr(data)}")
            except Exception as e:
                db.session.rollback()
                print(f"Error creating record for user {data.user}: {e}")