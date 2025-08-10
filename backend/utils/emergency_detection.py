"""
Emergency Detection System for AI Healthcare Assistant

This module provides critical symptom detection, emergency alerts,
and safety protocols with improved urgency calibration.
"""

from typing import Dict, List, Any, Optional
from enum import Enum
from datetime import datetime
import logging
from models.schemas import Symptom, SymptomInput, UrgencyLevel

logger = logging.getLogger(__name__)

class SafetyAlert(str, Enum):
    EMERGENCY_911 = "emergency_911"
    URGENT_CARE = "urgent_care"
    DOCTOR_CONSULT = "doctor_consult"
    MONITOR_SYMPTOMS = "monitor_symptoms"

class EmergencyDetectionSystem:
    """System for detecting emergency medical conditions with improved urgency calibration"""
    
    def __init__(self):
        self.emergency_patterns = self._load_emergency_patterns()
        self.red_flag_symptoms = self._load_red_flag_symptoms()
        
    def _load_emergency_patterns(self) -> Dict[str, Dict[str, Any]]:
        """Load emergency symptom patterns with calibrated thresholds"""
        return {
            "acute_mi": {
                "name": "Acute Myocardial Infarction",
                "keywords": ["chest pain", "crushing pain", "chest pressure", "left arm pain", "jaw pain"],
                "associated": ["sweating", "nausea", "shortness of breath", "dizziness"],
                "severity_triggers": ["severe", "crushing", "intense", "10/10", "worst ever"],
                "action": SafetyAlert.EMERGENCY_911,
                "message": "🚨 CALL 911 IMMEDIATELY - Possible heart attack",
                "confidence_threshold": 0.4  # Increased threshold to reduce false positives
            },
            "stroke": {
                "name": "Stroke/TIA", 
                "keywords": ["face drooping", "arm weakness", "speech difficulty", "sudden headache", "sudden confusion"],
                "associated": ["dizziness", "vision loss", "confusion", "numbness"],
                "severity_triggers": ["sudden", "severe", "worst ever", "drooping"],
                "action": SafetyAlert.EMERGENCY_911,
                "message": "🚨 CALL 911 IMMEDIATELY - Possible stroke",
                "confidence_threshold": 0.3  # Keep lower for stroke detection
            },
            "severe_allergic_reaction": {
                "name": "Anaphylaxis",
                "keywords": ["difficulty breathing", "swelling throat", "hives", "rapid pulse", "severe rash"],
                "associated": ["dizziness", "nausea", "vomiting", "face swelling"],
                "severity_triggers": ["severe", "rapid", "difficulty", "swelling"],
                "action": SafetyAlert.EMERGENCY_911,
                "message": "🚨 CALL 911 IMMEDIATELY - Severe allergic reaction",
                "confidence_threshold": 0.4  # Increased threshold
            },
            "severe_breathing": {
                "name": "Severe Respiratory Distress",
                "keywords": ["can't breathe", "gasping", "blue lips", "choking", "chest tightness"],
                "associated": ["wheezing", "chest pain", "panic", "coughing blood"],
                "severity_triggers": ["severe", "can't", "unable", "gasping", "blue"],
                "action": SafetyAlert.EMERGENCY_911,
                "message": "🚨 CALL 911 IMMEDIATELY - Severe breathing difficulty", 
                "confidence_threshold": 0.3  # Keep low for breathing issues
            },
            "severe_abdominal": {
                "name": "Acute Abdomen",
                "keywords": ["severe abdominal pain", "stabbing pain", "rigid abdomen"],
                "associated": ["vomiting", "fever", "unable to move"],
                "severity_triggers": ["severe", "stabbing", "worst ever", "rigid"],
                "action": SafetyAlert.URGENT_CARE,  # Changed to URGENT_CARE instead of EMERGENCY_911
                "message": "⚠️ SEEK IMMEDIATE MEDICAL CARE - Severe abdominal condition",
                "confidence_threshold": 0.5  # Increased threshold
            },
            "head_trauma": {
                "name": "Head Injury",
                "keywords": ["head injury", "loss of consciousness", "severe headache", "confusion"],
                "associated": ["vomiting", "dizziness", "memory loss", "vision changes"],
                "severity_triggers": ["severe", "worst ever", "sudden", "loss of"],
                "action": SafetyAlert.EMERGENCY_911,
                "message": "🚨 CALL 911 IMMEDIATELY - Head injury",
                "confidence_threshold": 0.5  # Increased threshold to reduce false positives
            },
            "respiratory_infection": {
                "name": "Respiratory Infection",
                "keywords": ["persistent cough", "fever", "productive cough", "pneumonia"],
                "associated": ["fatigue", "body aches", "headache", "sputum"],
                "severity_triggers": ["persistent", "worsening", "high fever"],
                "action": SafetyAlert.DOCTOR_CONSULT,
                "message": "📞 CONTACT YOUR DOCTOR - Possible respiratory infection",
                "confidence_threshold": 0.4
            },
            "urinary_tract_infection": {
                "name": "Urinary Tract Infection",
                "keywords": ["dysuria", "burning urination", "frequent urination", "urinary urgency"],
                "associated": ["fever", "pelvic pain", "blood in urine"],
                "severity_triggers": ["burning", "painful", "frequent"],
                "action": SafetyAlert.DOCTOR_CONSULT,
                "message": "📞 CONTACT YOUR DOCTOR - Possible urinary tract infection",
                "confidence_threshold": 0.4
            }
        }
    
    def _load_red_flag_symptoms(self) -> List[str]:
        """Load red flag symptoms that require immediate attention"""
        return [
            "chest pain", "shortness of breath", "severe headache", 
            "loss of consciousness", "severe abdominal pain", "difficulty breathing",
            "face drooping", "speech difficulty", "blue lips", "can't breathe",
            "crushing pain", "sudden weakness", "severe bleeding"
        ]
    
    def detect_emergency(self, symptom_input: SymptomInput) -> Dict[str, Any]:
        """
        Detect emergency conditions with improved urgency calibration
        
        Returns:
            Dict containing urgency level, alerts, and recommendations
        """
        symptoms = symptom_input.symptoms
        chief_complaint = symptom_input.chief_complaint.lower()
        
        emergency_score = 0.0
        detected_emergencies = []
        safety_alerts = []
        urgency_level = UrgencyLevel.LOW
        
        # Check emergency patterns
        for pattern_id, pattern in self.emergency_patterns.items():
            score = self._calculate_pattern_match(symptoms, chief_complaint, pattern)
            
            if score >= pattern["confidence_threshold"]:
                detected_emergencies.append({
                    "pattern": pattern["name"],
                    "score": score,
                    "action": pattern["action"],
                    "message": pattern["message"]
                })
                
                emergency_score = max(emergency_score, score)
                
                # Improved urgency calibration based on action type
                if pattern["action"] == SafetyAlert.EMERGENCY_911:
                    urgency_level = UrgencyLevel.EMERGENCY
                elif pattern["action"] == SafetyAlert.URGENT_CARE and urgency_level != UrgencyLevel.EMERGENCY:
                    urgency_level = UrgencyLevel.URGENT
                elif urgency_level == UrgencyLevel.LOW:
                    urgency_level = UrgencyLevel.MODERATE
        
        # Check for severity escalation
        if self._check_severity_escalation(symptoms):
            if urgency_level == UrgencyLevel.LOW:
                urgency_level = UrgencyLevel.MODERATE
            emergency_score += 0.2
        
        # Generate safety alerts based on urgency level
        if urgency_level == UrgencyLevel.EMERGENCY:
            safety_alerts.append({
                "type": SafetyAlert.EMERGENCY_911,
                "message": "🚨 CALL 911 IMMEDIATELY - Critical emergency detected",
                "priority": "IMMEDIATE"
            })
        elif urgency_level == UrgencyLevel.URGENT:
            safety_alerts.append({
                "type": SafetyAlert.URGENT_CARE,
                "message": "⚠️ SEEK IMMEDIATE MEDICAL CARE - Urgent condition detected",
                "priority": "URGENT"
            })
        elif urgency_level == UrgencyLevel.MODERATE:
            safety_alerts.append({
                "type": SafetyAlert.DOCTOR_CONSULT,
                "message": "📞 CONTACT YOUR DOCTOR - Medical evaluation recommended",
                "priority": "SAME_DAY"
            })
        else:
            safety_alerts.append({
                "type": SafetyAlert.MONITOR_SYMPTOMS,
                "message": "👁️ MONITOR SYMPTOMS - Watch for changes",
                "priority": "ROUTINE"
            })
        
        return {
            "urgency_level": urgency_level,
            "emergency_score": emergency_score,
            "detected_emergencies": detected_emergencies,
            "safety_alerts": safety_alerts,
            "requires_immediate_care": urgency_level in [UrgencyLevel.EMERGENCY, UrgencyLevel.URGENT],
            "timestamp": datetime.now().isoformat()
        }
    
    def _calculate_pattern_match(self, symptoms: List[Symptom], chief_complaint: str, pattern: Dict) -> float:
        """Calculate how well symptoms match an emergency pattern"""
        keyword_matches = 0
        severity_bonus = 0
        associated_matches = 0
        
        # Combine all symptom text
        all_symptom_text = chief_complaint + " "
        for symptom in symptoms:
            all_symptom_text += f"{symptom.name} {symptom.description} {symptom.severity} ".lower()
        
        # Check keyword matches - require exact phrase match for better precision
        for keyword in pattern["keywords"]:
            if keyword.lower() in all_symptom_text:
                keyword_matches += 1
        
        # Only proceed if we have some keyword matches
        if keyword_matches == 0:
            return 0.0
        
        # Check severity triggers for bonus scoring
        for trigger in pattern.get("severity_triggers", []):
            if trigger.lower() in all_symptom_text:
                severity_bonus += 0.2  # Reduced bonus to prevent over-escalation
        
        # Check associated symptoms  
        for associated in pattern.get("associated", []):
            if associated.lower() in all_symptom_text:
                associated_matches += 1
        
        # Calculate score with improved weighting - require higher keyword match ratio
        keyword_score = keyword_matches / len(pattern["keywords"]) if pattern["keywords"] else 0
        associated_score = associated_matches / len(pattern.get("associated", [1])) * 0.2  # Reduced weight
        
        # Require at least 60% keyword match for emergency patterns, 40% for others
        if pattern.get("action") == SafetyAlert.EMERGENCY_911 and keyword_score < 0.6:
            return 0.0
        elif pattern.get("action") == SafetyAlert.DOCTOR_CONSULT and keyword_score < 0.4:
            return 0.0
        
        total_score = keyword_score + severity_bonus + associated_score
        return min(total_score, 1.0)  # Cap at 1.0
    
    def _check_severity_escalation(self, symptoms: List[Symptom]) -> bool:
        """Check if symptoms indicate severe condition requiring escalation"""
        severe_keywords = ["severe", "unbearable", "worst ever", "10/10", "crushing", "sharp"]
        moderate_escalation_keywords = ["persistent", "worsening", "fever", "productive", "burning"]
        
        # Check for severe symptoms that require escalation
        for symptom in symptoms:
            if symptom.severity in ["severe", "critical"]:
                return True
            
            symptom_text = f"{symptom.name} {symptom.description}".lower()
            for keyword in severe_keywords:
                if keyword in symptom_text:
                    return True
        
        # Check for moderate symptoms that suggest medical attention needed
        moderate_symptom_count = 0
        for symptom in symptoms:
            if symptom.severity in ["moderate"]:
                moderate_symptom_count += 1
            
            symptom_text = f"{symptom.name} {symptom.description}".lower()
            for keyword in moderate_escalation_keywords:
                if keyword in symptom_text:
                    moderate_symptom_count += 0.5
        
        # If multiple moderate symptoms, escalate to moderate urgency
        return moderate_symptom_count >= 2.0

# Global instance
emergency_detector = EmergencyDetectionSystem()

def detect_emergency_conditions(symptom_input: SymptomInput) -> Dict[str, Any]:
    """Main function to detect emergency conditions"""
    return emergency_detector.detect_emergency(symptom_input)
