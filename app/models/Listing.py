from app import db

class Listing(db.Model):
    __tablename__ = 'listings'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    location = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=True)
    photo = db.Column(db.String(255), nullable=True)
    username = db.Column(db.String(80), nullable=False)  

    created_at = db.Column(db.DateTime, default=db.func.now())

    def __repr__(self):
        return f"<Listing {self.title}>"