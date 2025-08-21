import os
from fastapi import FastAPI, Request, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from supabase_config import get_certificate_by_id, get_all_certificates, supabase
from typing import Dict

# ----------------------
# App Setup
# ----------------------
app = FastAPI(title="Certificate Verification API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# ----------------------
# Helper Function
# ----------------------
def fetch_certificate(certificate_id: str) -> Dict:
    cert = get_certificate_by_id(certificate_id)
    if cert:
        return {"cert": cert, "status": "success"}
    return {"cert": None, "status": "failed"}

# ----------------------
# Frontend Pages
# ----------------------
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/cert/{certificate_id}")
async def certificate_page(request: Request, certificate_id: str):
    result = fetch_certificate(certificate_id)
    accept_header = request.headers.get("accept", "").lower()

    if "application/json" in accept_header:
        if result["status"] == "success":
            return JSONResponse({"success": True, "data": result["cert"]})
        return JSONResponse({"success": False, "message": "Certificate not found"}, status_code=404)

    if result["status"] == "success":
        return templates.TemplateResponse("certificate.html", {"request": request, "cert": result["cert"]})
    return templates.TemplateResponse("error.html", {"request": request, "message": "Certificate not found"})

@app.get("/verify/{certificate_id}", response_class=HTMLResponse)
async def verify_page(request: Request, certificate_id: str):
    result = fetch_certificate(certificate_id)
    return templates.TemplateResponse("result.html", {"request": request, **result})

# ----------------------
# API Routes
# ----------------------
@app.get("/api/certificates")
async def api_get_certificates():
    try:
        certificates = get_all_certificates()
        return {"success": True, "data": certificates}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/certificate/{certificate_id}")
async def api_get_certificate(certificate_id: str):
    result = fetch_certificate(certificate_id)
    if result["status"] == "success":
        return {"success": True, "data": result["cert"]}
    return JSONResponse({"success": False, "message": "Certificate not found"}, status_code=404)

@app.get("/api/verify/{certificate_id}")
async def api_verify_certificate(certificate_id: str):
    result = fetch_certificate(certificate_id)
    if result["status"] == "success":
        return {"success": True, "data": result["cert"]}
    return JSONResponse({"success": False, "message": "Certificate not found"}, status_code=404)

# ----------------------
# Debug Routes
# ----------------------
@app.get("/debug/supabase")
async def debug_supabase():
    if not supabase:
        return {"status": "error", "detail": "Supabase client not initialized"}
    try:
        response = supabase.table("certificates").select("*").limit(1).execute()
        return {"status": "connected", "sample": response.data}
    except Exception as e:
        return {"status": "error", "detail": str(e)}

@app.get("/debug/certificates")
async def debug_certificates(limit: int = 5, ids_only: bool = False):
    if not supabase:
        return {"success": False, "error": "Supabase client not initialized"}
    try:
        query = supabase.table("certificates").select("*" if not ids_only else "certificate_id")
        if limit:
            query = query.limit(limit)
        response = query.execute()
        return {"success": True, "data": response.data}
    except Exception as e:
        return {"success": False, "error": str(e)}
@app.get("/debug/supabase")
async def debug_supabase(certificate_id: str = None):
    """
    Test connection to Supabase and optionally fetch a certificate by ID.
    If certificate_id is provided, it performs a case-insensitive search.
    """
    if not supabase:
        return {"status": "error", "detail": "Supabase client not initialized"}

    try:
        # If no certificate_id is provided, fetch one record for testing
        if not certificate_id:
            response = supabase.table("certificates").select("*").limit(1).execute()
            return {"status": "connected", "sample": response.data}

        # Case-insensitive fetch by certificate_id
        certificate_id = certificate_id.strip().upper()
        response = supabase.table("certificates").select("*").ilike("certificate_id", certificate_id).execute()
        
        if response.data:
            return {"status": "connected", "certificate_found": True, "certificate": response.data[0]}
        return {"status": "connected", "certificate_found": False, "message": "Certificate not found"}

    except Exception as e:
        return {"status": "error", "detail": str(e)}
        @app.get("/debug/certificate_ids")
async def debug_certificate_ids():
    """
    Fetch all certificate IDs in both uppercase and lowercase for verification.
    """
    if not supabase:
        return {"success": False, "error": "Supabase client not initialized"}

    try:
        response = supabase.table("certificates").select("certificate_id").execute()
        if not response.data:
            return {"success": True, "certificate_ids": [], "message": "No certificates found"}

        ids_upper = [row["certificate_id"].upper() for row in response.data]
        ids_lower = [row["certificate_id"].lower() for row in response.data]

        return {
            "success": True,
            "certificate_ids_uppercase": ids_upper,
            "certificate_ids_lowercase": ids_lower,
            "total": len(ids_upper)
        }

    except Exception as e:
        return {"success": False, "error": str(e)}
@app.get("/debug/full")
async def debug_full():
    """
    Full debug: check Supabase connection, fetch sample, list all certificate IDs.
    """
    if not supabase:
        return {"success": False, "error": "Supabase client not initialized"}

    try:
        # Test connection & fetch one sample certificate
        sample_response = supabase.table("certificates").select("*").limit(1).execute()
        sample_cert = sample_response.data[0] if sample_response.data else None

        # Fetch all certificate IDs
        all_response = supabase.table("certificates").select("certificate_id").execute()
        ids_upper = [row["certificate_id"].upper() for row in all_response.data] if all_response.data else []
        ids_lower = [row["certificate_id"].lower() for row in all_response.data] if all_response.data else []

        return {
            "success": True,
            "sample_certificate": sample_cert,
            "certificate_ids_uppercase": ids_upper,
            "certificate_ids_lowercase": ids_lower,
            "total_certificates": len(ids_upper)
        }

    except Exception as e:
        return {"success": False, "error": str(e)}
