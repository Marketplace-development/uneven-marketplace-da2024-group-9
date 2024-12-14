from flask import Flask, render_template, request, redirect, session, flash, url_for
import os

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY')


# Simulated user data
users = {
    'technician1': 'technician',
    'student1': 'student'
}

# Dummy task data
tasks = [
    {
        'id': 'task1',
        'title': 'Fix a leaking tap',
        'category': 'Plumbing',
        'description': 'The tap in my bathroom is leaking.',
        'location': 'Antwerp',
        'address': 'Church Street 123',
        'photo': None,
        'username': 'student1',
        'assigned_technician': 'technician1',
        'completed': False
    }
]

# Chat data: key = tuple(sorted([sender, recipient]))
chats = {}

# Data opslag voor ratings van technici
technician_ratings = {
    'technician1': []  # Voorbeeld: lijst om ratings op te slaan
}

def calculate_average_rating(technician):
    ratings = technician_ratings.get(technician, [])
    if ratings:
        return round(sum(ratings) / len(ratings), 2)  # Gemiddelde berekening met afronding
    return "No ratings yet"

@app.route('/')
def home():
    return redirect('/login')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        user_type = users.get(username)

        if user_type:
            session['username'] = username
            session['user_type'] = user_type
            flash('Login successful!', 'success')
            return redirect(url_for('job_listing') if user_type == 'student' else url_for('technician_dashboard'))
        else:
            flash('Invalid username.', 'error')
    return render_template('login.html')



@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        user_type = request.form['user_type']

        if username in users:
            flash('Username already exists.', 'error')
            return redirect('/register')

        users[username] = user_type
        if user_type == 'technician':
            technician_ratings[username] = []  # Voeg nieuwe technieker toe
        print("DEBUG: Users dictionary:", users)
        print("DEBUG: Technician Ratings:", technician_ratings)

        flash('Registration successful. Please log in.', 'success')
        return redirect('/login')
    return render_template('register.html')


@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect('/login')


@app.route('/task/<string:task_id>')
def task_detail(task_id):
    task = next((t for t in tasks if t['id'] == task_id), None)
    if not task:
        return "Task not found", 404
    return render_template('task_detail.html', task=task)

@app.route('/send_message/<string:task_id>', methods=['POST'])
def send_message(task_id):
    if 'username' not in session:
        flash('You must log in to send messages.', 'error')
        return redirect('/login')

    sender = session['username']
    recipient = request.form.get('recipient')  # Ontvanger wordt expliciet ingegeven
    message = request.form.get('message')

    if not recipient:
        flash('Recipient is required.', 'error')
        return redirect(url_for('task_detail', task_id=task_id))

    # Voeg bericht toe aan de juiste chat
    if task_id not in chats:
        chats[task_id] = []

    chats[task_id].append({'sender': sender, 'recipient': recipient, 'message': message})
    flash('Message sent successfully!', 'success')

    return redirect(url_for('chats_page'))


@app.route('/chats')
def chats_page():
    if 'username' not in session:
        flash('You must log in to view chats.', 'error')
        return redirect('/login')

    username = session['username']
    user_chats = {}

    # Filter berichten waar de huidige gebruiker bij betrokken is
    for chat_key, messages in chats.items():
        # Controleer of de gebruiker betrokken is bij de berichten
        if any(msg['sender'] == username or msg.get('recipient') == username for msg in messages):
            partner = next(
                (msg['sender'] if msg['sender'] != username else msg.get('recipient', "Unknown")) 
                for msg in messages
            )
            user_chats[chat_key] = {
                'partner': partner,
                'messages': messages,
                'task_id': chat_key
            }

    # Geef calculate_average_rating door aan de template
    return render_template('chats.html', chats=user_chats, username=username, calculate_average_rating=calculate_average_rating)

@app.route('/job_listing')
def job_listing():
    if 'username' not in session or session['user_type'] != 'student':
        return redirect('/login')
    return render_template('job_listing.html', tasks=[t for t in tasks if not t['completed']], users=users)



