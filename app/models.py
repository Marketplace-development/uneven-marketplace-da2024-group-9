from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'
    

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

# Tabel voor technici
class Technician(db.Model):
    __tablename__ = 'technicians'
    technician_id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, nullable=False)
    skills = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Float, nullable=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    transactions = db.relationship('Transaction', backref='technician', lazy=True)

    # Methode om een account aan te maken
    @staticmethod
    def create_account(username, email, skills, created_at):
        new_technician = Technician(username=username, email=email, skills=skills, created_at=created_at)
        db.session.add(new_technician)
        db.session.commit()
        return new_technician

# Tabel voor listings
class Listing(db.Model):
    __tablename__ = 'listings'
    listing_id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, nullable=False)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=False)
    picture = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(50), default='open')  # 'open', 'in progress', 'completed'


# Tabel voor transacties
class Transaction(db.Model):
    __tablename__ = 'transactions'
    transaction_id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(50), default='pending')  # 'pending', 'agreed', 'completed'
    amount = db.Column(db.Integer, nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('listings.listing_id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('students.student_id'), nullable=False)
    technician_id = db.Column(db.Integer, db.ForeignKey('technicians.technician_id'), nullable=False)

# Tabel voor reviews
class Review(db.Model):
    __tablename__ = 'reviews'
    review_id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text, nullable=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.student_id'), nullable=False)
    technician_id = db.Column(db.Integer, db.ForeignKey('technicians.technician_id'), nullable=False)

# Tabel voor notificaties
class Notification(db.Model):
    __tablename__ = 'notifications'
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, nullable=False)
    viewed = db.Column(db.Boolean, default=False)
    notification_id = db.Column(db.Integer, nullable=False)

# Tabel voor categorieën
class Category(db.Model):
    __tablename__ = 'categories'
    category_id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, nullable=False)
    name = db.Column(db.String(120), nullable=False)
    