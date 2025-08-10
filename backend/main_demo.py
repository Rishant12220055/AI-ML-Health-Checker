"""
Simplified main application for demonstration
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any
import uvicorn
import os
from datetime import datetime

# Simplified models
class SimpleSymptom(BaseModel):
    name: str
    severity: str
    duration: str = ""

class SimplePatientInfo(BaseModel):
    age: int
    gender: str
    medical_history: List[str] = []

class SimpleSymptomInput(BaseModel):
    symptoms: List[SimpleSymptom]
    patient_info: SimplePatientInfo
    chief_complaint: str

class SimpleCondition(BaseModel):
    name: str
    probability: float
    description: str

class SimpleDiagnosisResponse(BaseModel):
    session_id: str
    timestamp: str
    urgency_level: str
    possible_conditions: List[SimpleCondition]
    next_steps: List[str]
    disclaimer: str

# Create FastAPI app
app = FastAPI(
    title="AI Healthcare Assistant (Demo)",
    description="Simplified demo version of the healthcare AI assistant",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "message": "AI Healthcare Assistant Demo",
        "status": "running",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat()
    }

@app.post("/analyze-symptoms", response_model=SimpleDiagnosisResponse)
async def analyze_symptoms(symptom_input: SimpleSymptomInput):
    """
    Simplified symptom analysis (demo version)
    """
    try:
        # Simple mock analysis
        session_id = f"demo_{int(datetime.utcnow().timestamp())}"
        
        # Mock condition matching based on symptoms
        conditions = []
        symptom_names = [s.name.lower() for s in symptom_input.symptoms]
        
        # Simple rule-based matching
        if any("fever" in name for name in symptom_names):
            conditions.append(SimpleCondition(
                name="Viral Infection",
                probability=0.7,
                description="Common viral infection with fever"
            ))
        
        if any("headache" in name for name in symptom_names):
            conditions.append(SimpleCondition(
                name="Tension Headache",
                probability=0.6,
                description="Common tension-type headache"
            ))
        
        if any("cough" in name for name in symptom_names):
            conditions.append(SimpleCondition(
                name="Upper Respiratory Infection",
                probability=0.65,
                description="Upper respiratory tract infection"
            ))
        
        # Default condition if none match
        if not conditions:
            conditions.append(SimpleCondition(
                name="General Malaise",
                probability=0.4,
                description="General feeling of discomfort"
            ))
        
        # Determine urgency
        severities = [s.severity for s in symptom_input.symptoms]
        if "critical" in severities or "severe" in severities:
            urgency = "urgent"
        elif "moderate" in severities:
            urgency = "moderate"
        else:
            urgency = "low"
        
        # Generate response
        response = SimpleDiagnosisResponse(
            session_id=session_id,
            timestamp=datetime.utcnow().isoformat(),
            urgency_level=urgency,
            possible_conditions=conditions,
            next_steps=[
                "Monitor symptoms closely",
                "Stay hydrated and get rest",
                "Contact healthcare provider if symptoms worsen",
                "Seek immediate medical attention if emergency symptoms develop"
            ],
            disclaimer="This is a demo AI assessment for educational purposes only. Always consult healthcare professionals for medical advice."
        )
        
        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing symptoms: {str(e)}")

@app.post("/assess-urgency")
async def assess_urgency(data: Dict[str, List[str]]):
    """Quick urgency assessment"""
    symptoms = data.get("symptoms", [])
    
    # Simple urgency rules
    emergency_keywords = ["chest pain", "difficulty breathing", "severe bleeding"]
    urgent_keywords = ["high fever", "severe pain", "persistent vomiting"]
    
    for symptom in symptoms:
        if any(keyword in symptom.lower() for keyword in emergency_keywords):
            return {"urgency_level": "emergency", "symptoms": symptoms}
        elif any(keyword in symptom.lower() for keyword in urgent_keywords):
            return {"urgency_level": "urgent", "symptoms": symptoms}
    
    return {"urgency_level": "moderate", "symptoms": symptoms}

@app.get("/conditions/{condition_name}")
async def get_condition_info(condition_name: str):
    """Get mock condition information"""
    mock_conditions = {
        "viral_infection": {
            "name": "Viral Infection",
            "description": "Common viral infection affecting various body systems",
            "symptoms": ["fever", "fatigue", "body aches"],
            "treatment": "Rest, fluids, symptom management"
        },
        "tension_headache": {
            "name": "Tension Headache",
            "description": "Most common type of headache",
            "symptoms": ["head pain", "muscle tension"],
            "treatment": "Rest, hydration, over-the-counter pain relief"
        }
    }
    
    condition_key = condition_name.lower().replace(" ", "_")
    if condition_key in mock_conditions:
        return mock_conditions[condition_key]
    else:
        raise HTTPException(status_code=404, detail="Condition not found")

if __name__ == "__main__":
    print("🏥 Starting AI Healthcare Assistant Demo...")
    print("📋 API Documentation: http://localhost:8000/docs")
    print("💡 This is a simplified demo version")
    
    # Pass the app object directly and disable reload to avoid reloader exit issues
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=False,
        log_level="info"
    )
