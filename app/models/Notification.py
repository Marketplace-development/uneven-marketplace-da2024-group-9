from . import db

class Notification(db.Model):
    __tablename__ = 'notifications'
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, nullable=False)
    viewed = db.Column(db.Boolean, default=False)
    notification_id = db.Column(db.Integer, nullable=False)
