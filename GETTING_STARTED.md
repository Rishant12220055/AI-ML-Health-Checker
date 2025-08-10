# 🚀 Getting Started with AI Healthcare Assistant

## Quick Start Guide

Follow these steps to get your AI Healthcare Assistant up and running:

### Prerequisites

- **Python 3.8+** (recommended: Python 3.10+)
- **Node.js 16+** (for frontend)
- **MongoDB** (local or cloud instance)
- **Git** (for cloning)

### 1. Backend Setup

#### Step 1: Navigate to Backend Directory
```bash
cd backend
```

#### Step 2: Create Virtual Environment
```bash
# Windows
python -m venv healthcare_env
healthcare_env\Scripts\activate

# macOS/Linux
python -m venv healthcare_env
source healthcare_env/bin/activate
```

#### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

#### Step 4: Environment Configuration
```bash
# Copy environment template
cp .env.example .env

# Edit .env file with your settings
# - MongoDB connection string
# - API keys (if using external services)
# - Other configuration options
```

#### Step 5: Run Setup Script
```bash
python setup.py
```

#### Step 6: Start the Backend Server
```bash
python main.py
```

The backend API will be available at `http://localhost:8000`

**API Documentation:** `http://localhost:8000/docs`

### 2. Frontend Setup

#### Step 1: Navigate to Frontend Directory
```bash
cd ../frontend
```

#### Step 2: Install Dependencies
```bash
npm install
```

#### Step 3: Configure Environment
```bash
# Create environment file
cp .env.example .env.local

# Edit with your backend API URL
VITE_API_BASE_URL=http://localhost:8000
```

#### Step 4: Start Development Server
```bash
npm run dev
```

The frontend will be available at `http://localhost:3000`

### 3. Database Setup

#### Option A: Local MongoDB
1. Install MongoDB Community Edition
2. Start MongoDB service
3. Use default connection string: `mongodb://localhost:27017`

#### Option B: MongoDB Atlas (Cloud)
1. Create account at mongodb.com
2. Create a new cluster
3. Get connection string
4. Update MONGODB_CONNECTION_STRING in .env

### 4. Testing the Application

1. **Health Check:**
   ```bash
   curl http://localhost:8000/health
   ```

2. **Frontend Access:**
   - Open `http://localhost:3000` in your browser
   - Fill out the symptom checker form
   - Submit for AI analysis

3. **API Testing:**
   - Visit `http://localhost:8000/docs` for interactive API documentation
   - Test endpoints using the Swagger UI

### 5. Production Deployment

#### Backend (AWS Lambda)
```bash
# Install serverless framework
npm install -g serverless

# Deploy to AWS
serverless deploy
```

#### Frontend (Vercel/Netlify)
```bash
# Build for production
npm run build

# Deploy to your preferred platform
```

### Troubleshooting

#### Common Issues:

1. **Import Errors:**
   - Ensure virtual environment is activated
   - Check Python version (3.8+ required)

2. **Database Connection:**
   - Verify MongoDB is running
   - Check connection string in .env

3. **Frontend Build Errors:**
   - Clear node_modules and reinstall
   - Check Node.js version (16+ required)

4. **API Calls Failing:**
   - Verify backend is running on correct port
   - Check CORS settings
   - Verify API base URL in frontend

#### Model Downloads:
- Models will download automatically on first use
- Ensure internet connection for initial setup
- Check available disk space (models can be large)

### Environment Variables

#### Backend (.env)
```bash
# Application
DEBUG=True
LOG_LEVEL=INFO
PORT=8000

# Database
MONGODB_CONNECTION_STRING=mongodb://localhost:27017
MONGODB_DATABASE=healthcare_assistant

# AI Models
HUGGINGFACE_CACHE_DIR=./models
MODEL_DEVICE=cpu

# Security
SECRET_KEY=your_secret_key_here
ALLOWED_ORIGINS=http://localhost:3000
```

#### Frontend (.env.local)
```bash
VITE_API_BASE_URL=http://localhost:8000
```

### Development Workflow

1. **Make Changes:**
   - Backend: Files auto-reload with uvicorn
   - Frontend: Hot reload with Vite

2. **Testing:**
   ```bash
   # Backend tests
   cd backend
   pytest
   
   # Frontend tests
   cd frontend
   npm test
   ```

3. **Linting & Formatting:**
   ```bash
   # Backend
   black . && flake8 .
   
   # Frontend
   npm run lint && npm run format
   ```

### Support

- **Documentation:** See README.md for detailed information
- **Issues:** Report bugs on GitHub
- **Medical Disclaimer:** This is for educational purposes only

---

**⚠️ IMPORTANT MEDICAL DISCLAIMER:**
This application is for educational and informational purposes only. It should not be used as a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of qualified healthcare providers.
