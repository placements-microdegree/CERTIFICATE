import os
import logging
from supabase import create_client, Client
from typing import Optional, List, Dict

# ----------------------
# Logging setup
# ----------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ----------------------
# Supabase credentials
# ----------------------
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise EnvironmentError("Supabase URL and Key must be set in environment variables")

logger.info(f"Supabase URL set: {SUPABASE_URL}")
logger.info(f"Supabase Key is set: {'Yes' if SUPABASE_KEY else 'No'}")

# ----------------------
# Supabase client
# ----------------------
supabase: Optional[Client] = None
try:
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    logger.info("✅ Supabase client initialized successfully")
except Exception as e:
    logger.error(f"⚠️ Error initializing Supabase client: {e}")

# ----------------------
# Table configuration
# ----------------------
TABLE_NAME = "certificates"

# ----------------------
# Functions
# ----------------------
def get_certificate_by_id(certificate_id: str) -> Optional[Dict]:
    """
    Fetch a certificate by certificate_id (case-insensitive)
    """
    if not supabase:
        logger.warning("⚠️ Supabase client not initialized")
        return None

    certificate_id = certificate_id.strip().upper()
    try:
        response = (
            supabase.table(TABLE_NAME)
            .select("*")
            .ilike("certificate_id", certificate_id)
            .execute()
        )
        if response.data:
            cert = response.data[0]
            return {
                "student_name": cert.get("student_name"),
                "course_name": cert.get("course_name"),
                "completion_date": cert.get("completion_date"),
                "certificate_id": cert.get("certificate_id"),
                "certificate_url": cert.get("certificate_url"),
                "issued_to": cert.get("student_name"),
            }
        return None
    except Exception as e:
        logger.error(f"[ERROR] Failed to fetch certificate: {e}")
        return None

def get_all_certificates(limit: int = 20) -> List[Dict]:
    """
    Fetch all certificates from the certificates table
    """
    if not supabase:
        logger.warning("⚠️ Supabase client not initialized")
        return []

    try:
        response = supabase.table(TABLE_NAME).select("*").limit(limit).execute()
        return response.data or []
    except Exception as e:
        logger.error(f"[ERROR] Failed to fetch all certificates: {e}")
        return []

def add_sample_data():
    """
    Insert sample certificates for testing purposes
    """
    if not supabase:
        logger.warning("⚠️ Supabase client not initialized")
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
        logger.info("✅ Sample data inserted successfully")
    except Exception as e:
        logger.error(f"[ERROR] Failed to insert sample data: {e}")
