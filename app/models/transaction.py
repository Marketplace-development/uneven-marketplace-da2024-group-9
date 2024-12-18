from app import db
from datetime import datetime

class Transaction(db.Model):
    __tablename__ = 'transactions'

    id = db.Column(db.Integer, primary_key=True)
    listing_id = db.Column(db.Integer, db.ForeignKey('listings.id'), nullable=False)
    student_username = db.Column(db.String(80), nullable=False)  # Degene die de taak plaatst
    technician_id = db.Column(db.Integer, db.ForeignKey('technicians.id'), nullable=False)  # Nieuwe FK  # Degene die de taak uitvoert
    technician_username = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default="pending")  # "pending", "completed", "cancelled"
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relatie met Listing
    technician = db.relationship('Technician', backref='transactions')
    listing = db.relationship('Listing', backref='parent_transactions', lazy=True)
    
    def __repr__(self):
        return f"<Transaction {self.id} | Listing {self.listing_id} | Status {self.status}>"
