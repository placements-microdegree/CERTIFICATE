from fastapi import FastAPI
from supabase_config import get_certificate_by_id
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/{cert_id:path}")
async def get_certificate(cert_id: str):
    cert = get_certificate_by_id(cert_id)
    if cert:
        return cert
    return JSONResponse(status_code=404, content={"detail": "Not Found"}) 