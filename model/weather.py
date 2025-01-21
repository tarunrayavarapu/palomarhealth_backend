from sqlalchemy import Integer
from __init__ import app, db

class Weather(db.Model):
    
    __tablename__ = 'packing_checklists'
    
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(3), nullable=False)
    item = db.Column(db.String(3), nullable=False)

    def __init__(self, user, item):
        self.user = user
        self.item = item

    def __repr__(self):

        return f"Weather(id={self.id}, user={self.user}, item={self.item})"
    
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
        
    def update(self, data):

        self.user = data.get('user', self.user)
        self.item = data.get('item', self.item)
        try:
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
            Weather(user='Aaditya Taleppady', item="Hat"),
            Weather(user='Toby', item="Sunglasses"),
            Weather(user='Mr. Mort', item="French Dictionary"),
        ]
        
        for data in test_data:
            try:
                db.session.add(data)
                db.session.commit()
                print(f"Record created: {repr(data)}")
            except Exception as e:
                db.session.rollback()
                print(f"Error creating record for user {data.user}: {e}")