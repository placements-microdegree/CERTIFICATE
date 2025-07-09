from flask import Flask, render_template_string
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Certificate Verification</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-100 flex items-center justify-center min-h-screen">
  <div class="bg-white shadow-lg rounded-lg p-8 max-w-md w-full" id="certificate-card">
    <h1 class="text-2xl font-bold text-center text-gray-800 mb-4">Certificate Verification</h1>
    <div class="mb-6">
      <p class="text-gray-600 text-center">Student Name</p>
      <p class="text-xl font-semibold text-center text-blue-700 mt-2" id="student-name">Loading...</p>
    </div>
    <div class="mb-6">
      <p class="text-gray-600 text-center">Course</p>
      <p class="text-lg font-medium text-center text-green-700 mt-2" id="course-name">Loading...</p>
    </div>
    <div class="mb-6">
      <p class="text-gray-600 text-center">Completion Date</p>
      <p class="text-md text-center text-gray-800 mt-2" id="completion-date">Loading...</p>
    </div>
  </div>
  <script>
    const pathParts = window.location.pathname.split('/');
    const certificateId = pathParts[pathParts.length - 1] || pathParts[pathParts.length - 2] || 'test123';
    const apiUrl = `https://certificate-verification-aqvv.onrender.com/certificates/${certificateId}`;
    
    console.log('Fetching from:', apiUrl);
    
    fetch(apiUrl)
      .then(response => {
        console.log('Response status:', response.status);
        if (!response.ok) throw new Error("Certificate not found");
        return response.json();
      })
      .then(data => {
        console.log('Received data:', data);
        document.getElementById("student-name").textContent = data.student_name;
        document.getElementById("course-name").textContent = data.course;
        document.getElementById("completion-date").textContent = data.completion_date;
      })
      .catch(error => {
        console.error('Fetch error:', error);
        document.getElementById("certificate-card").innerHTML = `
          <h1 class="text-2xl font-bold text-center text-red-600 mb-4">Error</h1>
          <p class="text-center text-gray-700">${error.message}</p>
        `;
      });
  </script>
</body>
</html>
"""

@app.route('/')
def read_root():
    return {"message": "Certificates Backend API (Flask)", "status": "running", "version": "1.0.0"}

@app.route('/certificates/<cert_id>')
def get_certificate(cert_id):
    return {
        "student_name": "Jane Doe",
        "course": "Advanced Python Programming",
        "completion_date": "2024-01-15",
        "certificate_id": cert_id
    }

@app.route('/cert/<certificate_id>')
def serve_certificate_page(certificate_id):
    return render_template_string(HTML_TEMPLATE)

if __name__ == '__main__':
    app.run(debug=True)