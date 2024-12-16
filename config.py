
import os
from dotenv import load_dotenv

load_dotenv()  # Zorg ervoor dat je .env wordt geladen

SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
SQLALCHEMY_TRACK_MODIFICATIONS = False

