from flask import render_template, redirect, url_for, flash, request, session, jsonify
from app import db
from app.models.student import Student
from app.models.technician import Technician
def init_routes(app):
    @app.route('/')
    def home():
        return redirect(url_for('login'))

    
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form['username']
            # Simuleer validatie voor studenten en technici
            student = Student.query.filter_by(username=username).first()
            technician = Technician.query.filter_by(username=username).first()

            if student or technician:
                session['username'] = username
                flash('Login successful!', 'success')
                return redirect(url_for('job_listing'))
            else:
                flash('Invalid username. Please try again.', 'error')
        return render_template('login.html')
    
    @app.route("/register", methods=["GET", "POST"])
    def register():
        if request.method == 'POST':
            try:
                # Data ophalen uit formulier
                username = request.form['username']
                first_name = request.form['firstname']
                last_name = request.form['lastname']
                email = request.form['email']
                phone_number = request.form['phone']
                role = request.form['user_type']

                print(f"Received data - Username: {username}, Role: {role}")  # Debugging

                # Validatie voor duplicate gebruikers
                if role == 'student':
                    if Student.query.filter_by(username=username).first():
                        flash('Student username already exists!', 'error')
                        return redirect(url_for('register'))
                    new_user = Student(username=username, first_name=first_name, last_name=last_name, email=email, phone_number=phone_number)
                elif role == 'technician':
                    if Technician.query.filter_by(username=username).first():
                        flash('Technician username already exists!', 'error')
                        return redirect(url_for('register'))
                    new_user = Technician(username=username, first_name=first_name, last_name=last_name, email=email, phone_number=phone_number)
                else:
                    flash('Invalid role selected!', 'error')
                    return redirect(url_for('register'))

                # Toevoegen aan database
                db.session.add(new_user)
                db.session.commit()
                flash('Registration successful! Please login.', 'success')
                return redirect(url_for('login'))
            
            except Exception as e:
                db.session.rollback()  # Zorg dat er geen corrupte transacties ontstaan
                print(f"Error during registration: {e}")  # Log fout
                flash('An error occurred during registration.', 'error')
                return redirect(url_for('register'))

        return render_template('register.html')



