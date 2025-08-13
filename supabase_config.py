import os
from supabase import create_client, Client

# Mock fallback data if Supabase is down or cert not found
MOCK_CERTIFICATES = [
    {
        "certificate_id": "MD-12345678",
        "name": "John Doe",
        "course": "Full Stack Development",
        "date": "2025-08-01",
        "status": "Verified"
    },
    {
        "certificate_id": "MD-87654321",
        "name": "Jane Smith",
        "course": "Data Science",
        "date": "2025-07-20",
        "status": "Verified"
    }
]

# Load environment variables
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = None
if SUPABASE_URL and SUPABASE_KEY:
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
else:
    print("⚠️ Warning: Missing SUPABASE_URL or SUPABASE_KEY. Running in fallback mode.")

def get_certificate_by_id(cert_id: str):
    """
    Fetch certificate details from Supabase by certificate ID.
    Falls back to mock data if Supabase is unavailable or fails.
    """
    # Try Supabase first
    if supabase:
        try:
            response = (
                supabase.table("certificates")
                .select("*")
                .eq("certificate_id", cert_id)
                .execute()
            )
            if response.data:
                return response.data[0]
        except Exception as e:
            print(f"❌ Error fetching certificate {cert_id} from Supabase: {e}")

    # Fallback to mock data
    print(f"ℹ️ Using fallback data for certificate: {cert_id}")
    for cert in MOCK_CERTIFICATES:
        if cert["certificate_id"] == cert_id:
            return cert

    return None
