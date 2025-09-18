import os
from supabase import create_client, Client
from typing import Optional, List, Dict
from datetime import datetime

# ----------------------
# Supabase credentials

# Debug
# ----------------------
print(f"[DEBUG] SUPABASE_URL: {SUPABASE_URL}")
print(f"[DEBUG] SUPABASE_KEY is {'set' if SUPABASE_KEY else 'MISSING'}")

# ----------------------
# Supabase client
# ----------------------
supabase: Optional[Client] = None
try:
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    print("✅ Supabase client initialized successfully")
except Exception as e:
    print(f"⚠️ Error initializing Supabase client: {e}")

# ----------------------
# Table configuration
# ----------------------
TABLE_NAME = "certificates"  # ONLY use this table now

# ----------------------
# Date formatter
# ----------------------
def format_date(date_value: Optional[str]) -> Optional[str]:
    """
    Convert YYYY-MM-DD (from Supabase DATE) → DD/MM/YYYY
    """
    if not date_value:
        return None
    try:
        date_obj = datetime.strptime(str(date_value), "%Y-%m-%d")
        return date_obj.strftime("%d/%m/%Y")
    except Exception:
        return str(date_value)  # fallback

# ----------------------
# Functions
# ----------------------
def get_certificate_by_id(certificate_id: str) -> Optional[Dict]:
    """
    Fetch a certificate by certificate_id (case-insensitive)
    """
    if not supabase:
        print("⚠️ Supabase client not initialized")
        return None

    certificate_id = certificate_id.strip().upper()
    print(f"[DEBUG] Fetching certificate with ID: {certificate_id} from table: {TABLE_NAME}")
    
    try:
        response = supabase.table(TABLE_NAME).select("*").ilike("certificate_id", certificate_id).execute()
        if response.data:
            cert = response.data[0]
            return {
                "student_name": cert.get("student_name"),
                "course_name": cert.get("course_name"),
                "completion_date": format_date(cert.get("completion_date")),  # 👈 formatted here
                "certificate_id": cert.get("certificate_id"),
                "certificate_url": cert.get("certificate_url"),
                "issued_to": cert.get("student_name"),
            }
        return None
    except Exception as e:
        print(f"[ERROR] Failed to fetch certificate: {e}")
        return None

def get_all_certificates(limit: int = 20) -> List[Dict]:
    """
    Fetch all certificates from the certificates table
    """
    if not supabase:
        print("⚠️ Supabase client not initialized")
        return []
    print(f"[DEBUG] Fetching all certificates (limit={limit}) from table: {TABLE_NAME}")
    try:
        response = supabase.table(TABLE_NAME).select("*").limit(limit).execute()
        certificates = response.data or []
        # format dates for all
        for cert in certificates:
            cert["completion_date"] = format_date(cert.get("completion_date"))
        return certificates
    except Exception as e:
        print(f"[ERROR] Failed to fetch all certificates: {e}")
        return []

def add_sample_data():
    """
    Insert sample certificates for testing purposes
    """
    if not supabase:
        print("⚠️ Supabase client not initialized")
        return

    sample_data = [
        {
            "certificate_id": "MD-12345678",
            "student_name": "Habin Rahman",
            "course_name": "Advanced Python Programming",
            "completion_date": "2024-01-15",
            "certificate_url": "https://cert.microdegree.work/cert/MD-12345678",
        },
        {
            "certificate_id": "I1",
            "student_name": "HABIN",
            "course_name": "JAVA",
            "completion_date": "2025-08-05",
            "certificate_url": "https://cert.microdegree.work/cert/I1",
        },
    ]

    try:
        for cert in sample_data:
            supabase.table(TABLE_NAME).insert(cert).execute()
        print("✅ Sample data inserted successfully")
    except Exception as e:
        print(f"[ERROR] Failed to insert sample data: {e}")
