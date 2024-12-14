from . import db

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