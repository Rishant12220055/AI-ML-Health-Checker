"""
Symptom Classifier Agent

This agent is responsible for:
1. Validating and cleaning symptom inputs
2. Classifying symptoms by body system
3. Identifying symptom patterns and clusters
4. Extracting relevant medical features

The agent degrades gracefully when ML libraries (transformers, sentence-transformers,
torch, numpy) are unavailable; it falls back to rule-based classification only.
"""

import asyncio
from typing import List, Dict, Any, Tuple
import logging

# Optional heavy deps
try:
    from transformers import AutoTokenizer, AutoModel  # type: ignore
    import torch  # type: ignore
    TRANSFORMERS_AVAILABLE = True
except Exception:  # pragma: no cover
    AutoTokenizer = None  # type: ignore
    AutoModel = None  # type: ignore
    TRANSFORMERS_AVAILABLE = False

try:
    from sentence_transformers import SentenceTransformer  # type: ignore
    ST_AVAILABLE = True
except Exception:  # pragma: no cover
    SentenceTransformer = None  # type: ignore
    ST_AVAILABLE = False

try:
    import numpy as np  # type: ignore
    NP_AVAILABLE = True
except Exception:  # pragma: no cover
    np = None  # type: ignore
    NP_AVAILABLE = False

from models.schemas import Symptom, SymptomInput, AgentResponse

logger = logging.getLogger(__name__)

