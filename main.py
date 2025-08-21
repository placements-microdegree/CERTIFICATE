import os
from fastapi import FastAPI, Request, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from supabase_config import get_certificate_by_id, get_all_certificates, supabase

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
def fetch_certificate(certificate_id: str):
    """
    Fetch certificate and return dict with status.
    """
    cert = get_certificate_by_id(certificate_id)
    if cert:
        return {"cert": cert, "status": "success"}
    else:
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
    accept_header = request.headers.get("accept", "")
    
    if "application/json" in accept_header:
        # Return JSON if requested
        if result["status"] == "success":
            return JSONResponse({"success": True, "data": result["cert"]})
        else:
            return JSONResponse({"success": False, "message": "Certificate not found"}, status_code=404)
    
    # Default: render HTML
    if result["status"] == "success":
        return templates.TemplateResponse("certificate.html", {"request": request, "cert": result["cert"]})
    else:
        return templates.TemplateResponse(
            "error.html",
            {"request": request, "message": "Certificate not found"}
        )

@app.get("/verify/{certificate_id}", response_class=HTMLResponse)
async def verify_page(request: Request, certificate_id: str):
    result = fetch_certificate(certificate_id)
    return templates.TemplateResponse(
        "result.html",
        {"request": request, **result}
    )

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
    else:
        return {"success": False, "message": "Certificate not found"}

@app.get("/api/verify/{certificate_id}")
async def api_verify_certificate(certificate_id: str):
    result = fetch_certificate(certificate_id)
    if result["status"] == "success":
        return {"success": True, "data": result["cert"]}
    else:
        return {"success": False, "message": "Certificate not found"}

# ----------------------
# Debug Routes
# ----------------------
@app.get("/debug/supabase")
async def debug_supabase():
    try:
        response = supabase.table("certificates").select("*").limit(1).execute()
        return {"status": "connected", "sample": response.data}
    except Exception as e:
        return {"status": "error", "detail": str(e)}

@app.get("/debug/certificates")
def debug_certificates():
    try:
        data = supabase.table("certificates").select("*").limit(5).execute()
        return {"success": True, "data": data.data}
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.get("/debug/all_certificate_ids")
async def debug_all_certificate_ids():
    """
    Returns a list of all certificate IDs in the certificates table.
    For testing/debugging purposes only.
    """
    try:
        response = supabase.table("certificates").select("certificate_id").execute()
        ids = [row["certificate_id"] for row in response.data] if response.data else []
        return {"success": True, "certificate_ids": ids}
    except Exception as e:
        return {"success": False, "error": str(e)}