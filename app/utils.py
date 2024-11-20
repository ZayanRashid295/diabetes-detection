import pandas as pd
import numpy as np
from werkzeug.utils import secure_filename
import os

def allowed_file(filename, allowed_extensions):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

def process_file(file, filepath):
    """Process uploaded file and return DataFrame"""
    filename = secure_filename(file.filename)
    
    try:
        file.save(filepath)
        
        if filename.endswith('.csv'):
            df = pd.read_csv(filepath)
        else:
            df = pd.read_excel(filepath)
            
        return df
        
    finally:
        if os.path.exists(filepath):
            os.remove(filepath)

def validate_medical_data(df):
    """Validate that DataFrame has required columns"""
    required_columns = ['glucose', 'blood_pressure', 'insulin', 'bmi', 'diabetes_pedigree', 'result']
    missing_columns = [col for col in required_columns if col not in df.columns]
    
    if missing_columns:
        raise ValueError(f"Missing required columns: {', '.join(missing_columns)}")
    
    return True

def calculate_statistics(records):
    """Calculate statistics from medical records"""
    if not records:
        return None
        
    stats = {
        'total_records': len(records),
        'glucose': {
            'mean': np.mean([r.glucose for r in records]),
            'min': min([r.glucose for r in records]),
            'max': max([r.glucose for r in records])
        },
        'blood_pressure': {
            'mean': np.mean([r.blood_pressure for r in records]),
            'min': min([r.blood_pressure for r in records]),
            'max': max([r.blood_pressure for r in records])
        },
        'insulin': {
            'mean': np.mean([r.insulin for r in records]),
            'min': min([r.insulin for r in records]),
            'max': max([r.insulin for r in records])
        },
        'bmi': {
            'mean': np.mean([r.bmi for r in records]),
            'min': min([r.bmi for r in records]),
            'max': max([r.bmi for r in records])
        },
        'diabetes_pedigree': {
            'mean': np.mean([r.diabetes_pedigree for r in records]),
            'min': min([r.diabetes_pedigree for r in records]),
            'max': max([r.diabetes_pedigree for r in records])
        },
        'positive_results': sum(1 for r in records if r.result),
        'negative_results': sum(1 for r in records if not r.result)
    }
    
    stats['positive_percentage'] = (stats['positive_results'] / stats['total_records']) * 100
    
    return stats