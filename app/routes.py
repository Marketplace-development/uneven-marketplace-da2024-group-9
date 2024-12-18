from flask import render_template, redirect, url_for, flash, request, session, jsonify, Response
from app import db
from app.models.student import Student
from app.models.technician import Technician
from app.models.listing import Listing
from app.models.chat import ChatMessage
from app.models.transaction import Transaction
from werkzeug.utils import secure_filename
import os
from datetime import datetime
from sqlalchemy.sql import func
from sqlalchemy.sql import func



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

            if student:
                session['username'] = student.username
                flash('Login successful!', 'success')
                return redirect(url_for('job_listing'))
            elif technician:
                session['username'] = technician.username
                flash('Login successful!', 'success')
                return redirect(url_for('technician_dashboard'))
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
    @app.route('/job_listing')
    def job_listing():
        # Logica om job listings op te halen
        technicians = Technician.query.all()
        tasks = Listing.query.outerjoin(Transaction, Listing.id == Transaction.listing_id).filter(
            (Transaction.status != "completed") | (Transaction.status == None)
        ).all()
        for task in tasks:
         print(task.photo)
        
        return render_template('job_listing.html', tasks=tasks, technicians = technicians)
    
    @app.route('/technician_dashboard')
    def technician_dashboard():
        tasks = Listing.query.outerjoin(Transaction, Listing.id == Transaction.listing_id).filter(
            (Transaction.status != "completed") | (Transaction.status == None)
        ).all()
        return render_template('technician_dashboard.html', tasks=tasks)
    
    @app.route('/add_listing', methods=['GET', 'POST'])
    def add_listing():
        avg_price = None

        # Handle POST Request - Nieuwe Listing Toevoegen
        if request.method == 'POST':
            title = request.form['title']
            category = request.form['category']
            description = request.form['description']
            location = request.form['location']
            address = request.form['address']
            price = float(request.form['price']) if request.form['price'] else None
            photo = request.files['photo']

            photo_data = None
            mime_type = None

            if photo and photo.filename != '':
                photo_data = photo.read()  # Lees de foto als binary data
                mime_type = photo.mimetype

            # Voeg de nieuwe listing toe
            new_listing = Listing(
                title=title,
                category=category,
                description=description,
                location=location,
                address=address,
                price=price,
                photo=photo_data,
                mime_type=mime_type,
                username=session.get('username')  # Huidige gebruiker
            )
            db.session.add(new_listing)
            db.session.commit()

            flash('Listing successfully added!', 'success')
            return redirect(url_for('job_listing'))

        # Handle AJAX-aanroep voor gemiddelde prijs
        if request.args.get('category'):
            category = request.args.get('category')
            avg_price = db.session.query(func.avg(Transaction.price)).join(Listing).filter(
                Listing.category == category, Transaction.status == "completed"
            ).scalar()
            return jsonify({'avg_price': round(avg_price, 2) if avg_price else 'N/A'})

        # Render de pagina voor GET Request (zonder AJAX)
        return render_template('add_listing.html', avg_price=avg_price)

    @app.route('/image/<int:listing_id>')
    def get_image(listing_id):
        listing = Listing.query.get_or_404(listing_id)
        if not listing.photo:
            return '', 404  # Geen afbeelding gevonden
        return Response(listing.photo, mimetype=listing.mime_type)

    @app.route('/chats')
    def chats():
        if 'username' not in session:
            flash("You must be logged in to view chats.", "error")
            return redirect(url_for('login'))
        
        username = session['username']

        # Bepaal het user_type
        student = Student.query.filter_by(username=username).first()
        technician = Technician.query.filter_by(username=username).first()

        if student:
            user_type = 'student'
        elif technician:
            user_type = 'technician'
        else:
            user_type = 'unknown'

        # Haal alle unieke chats voor de huidige gebruiker
        partners = db.session.query(
            ChatMessage.sender_username, ChatMessage.receiver_username
        ).filter(
            (ChatMessage.sender_username == username) | (ChatMessage.receiver_username == username)
        ).distinct().all()

        chats = {}
        for sender, receiver in partners:
            partner = receiver if sender == username else sender
            messages = ChatMessage.query.filter(
                ((ChatMessage.sender_username == username) & (ChatMessage.receiver_username == partner)) |
                ((ChatMessage.sender_username == partner) & (ChatMessage.receiver_username == username))
            ).order_by(ChatMessage.timestamp.asc()).all()
            
            # Haal de rating en rating_count op voor de technician
            technician_rating = None
            technician_rating_count = None
            technician = Technician.query.filter_by(username=partner).first()
            if technician:
                technician_rating = round(technician.rating, 2) if technician.rating else None  # Directe toegang tot de rating
                technician_rating_count = technician.rating_count  # Directe toegang tot rating_count
            
            chats[partner] = {
                'partner': partner,
                'messages': messages,
                'rating': technician_rating,
                'rating_count': technician_rating_count
            }

        # Voeg user_type toe aan de render_template
        return render_template('chat.html', chats=chats, username=username, user_type=user_type)


   
    @app.route('/send_message', methods=['POST'])
    def send_message():
        recipient = request.form.get('recipient')
        message = request.form.get('message')

        new_message = ChatMessage(
            sender_username=session['username'],
            receiver_username=recipient,
            message=message,
            timestamp=datetime.now()
        )
        db.session.add(new_message)
        db.session.commit()

        flash('Message sent successfully!', 'success')
        return redirect(url_for('chats'))




    @app.route('/task_detail/<int:task_id>', methods=['GET', 'POST'])
    def task_detail(task_id):
        if 'username' not in session:
            flash("You must be logged in to view this page.", "error")
            return redirect(url_for('login'))
        
        # Haal taakdetails op uit de database
        task = Listing.query.get_or_404(task_id)
        transaction = Transaction.query.filter_by(listing_id=task_id).first()
        if request.method == 'POST':
            sender = session['username']
            recipient = task.username
            message = request.form['message']

            # Sla het bericht op in de database
            new_message = ChatMessage(
                sender_username=sender,
                receiver_username=recipient,
                message=message
            )
            db.session.add(new_message)
            db.session.commit()
            flash("Message sent successfully!", "success")
            return redirect(url_for('task_detail', task_id=task_id))

        return render_template('task_detail.html', task=task, transaction = transaction)
    
    

    @app.route('/profile')
    def profile():
        # Haal de huidige gebruiker op uit de sessie
        username = session.get('username')
        if not username:
            return redirect(url_for('login'))  # Gebruiker moet ingelogd zijn

        # Controleer of de gebruiker een student is
        student = Student.query.filter_by(username=username).first()
        if student:
            user_type = 'student'
            return render_template('profile.html',
                                username=student.username,
                                user_type=user_type,
                                back_link=url_for('job_listing'))

        # Controleer of de gebruiker een technieker is
        technician = Technician.query.filter_by(username=username).first()
        if technician:
            user_type = 'technician'
            average_rating = round(technician.rating, 2) if technician.rating_count > 0 else 'No ratings yet'
            return render_template('profile.html',
                                username=technician.username,
                                user_type=user_type,
                                average_rating=average_rating,
                                back_link=url_for('technician_dashboard'))

        # Als de gebruiker niet in een van de tabellen staat, log uit
        return redirect(url_for('logout'))
    
    @app.route('/logout')
    def logout():
        session.clear()  # Leeg de sessie om de gebruiker uit te loggen
        return redirect(url_for('login'))
    
    @app.route('/contact')
    def contact():
        return render_template('contact.html')
    
    @app.route('/get_avg_price', methods=['POST'])
    def get_avg_price():
        category = request.json.get('category')

        # Bereken gemiddelde prijs van alle transacties met die categorie
        avg_price = db.session.query(db.func.avg(Transaction.price)).join(Listing).filter(Listing.category == category).scalar()

        return {'avg_price': round(avg_price, 2) if avg_price else 0}

    
    @app.route('/create_transaction/<int:listing_id>', methods=['POST'])
    def create_transaction(listing_id):
        if 'username' not in session:
            flash("You must be logged in to perform this action.", "error")
            return redirect(url_for('login'))

        technician_username = session['username']
        price = request.form['price']  # Prijs wordt opgegeven bij aanmaak

        # Controleer of listing bestaat
        listing = Listing.query.get_or_404(listing_id)

        # Maak nieuwe transactie
        new_transaction = Transaction(
            listing_id=listing.id,
            student_username=listing.username,  # Wie de taak postte
            technician_username=technician_username,
            price=float(price),  # Zorg dat de prijs een float is
            status="pending"
        )
        db.session.add(new_transaction)
        db.session.commit()

        flash("Transaction created successfully!", "success")
        return redirect(url_for('technician_dashboard'))
    
    @app.route('/remove_listing/<int:task_id>', methods=['POST'])
    def remove_listing(task_id):
        listing = Listing.query.get(task_id)
        if listing:
            db.session.delete(listing)
            db.session.commit()
            flash('Listing successfully removed!', 'success')
        else:
            flash('Listing not found!', 'error')
        return redirect(url_for('job_listing'))
    
    @app.route('/mark_completed_with_technician/<int:task_id>', methods=['POST'])
    def mark_completed_with_technician(task_id):
        technician_username = request.form['technician']
        rating = int(request.form['rating'])

        listing = Listing.query.get_or_404(task_id)
        price = listing.price
        # Zoek of er al een transactie bestaat, zo niet, maak er een aan
        transaction = Transaction.query.filter_by(listing_id=task_id).first()
        if not transaction:
            transaction = Transaction(
                listing_id=task_id,
                student_username=session['username'],  # Degene die de taak aanmaakte
                technician_username=technician_username,
                price=price,  # Geen prijs nodig, wordt apart beheerd
                status="completed"
            )
            db.session.add(transaction)
        else:
            transaction.status = "completed"
            transaction.price = price

        # Update de rating van de technician
        technician = Technician.query.filter_by(username=technician_username).first()
        if technician:
            technician.rating_count += 1
            technician.rating = round(((technician.rating * (technician.rating_count - 1)) + rating) / technician.rating_count, 2)
        
       

        
        db.session.commit()
        flash("Task marked as completed!", "success")
        return redirect(url_for('job_listing'))



