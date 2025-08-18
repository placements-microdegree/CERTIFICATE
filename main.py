import os
from fastapi.templating import Jinja2Templates
from fastapi import Request, FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from supabase_config import (
    get_certificate_by_id,
    get_all_certificates,
    SUPABASE_URL,
    TABLE_NAME,
)

app = FastAPI(title="Certificate Verification API", version="1.0.1")
templates = Jinja2Templates(directory="templates")

# ---------------- CORS ---------------- #
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://cert.microdegree.in",
        "http://localhost:5000",
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- Static ---------------- #
app.mount("/static", StaticFiles(directory="static"), name="static")

# ---------------- ROUTES ---------------- #

@app.get("/", response_class=HTMLResponse)
async def read_root():
    """Serve index.html"""
    try:
        with open("index.html", "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error serving root page: {e}")


@app.get("/cert/{certificate_id}", response_class=HTMLResponse)
async def serve_certificate_page(request: Request, certificate_id: str):
    """Serve certificate display page (frontend)."""
    print(f"📩 [UI] /cert/{certificate_id} requested")
    cert_data = get_certificate_by_id(certificate_id)
    if not cert_data:
        print(f"❌ Certificate {certificate_id} not found in {TABLE_NAME}")
        return HTMLResponse(
            "<h2 style='text-align:center;color:#b91c1c;margin-top:3em'>Certificate Not Found</h2>",
            status_code=404,
        )

    return templates.TemplateResponse(
        "certificate.html",
        {
            "request": request,
            "student_name": cert_data.get("student_name"),
            "course_name": cert_data.get("course_name"),
            "completion_date": cert_data.get("completion_date"),
            "certificate_id": cert_data.get("certificate_id"),
        },
    )


@app.get("/api/certificate/{cert_id}")
async def get_certificate_api(cert_id: str):
    """Public API for certificate verification."""
    print(f"📩 [API] Verifying cert_id={cert_id}")
    cert_data = get_certificate_by_id(cert_id)
    if not cert_data:
        print(f"❌ [API] cert_id={cert_id} not found in {TABLE_NAME}")
        return JSONResponse(
            status_code=404, content={"success": False, "message": "Certificate not found"}
        )

    print(f"✅ [API] Found certificate {cert_id}")
    return {
        "success": True,
        "certificate": {
            "id": cert_data.get("certificate_id"),
            "recipient_name": cert_data.get("student_name"),
            "course_name": cert_data.get("course_name"),
            "issue_date": cert_data.get("completion_date"),
            "issuer": "MicroDegree Academy",
        },
    }


@app.get("/certificates")
async def get_all_certificates_route():
    """Return all certificates (for admin use)."""
    print("📩 [ADMIN] Fetching all certificates")
    certificates = get_all_certificates()
    return {"certificates": certificates}


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "message": "API is running"}


@app.get("/api/debug")
async def debug_certificates():
    """Debug Supabase connection + data preview."""
    print("🐞 [DEBUG] Fetching all certificates for inspection")
    certificates = get_all_certificates()
    return {
        "supabase_url": SUPABASE_URL,
        "table": TABLE_NAME,
        "count": len(certificates),
        "sample": certificates[:5],  # only first 5
    }


# ---------------- MAIN ENTRY ---------------- #
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
