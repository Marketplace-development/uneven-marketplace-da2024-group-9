from flask import Flask
from .config import Config
from flask import Blueprint

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # importeer modellen & database instantie
    from .models import db, Category, Listing, Notification, Review, Student, Technician, User

    db.init_app(app)
    with app.app_context():
        db.create_all()  # Create sql tables for our data models

    from .routes import main
    app.register_blueprint(main)

    return app


