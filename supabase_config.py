import os
from supabase import create_client, Client
from typing import Optional

# ✅ Use environment variables for Supabase credentials
SUPABASE_URL = os.getenv("SUPABASE_URL", "https://ppwdqxeiksycubxznhgi.supabase.co")
SUPABASE_KEY = os.getenv(
    "SUPABASE_KEY",
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBwd2RxeGVpa3N5Y3VieHpuaGdpIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTMyNjc2OTIsImV4cCI6MjA2ODg0MzY5Mn0.2I5onLomqWgjOW5W4OVPmk9rAIxAg63InltNrYPYbBw"
)

# Debug: confirm environment variables
print(f"[DEBUG] SUPABASE_URL: {SUPABASE_URL}")
print(f"[DEBUG] SUPABASE_KEY is {'set' if SUPABASE_KEY else 'MISSING'}")

# Create Supabase client
supabase: Optional[Client] = None
try:
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    print("✅ Supabase client initialized successfully")
except Exception as e:
    print(f"⚠️ Error initializing Supabase client: {e}")

TABLE_NAME = "certificate_users"  # Supabase table for issued certificates


def get_certificate_by_id(certificate_id: str):
    """
    Fetch a certificate by ID (case-insensitive).
    Returns dict with student_name, course_name, completion_date, certificate_id, certificate_url.
    """
    certificate_id = certificate_id.strip()
    print(f"[DEBUG] Looking for certificate_id (case-insensitive): {certificate_id}")

    try:
        # Case-insensitive search
        user_cert_response = (
            supabase.table(TABLE_NAME)
            .select("*")
            .ilike("certificate_id", certificate_id)
            .execute()
        )
        print(f"[DEBUG] Query result: {user_cert_response.data}")

        if not user_cert_response.data:
            print("[DEBUG] Certificate not found in certificate_users")
            return None

        user_cert = user_cert_response.data[0]
        return {
            "student_name": user_cert.get("student_name"),
            "course_name": user_cert.get("course_name"),
            "completion_date": user_cert.get("completion_date"),
            "certificate_id": user_cert.get("certificate_id"),
            "certificate_url": user_cert.get("certificate_url"),
            "issued_to": user_cert.get("student_name"),
        }
    except Exception as e:
        print(f"[ERROR] Failed to fetch certificate: {e}")
        return None


def get_all_certificates():
    """
    Fetch all certificates from certificate_users.
    """
    if not supabase:
        print("⚠️ Supabase client not initialized")
        return []

    try:
        response = supabase.table(TABLE_NAME).select("*").execute()
        print(f"[DEBUG] Total certificates fetched: {len(response.data)}")
        return response.data or []
    except Exception as e:
        print(f"[ERROR] Failed to fetch all certificates: {e}")
        return []


def add_sample_data():
    """
    Insert sample certificates for testing.
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
