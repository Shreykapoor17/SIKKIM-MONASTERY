# sih-backend/create_db.py
import os
import sys

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import quote_plus

# Create a minimal Flask app for database operations
app = Flask(__name__)

# Database Configuration (same as in app.py)
encoded_password = quote_plus("Prat#514")
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://postgres:{encoded_password}@localhost:5432/monastery_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define ALL the models
class Monastery(db.Model):
    __tablename__ = 'monastery'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    era = db.Column(db.String(50))
    description = db.Column(db.Text)
    image_url = db.Column(db.String(255))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    virtual_tour_url = db.Column(db.String(255))
    overview_text = db.Column(db.Text)
    narration_audio_url = db.Column(db.String(255))

class ArchiveItem(db.Model):
    __tablename__ = 'archive_item'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    document_type = db.Column(db.String(50))
    file_url = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    monastery_id = db.Column(db.Integer, db.ForeignKey('monastery.id'))
    monastery = db.relationship('Monastery')

# vvvvvvvvvv NEW MODEL DEFINITION ADDED HERE vvvvvvvvvv
class NearbyAttraction(db.Model):
    __tablename__ = 'nearby_attraction'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    attraction_type = db.Column(db.String(100))
    description = db.Column(db.Text)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    monastery_id = db.Column(db.Integer, db.ForeignKey('monastery.id'), nullable=False)
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

# Create the database tables
with app.app_context():
    db.drop_all() # Drop all tables first for a clean slate
    db.create_all() # Create all tables, including the new one
    print("Database tables dropped and recreated successfully!")