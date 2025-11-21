"""
Flask Application Initialization
No SQLAlchemy - using raw Oracle database connections
"""
from flask import Flask
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
import os

# Load environment variables first
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Secret key
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'supersecretkey')

# Initialize extensions
bcrypt = Bcrypt(app)

# Import models (now just helper functions)
from app.models.user import User, Transaction, Beneficiary, BillPayment, insert_hyphens

# Import routes (after models are defined)
from app.routes.root import *
from app.routes.user import *

# Add filter
app.jinja_env.filters['insert_hyphens'] = insert_hyphens

# Verify database connection on startup
from app.database import db
try:
    if db.verify_connection():
        print("Database connection verified successfully")
    else:
        print("Warning: Database connection verification failed")
except Exception as e:
    print(f"Warning: Could not verify database connection: {str(e)}")
