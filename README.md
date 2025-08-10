# 🏥 AI Healthcare Assistant

A comprehensive multi-agent AI healthcare assistant system built with FastAPI, React, and advanced machine learning models. This system provides intelligent symptom analysis, differential diagnosis, treatment recommendations, and emergency detection with explainable AI capabilities.

## 🌟 Features

### 🤖 Multi-Agent AI System
- **Symptom Classifier Agent**: Analyzes and categorizes patient symptoms
- **Condition Matcher Agent**: Matches symptoms to possible medical conditions
- **Treatment Retriever Agent**: Recommends appropriate treatments
- **Agent Coordinator**: Orchestrates all agents for comprehensive diagnosis

### 🎯 Core Capabilities
- **Intelligent Symptom Analysis**: Advanced NLP processing of patient symptoms
- **Differential Diagnosis**: Multiple possible conditions with confidence scores
- **Emergency Detection**: Real-time identification of urgent medical situations
- **Treatment Recommendations**: Evidence-based treatment suggestions
- **Explainable AI**: Clear reasoning behind all diagnostic decisions
- **Regulatory Compliance**: Medical disclaimers and safety guidelines

### 💻 Modern Web Interface
- **Progressive Web App (PWA)**: Works offline and installable
- **Responsive Design**: Optimized for desktop, tablet, and mobile
- **Modern UI**: Clean, intuitive Material-UI interface
- **Real-time Processing**: Instant symptom analysis and results
- **Comprehensive Reports**: Detailed diagnosis with next steps

## 🛠️ Technology Stack

### Backend
- **FastAPI**: High-performance Python web framework
- **Python 3.13**: Latest Python with advanced features
- **ClinicalBERT**: Specialized medical language model
- **Sentence Transformers**: Semantic similarity matching
- **LangGraph**: Multi-agent workflow orchestration
- **Motor**: Async MongoDB driver (optional)
- **Pydantic**: Data validation and serialization

### Frontend
- **React 18**: Modern React with hooks and concurrent features
- **TypeScript**: Type-safe development
- **Material-UI (MUI)**: Professional UI components
- **React Router**: Client-side routing
- **Axios**: HTTP client for API communication
- **Vite**: Fast build tool and dev server
- **PWA**: Progressive Web App capabilities

### AI/ML Components
- **Transformers**: Hugging Face transformers library
- **Scikit-learn**: Machine learning utilities
- **NumPy**: Numerical computing
- **Pandas**: Data manipulation
- **NLTK**: Natural language processing

## 🚀 Quick Start

### Prerequisites
- Python 3.11+ 
- Node.js 16+
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Rishant12220055/AI-ML-Health-Checker.git
   cd AI-ML-Health-Checker
   ```

2. **Backend Setup**
   ```bash
   cd backend
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Frontend Setup**
   ```bash
   cd frontend
   npm install
   ```

4. **Environment Configuration**
   ```bash
   cd backend
   cp .env.example .env
   # Edit .env with your configuration
   ```

### Running the Application

1. **Start the Backend Server**
   ```bash
   cd backend
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

2. **Start the Frontend Development Server**
   ```bash
   cd frontend
   npm run dev
   ```

3. **Access the Application**
   - Frontend: `http://localhost:5173`
   - Backend API: `http://localhost:8000`
   - API Documentation: `http://localhost:8000/docs`

## 📊 Accuracy Metrics

Current system performance (based on comprehensive testing):

- **Diagnostic Accuracy**: 60.0% (Fair - under continuous improvement)
- **Urgency Assessment**: 60.0% (Being enhanced for better emergency detection)
- **Processing Speed**: Excellent (0.03 seconds average)
- **Confidence Scoring**: 67.1% average confidence
- **System Reliability**: Production-ready architecture

## 🧪 Testing

### Run Comprehensive Tests
```bash
# Backend tests
python test_diagnosis_complete.py

# Accuracy analysis
python accuracy_analysis.py

# Frontend build test
cd frontend && npm run build
```

### Test Cases Included
- Common cold symptoms
- Emergency chest pain scenarios
- Headache and fever combinations
- Migraine detection
- Respiratory conditions

## 📋 API Endpoints

