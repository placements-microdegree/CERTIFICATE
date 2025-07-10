from flask import Flask, render_template_string, send_from_directory, request
from flask_cors import CORS
import os

app = Flask(__name__, static_folder='static')
CORS(app)

@app.route('/')
def read_root():
    try:
        # Read the index.html file
        with open('index.html', 'r', encoding='utf-8') as f:
            html_content = f.read()
        return html_content
    except Exception as e:
        return f"Error serving index page: {str(e)}", 500

@app.route('/certificates/<cert_id>')
def get_certificate(cert_id):
    return {
        "student_name": "Habin Rahman",
        "course": "Advanced Python Programming",
        "completion_date": "2024-01-15",
        "certificate_id": cert_id
    }

@app.route('/cert/<certificate_id>')
def serve_certificate_page(certificate_id):
    try:
        # Read the certificate.html file
        with open('certificate.html', 'r', encoding='utf-8') as f:
            html_content = f.read()
        return html_content
    except Exception as e:
        return f"Error serving certificate page: {str(e)}", 500

@app.route('/certificate/<certificate_id>')
def serve_certificate_template(certificate_id):
    try:
        # Check if certificate.html exists
        if not os.path.exists('certificate.html'):
            return f"Error: certificate.html not found. Current directory: {os.getcwd()}, Files: {os.listdir('.')}", 500
        
        # Read the certificate template
        with open('certificate.html', 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        return html_content
    except Exception as e:
        return f"Error serving certificate template: {str(e)}", 500

@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

@app.route('/health')
def health_check():
    return {"status": "healthy", "message": "API is running"}

# For Vercel deployment
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

# For Vercel serverless
app.debug = True