import os
from fastapi.templating import Jinja2Templates
from fastapi import Request, FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from supabase_config import get_certificate_by_id, get_all_certificates, supabase

app = FastAPI(title="Certificate Verification API", version="1.0.0")
templates = Jinja2Templates(directory="templates")

# CORS for local, Vercel, and microdegree domains
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://certificate-verification-ecru.vercel.app",
        "https://certificate-three-wheat.vercel.app",
        "https://cert.microdegree.in",
        "http://localhost:5000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static assets (CSS, images)
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def read_root():
    try:
        with open("index.html", "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error serving root page: {e}")


@app.get("/home", response_class=HTMLResponse)
async def home_page():
    try:
        with open("home.html", "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error serving home page: {e}")


@app.get("/verify", response_class=HTMLResponse)
async def verification_portal():
    try:
        with open("index.html", "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error serving verification page: {e}")


@app.get("/api/certificate/{cert_id}")
async def get_certificate(cert_id: str):
    try:
        cert_data = get_certificate_by_id(cert_id)
        if not cert_data:
            return JSONResponse(
                status_code=404, content={"success": False, "message": "Certificate not found"}
            )

        return {
            "success": True,
            "certificate": {
                "id": cert_data["certificate_id"],
                "recipient_name": cert_data["student_name"],
                "course_name": cert_data["course_name"],
                "issue_date": cert_data["completion_date"],
                "issuer": "MicroDegree Academy",
            },
        }
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


@app.get("/cert/{certificate_id}", response_class=HTMLResponse)
async def serve_certificate_page(request: Request, certificate_id: str):
    try:
        cert_data = get_certificate_by_id(certificate_id)
        if not cert_data:
            return HTMLResponse(
                "<h2 style='text-align:center;color:#b91c1c;margin-top:3em'>Certificate Not Found</h2>",
                status_code=404,
            )

        # Ensure the URL is correct for your custom domain
        cert_url = f"https://cert.microdegree.in/cert/{certificate_id}"
        # Optional: update Supabase if missing
        if not cert_data.get("certificate_url"):
            supabase.table("certificate_users").update({"certificate_url": cert_url}).eq(
                "certificate_id", certificate_id
            ).execute()

        return templates.TemplateResponse(
            "certificate.html",
            {
                "request": request,
                "student_name": cert_data["student_name"],
                "course_name": cert_data["course_name"],
                "completion_date": cert_data["completion_date"],
                "certificate_id": cert_data["certificate_id"],
            },
        )
    except Exception as e:
        return HTMLResponse(
            f"<h2 style='text-align:center;color:#b91c1c;margin-top:3em'>Error: {str(e)}</h2>",
            status_code=500,
        )


@app.get("/certificates")
async def get_all_certificates_route():
    try:
        certificates = get_all_certificates()
        return {"certificates": certificates}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "API is running"}


@app.get("/debug")
async def debug_info():
    return {
        "supabase_url_set": bool(os.getenv("SUPABASE_URL")),
        "supabase_key_set": bool(os.getenv("SUPABASE_KEY")),
        "supabase_url": os.getenv("SUPABASE_URL", "Not set"),
        "environment": os.getenv("VERCEL_ENV", "local"),
    }


@app.get("/debug/certificates")
async def debug_all_certs():
    try:
        response = supabase.table("certificate_users").select("*").execute()
        return response.data
    except Exception as e:
        return {"error": str(e)}


if __name__ == "__main__":
    import uvicorn

    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