### Symptom Analysis
- `POST /api/symptoms/analyze` - Analyze patient symptoms
- `GET /api/health` - System health check
- `GET /api/conditions` - Available medical conditions
- `GET /api/treatments` - Treatment options

### WebSocket Support
- `WS /ws/diagnosis` - Real-time diagnosis updates

## 🏗️ Architecture

```
AI Healthcare Assistant/
├── backend/               # FastAPI backend
│   ├── agents/           # Multi-agent system
│   ├── api/              # API endpoints
│   ├── models/           # Data models
│   ├── utils/            # Utilities
│   └── main.py           # Application entry
├── frontend/             # React frontend
│   ├── src/
│   │   ├── components/   # React components
│   │   ├── pages/        # Application pages
│   │   ├── services/     # API services
│   │   └── utils/        # Utilities
├── docs/                 # Documentation
└── tests/                # Test files
```

## 🔒 Security & Compliance

- **Medical Disclaimers**: All recommendations include appropriate disclaimers
- **Data Privacy**: No personal health data stored permanently
- **HIPAA Considerations**: Architecture supports compliance requirements
- **Input Validation**: Comprehensive validation of all user inputs
- **Rate Limiting**: API protection against abuse

## 🚧 Roadmap

### Short Term
- [ ] Improve emergency detection accuracy
- [ ] Enhance symptom-to-condition mapping
- [ ] Add more comprehensive test cases
- [ ] Implement user feedback collection

### Medium Term
- [ ] Integration with medical databases
- [ ] Multi-language support
- [ ] Advanced analytics dashboard
- [ ] Mobile app development

### Long Term
- [ ] Clinical trial integration
- [ ] FDA compliance pathway
- [ ] Telemedicine platform integration
- [ ] AI model continuous learning

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## ⚠️ Medical Disclaimer

This AI Healthcare Assistant is for **informational purposes only** and should **NOT replace professional medical advice, diagnosis, or treatment**. Always consult with qualified healthcare providers for medical concerns. In case of emergency, contact your local emergency services immediately.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors

- **Rishant** - Initial work - [Rishant12220055](https://github.com/Rishant12220055)

## 🙏 Acknowledgments

- ClinicalBERT team for the medical language model
- Hugging Face for transformer models
- FastAPI and React communities
- Medical professionals who provided guidance

## 📞 Support

For support, email: [your-email@example.com] or create an issue in this repository.

---

**⚡ Built with passion for improving healthcare accessibility through AI ⚡**
- **Differential Diagnosis Model**
- **Urgency Level Assessment**
- **Treatment Guidelines Integration**
- **WHO & CDC Guidelines Compliance**
- **Explainable AI Output**
- **Progressive Web App Interface**

## Tech Stack

### Backend
- **Framework**: FastAPI
- **AI Models**: ClinicalBERT, LangGraph for multi-step reasoning
- **Database**: MongoDB
- **Cloud**: AWS Lambda ready
- **API**: RESTful with real-time capabilities

### Frontend
- **Type**: Progressive Web App (PWA)
- **Interface**: Conversational UI
- **Features**: Offline capability, push notifications

## Project Structure

```
AI HealthCare Assistant/
├── backend/
│   ├── agents/              # Multi-agent AI system
│   ├── models/              # Data models and schemas
│   ├── utils/               # Utility functions
│   ├── data/                # Medical data and guidelines
│   ├── main.py             # FastAPI application
│   └── requirements.txt    # Python dependencies
├── frontend/               # Progressive Web App
└── README.md
```

## Getting Started

### Prerequisites
- Python 3.8+
- Node.js 16+
- MongoDB
- AWS Account (for deployment)

### Installation

1. Clone the repository
2. Install backend dependencies:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```
3. Install frontend dependencies:
   ```bash
   cd frontend
   npm install
   ```
4. Set up environment variables
5. Start the development servers

## Medical Disclaimer

⚠️ **IMPORTANT**: This application is for educational and informational purposes only. It should not be used as a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of qualified healthcare providers.

## Compliance

- Follows WHO guidelines
- Integrates CDC recommendations
- Implements explainable AI for regulatory compliance
- Designed with healthcare data privacy in mind

## License

This project is licensed under the MIT License - see the LICENSE file for details.