@app.route('/technician_dashboard')
def technician_dashboard():
    if 'username' not in session or session['user_type'] != 'technician':
        flash('Unauthorized access!', 'error')
        return redirect('/login')

    # Filter taken die nog niet zijn gemarkeerd als "completed"
    available_tasks = [task for task in tasks if not task['completed']]
    return render_template(
        'technician_dashboard.html',
        tasks=available_tasks,
        calculate_average_rating=calculate_average_rating
    )




@app.route('/add_listing', methods=['GET', 'POST'])
def add_listing():
    if 'username' not in session or session['user_type'] != 'student':
        return redirect('/login')

    if request.method == 'POST':
        title = request.form['title']
        category = request.form['category']
        description = request.form['description']
        location = request.form['location']
        address = request.form['address']
        file = request.files.get('photo')

        photo_filename = None
        if file and '.' in file.filename:
            photo_filename = file.filename
            file.save(os.path.join('static/uploads', photo_filename))

        tasks.append({
            'id': f'task{len(tasks)+1}',
            'title': title,
            'category': category,
            'description': description,
            'location': location,
            'address': address,
            'photo': photo_filename,
            'username': session['username'],
            'assigned_technician': None,
            'completed': False
        })
        flash('Task added successfully.', 'success')
        return redirect('/job_listing')

    return render_template('add_listing.html')


@app.route('/profile')
def profile():
    if 'username' not in session:
        flash('You must log in to view your profile.', 'error')
        return redirect('/login')

    username = session['username']
    user_type = session['user_type']
    back_link = '/job_listing' if user_type == 'student' else '/technician_dashboard'

    return render_template('profile.html', username=username, user_type=user_type, back_link=back_link, calculate_average_rating=calculate_average_rating)


@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/remove_listing/<string:task_id>', methods=['POST'])
def remove_listing(task_id):
    if 'username' not in session or session['user_type'] != 'student':
        flash('Unauthorized access!', 'error')
        return redirect(url_for('job_listing'))

    # Verwijder taak indien het van de ingelogde student is
    global tasks
    tasks = [task for task in tasks if task['id'] != task_id or task['username'] != session['username']]

    flash('Listing removed successfully!', 'success')
    return redirect(url_for('job_listing'))



@app.route('/mark_completed_with_technician', methods=['POST'])
def mark_completed_with_technician():
    if 'username' not in session or session['user_type'] != 'student':
        flash('Unauthorized access!', 'error')
        return redirect(url_for('job_listing'))

    task_id = request.form.get('task_id')
    technician = request.form.get('technician')
    rating = request.form.get('rating')

    # Zoek de taak
    task = next((t for t in tasks if t['id'] == task_id), None)
    if task and task['username'] == session['username']:
        task['completed'] = True
        task['assigned_technician'] = technician

        # Sla de rating op voor de technieker
        if technician in technician_ratings:
            technician_ratings[technician].append(int(rating))
        else:
            technician_ratings[technician] = [int(rating)]

        flash(f'Task marked as completed and rated {rating} stars!', 'success')
    else:
        flash('Task not found or unauthorized action.', 'error')

    return redirect(url_for('job_listing'))


@app.route('/submit_feedback/<string:task_id>', methods=['POST'])
def submit_feedback(task_id):
    if 'username' not in session or session['user_type'] != 'student':
        flash('Unauthorized access!', 'error')
        return redirect(url_for('job_listing'))

    task = next((t for t in tasks if t['id'] == task_id), None)
    if task and task['username'] == session['username'] and task['completed']:
        rating = request.form['rating']
        comment = request.form['comment']
        task['feedback'] = {'rating': rating, 'comment': comment}
        flash('Feedback submitted successfully!', 'success')
    else:
        flash('Invalid operation.', 'error')

    return redirect(url_for('job_listing'))

if __name__ == '__main__':
    if not os.path.exists('static/uploads'):
        os.makedirs('static/uploads')
    app.run(debug=True)
