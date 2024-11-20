from flask import Blueprint, request, jsonify
from app.models import Patient, MedicalRecord
from app.utils import allowed_file, process_file, validate_medical_data, calculate_statistics
from werkzeug.utils import secure_filename
import os
from flask import current_app
from datetime import datetime
from mongoengine.errors import ValidationError, DoesNotExist

main = Blueprint('main', __name__)

ALLOWED_EXTENSIONS = {'csv', 'xlsx', 'xls'}

@main.route('/patients', methods=['POST'])
def create_patient():
    try:
        data = request.json
        required_fields = ['name', 'age', 'gender']
        
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400
            
        patient = Patient(
            name=data['name'],
            age=data['age'],
            gender=data['gender']
        )
        patient.save()
        
        return jsonify({
            'message': 'Patient created successfully',
            'patient_id': str(patient.id)
        }), 201
        
    except ValidationError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500

@main.route('/patients/<patient_id>', methods=['GET'])
def get_patient(patient_id):
    try:
        patient = Patient.objects.get(id=patient_id)
        stats = calculate_statistics(patient.records)
        
        return jsonify({
            'patient': {
                'id': str(patient.id),
                'name': patient.name,
                'age': patient.age,
                'gender': patient.gender,
                'created_at': patient.created_at.isoformat(),
            },
            'statistics': stats
        }), 200
        
    except DoesNotExist:
        return jsonify({'error': 'Patient not found'}), 404
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500

@main.route('/patients', methods=['GET'])
def get_all_patients():
    try:
        patients = Patient.objects.all()
        return jsonify({
            'patients': [{
                'id': str(patient.id),
                'name': patient.name,
                'age': patient.age,
                'gender': patient.gender,
                'created_at': patient.created_at.isoformat(),
                'records_count': len(patient.records)
            } for patient in patients]
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500

@main.route('/patients/<patient_id>/records', methods=['POST'])
def upload_medical_records(patient_id):
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
            
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
            
        if not allowed_file(file.filename, ALLOWED_EXTENSIONS):
            return jsonify({'error': 'File type not allowed'}), 400
            
        patient = Patient.objects.get(id=patient_id)
        
        filepath = os.path.join(
            current_app.config['UPLOAD_FOLDER'],
            secure_filename(file.filename)
        )
        
        df = process_file(file, filepath)
        validate_medical_data(df)
        
        records_created = 0
        for _, row in df.iterrows():
            record = MedicalRecord(
                patient=patient,
                glucose=float(row['glucose']),
                blood_pressure=float(row['blood_pressure']),
                insulin=float(row['insulin']),
                bmi=float(row['bmi']),
                diabetes_pedigree=float(row['diabetes_pedigree']),
                result=bool(row['result'])
            )
            record.save()
            patient.records.append(record)
            records_created += 1
            
        patient.save()
        
        return jsonify({
            'message': 'Medical records uploaded successfully',
            'records_created': records_created
        }), 201
        
    except DoesNotExist:
        return jsonify({'error': 'Patient not found'}), 404
    except ValidationError as e:
        return jsonify({'error': str(e)}), 400
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500

@main.route('/patients/<patient_id>/records', methods=['GET'])
def get_patient_records(patient_id):
    try:
        patient = Patient.objects.get(id=patient_id)
        return jsonify({
            'records': [{
                'id': str(record.id),
                'glucose': record.glucose,
                'blood_pressure': record.blood_pressure,
                'insulin': record.insulin,
                'bmi': record.bmi,
                'diabetes_pedigree': record.diabetes_pedigree,
                'result': record.result,
                'created_at': record.created_at.isoformat()
            } for record in patient.records]
        }), 200
        
    except DoesNotExist:
        return jsonify({'error': 'Patient not found'}), 404
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500