class SymptomClassifierAgent:
    """AI Agent for symptom classification and feature extraction"""
    
    def __init__(self):
        self.model_name = "emilyalsentzer/Bio_ClinicalBERT"
        self.tokenizer = None
        self.model = None
        self.sentence_transformer = None
        self.symptom_embeddings = {}
        self.available = False
        self.body_systems = {
            "cardiovascular": ["chest pain", "palpitations", "shortness of breath", "swelling"],
            "respiratory": ["cough", "shortness of breath", "wheezing", "chest tightness"],
            "gastrointestinal": ["nausea", "vomiting", "diarrhea", "abdominal pain"],
            "neurological": ["headache", "dizziness", "seizure", "weakness"],
            "musculoskeletal": ["joint pain", "muscle pain", "stiffness", "swelling"],
            "dermatological": ["rash", "itching", "redness", "lesions"],
            "genitourinary": ["painful urination", "frequency", "urgency", "blood in urine"],
            "endocrine": ["fatigue", "weight loss", "weight gain", "excessive thirst"],
            "infectious": ["fever", "chills", "fatigue", "body aches"]
        }
    
    async def initialize(self):
        """Initialize the ClinicalBERT model and sentence transformer"""
        try:
            logger.info("Initializing Symptom Classifier Agent...")
            if TRANSFORMERS_AVAILABLE:
                self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
                self.model = AutoModel.from_pretrained(self.model_name)
            else:
                logger.warning("Transformers not available; skipping ClinicalBERT load")

            if ST_AVAILABLE:
                self.sentence_transformer = SentenceTransformer('all-MiniLM-L6-v2')
                # Pre-compute embeddings for common symptoms
                await self._precompute_symptom_embeddings()
            else:
                logger.warning("sentence-transformers not available; skipping embeddings")

            self.available = True
            logger.info("Symptom Classifier Agent initialized (with fallbacks if needed)")
            
        except Exception as e:
            logger.error(f"Error initializing Symptom Classifier Agent: {e}")
            # Fallback to rule-based only
            self.available = False
    
    async def _precompute_symptom_embeddings(self):
        """Pre-compute embeddings for common medical symptoms"""
        common_symptoms = [
            "headache", "fever", "nausea", "vomiting", "diarrhea", "constipation",
            "chest pain", "shortness of breath", "cough", "fatigue", "dizziness",
            "abdominal pain", "back pain", "joint pain", "muscle pain", "rash",
            "sore throat", "runny nose", "congestion", "loss of appetite"
        ]
        
        if ST_AVAILABLE and self.sentence_transformer is not None:
            embeddings = self.sentence_transformer.encode(common_symptoms)
            self.symptom_embeddings = dict(zip(common_symptoms, embeddings))
        else:
            self.symptom_embeddings = {}
    
    async def process_symptoms(self, symptom_input: SymptomInput) -> AgentResponse:
        """
        Main processing function for symptom classification
        
        Args:
            symptom_input: Patient symptoms and information
            
        Returns:
            AgentResponse with classification results
        """
        start_time = asyncio.get_event_loop().time()
        
        try:
            # 1. Validate and clean symptoms
            cleaned_symptoms = await self._clean_and_validate_symptoms(symptom_input.symptoms)
            
            # 2. Classify symptoms by body system
            system_classification = await self._classify_by_body_system(cleaned_symptoms)
            
            # 3. Extract medical features
            medical_features = await self._extract_medical_features(symptom_input)
            
            # 4. Identify symptom patterns
            patterns = await self._identify_symptom_patterns(cleaned_symptoms)
            
            # 5. Calculate severity scores
            severity_scores = await self._calculate_severity_scores(cleaned_symptoms)
            
            # 6. Generate embeddings for symptoms
            symptom_embeddings = await self._generate_symptom_embeddings(cleaned_symptoms)
            
            processing_time = asyncio.get_event_loop().time() - start_time
            
            results = {
                "cleaned_symptoms": [symptom.model_dump() for symptom in cleaned_symptoms],
                "system_classification": system_classification,
                "medical_features": medical_features,
                "symptom_patterns": patterns,
                "severity_scores": severity_scores,
                "symptom_embeddings": (symptom_embeddings.tolist() if NP_AVAILABLE and hasattr(symptom_embeddings, 'tolist') else symptom_embeddings),
                "total_symptoms": len(cleaned_symptoms),
                "primary_systems_affected": list(system_classification.keys())[:3]
            }
            
            confidence = self._calculate_confidence(results)
            
            return AgentResponse(
                agent_name="SymptomClassifier",
                processing_time=processing_time,
                confidence=confidence,
                results=results,
                errors=[]
            )
            
        except Exception as e:
            processing_time = asyncio.get_event_loop().time() - start_time
            logger.error(f"Error in symptom classification: {e}")
            
            return AgentResponse(
                agent_name="SymptomClassifier",
                processing_time=processing_time,
                confidence=0.0,
                results={},
                errors=[str(e)]
            )
    
    async def _clean_and_validate_symptoms(self, symptoms: List[Symptom]) -> List[Symptom]:
        """Clean and validate symptom inputs"""
        cleaned_symptoms = []
        
        for symptom in symptoms:
            # Basic validation
            if not symptom.name or len(symptom.name.strip()) < 2:
                continue
                
            # Normalize symptom name
            normalized_name = symptom.name.lower().strip()
            
            # Create cleaned symptom
            cleaned_symptom = Symptom(
                name=normalized_name,
                severity=symptom.severity,
                duration=symptom.duration,
                description=symptom.description,
                location=symptom.location
            )
            
            cleaned_symptoms.append(cleaned_symptom)
        
        return cleaned_symptoms
    
    async def _classify_by_body_system(self, symptoms: List[Symptom]) -> Dict[str, List[str]]:
        """Classify symptoms by body system"""
        classification = {}
        
        for symptom in symptoms:
            symptom_name = symptom.name.lower()
            
            for system, system_symptoms in self.body_systems.items():
                # Check for direct matches or partial matches
                for system_symptom in system_symptoms:
                    if system_symptom in symptom_name or symptom_name in system_symptom:
                        if system not in classification:
                            classification[system] = []
                        if symptom.name not in classification[system]:
                            classification[system].append(symptom.name)
                        break
        
        return classification
    
    async def _extract_medical_features(self, symptom_input: SymptomInput) -> Dict[str, Any]:
        """Extract relevant medical features from symptoms and patient info"""
        features = {
            "patient_age": symptom_input.patient_info.age,
            "patient_gender": symptom_input.patient_info.gender,
            "has_medical_history": len(symptom_input.patient_info.medical_history) > 0,
            "takes_medications": len(symptom_input.patient_info.medications) > 0,
            "has_allergies": len(symptom_input.patient_info.allergies) > 0,
            "chief_complaint": symptom_input.chief_complaint,
            "symptom_count": len(symptom_input.symptoms),
            "severity_distribution": self._get_severity_distribution(symptom_input.symptoms),
            "duration_patterns": self._analyze_duration_patterns(symptom_input.symptoms)
        }
        
        return features
    
    def _get_severity_distribution(self, symptoms: List[Symptom]) -> Dict[str, int]:
        """Analyze severity distribution of symptoms"""
        distribution = {"mild": 0, "moderate": 0, "severe": 0, "critical": 0}
        
        for symptom in symptoms:
            sev = getattr(symptom.severity, 'value', symptom.severity)
            if sev in distribution:
                distribution[sev] += 1
        
        return distribution
    
    def _analyze_duration_patterns(self, symptoms: List[Symptom]) -> Dict[str, Any]:
        """Analyze duration patterns of symptoms"""
        durations = [symptom.duration for symptom in symptoms if symptom.duration]
        
        return {
            "has_duration_info": len(durations) > 0,
            "duration_count": len(durations),
            "acute_symptoms": len([d for d in durations if d and ("hour" in d or "day" in d)]),
            "chronic_symptoms": len([d for d in durations if d and ("week" in d or "month" in d or "year" in d)])
        }
    
    async def _identify_symptom_patterns(self, symptoms: List[Symptom]) -> Dict[str, Any]:
        """Identify patterns in symptom presentation"""
        patterns = {
            "symptom_clusters": [],
            "severity_patterns": [],
            "location_patterns": [],
            "temporal_patterns": []
        }
        
        # Identify symptom clusters (symptoms that commonly occur together)
        symptom_names = [s.name for s in symptoms]
        
        # Common symptom clusters
        clusters = {
            "flu_like": ["fever", "fatigue", "body aches", "headache"],
            "gi_upset": ["nausea", "vomiting", "diarrhea", "abdominal pain"],
            "respiratory": ["cough", "shortness of breath", "chest tightness"],
            "cardiac": ["chest pain", "palpitations", "shortness of breath"]
        }
        
        for cluster_name, cluster_symptoms in clusters.items():
            matches = len([s for s in symptom_names if any(cs in s for cs in cluster_symptoms)])
            if matches >= 2:
                patterns["symptom_clusters"].append({
                    "cluster": cluster_name,
                    "matches": matches,
                    "total_in_cluster": len(cluster_symptoms)
                })
        
        return patterns
    
    async def _calculate_severity_scores(self, symptoms: List[Symptom]) -> Dict[str, float]:
        """Calculate severity scores for symptoms"""
        severity_weights = {
            "mild": 1.0,
            "moderate": 2.0,
            "severe": 3.0,
            "critical": 4.0
        }
        
        if not symptoms:
            return {"overall_score": 0.0, "max_severity": 0.0, "avg_severity": 0.0}
        
        def sev_val(s):
            return getattr(s.severity, 'value', s.severity)
        scores = [severity_weights.get(sev_val(symptom), 1.0) for symptom in symptoms]
        
        return {
            "overall_score": sum(scores),
            "max_severity": max(scores),
            "avg_severity": sum(scores) / len(scores),
            "symptom_count": len(symptoms)
        }
    
    async def _generate_symptom_embeddings(self, symptoms: List[Symptom]) -> Any:
        """Generate embeddings for symptoms using sentence transformer"""
        if not symptoms or not ST_AVAILABLE or self.sentence_transformer is None or not NP_AVAILABLE:
            return []

        symptom_texts = [f"{s.name} {getattr(s.severity, 'value', s.severity)}" for s in symptoms]
        embeddings = self.sentence_transformer.encode(symptom_texts)

        # Return mean embedding as overall symptom representation
        return np.mean(embeddings, axis=0)
    
    def _calculate_confidence(self, results: Dict[str, Any]) -> float:
        """Calculate confidence score for the classification results"""
        confidence_factors = {
            "symptom_count": min(results.get("total_symptoms", 0) / 10.0, 1.0),
            "system_classification": min(len(results.get("system_classification", {})) / 3.0, 1.0),
            "severity_info": 1.0 if results.get("severity_scores", {}).get("overall_score", 0) > 0 else 0.5,
            "patterns_found": min(len(results.get("symptom_patterns", {}).get("symptom_clusters", [])) / 2.0, 1.0)
        }
        
        return sum(confidence_factors.values()) / len(confidence_factors)
    
    async def health_check(self) -> bool:
        """Check if the agent is ready and healthy"""
        # Healthy if either full ML stack is loaded or fallback rule-based is available
        return True
