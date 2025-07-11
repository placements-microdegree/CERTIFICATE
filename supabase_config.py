import os
from supabase import create_client, Client
from typing import Optional

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    try:
        load_dotenv(encoding='utf-8')
    except UnicodeDecodeError:
        # If .env file has encoding issues, skip it
        print("Warning: .env file has encoding issues, using environment variables directly")
except ImportError:
    print("Warning: python-dotenv not installed. Install with: pip install python-dotenv")

# Supabase configuration
SUPABASE_URL = os.getenv('SUPABASE_URL', 'your-supabase-url')
SUPABASE_KEY = os.getenv('SUPABASE_KEY', 'your-supabase-anon-key')

# Initialize Supabase client
try:
    supabase: Optional[Client] = create_client(SUPABASE_URL, SUPABASE_KEY)
except Exception as e:
    print(f"Warning: Could not initialize Supabase client: {e}")
    supabase = None

def get_certificate_by_id(certificate_id: str):
    """Get certificate data from Supabase by certificate ID"""
    if not supabase:
        print("Supabase client not initialized")
        return None
        
    try:
        response = supabase.table('certificates').select('*').eq('certificate_id', certificate_id).execute()
        
        if response.data and len(response.data) > 0:
            certificate = response.data[0]
            return {
                "student_name": certificate['student_name'],
                "course": certificate['course_name'],
                "completion_date": certificate['completion_date'],
                "certificate_id": certificate['certificate_id']
            }
        else:
            return None
    except Exception as e:
        print(f"Error fetching certificate: {e}")
        return None

def get_all_certificates():
    """Get all certificates from Supabase"""
    if not supabase:
        print("Supabase client not initialized")
        return []
        
    try:
        response = supabase.table('certificates').select('*').execute()
        return response.data
    except Exception as e:
        print(f"Error fetching certificates: {e}")
        return []

def add_sample_data():
    """Add sample certificate data to Supabase"""
    if not supabase:
        print("Supabase client not initialized")
        return
        
    sample_certificates = [
        {
            "certificate_id": "MD-12345678",
            "student_name": "Habin Rahman",
            "course_name": "Advanced Python Programming",
            "completion_date": "2024-01-15",
            "certificate_url": "https://cert.microdegree.work/cert/MD-12345678"
        },
        {
            "certificate_id": "MD-87654321",
            "student_name": "Sarah Johnson",
            "course_name": "Web Development Fundamentals",
            "completion_date": "2024-02-20",
            "certificate_url": "https://cert.microdegree.work/cert/MD-87654321"
        },
        {
            "certificate_id": "MD-11223344",
            "student_name": "Michael Chen",
            "course_name": "Data Science Essentials",
            "completion_date": "2024-03-10",
            "certificate_url": "https://cert.microdegree.work/cert/MD-11223344"
        }
    ]
    
    try:
        for cert in sample_certificates:
            supabase.table('certificates').insert(cert).execute()
        print("Sample data added successfully!")
    except Exception as e:
        print(f"Error adding sample data: {e}") 