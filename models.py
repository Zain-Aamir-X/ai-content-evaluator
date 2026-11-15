from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Content(db.Model):
    __tablename__ = 'content'
    id = db.Column(db.Integer, primary_key=True)
    text_data = db.Column(db.Text, nullable=False)
    source_type = db.Column(db.String(50)) # 'File' or 'Text'
    submission_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship to the report
    report = db.relationship('EvaluationReport', backref='content', uselist=False)

class EvaluationReport(db.Model):
    __tablename__ = 'evaluation_reports'
    id = db.Column(db.Integer, primary_key=True)
    content_id = db.Column(db.Integer, db.ForeignKey('content.id'), nullable=False)
    
    # Labels (Appropriate, Borderline, Inappropriate)
    linguistic_label = db.Column(db.String(20))
    cognitive_label = db.Column(db.String(20))
    socio_emotional_label = db.Column(db.String(20))
    moral_label = db.Column(db.String(20))
    
    # Feedback for the teacher
    linguistic_feedback = db.Column(db.Text)
    cognitive_feedback = db.Column(db.Text)
    socio_emotional_feedback = db.Column(db.Text)
    moral_feedback = db.Column(db.Text)
    
    date_generated = db.Column(db.DateTime, default=datetime.utcnow)