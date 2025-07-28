import os
from supabase import create_client, Client
from typing import Optional

# For production, set SUPABASE_URL and SUPABASE_KEY in your deployment platform's environment variables (Vercel/Render).
# The following fallback is for local development only.
if not os.getenv('SUPABASE_URL'):
    os.environ['SUPABASE_URL'] = 'https://wyszrjhxucxblyvhrktn.supabase.co'
if not os.getenv('SUPABASE_KEY'):
    os.environ['SUPABASE_KEY'] = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Ind5c3pyamh4dWN4Ymx5dmhya3RuIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTE4OTAzNzgsImV4cCI6MjA2NzQ2NjM3OH0.ZEPZIXsIVXbor8vY1uJM9VVVnody5iDJOgabbov14Xw'

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')

supabase: Optional[Client] = None
if SUPABASE_URL and SUPABASE_KEY:
    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        print(f"Supabase client initialized successfully with URL: {SUPABASE_URL}")
    except Exception as e:
        print(f"Warning: Could not initialize Supabase client: {e}")
        supabase = None
else:
    print("Warning: SUPABASE_URL or SUPABASE_KEY is not set. Supabase client not initialized.")

# Mock data for testing when database is empty
MOCK_CERTIFICATES = [
    {
        "certificate_id": "CERT-001",
        "student_name": "Habin Rahman",
        "course_name": "ReactJS with Supabase",
        "completion_date": "2025-07-07",
        "certificate_url": "https://cert.microdegree.work/cert/CERT-001"
    },
    {
        "certificate_id": "HR08",
        "student_name": "HABIN",
        "course_name": "PYTHON",
        "completion_date": "2025-07-11",
        "certificate_url": "https://cert.microdegree.work/cert/HR08"
    },
    {
        "certificate_id": "test123",
        "student_name": "Michael Chen",
        "course_name": "Data Science Essentials",
        "completion_date": "2024-03-10",
        "certificate_url": "https://cert.microdegree.work/cert/test123"
    },
    {
        "certificate_id": "CERT-002",
        "student_name": "Habin Rahman",
        "course_name": "FastAPI Advanced",
        "completion_date": "2025-07-08",
        "certificate_url": "https://cert.microdegree.work/cert/CERT-002"
    },
    {
        "certificate_id": "RK01",
        "student_name": "RAKESH",
        "course_name": "SQL",
        "completion_date": "2025-07-11",
        "certificate_url": "https://cert.microdegree.work/cert/RK01"
    },
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
    }
]

def get_certificate_by_id(certificate_id: str):
    """Get certificate data from Supabase by certificate ID"""
    global supabase
    
    if not supabase:
        print("Supabase client not initialized, using mock data")
        # Use mock data as fallback
        for cert in MOCK_CERTIFICATES:
            if cert['certificate_id'] == certificate_id:
                return {
                    "student_name": cert['student_name'],
                    "course": cert['course_name'],
                    "completion_date": cert['completion_date'],
                    "certificate_id": cert['certificate_id']
                }
        return None
    
    try:
        print(f"Attempting to fetch certificate {certificate_id} from Supabase...")
        response = supabase.table('certificates').select('*').eq('certificate_id', certificate_id).execute()
        print(f"Supabase response: {response}")
        
        if response.data and len(response.data) > 0:
            certificate = response.data[0]
            print(f"Found certificate in database: {certificate}")
            return {
                "student_name": certificate['student_name'],
                "course": certificate['course_name'],
                "completion_date": certificate['completion_date'],
                "certificate_id": certificate['certificate_id']
            }
        else:
            print(f"Certificate {certificate_id} not found in database")
            return None
    except Exception as e:
        print(f"Error fetching certificate from Supabase: {e}")
        print("Attempting to reconnect to Supabase...")
        
        # Try to reinitialize the Supabase client
        try:
            if SUPABASE_URL and SUPABASE_KEY:
                supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
                print("Supabase client reinitialized successfully")
            else:
                print("Cannot reconnect: SUPABASE_URL or SUPABASE_KEY is None")
                return None
            
            # Try the query again
            response = supabase.table('certificates').select('*').eq('certificate_id', certificate_id).execute()
            if response.data and len(response.data) > 0:
                certificate = response.data[0]
                return {
                    "student_name": certificate['student_name'],
                    "course": certificate['course_name'],
                    "completion_date": certificate['completion_date'],
                    "certificate_id": certificate['certificate_id']
                }
        except Exception as reconnect_error:
            print(f"Failed to reconnect to Supabase: {reconnect_error}")
        
        return None

def get_all_certificates():
    """Get all certificates from Supabase"""
    if not supabase:
        print("Supabase client not initialized, using mock data")
        return MOCK_CERTIFICATES
    
    try:
        response = supabase.table('certificates').select('*').execute()
        if response.data and len(response.data) > 0:
            return response.data
        else:
            # Return mock data if database is empty
            return MOCK_CERTIFICATES
    except Exception as e:
        print(f"Error fetching certificates: {e}")
        return MOCK_CERTIFICATES

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