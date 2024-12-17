from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from dotenv import load_dotenv
load_dotenv()


db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__, static_url_path='/static', static_folder='static')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres.eupxuakhfykloqrojzbr:peZGTKWfDmLCcSWn@aws-0-eu-central-1.pooler.supabase.com:6543/postgres'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev_key')  # Zet een veilige sleutel in productie
    UPLOAD_FOLDER = os.path.join(app.static_folder, 'uploads')
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    db.init_app(app)
    migrate.init_app(app, db)

    from app.models.student import Student
    from app.models.technician import Technician
    from app.models.listing import Listing
    

    from app.routes import init_routes
    init_routes(app)

    return app
