import os
from supabase import create_client, Client
from typing import Optional

# Set Supabase environment variables directly
if not os.getenv('SUPABASE_URL'):
    os.environ['SUPABASE_URL'] = 'https://wyszrjhxucxblyvhrktn.supabase.co'
if not os.getenv('SUPABASE_KEY'):
    os.environ['SUPABASE_KEY'] = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Ind5c3pyamh4dWN4Ymx5dmhya3RuIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTE4OTAzNzgsImV4cCI6MjA2NzQ2NjM3OH0.ZEPZIXsIVXbor8vY1uJM9VVVnody5iDJOgabbov14Xw'

# Supabase configuration
SUPABASE_URL = os.getenv('SUPABASE_URL', 'https://wyszrjhxucxblyvhrktn.supabase.co')
SUPABASE_KEY = os.getenv('SUPABASE_KEY', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Ind5c3pyamh4dWN4Ymx5dmhya3RuIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTE4OTAzNzgsImV4cCI6MjA2NzQ2NjM3OH0.ZEPZIXsIVXbor8vY1uJM9VVVnody5iDJOgabbov14Xw')

# Initialize Supabase client
try:
    supabase: Optional[Client] = create_client(SUPABASE_URL, SUPABASE_KEY)
    print(f"Supabase client initialized successfully with URL: {SUPABASE_URL}")
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