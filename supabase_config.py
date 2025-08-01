import os
from supabase import create_client, Client
from typing import Optional

# ✅ Use your new Supabase credentials
if not os.getenv("SUPABASE_URL"):
    os.environ["SUPABASE_URL"] = "https://ppwdqxeiksycubxznhgi.supabase.co"
if not os.getenv("SUPABASE_KEY"):
    os.environ["SUPABASE_KEY"] = (
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBwd2RxeGVpa3N5Y3VieHpuaGdpIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTMyNjc2OTIsImV4cCI6MjA2ODg0MzY5Mn0.2I5onLomqWgjOW5W4OVPmk9rAIxAg63InltNrYPYbBw"
    )

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Optional[Client] = None
if SUPABASE_URL and SUPABASE_KEY:
    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        print(f"✅ Supabase client initialized with URL: {SUPABASE_URL}")
    except Exception as e:
        print(f"⚠️ Error initializing Supabase client: {e}")
        supabase = None
else:
    print("⚠️ SUPABASE_URL or SUPABASE_KEY is not set.")

# ✅ Use new table name: certificate_users
def get_certificate_by_id(certificate_id: str):
    if not supabase:
        print("Supabase not initialized.")
        return None

    try:
        response = (
            supabase.table("certificate_users")
            .select("*")
            .eq("certificate_id", certificate_id.upper())
            .execute()
        )

        if response.data and len(response.data) > 0:
            cert = response.data[0]
            return {
                "student_name": cert["student_name"],
                "course": cert["course_name"],
                "completion_date": cert["completion_date"],
                "certificate_id": cert["certificate_id"],
                "certificate_url": cert.get("certificate_url", "")
            }
        else:
            return None
    except Exception as e:
        print(f"Error fetching certificate: {e}")
        return None


def get_all_certificates():
    if not supabase:
        print("Supabase not initialized.")
        return []

    try:
        response = supabase.table("certificate_users").select("*").execute()
        return response.data or []
    except Exception as e:
        print(f"Error fetching all certificates: {e}")
        return []


def add_sample_data():
    if not supabase:
        print("Supabase not initialized.")
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
            "certificate_id": "HR08",
            "student_name": "HABIN",
            "course_name": "PYTHON",
            "completion_date": "2025-07-11",
            "certificate_url": "https://cert.microdegree.work/cert/HR08",
        },
    ]

    try:
        for cert in sample_data:
            supabase.table("certificate_users").insert(cert).execute()
        print("✅ Sample data inserted into certificate_users.")
    except Exception as e:
        print(f"Error inserting sample data: {e}")
