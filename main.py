import os
from fastapi import FastAPI, Request, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from supabase_config import get_certificate_by_id, get_all_certificates

from supabase import create_client, Client
app = FastAPI(title="Certificate Verification API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict later to frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# ----------------------
# Frontend Pages
# ----------------------
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/cert/{certificate_id}", response_class=HTMLResponse)
async def certificate_page(request: Request, certificate_id: str):
    cert = get_certificate_by_id(certificate_id)
    if not cert:
        return templates.TemplateResponse(
            "error.html",
            {"request": request, "message": "Certificate not found"}
        )
    return templates.TemplateResponse("certificate.html", {"request": request, "cert": cert})

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
    try:
        cert = get_certificate_by_id(certificate_id)
        if not cert:
            return {"success": False, "message": "Certificate not found"}
        return {"success": True, "data": cert}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ----------------------
# New Verify API (like MicroDegree's)
# ----------------------
@app.get("/verify/{certificate_id}")
async def verify_certificate(certificate_id: str):
    try:
        cert = get_certificate_by_id(certificate_id)
        if not cert:
            return {"success": False, "message": "Certificate not found"}
        return {"success": True, "data": cert}
    except Exception as e:
        return {"success": False, "message": str(e)}

# ----------------------
# Debug Route (optional)
# ----------------------
@app.get("/debug/supabase")
async def debug_supabase():
    try:
        certificates = get_all_certificates()
        return {"success": True, "count": len(certificates)}
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.get("/debug/certs")
async def debug_certs():
    try:
        data = supabase.table("certificates").select("*").limit(5).execute()
        return {"success": True, "data": data.data}
    except Exception as e:
        return {"success": False, "error": str(e)}
