# import_data.py
import os
import sys
import csv

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

# Define the models (same as in app.py)
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

def import_monasteries():
    with app.app_context():
        # Clear existing data
        db.session.query(Monastery).delete()
        
        # Get the path to the CSV file
        csv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'monasteries.csv')
        
        with open(csv_path, 'r', encoding='utf-8-sig') as file:  # Use utf-8-sig to handle BOM
            csv_reader = csv.DictReader(file)
            
            # Debug: Print the fieldnames to see what columns are actually in the CSV
            print("CSV columns found:", csv_reader.fieldnames)
            
            for row_num, row in enumerate(csv_reader, 1):
                try:
                    # Handle empty values for numeric fields
                    latitude = float(row['Latitude']) if row['Latitude'] else None
                    longitude = float(row['Longitude']) if row['Longitude'] else None
                    
                    monastery = Monastery(
                        id=int(row['MonasteryID']),
                        name=row['Name'],
                        era=row['Era'],
                        description=row['Description'],
                        image_url=row['ImageURL'],
                        latitude=latitude,
                        longitude=longitude,
                        virtual_tour_url=row['VirtualTourURL'],
                        overview_text=row['OverviewText'],
                        narration_audio_url=row['NarrationAudioURL']
                    )
                    db.session.add(monastery)
                    print(f"Added monastery: {row['Name']}")
                    
                except KeyError as e:
                    print(f"Error in row {row_num}: Missing column {e}")
                    print(f"Row data: {row}")
                    return
                except Exception as e:
                    print(f"Error in row {row_num}: {e}")
                    print(f"Row data: {row}")
                    return
        
        db.session.commit()
        print("Data imported successfully!")

if __name__ == '__main__':
    import_monasteries()