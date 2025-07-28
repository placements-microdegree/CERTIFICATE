from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/")
async def test_root():
    return {"message": "Vercel test endpoint working", "status": "ok"}

@app.get("/api/certificate/{cert_id}")
async def test_certificate(cert_id: str):
    # Simple test response
    return {
        "success": True,
        "certificate": {
            "id": cert_id,
            "recipient_name": "Test User",
            "course_name": "Test Course",
            "issue_date": "2025-07-28",
            "issuer": "Test Academy"
        }
    }
