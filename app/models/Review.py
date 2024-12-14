from . import db

class Review(db.Model):
    __tablename__ = 'reviews'
    review_id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text, nullable=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.student_id'), nullable=False)
    technician_id = db.Column(db.Integer, db.ForeignKey('technicians.technician_id'), nullable=False)