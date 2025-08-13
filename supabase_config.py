import os
from supabase import create_client, Client

# Get environment variables
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Debug: log environment variable presence (not the key itself)
print(f"[DEBUG] Using SUPABASE_URL: {SUPABASE_URL}")
print(f"[DEBUG] SUPABASE_KEY is {'set' if SUPABASE_KEY else 'MISSING'}")

# Create client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

TABLE_NAME = "certificates"  # Ensure this matches your Supabase table exactly
COLUMN_NAME = "certificate_id"  # Ensure this matches your Supabase column name exactly


def get_certificate_by_id(certificate_id: str):
    """
    Fetch a certificate from Supabase by its certificate_id.
    """
    try:
        # Debug: Show the ID we're searching for
        print(f"[DEBUG] Querying certificate with ID: '{certificate_id}'")

        # Strip spaces & make sure ID is exact
        certificate_id = certificate_id.strip()

        # Query Supabase
        response = (
            supabase.table(TABLE_NAME)
            .select("*")
            .eq(COLUMN_NAME, certificate_id)
            .execute()
        )

        # Debug: Print raw response
        print(f"[DEBUG] Supabase raw data: {response.data}")

        if response.data:
            return response.data[0]  # Return the first matching certificate
        else:
            print("[DEBUG] No matching certificate found in Supabase.")
            return None

    except Exception as e:
        print(f"[ERROR] Failed to fetch certificate: {e}")
        return None
