from flask import Flask, render_template_string, send_from_directory, request
from flask_cors import CORS
import os
from supabase_config import get_certificate_by_id, get_all_certificates

# Set Supabase environment variables for Vercel deployment
if not os.getenv('SUPABASE_URL'):
    os.environ['SUPABASE_URL'] = 'https://wyszrjhxucxblyvhrktn.supabase.co'
if not os.getenv('SUPABASE_KEY'):
    os.environ['SUPABASE_KEY'] = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Ind5c3pyamh4dWN4Ymx5dmhya3RuIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTE4OTAzNzgsImV4cCI6MjA2NzQ2NjM3OH0.ZEPZIXsIVXbor8vY1uJM9VVVnody5iDJOgabbov14Xw'

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
    # Get certificate data from Supabase
    certificate_data = get_certificate_by_id(cert_id)
    
    if certificate_data:
        return certificate_data
    else:
        return {"error": "Certificate not found"}, 404

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

@app.route('/certificates')
def get_all_certificates_route():
    certificates = get_all_certificates()
    return {"certificates": certificates}

# For Vercel deployment
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

# For Vercel serverless
app.debug = True