from fastapi import FastAPI, HTTPException
from supabase import create_client
from dotenv import load_dotenv
import os
from fastapi.responses import HTMLResponse

# Load .env variables
load_dotenv()

# Supabase credentials
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError("SUPABASE_URL and SUPABASE_KEY must be set in the environment variables or .env file.")

# Initialize Supabase client
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Initialize FastAPI app
app = FastAPI()

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang=\"en\">
<head>
  <meta charset=\"UTF-8\">
  <title>Certificate Verification</title>
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">
  <script src=\"https://cdn.tailwindcss.com\"></script>
</head>
<body class=\"bg-gray-100 flex items-center justify-center min-h-screen\">
  <div class=\"bg-white shadow-lg rounded-lg p-8 max-w-md w-full\" id=\"certificate-card\">
    <h1 class=\"text-2xl font-bold text-center text-gray-800 mb-4\">Certificate Verification</h1>
    <div class=\"mb-6\">
      <p class=\"text-gray-600 text-center\">Student Name</p>
      <p class=\"text-xl font-semibold text-center text-blue-700 mt-2\" id=\"student-name\">Loading...</p>
    </div>
    <div class=\"mb-6\">
      <p class=\"text-gray-600 text-center\">Course</p>
      <p class=\"text-lg font-medium text-center text-green-700 mt-2\" id=\"course-name\">Loading...</p>
    </div>
    <div class=\"mb-6\">
      <p class=\"text-gray-600 text-center\">Completion Date</p>
      <p class=\"text-md text-center text-gray-800 mt-2\" id=\"completion-date\">Loading...</p>
    </div>
  </div>
  <script>
    // Get the certificate ID from the URL path (e.g., /cert/123)
    const pathParts = window.location.pathname.split('/');
    const certificateId = pathParts[pathParts.length - 1] || pathParts[pathParts.length - 2];

    // Adjust the API URL to match your FastAPI backend
    const apiUrl = `http://localhost:8000/certificates/${certificateId}`;

    fetch(apiUrl)
      .then(response => {
        if (!response.ok) throw new Error("Certificate not found");
        return response.json();
      })
      .then(data => {
        document.getElementById("student-name").textContent = data.student_name;
        document.getElementById("course-name").textContent = data.course;
        document.getElementById("completion-date").textContent = data.completion_date;
      })
      .catch(error => {
        document.getElementById("certificate-card").innerHTML = `
          <h1 class=\"text-2xl font-bold text-center text-red-600 mb-4\">Error</h1>
          <p class=\"text-center text-gray-700\">${error.message}</p>
        `;
      });
  </script>
</body>
</html>
"""

@app.get("/")
def read_root():
    return {"message": "Certificates Backend API (FastAPI)", "status": "running", "version": "1.0.0"}

@app.get("/certificates/{certificate_id}")
def get_certificate(certificate_id: str):
    try:
        response = supabase.table("certificates").select("*").eq("certificate_id", certificate_id).execute()
        if not response.data:
            raise HTTPException(status_code=404, detail="Certificate not found")
        return response.data[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/cert/{certificate_id}", response_class=HTMLResponse)
def serve_certificate_page(certificate_id: str):
    return HTML_TEMPLATE
