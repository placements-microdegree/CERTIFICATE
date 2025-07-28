from fastapi import FastAPI
from fastapi.responses import JSONResponse
import sys
import os

# Add the parent directory to the path so we can import from the root
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from supabase_config import get_certificate_by_id

app = FastAPI()

@app.get("/{cert_id:path}")
async def get_certificate(cert_id: str):
    """Get certificate data from Supabase by certificate ID"""
    try:
        certificate_data = get_certificate_by_id(cert_id)
        if certificate_data:
            return {"success": True, "certificate": {
                "id": certificate_data["certificate_id"],
                "recipient_name": certificate_data["student_name"],
                "course_name": certificate_data["course"],
                "issue_date": certificate_data["completion_date"],
                "issuer": "MicroDegree Academy"
            }}
        else:
            return {"success": False, "message": "Certificate not found"}
    except Exception as e:
        return JSONResponse(status_code=500, content={"success": False, "message": str(e)})
