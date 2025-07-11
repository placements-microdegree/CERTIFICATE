from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import os
from supabase_config import get_certificate_by_id, get_all_certificates

app = FastAPI(title="Certificate Verification API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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
    """Get certificate data from Supabase by certificate ID"""
    certificate_data = get_certificate_by_id(cert_id)
    
    if certificate_data:
        return certificate_data
    else:
        raise HTTPException(status_code=404, detail="Certificate not found")

@app.get("/cert/{certificate_id}")
async def serve_certificate_page(certificate_id: str):
    """Serve the certificate template"""
    try:
        with open('certificate.html', 'r', encoding='utf-8') as f:
            html_content = f.read()
        return HTMLResponse(content=html_content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error serving certificate page: {str(e)}")

@app.get("/certificates")
async def get_all_certificates_route():
    """Get all certificates from database"""
    certificates = get_all_certificates()
    return {"certificates": certificates}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000) 