import os
import re
import traceback
from fastapi import FastAPI, Request, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from supabase_config import get_certificate_by_id, get_all_certificates
from supabase import create_client
from dateutil import parser

# ----------------------
# Load environment variables
# ----------------------
# Only load .env if running locally
if os.path.exists(".env"):
    from dotenv import load_dotenv
    load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

print("DEBUG Supabase URL:", SUPABASE_URL)
print("DEBUG Supabase KEY present:", bool(SUPABASE_KEY))

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError(
        "❌ Supabase credentials are missing. "
        "On Render, go to your service → Environment → Add SUPABASE_URL and SUPABASE_KEY"
    )

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

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
# Helper Functions
# ----------------------
def sanitize_cert_id(cert_id: str) -> str:
    """Normalize certificate ID to AWSC-XXXX format."""
    cert_id = cert_id.strip()
    if cert_id.endswith(".0"):
        cert_id = cert_id[:-2]
    cert_id = re.sub(r"[^A-Za-z0-9\-]", "", cert_id)
    if not cert_id.upper().startswith("AWSC-"):
        cert_id = f"AWSC-{cert_id}"
    return cert_id.upper()


def fetch_certificate(cert_id: str) -> dict:
    """Fetch certificate and format completion_date."""
    cert_id = sanitize_cert_id(cert_id)
    cert = get_certificate_by_id(cert_id)
    if not cert:
        return {"status": "error", "cert": None}
    try:
        raw_date = cert.get("completion_date")
        if raw_date:
            dt = parser.parse(str(raw_date))
            cert["completion_date"] = dt.strftime("%d-%m-%Y")
        else:
            cert["completion_date"] = "N/A"
    except Exception:
        cert["completion_date"] = "N/A"
    return {"status": "success", "cert": cert}

# ----------------------
# Frontend Pages
# ----------------------
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/cert/{certificate_id}", response_class=HTMLResponse)
async def certificate_page(request: Request, certificate_id: str):
    try:
        original_id = certificate_id
        certificate_id = sanitize_cert_id(certificate_id)
        print(f"[DEBUG] Original ID: {original_id}, Sanitized ID: {certificate_id}")

        # Redirect if URL is not normalized
        if original_id != certificate_id:
            return RedirectResponse(f"/cert/{certificate_id}")

        result = fetch_certificate(certificate_id)
        print(f"[DEBUG] Fetched certificate result: {result}")

        if result["status"] == "success":
            return templates.TemplateResponse(
                "certificate.html",
                {"request": request, "certificate": result["cert"]},
            )

        return templates.TemplateResponse(
            "error.html", {"request": request, "message": "Certificate not found"}
        )
    except Exception as e:
        print("[ERROR] Exception in certificate_page:", e)
        traceback.print_exc()
        return templates.TemplateResponse(
            "error.html", {"request": request, "message": f"Internal error: {e}"}
        )


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
# PDF Download
# ----------------------
@app.get("/download/{cert_id}")
async def download_pdf(cert_id: str):
    cert_id = sanitize_cert_id(cert_id)
    file_path = os.path.join("static", "certificates", f"{cert_id}.pdf")
    if os.path.exists(file_path):
        return FileResponse(file_path, filename=f"{cert_id}.pdf", media_type="application/pdf")
    return JSONResponse({"success": False, "message": "Certificate file not found"}, status_code=404)

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

        certificate_id = sanitize_cert_id(certificate_id)
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
        return {"success": True, "certificate_ids_uppercase": ids_upper, "certificate_ids_lowercase": ids_lower, "total": len(ids_upper)}
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
            "total_certificates": len(ids_upper),
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

# ----------------------
# Environment Debug
# ----------------------
@app.get("/debug/env")
async def debug_env():
    return {
        "SUPABASE_URL": SUPABASE_URL,
        "SUPABASE_KEY_present": bool(SUPABASE_KEY)
    }
