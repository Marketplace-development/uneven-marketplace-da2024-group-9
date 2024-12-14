from . import db

class Transaction(db.Model):
    __tablename__ = 'transactions'
    transaction_id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(50), default='pending')  # 'pending', 'agreed', 'completed'
    amount = db.Column(db.Integer, nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('listings.listing_id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('students.student_id'), nullable=False)
    technician_id = db.Column(db.Integer, db.ForeignKey('technicians.technician_id'), nullable=False)