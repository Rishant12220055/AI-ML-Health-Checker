from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any, Union
from datetime import datetime
from enum import Enum

class UrgencyLevel(str, Enum):
    """Urgency levels for medical conditions"""
    EMERGENCY = "emergency"
    URGENT = "urgent"
    MODERATE = "moderate"
    LOW = "low"

class Severity(str, Enum):
    """Symptom severity levels"""
    MILD = "mild"
    MODERATE = "moderate" 
    SEVERE = "severe"
    CRITICAL = "critical"

class Symptom(BaseModel):
    """Individual symptom model"""
    name: str = Field(..., description="Symptom name")
    severity: Severity = Field(..., description="Symptom severity")
    duration: Optional[str] = Field(None, description="How long symptom has been present")
    description: Optional[str] = Field(None, description="Additional symptom details")
    location: Optional[str] = Field(None, description="Body part/location if applicable")

class PatientInfo(BaseModel):
    """Patient demographic and basic info"""
    age: int = Field(..., ge=0, le=150, description="Patient age")
    gender: str = Field(..., description="Patient gender")
    medical_history: Optional[List[str]] = Field(default=[], description="Previous medical conditions")
    medications: Optional[List[str]] = Field(default=[], description="Current medications")
    allergies: Optional[List[str]] = Field(default=[], description="Known allergies")

class SymptomInput(BaseModel):
    """Input model for symptom analysis"""
    symptoms: List[Symptom] = Field(..., description="List of patient symptoms")
    patient_info: PatientInfo = Field(..., description="Patient information")
    chief_complaint: str = Field(..., description="Main reason for consultation")
    additional_notes: Optional[str] = Field(None, description="Any additional information")
    
    @validator('symptoms')
    def symptoms_not_empty(cls, v):
        if not v:
            raise ValueError('At least one symptom must be provided')
        return v

class Condition(BaseModel):
    """Medical condition model"""
    name: str = Field(..., description="Condition name")
    icd_code: Optional[str] = Field(None, description="ICD-10 code")
    probability: float = Field(..., ge=0, le=1, description="Probability of this condition")
    confidence: float = Field(..., ge=0, le=1, description="AI confidence in diagnosis")
    description: str = Field(..., description="Condition description")
    symptoms_match: List[str] = Field(..., description="Matching symptoms")
    risk_factors: List[str] = Field(default=[], description="Associated risk factors")

class Treatment(BaseModel):
    """Treatment recommendation model"""
    name: str = Field(..., description="Treatment name")
    type: str = Field(..., description="Treatment type (medication, procedure, lifestyle)")
    description: str = Field(..., description="Treatment description")
    dosage: Optional[str] = Field(None, description="Dosage information if applicable")
    duration: Optional[str] = Field(None, description="Treatment duration")
    side_effects: Optional[List[str]] = Field(default=[], description="Potential side effects")
    contraindications: Optional[List[str]] = Field(default=[], description="When not to use")
    who_guideline: Optional[str] = Field(None, description="WHO guideline reference")
    cdc_guideline: Optional[str] = Field(None, description="CDC guideline reference")

class DiagnosisExplanation(BaseModel):
    """Explainable AI output for diagnosis"""
    reasoning_steps: List[str] = Field(..., description="Step-by-step reasoning")
    evidence_supporting: List[str] = Field(..., description="Supporting evidence")
    evidence_against: List[str] = Field(default=[], description="Contradicting evidence")
    alternative_diagnoses: List[str] = Field(default=[], description="Other possibilities considered")
    confidence_factors: Dict[str, float] = Field(..., description="Factors affecting confidence")
    guidelines_used: List[str] = Field(default=[], description="Medical guidelines referenced")

class DiagnosisResponse(BaseModel):
    """Complete diagnosis response"""
    session_id: str = Field(..., description="Unique session identifier")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Analysis timestamp")
    urgency_level: UrgencyLevel = Field(..., description="Overall urgency assessment")
    
    # Multi-agent results
    symptom_classification: Dict[str, Any] = Field(..., description="Symptom classifier results")
    possible_conditions: List[Condition] = Field(..., description="Differential diagnosis")
    recommended_treatments: List[Treatment] = Field(..., description="Treatment recommendations")
    
    # Additional information
    next_steps: List[str] = Field(..., description="Recommended next steps")
    warning_signs: List[str] = Field(default=[], description="Warning signs to watch for")
    when_to_seek_care: str = Field(..., description="When to seek immediate care")
    
    # Explainable AI
    explanation: DiagnosisExplanation = Field(..., description="AI reasoning explanation")
    
    # Regulatory compliance
    disclaimer: str = Field(
        default="This AI assessment is for informational purposes only and should not replace professional medical advice.",
        description="Medical disclaimer"
    )

class HealthAssessment(BaseModel):
    """General health assessment model"""
    overall_score: float = Field(..., ge=0, le=100, description="Overall health score")
    risk_level: UrgencyLevel = Field(..., description="Overall risk level")
    recommendations: List[str] = Field(..., description="General health recommendations")
    follow_up_needed: bool = Field(..., description="Whether follow-up is recommended")

class ConsultationLog(BaseModel):
    """Model for logging consultations"""
    session_id: str = Field(..., description="Session identifier")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    symptoms_input: SymptomInput = Field(..., description="Original symptom input")
    diagnosis_response: DiagnosisResponse = Field(..., description="AI response")
    user_feedback: Optional[Dict[str, Any]] = Field(None, description="User feedback if provided")

class AgentResponse(BaseModel):
    """Response from individual AI agents"""
    agent_name: str = Field(..., description="Name of the agent")
    processing_time: float = Field(..., description="Processing time in seconds")
    confidence: float = Field(..., ge=0, le=1, description="Agent confidence")
    results: Dict[str, Any] = Field(..., description="Agent-specific results")
    errors: Optional[List[str]] = Field(default=[], description="Any errors encountered")

class SystemHealth(BaseModel):
    """System health status"""
    status: str = Field(..., description="Overall system status")
    database_connected: bool = Field(..., description="Database connection status")
    guidelines_loaded: bool = Field(..., description="Guidelines loading status")
    agents_ready: bool = Field(..., description="AI agents status")
    last_check: datetime = Field(default_factory=datetime.utcnow)

class HealthCheckResponse(BaseModel):
    """Enhanced health check response"""
    status: str = Field(..., description="System status")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    system_health: SystemHealth = Field(..., description="Detailed system health")
    performance_metrics: Optional[Dict[str, Any]] = Field(None, description="Performance metrics")
    active_sessions: int = Field(default=0, description="Number of active user sessions")
    uptime_hours: float = Field(default=0.0, description="System uptime in hours")
