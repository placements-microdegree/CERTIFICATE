from flask import Flask, render_template_string, send_from_directory
from flask_cors import CORS
import os

app = Flask(__name__, static_folder='static')
CORS(app)

@app.route('/')
def read_root():
    return {"message": "Certificates Backend API (Flask)", "status": "running", "version": "1.0.0"}

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
    # Read the HTML template
    with open('index.html', 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Replace the CDN script with our built CSS
    html_content = html_content.replace(
        '<script src="https://cdn.tailwindcss.com"></script>',
        '<link href="/static/output.css" rel="stylesheet">'
    )
    
    return html_content

@app.route('/certificate/<certificate_id>')
def serve_certificate_template(certificate_id):
    # Read the certificate template
    with open('certificate.html', 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    return html_content

@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)