from . import db

class Listing(db.Model):
    __tablename__ = 'listings'
    listing_id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, nullable=False)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=False)
    picture = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(50), default='open')  # 'open', 'in progress', 'completed'