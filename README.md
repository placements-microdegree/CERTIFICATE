# Certificate Verification Backend

A Flask-based backend for certificate verification with a modern Tailwind CSS frontend.

## ✅ Fixed Issues

### 1. Tailwind CSS Production Setup
- ✅ Removed CDN dependency (`cdn.tailwindcss.com`)
- ✅ Set up proper Tailwind CSS build process
- ✅ Created `static/output.css` with essential Tailwind utilities
- ✅ Added build scripts to `package.json`

### 2. Backend 404 Error
- ✅ Fixed API URL to use relative paths (`/certificates/<id>`)
- ✅ Added proper static file serving
- ✅ Improved error handling and user feedback
- ✅ Added multiple certificate template routes

## 🚀 Quick Start

### 1. Install Dependencies
```bash
# Python dependencies
pip install -r requirements.txt

# Node.js dependencies (for Tailwind CSS)
npm install
```

### 2. Build CSS (Optional)
```bash
npm run build:css
```

### 3. Run the Application
```bash
python app.py
```

The server will start on `http://localhost:5000`

## 📋 Available Routes

### API Endpoints
- `GET /` - API status
- `GET /certificates/<cert_id>` - Get certificate data (JSON)

### Frontend Pages
- `GET /cert/<certificate_id>` - Simple certificate verification page
- `GET /certificate/<certificate_id>` - Full certificate template
- `GET /static/<filename>` - Static files (CSS, etc.)

## 🎨 Features

- **Modern UI**: Clean, responsive design with Tailwind CSS
- **Error Handling**: Proper error messages for missing certificates
- **Multiple Templates**: Both simple verification and full certificate views
- **Production Ready**: No CDN dependencies, built CSS for production

## 🔧 Development

### Rebuilding CSS
```bash
# Build once
npm run build:css

# Watch for changes
npm run watch:css
```

### Testing Certificates
Visit these URLs to test:
- `http://localhost:5000/cert/test123` - Simple verification
- `http://localhost:5000/certificate/test123` - Full certificate

## 📁 Project Structure

```
certificates-backend/
├── app.py                 # Flask backend
├── index.html            # Simple verification page
├── certificate.html      # Full certificate template
├── static/
│   └── output.css       # Built Tailwind CSS
├── input.css            # Tailwind input file
├── tailwind.config.js   # Tailwind configuration
├── package.json         # Node.js dependencies
└── requirements.txt     # Python dependencies
```

## 🚀 Deployment

The application is ready for deployment on platforms like:
- Render (see `render.yaml`)
- Vercel (see `vercel.json`)
- Heroku
- Any Python hosting platform

The built CSS eliminates the Tailwind CDN warning in production. 