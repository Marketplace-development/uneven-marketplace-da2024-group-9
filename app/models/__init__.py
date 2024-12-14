from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .Category import Category
from .Listing import Listing
from .Notification import Notification
from .Review import Review
from .Student import Student
from .Technician import Technician
from .Transaction import Transaction
from .User import User

__all__ = ["db", "Category", "Listing", "Notification", "Review", "Student", "Technician", "Student", "Transaction", "User"]
