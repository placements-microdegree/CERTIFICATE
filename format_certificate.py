from datetime import datetime

def format_certificate(certificate):
    if certificate.get("completion_date"):
        try:
            # Convert from "2025-09-07" → "07/09/2025"
            date_obj = datetime.strptime(certificate["completion_date"], "%Y-%m-%d")
            certificate["completion_date"] = date_obj.strftime("%d/%m/%Y")
        except Exception:
            certificate["completion_date"] = certificate["completion_date"]
    return certificate


@app.get("/cert/{cert_id}")
async def get_certificate(cert_id: str, request: Request):
    certificate = get_certificate_by_id(cert_id)
    if not certificate:
        return templates.TemplateResponse("error.html", {"request": request, "message": "Certificate not found"})

    # ✅ Format the date here before rendering
    certificate = format_certificate(certificate)

    return templates.TemplateResponse(
        "certificate.html",
        {"request": request, "certificate": certificate}
    )
