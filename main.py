import os
from fastapi import FastAPI, Request, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse, FileResponse
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
    certificate_id = certificate_id.strip().upper()
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
# Single Download Route
# ----------------------
@app.get("/api/certificate/{certificate_id}/download")
async def download_certificate(certificate_id: str):
    result = fetch_certificate(certificate_id)
    if result["status"] == "success":
        file_path = os.path.join("static", "certificates", f"{certificate_id}.pdf")
        if os.path.exists(file_path):
            return FileResponse(path=file_path, filename=f"{certificate_id}.pdf", media_type='application/pdf')
        else:
            return JSONResponse({"success": False, "message": "Certificate file not found"}, status_code=404)
    return JSONResponse({"success": False, "message": "Certificate not found"}, status_code=404)

# ----------------------
# Debug Routes
# ----------------------
@app.get("/debug/supabase")
async def debug_supabase(certificate_id: str = None):
    if not supabase:
        return {"status": "error", "detail": "Supabase client not initialized"}
    try:
        if not certificate_id:
            response = supabase.table("certificates").select("*").limit(1).execute()
            return {"status": "connected", "sample": response.data}

        certificate_id = certificate_id.strip().upper()
        response = supabase.table("certificates").select("*").ilike("certificate_id", certificate_id).execute()
        if response.data:
            return {"status": "connected", "certificate_found": True, "certificate": response.data[0]}
        return {"status": "connected", "certificate_found": False, "message": "Certificate not found"}
    except Exception as e:
        return {"status": "error", "detail": str(e)}

@app.get("/debug/certificate_ids")
async def debug_certificate_ids():
    if not supabase:
        return {"success": False, "error": "Supabase client not initialized"}
    try:
        response = supabase.table("certificates").select("certificate_id").execute()
        ids_upper = [row["certificate_id"].upper() for row in response.data] if response.data else []
        ids_lower = [row["certificate_id"].lower() for row in response.data] if response.data else []
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
    if not supabase:
        return {"success": False, "error": "Supabase client not initialized"}
    try:
        sample_response = supabase.table("certificates").select("*").limit(1).execute()
        sample_cert = sample_response.data[0] if sample_response.data else None

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
@app.get("/cert/{cert_id}", response_class=HTMLResponse)
async def certificate_view(request: Request, cert_id: str):
    cert = get_certificate_by_id(cert_id)  # fetch from Supabase
    
    if not cert:
        raise HTTPException(status_code=404, detail="Certificate not found")

    return templates.TemplateResponse(
        "certificate.html",
        {
            "request": request,
            "cert": cert  # pass full certificate data
        }
    )
