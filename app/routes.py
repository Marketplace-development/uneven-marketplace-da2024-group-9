from flask import render_template, request, redirect, url_for, session
from flask import Blueprint

# In-memory gebruikersdata
users = set()

main = Blueprint('main', __name__)

@main.route('/')
def index():
    """Homepagina."""
    # 1. Check of user ingelogd is via session
    # 2. niet ingelogd - redirect naar login pagina
    # 3. Wel ingelogd? Toon home pagina (return template in deze functie)
    print(session)


    username = session.get('username')
    if username:
        return f"Welcome, {username}!"
    return "You are not logged in. Please login or register."

@main.route('/login', methods=['GET', 'POST'])
def login():
    """Loginpagina."""
    if request.method == 'POST':
        username = request.form.get('username')
        if username in users:
            session['username'] = username
            return redirect(url_for('index'))
        else:
            return "User not found. Please register first.", 401
    return render_template('login.html')  # Verwijzing naar login.html

@main.route('/register', methods=['GET', 'POST'])
def register():
    """Registerpagina."""
    if request.method == 'POST':
        username = request.form.get('username')
        if username not in users:
            users.add(username)
            session['username'] = username
            return redirect(url_for('index'))
        else:
            return "User already exists. Please login.", 400
    return render_template('register.html')  # Verwijzing naar register.html

@main.route('/logout', methods=['POST'])
def logout():
    """Uitloggen."""
    session.pop('username', None)
    return redirect(url_for('index'))

@main.route('/identify_role', methods=['POST'])
def identify_role():
    """Identify Role"""
    return 'ADMIN'

@main.route('/overview')
def overview():
    db

@main.route('/listing')  # Lowercase route
def listing():
    """Render the listing page."""
    return render_template('listing.html')  # Match template filename
