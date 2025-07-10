# Certificate Verification Backend
HABIN RAHMAN
A clean Flask-based backend for certificate verification with a modern Tailwind CSS frontend.

## ✅ Features

- **Flask Backend**: Clean, production-ready Flask API
- **Modern UI**: Responsive design with Tailwind CSS
- **Multiple Templates**: Both simple verification and full certificate views
- **Production Ready**: Deployed on Vercel with proper build process
- **No CDN Dependencies**: Built CSS for production

## 🚀 Quick Start

### 1. Install Dependencies
```bash
# Python dependencies
pip install -r requirements.txt

# Node.js dependencies (for Tailwind CSS)
npm install
```

### 2. Build CSS
```bash
npm run build:css
```

### 3. Run Locally
```bash
python app.py
```

The server will start on `http://localhost:5000`

## 📋 Available Routes

### API Endpoints
- `GET /` - API status
- `GET /certificates/<cert_id>` - Get certificate data (JSON)
- `GET /health` - Health check

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
├── app.py                 # Flask backend (main file)
├── index.html            # Simple verification page
├── certificate.html      # Full certificate template
├── static/
│   └── output.css       # Built Tailwind CSS
├── input.css            # Tailwind input file
├── tailwind.config.js   # Tailwind configuration
├── package.json         # Node.js dependencies
├── requirements.txt     # Python dependencies
└── vercel.json         # Vercel deployment config
```

## 🚀 Deployment

### Vercel Deployment
The application is configured for easy deployment on Vercel:

1. **Connect to GitHub**: Your repo is ready for Vercel
2. **Auto-deploy**: Vercel will automatically build and deploy
3. **Custom domain**: Easy to add custom domains

### Manual Deployment
```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel
```

## 🎯 Tech Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML + Tailwind CSS
- **Deployment**: Vercel
- **Build Tool**: Tailwind CSS CLI

## 📝 License

This project is open source and available under the [MIT License](LICENSE). 
