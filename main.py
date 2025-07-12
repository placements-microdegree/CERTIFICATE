from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os
from supabase_config import get_certificate_by_id, get_all_certificates

app = FastAPI(title="Certificate Verification API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://your-actual-vercel-frontend-url.vercel.app",  # Replace with your actual Vercel URL
        "http://localhost:5000"  # local testing
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def read_root():
    """Serve the verification portal"""
    try:
        with open('index.html', 'r', encoding='utf-8') as f:
            html_content = f.read()
        return HTMLResponse(content=html_content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error serving index page: {str(e)}")

@app.get("/certificates/{cert_id}")
async def get_certificate(cert_id: str):
    print(f"Received request for certificate_id: {cert_id}")
    """Get certificate data from Supabase by certificate ID"""
    try:
        certificate_data = get_certificate_by_id(cert_id)
        print(f"Certificate data: {certificate_data}")
        if certificate_data:
            return certificate_data
        else:
            print("Certificate not found")
            # Always return a JSON error if not found
            return JSONResponse(status_code=404, content={"error": "Certificate not found"})
    except Exception as e:
        print(f"Exception occurred: {e}")
        # Always return a JSON error if something goes wrong
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/cert/{certificate_id}")
async def serve_certificate_page(certificate_id: str):
    """Serve the certificate template with dynamic data"""
    from fastapi.responses import HTMLResponse
    from supabase_config import get_certificate_by_id
    try:
        with open("certificate.html", "r", encoding="utf-8") as f:
            html_content = f.read()
        cert_data = get_certificate_by_id(certificate_id)
        if not cert_data:
            return HTMLResponse(
                content="<h2 style='text-align:center;color:#b91c1c;margin-top:3em'>Certificate Not Found</h2>",
                status_code=404,
            )
        # Replace placeholders
        html_content = (
            html_content.replace("{{student_name}}", cert_data["student_name"])
            .replace("{{course_name}}", cert_data["course"])
            .replace("{{completion_date}}", cert_data["completion_date"])
            .replace("{{certificate_id}}", cert_data["certificate_id"])
        )
        return HTMLResponse(content=html_content)
    except Exception as e:
        return HTMLResponse(
            content=f"<h2 style='text-align:center;color:#b91c1c;margin-top:3em'>Error: {str(e)}</h2>",
            status_code=500,
        )

@app.get("/certificates")
async def get_all_certificates_route():
    """Get all certificates from database"""
    certificates = get_all_certificates()
    return {"certificates": certificates}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "API is running"}

@app.get("/debug")
async def debug_info():
    """Debug endpoint to check environment and connection"""
    import os
    return {
        "supabase_url_set": bool(os.getenv('SUPABASE_URL')),
        "supabase_key_set": bool(os.getenv('SUPABASE_KEY')),
        "supabase_url": os.getenv('SUPABASE_URL', 'Not set'),
        "environment": os.getenv('VERCEL_ENV', 'local')
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000) 