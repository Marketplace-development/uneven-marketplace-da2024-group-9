from . import db

class Student(db.Model):
    __tablename__ = 'students'
    student_id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    listings = db.relationship('Listing', backref='student', lazy=True)
    reviews = db.relationship('Review', backref='student', lazy=True)
    transactions = db.relationship('Transaction', backref='student', lazy=True)

    # Methode om een account aan te maken
    @staticmethod
    def create_account(username, email, created_at):
        new_student = Student(username=username, email=email, created_at=created_at)
        db.session.add(new_student)
        db.session.commit()
        return new_student

    # Methode om een klus te plaatsen
    def place_job(self, name, description, picture, status):
        new_job = Listing(name=name, description=description, picture=picture, status=status, student=self)
        db.session.add(new_job)
        db.session.commit()
        return new_job

    # Methode om een klus te verwijderen
    def delete_job(self, listing_id):
        job = Listing.query.filter_by(listing_id=listing_id, student_id=self.student_id).first()
        if job:
            db.session.delete(job)
            db.session.commit()
            return f"Job {listing_id} deleted."
        return "Job not found."