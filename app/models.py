from app.database import db
from datetime import datetime

class Patient(db.Document):
    name = db.StringField(required=True)
    age = db.IntField(required=True)
    gender = db.StringField(required=True)
    created_at = db.DateTimeField(default=datetime.utcnow)
    records = db.ListField(db.ReferenceField('MedicalRecord'))
    
    meta = {
        'collection': 'patients',
        'ordering': ['-created_at']
    }

class MedicalRecord(db.Document):
    patient = db.ReferenceField(Patient, required=True)
    glucose = db.FloatField(required=True)
    blood_pressure = db.FloatField(required=True)
    insulin = db.FloatField(required=True)
    bmi = db.FloatField(required=True)
    diabetes_pedigree = db.FloatField(required=True)
    result = db.BooleanField(required=True)
    created_at = db.DateTimeField(default=datetime.utcnow)
    
    meta = {
        'collection': 'medical_records',
        'ordering': ['-created_at']
    }