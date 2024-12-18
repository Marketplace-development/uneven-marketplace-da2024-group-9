from app import db


class Listing(db.Model):
    __tablename__ = 'listings'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    location = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=True)
    photo = db.Column(db.LargeBinary, nullable=True)
    mime_type = db.Column(db.String(100), nullable=True)
    price = db.Column(db.Float, nullable=True)  
    username = db.Column(db.String(80),  nullable=False)  
    
    created_at = db.Column(db.DateTime, default=db.func.now())
    transactions = db.relationship('Transaction', backref='parent_listing', lazy=True)
    
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    student = db.relationship('Student', back_populates='listings')
    def __repr__(self):
        return f"<Listing {self.title}>"
