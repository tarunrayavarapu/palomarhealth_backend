# palomar.py
import logging
from sqlalchemy.exc import IntegrityError
from __init__ import app, db

class Palomar(db.Model):
    """
    PalomarHealth Model — Represents a social media post for Palomar Health.
    """
    __tablename__ = 'PalomarHealth'

    id = db.Column(db.Integer, primary_key=True)
    caption = db.Column(db.String(255), nullable=False)
    platform = db.Column(db.String(50), nullable=False)
    post_type = db.Column(db.String(50), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())
    updated_at = db.Column(db.DateTime, nullable=True)

    def __init__(self, caption, platform, post_type, content):
        self.caption = caption
        self.platform = platform
        self.post_type = post_type
        self.content = content

    def __repr__(self):
        return f"Palomar(id={self.id}, caption={self.caption}, platform={self.platform}, post_type={self.post_type})"

    def create(self):
        try:
            db.session.add(self)
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            logging.warning(f"IntegrityError: Could not save post '{self.caption}' due to {str(e)}.")
            return None
        return self

    def read(self):
        return {
            "id": self.id,
            "caption": self.caption,
            "platform": self.platform,
            "post_type": self.post_type,
            "content": self.content,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    def update(self, data):
        self.caption = data.get('caption', self.caption)
        self.platform = data.get('platform', self.platform)
        self.post_type = data.get('post_type', self.post_type)
        self.content = data.get('content', self.content)
        self.updated_at = db.func.now()
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

def initPalomarHealth():
    """
    Initialize the PalomarHealth table with static data.
    """
    with app.app_context():
        db.create_all()

        test_posts = [
            Palomar(caption="Stay Hydrated!", platform="Twitter", post_type="Health Tip", content="Drink 8 glasses of water a day!"),
            Palomar(caption="Free Health Checkup!", platform="Instagram", post_type="Event", content="Join us for a free health checkup event at our clinic!"),
            Palomar(caption="Boost Your Energy!", platform="Facebook", post_type="Motivational", content="Get moving with a 20-minute workout every morning!"),
            Palomar(caption="Did You Know?", platform="Twitter", post_type="Educational", content="Heart disease is the leading cause of death globally. Stay healthy!"),
            Palomar(caption="Upcoming Health Webinar", platform="LinkedIn", post_type="Event", content="Sign up for our upcoming health and wellness webinar!"),
            Palomar(caption="Mental Health Matters", platform="Instagram", post_type="Health Tip", content="Take time for your mental health. It's just as important!"),
        ]

        for post in test_posts:
            try:
                result = post.create()
                if result:
                    print(f"Record created: {repr(post)}")
            except IntegrityError:
                db.session.remove()
                print(f"Error or duplicate: {post.caption}, {post.platform}, {post.post_type}")
