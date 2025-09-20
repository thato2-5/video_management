from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    original_filename = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(500), nullable=False)
    file_size = db.Column(db.Integer, nullable=False)
    duration = db.Column(db.Float, nullable=True)
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)
    selected = db.Column(db.Boolean, default=False)
    
    def __repr__(self):
        return f'<Video {self.original_filename}>'

