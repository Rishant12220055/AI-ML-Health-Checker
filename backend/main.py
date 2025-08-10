from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import uvicorn
import os
from dotenv import load_dotenv
import logging

from agents.symptom_classifier import SymptomClassifierAgent
from agents.condition_matcher import ConditionMatcherAgent
from agents.treatment_retriever import TreatmentRetrieverAgent
from agents.coordinator import AgentCoordinator
from models.schemas import SymptomInput, DiagnosisResponse, HealthAssessment
from utils.database import DatabaseManager
from utils.medical_guidelines import MedicalGuidelinesManager
from api.enhanced_endpoints import get_enhanced_router

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Enhanced AI Healthcare Assistant",
    description="Multi-agent AI system with advanced safety, analytics, and uncertainty quantification",
    version="2.0.0-enhanced",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
db_manager = DatabaseManager()
guidelines_manager = MedicalGuidelinesManager()
agent_coordinator = AgentCoordinator(db_manager, guidelines_manager)

# Include enhanced API endpoints
app.include_router(get_enhanced_router())

@app.on_event("startup")
async def startup_event():
    """Initialize database connections and load models"""
    logger.info("Starting Enhanced AI Healthcare Assistant...")
    await db_manager.connect()
    await guidelines_manager.load_guidelines()
    await agent_coordinator.initialize_agents()
    
    # Initialize enhanced API components
    from api.enhanced_endpoints import initialize_enhanced_api
    await initialize_enhanced_api()
    
    logger.info("Enhanced AI Healthcare Assistant startup complete")

@app.on_event("shutdown")
async def shutdown_event():
    """Clean up resources"""
    await db_manager.disconnect()

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "Enhanced AI Healthcare Assistant",
        "status": "running",
        "version": "2.0.0-enhanced",
        "features": [
            "Emergency Detection & Triage",
            "Drug Interaction Checking", 
            "Advanced Risk Assessment",
            "Uncertainty Quantification",
            "Real-time Analytics",
            "Explainable AI"
        ],
        "api_docs": "/docs"
    }

@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "database": await db_manager.health_check(),
        "guidelines": guidelines_manager.is_loaded(),
        "agents": await agent_coordinator.health_check()
    }

@app.post("/analyze-symptoms", response_model=DiagnosisResponse)
async def analyze_symptoms(symptom_input: SymptomInput):
    """
    Analyze symptoms using multi-agent AI system
    
    This endpoint processes patient symptoms through three specialized agents:
    1. Symptom Classification Agent - categorizes and validates symptoms
    2. Condition Matching Agent - performs differential diagnosis
    3. Treatment Retrieval Agent - suggests treatments and urgency levels
    """
    try:
        # Process symptoms through multi-agent system
        analysis_result = await agent_coordinator.process_symptoms(symptom_input)
        
        # Log the interaction for medical record keeping
        await db_manager.log_consultation(symptom_input, analysis_result)
        
        return analysis_result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing symptoms: {str(e)}")

@app.post("/assess-urgency")
async def assess_urgency(symptoms: List[str]):
    """
    Quick urgency assessment for triage purposes
    """
    try:
        urgency_level = await agent_coordinator.assess_urgency(symptoms)
        return {"urgency_level": urgency_level, "symptoms": symptoms}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error assessing urgency: {str(e)}")

@app.get("/conditions/{condition_name}")
async def get_condition_info(condition_name: str):
    """
    Get detailed information about a specific medical condition
    """
    try:
        condition_info = await guidelines_manager.get_condition_info(condition_name)
        if not condition_info:
            raise HTTPException(status_code=404, detail="Condition not found")
        return condition_info
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving condition info: {str(e)}")

@app.get("/treatments/{condition_name}")
async def get_treatments(condition_name: str):
    """
    Get treatment guidelines for a specific condition
    """
    try:
        treatments = await guidelines_manager.get_treatment_guidelines(condition_name)
        if not treatments:
            raise HTTPException(status_code=404, detail="Treatment guidelines not found")
        return treatments
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving treatments: {str(e)}")

@app.post("/explain-diagnosis")
async def explain_diagnosis(diagnosis_id: str):
    """
    Get explainable AI output for a diagnosis (regulatory compliance)
    """
    try:
        explanation = await agent_coordinator.explain_diagnosis(diagnosis_id)
        return explanation
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating explanation: {str(e)}")

@app.get("/medical-guidelines/who")
async def get_who_guidelines():
    """
    Get WHO medical guidelines
    """
    try:
        guidelines = await guidelines_manager.get_who_guidelines()
        return guidelines
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving WHO guidelines: {str(e)}")

@app.get("/medical-guidelines/cdc")
async def get_cdc_guidelines():
    """
    Get CDC medical guidelines
    """
    try:
        guidelines = await guidelines_manager.get_cdc_guidelines()
        return guidelines
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving CDC guidelines: {str(e)}")

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler for better error reporting"""
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": "An unexpected error occurred. Please try again later.",
            "request_id": getattr(request.state, "request_id", None)
        }
    )

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
        reload=True,
        log_level="info"
    )
