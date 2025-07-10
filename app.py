from flask import Flask, render_template_string
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

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

if __name__ == '__main__':
    app.run(debug=True)