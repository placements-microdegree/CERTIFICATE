from main import app


app = FastAPI(title="Certificate Verification API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://certificate-three-wheat.vercel.app",
        "https://certificate-czlvnefi0-habins-projects-2ddf3087.vercel.app",
        "http://localhost:5000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mock data for testing
MOCK_CERTIFICATES = [
    {
        "certificate_id": "CERT-001",
        "student_name": "Habin Rahman",
        "course_name": "ReactJS with Supabase",
        "completion_date": "2025-07-07",
    },
    {
        "certificate_id": "HR08",
        "student_name": "HABIN",
        "course_name": "PYTHON",
        "completion_date": "2025-07-11",
    },
    {
        "certificate_id": "test123",
        "student_name": "Michael Chen",
        "course_name": "Data Science Essentials",
        "completion_date": "2024-03-10",
    },
]


def get_certificate_by_id(certificate_id: str):
    """Get certificate data by ID"""
    for cert in MOCK_CERTIFICATES:
        if cert["certificate_id"] == certificate_id:
            return {
                "student_name": cert["student_name"],
                "course": cert["course_name"],
                "completion_date": cert["completion_date"],
                "certificate_id": cert["certificate_id"],
            }
    return None


@app.get("/")
async def read_root():
    """Serve the verification portal"""
    try:
        with open("index.html", "r", encoding="utf-8") as f:
            html_content = f.read()
        return HTMLResponse(content=html_content)
    except Exception as e:
        return HTMLResponse(
            content=f"<h1>Certificate Verification Portal</h1><p>Error: {str(e)}</p>"
        )


@app.get("/api/certificate/{cert_id}")
async def get_certificate(cert_id: str):
    """Get certificate data from database by certificate ID"""
    try:
        certificate_data = get_certificate_by_id(cert_id)
        if certificate_data:
            return {
                "success": True,
                "certificate": {
                    "id": certificate_data["certificate_id"],
                    "recipient_name": certificate_data["student_name"],
                    "course_name": certificate_data["course"],
                    "issue_date": certificate_data["completion_date"],
                    "issuer": "MicroDegree Academy",
                },
            }
        else:
            return {"success": False, "message": "Certificate not found"}
    except Exception as e:
        return JSONResponse(
            status_code=500, content={"success": False, "message": str(e)}
        )


@app.get("/cert/{certificate_id}")
async def serve_certificate_page(certificate_id: str):
    """Serve the certificate template with dynamic data"""
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


@app.get("/{certificate_id}")
async def serve_verification_page(certificate_id: str):
    """Serve the verification page with certificate data for direct certificate ID access"""
    try:
        with open("index.html", "r", encoding="utf-8") as f:
            html_content = f.read()
        return HTMLResponse(content=html_content)
    except Exception as e:
        return HTMLResponse(
            content=f"<h1>Error loading verification page: {str(e)}</h1>"
        )
