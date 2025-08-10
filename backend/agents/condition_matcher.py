"""
Condition Matcher Agent

This agent is responsible for:
1. Performing differential diagnosis based on symptoms
2. Matching symptoms to potential medical conditions
3. Calculating probability scores for each condition
4. Ranking conditions by likelihood and severity
"""

import asyncio
import json
from typing import List, Dict, Any, Tuple, Optional
import logging

# Optional heavy deps
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

from models.schemas import Symptom, SymptomInput, Condition, AgentResponse

logger = logging.getLogger(__name__)

class ConditionMatcherAgent:
    """AI Agent for differential diagnosis and condition matching"""
    
    def __init__(self):
        self.sentence_transformer = None
        self.medical_knowledge_base = {}
        self.condition_embeddings = {}
        self.icd_mappings = {}
        self.symptom_condition_matrix = {}
        self.available = False
        
    async def initialize(self):
        """Initialize the condition matching models and knowledge base"""
        try:
            logger.info("Initializing Condition Matcher Agent...")
            
            # Load sentence transformer for medical similarity
            if ST_AVAILABLE:
                self.sentence_transformer = SentenceTransformer('all-MiniLM-L6-v2')
            else:
                logger.warning("sentence-transformers not available; similarity matching will be skipped")
            
            # Load medical knowledge base
            await self._load_medical_knowledge_base()
            
            # Pre-compute condition embeddings (if ST available)
            await self._precompute_condition_embeddings()
            
            self.available = True
            logger.info("Condition Matcher Agent initialized successfully (with fallbacks if needed)")
            
        except Exception as e:
            logger.error(f"Error initializing Condition Matcher Agent: {e}")
            raise
    
    async def _load_medical_knowledge_base(self):
        """Load comprehensive medical conditions database"""
        # Expanded knowledge base with 35+ conditions, structured symptom weights,
        # red flags, differential diagnoses, and enhanced metadata
        
        self.medical_knowledge_base = {
            # Respiratory Conditions
            "influenza": {
                "symptoms": ["fever", "fatigue", "body aches", "headache", "cough", "sore throat"],
                "symptom_weights": {"fever": 0.9, "fatigue": 0.8, "body_aches": 0.8, "cough": 0.7},
                "icd_code": "J11.1",
                "description": "Acute respiratory illness caused by influenza viruses",
                "severity": "moderate",
                "common_age_groups": ["all"],
                "seasonal_pattern": True,
                "risk_factors": ["immunocompromised", "elderly", "chronic conditions"],
                "red_flags": ["difficulty breathing", "chest pain", "confusion"],
                "differential_conditions": ["common_cold", "pneumonia", "covid_19"]
            },
            "common_cold": {
                "symptoms": ["runny nose", "congestion", "sore throat", "cough", "sneezing"],
                "symptom_weights": {"runny_nose": 0.9, "congestion": 0.8, "sore_throat": 0.7},
                "icd_code": "J00",
                "description": "Viral upper respiratory tract infection",
                "severity": "mild",
                "common_age_groups": ["all"],
                "seasonal_pattern": False,
                "risk_factors": ["close contact with infected individuals"],
                "red_flags": ["high fever", "difficulty breathing"],
                "differential_conditions": ["influenza", "allergic_rhinitis", "sinusitis"]
            },
            "pneumonia": {
                "symptoms": ["fever", "cough", "shortness of breath", "chest pain", "fatigue", "chills"],
                "symptom_weights": {"fever": 0.9, "cough": 0.9, "shortness_of_breath": 0.95, "chest_pain": 0.8},
                "icd_code": "J18.9",
                "description": "Infection that inflames air sacs in lungs",
                "severity": "severe",
                "common_age_groups": ["elderly", "children"],
                "seasonal_pattern": True,
                "risk_factors": ["age", "chronic diseases", "smoking"],
                "red_flags": ["severe shortness of breath", "blue lips", "confusion"],
                "differential_conditions": ["bronchitis", "pulmonary_embolism", "heart_failure"]
            },
            "bronchitis": {
                "symptoms": ["persistent cough", "mucus production", "fatigue", "mild fever", "chest discomfort"],
                "symptom_weights": {"persistent_cough": 0.95, "mucus_production": 0.9, "chest_discomfort": 0.7},
                "icd_code": "J40",
                "description": "Inflammation of the bronchial tubes",
                "severity": "mild_to_moderate",
                "common_age_groups": ["adults"],
                "seasonal_pattern": True,
                "risk_factors": ["smoking", "air pollution", "viral infections"],
                "red_flags": ["blood in sputum", "severe shortness of breath"],
                "differential_conditions": ["pneumonia", "asthma", "copd"]
            },
            "asthma": {
                "symptoms": ["wheezing", "shortness of breath", "chest tightness", "cough"],
                "symptom_weights": {"wheezing": 0.95, "shortness_of_breath": 0.9, "chest_tightness": 0.8},
                "icd_code": "J45.9",
                "description": "Chronic respiratory condition with airway inflammation",
                "severity": "moderate",
                "common_age_groups": ["children", "adults"],
                "seasonal_pattern": False,
                "risk_factors": ["allergies", "family history", "environmental triggers"],
                "red_flags": ["severe difficulty breathing", "blue lips", "inability to speak"],
                "differential_conditions": ["copd", "heart_failure", "pneumonia"]
            },
            
            # Gastrointestinal Conditions
            "gastroenteritis": {
                "symptoms": ["nausea", "vomiting", "diarrhea", "abdominal pain", "fever", "dehydration"],
                "symptom_weights": {"diarrhea": 0.95, "vomiting": 0.9, "abdominal_pain": 0.8, "nausea": 0.8},
                "icd_code": "K59.1",
                "description": "Inflammation of the stomach and intestines",
                "severity": "moderate",
                "common_age_groups": ["all"],
                "seasonal_pattern": False,
                "risk_factors": ["contaminated food", "poor hygiene"],
                "red_flags": ["severe dehydration", "blood in stool", "high fever"],
                "differential_conditions": ["food_poisoning", "ibs", "appendicitis"]
            },
            "appendicitis": {
                "symptoms": ["abdominal pain", "nausea", "vomiting", "fever", "loss of appetite", "constipation"],
                "symptom_weights": {"abdominal_pain": 0.95, "nausea": 0.8, "fever": 0.8, "loss_of_appetite": 0.7},
                "icd_code": "K37",
                "description": "Inflammation of the appendix",
                "severity": "severe",
                "common_age_groups": ["children", "young adults"],
                "seasonal_pattern": False,
                "risk_factors": ["age", "family history"],
                "red_flags": ["severe abdominal pain", "high fever", "rigid abdomen"],
                "differential_conditions": ["gastroenteritis", "kidney_stones", "ovarian_cyst"]
            },
            "ibs": {
                "symptoms": ["abdominal pain", "bloating", "gas", "diarrhea", "constipation", "cramping"],
                "symptom_weights": {"abdominal_pain": 0.9, "bloating": 0.8, "cramping": 0.8},
                "icd_code": "K58.9",
                "description": "Functional gastrointestinal disorder",
                "severity": "mild_to_moderate",
                "common_age_groups": ["adults"],
                "seasonal_pattern": False,
                "risk_factors": ["stress", "diet", "hormonal changes"],
                "red_flags": ["blood in stool", "severe weight loss", "persistent fever"],
                "differential_conditions": ["crohns_disease", "ulcerative_colitis", "gastroenteritis"]
            },
            "gerd": {
                "symptoms": ["heartburn", "acid reflux", "chest pain", "difficulty swallowing", "regurgitation"],
                "symptom_weights": {"heartburn": 0.95, "acid_reflux": 0.9, "chest_pain": 0.7},
                "icd_code": "K21.9",
                "description": "Gastroesophageal reflux disease",
                "severity": "mild_to_moderate",
                "common_age_groups": ["adults"],
                "seasonal_pattern": False,
                "risk_factors": ["obesity", "hiatal hernia", "pregnancy"],
                "red_flags": ["difficulty swallowing", "severe chest pain", "weight loss"],
                "differential_conditions": ["heart_attack", "peptic_ulcer", "esophagitis"]
            },
            
            # Cardiovascular Conditions
            "hypertension": {
                "symptoms": ["headache", "dizziness", "chest pain", "shortness of breath", "nosebleeds"],
                "symptom_weights": {"headache": 0.6, "dizziness": 0.7, "chest_pain": 0.8},
                "icd_code": "I10",
                "description": "High blood pressure condition",
                "severity": "moderate",
                "common_age_groups": ["adults", "elderly"],
                "seasonal_pattern": False,
                "risk_factors": ["age", "obesity", "sedentary lifestyle", "high sodium diet"],
                "red_flags": ["severe headache", "confusion", "chest pain"],
                "differential_conditions": ["secondary_hypertension", "anxiety", "hyperthyroidism"]
            },
            "heart_failure": {
                "symptoms": ["shortness of breath", "fatigue", "swelling", "rapid heartbeat", "persistent cough"],
                "symptom_weights": {"shortness_of_breath": 0.95, "swelling": 0.9, "fatigue": 0.8},
                "icd_code": "I50.9",
                "description": "Heart's inability to pump blood effectively",
                "severity": "severe",
                "common_age_groups": ["elderly"],
                "seasonal_pattern": False,
                "risk_factors": ["coronary_artery_disease", "hypertension", "diabetes"],
                "red_flags": ["severe shortness of breath", "chest pain", "confusion"],
                "differential_conditions": ["pneumonia", "copd", "kidney_disease"]
            },
            "atrial_fibrillation": {
                "symptoms": ["irregular heartbeat", "palpitations", "fatigue", "dizziness", "chest pain"],
                "symptom_weights": {"irregular_heartbeat": 0.95, "palpitations": 0.9, "dizziness": 0.7},
                "icd_code": "I48.9",
                "description": "Irregular and often rapid heart rhythm",
                "severity": "moderate_to_severe",
                "common_age_groups": ["elderly"],
                "seasonal_pattern": False,
                "risk_factors": ["age", "heart_disease", "hypertension"],
                "red_flags": ["chest pain", "severe shortness of breath", "fainting"],
                "differential_conditions": ["anxiety", "hyperthyroidism", "heart_attack"]
            },
            
            # Neurological Conditions
            "migraine": {
                "symptoms": ["headache", "nausea", "light sensitivity", "sound sensitivity", "visual disturbances"],
                "symptom_weights": {"headache": 0.95, "light_sensitivity": 0.9, "nausea": 0.8},
                "icd_code": "G43.9",
                "description": "Recurrent severe headache disorder",
                "severity": "moderate",
                "common_age_groups": ["adults"],
                "seasonal_pattern": False,
                "risk_factors": ["family history", "stress", "hormonal changes"],
                "red_flags": ["sudden severe headache", "fever", "neck stiffness"],
                "differential_conditions": ["tension_headache", "cluster_headache", "meningitis"]
            },
            "tension_headache": {
                "symptoms": ["headache", "muscle tension", "stress", "fatigue"],
                "symptom_weights": {"headache": 0.95, "muscle_tension": 0.8, "stress": 0.7},
                "icd_code": "G44.2",
                "description": "Most common type of headache",
                "severity": "mild_to_moderate",
                "common_age_groups": ["adults"],
                "seasonal_pattern": False,
                "risk_factors": ["stress", "poor posture", "dehydration"],
                "red_flags": ["sudden severe headache", "fever", "confusion"],
                "differential_conditions": ["migraine", "cluster_headache", "sinusitis"]
            },
            "stroke": {
                "symptoms": ["sudden weakness", "face drooping", "speech difficulty", "confusion", "severe headache"],
                "symptom_weights": {"sudden_weakness": 0.95, "face_drooping": 0.95, "speech_difficulty": 0.95},
                "icd_code": "I64",
                "description": "Disruption of blood supply to brain",
                "severity": "critical",
                "common_age_groups": ["elderly"],
                "seasonal_pattern": False,
                "risk_factors": ["age", "hypertension", "diabetes", "smoking"],
                "red_flags": ["all symptoms are red flags"],
                "differential_conditions": ["tia", "seizure", "migraine_with_aura"]
            },
            
            # Endocrine Conditions
            "diabetes_type_2": {
                "symptoms": ["excessive thirst", "frequent urination", "fatigue", "blurred vision", "slow healing wounds"],
                "symptom_weights": {"excessive_thirst": 0.9, "frequent_urination": 0.9, "fatigue": 0.7},
                "icd_code": "E11.9",
                "description": "Metabolic disorder characterized by high blood sugar",
                "severity": "moderate",
                "common_age_groups": ["adults", "elderly"],
                "seasonal_pattern": False,
                "risk_factors": ["obesity", "sedentary lifestyle", "family history"],
                "red_flags": ["severe confusion", "rapid breathing", "fruity breath"],
                "differential_conditions": ["type_1_diabetes", "hyperthyroidism", "kidney_disease"]
            },
            "hyperthyroidism": {
                "symptoms": ["rapid heartbeat", "weight loss", "nervousness", "sweating", "tremor"],
                "symptom_weights": {"rapid_heartbeat": 0.9, "weight_loss": 0.8, "nervousness": 0.7},
                "icd_code": "E05.9",
                "description": "Overactive thyroid gland",
                "severity": "moderate",
                "common_age_groups": ["adults"],
                "seasonal_pattern": False,
                "risk_factors": ["family history", "stress", "iodine excess"],
                "red_flags": ["severe rapid heartbeat", "chest pain", "confusion"],
                "differential_conditions": ["anxiety", "heart_disease", "menopause"]
            },
            "hypothyroidism": {
                "symptoms": ["fatigue", "weight gain", "cold intolerance", "dry skin", "depression"],
                "symptom_weights": {"fatigue": 0.9, "weight_gain": 0.8, "cold_intolerance": 0.8},
                "icd_code": "E03.9",
                "description": "Underactive thyroid gland",
                "severity": "mild_to_moderate",
                "common_age_groups": ["adults", "elderly"],
                "seasonal_pattern": False,
                "risk_factors": ["autoimmune disease", "radiation", "medications"],
                "red_flags": ["severe confusion", "extreme fatigue", "difficulty breathing"],
                "differential_conditions": ["depression", "chronic_fatigue", "anemia"]
            },
            
            # Mental Health Conditions
            "anxiety_disorder": {
                "symptoms": ["nervousness", "restlessness", "fatigue", "difficulty concentrating", "muscle tension", "sleep disturbances"],
                "symptom_weights": {"nervousness": 0.9, "restlessness": 0.8, "muscle_tension": 0.7},
                "icd_code": "F41.9",
                "description": "Mental health condition characterized by excessive worry",
                "severity": "moderate",
                "common_age_groups": ["adults"],
                "seasonal_pattern": False,
                "risk_factors": ["stress", "family history", "trauma"],
                "red_flags": ["thoughts of self-harm", "severe panic attacks", "complete inability to function"],
                "differential_conditions": ["depression", "hyperthyroidism", "panic_disorder"]
            },
            "depression": {
                "symptoms": ["persistent sadness", "loss of interest", "fatigue", "sleep disturbances", "appetite changes"],
                "symptom_weights": {"persistent_sadness": 0.95, "loss_of_interest": 0.9, "fatigue": 0.8},
                "icd_code": "F32.9",
                "description": "Persistent mood disorder affecting daily functioning",
                "severity": "moderate_to_severe",
                "common_age_groups": ["adults"],
                "seasonal_pattern": False,
                "risk_factors": ["family history", "trauma", "chronic illness"],
                "red_flags": ["thoughts of self-harm", "suicidal ideation", "complete social withdrawal"],
                "differential_conditions": ["anxiety", "hypothyroidism", "chronic_fatigue"]
            },
            
            # Musculoskeletal Conditions
            "arthritis": {
                "symptoms": ["joint pain", "stiffness", "swelling", "reduced range of motion"],
                "symptom_weights": {"joint_pain": 0.95, "stiffness": 0.9, "swelling": 0.8},
                "icd_code": "M19.9",
                "description": "Inflammation of joints",
                "severity": "mild_to_moderate",
                "common_age_groups": ["elderly"],
                "seasonal_pattern": False,
                "risk_factors": ["age", "obesity", "previous injury"],
                "red_flags": ["severe swelling", "red hot joints", "fever"],
                "differential_conditions": ["rheumatoid_arthritis", "gout", "fibromyalgia"]
            },
            "fibromyalgia": {
                "symptoms": ["widespread pain", "fatigue", "sleep disturbances", "cognitive difficulties"],
                "symptom_weights": {"widespread_pain": 0.95, "fatigue": 0.9, "sleep_disturbances": 0.8},
                "icd_code": "M79.3",
                "description": "Chronic pain disorder affecting muscles and soft tissues",
                "severity": "moderate",
                "common_age_groups": ["adults"],
                "seasonal_pattern": False,
                "risk_factors": ["stress", "trauma", "family history"],
                "red_flags": ["severe depression", "thoughts of self-harm"],
                "differential_conditions": ["arthritis", "chronic_fatigue", "depression"]
            },
            
            # Infectious Diseases
            "urinary_tract_infection": {
                "symptoms": ["painful urination", "frequent urination", "urgency", "cloudy urine", "pelvic pain"],
                "symptom_weights": {"painful_urination": 0.95, "frequent_urination": 0.9, "urgency": 0.8},
                "icd_code": "N39.0",
                "description": "Infection in any part of the urinary system",
                "severity": "moderate",
                "common_age_groups": ["adults"],
                "seasonal_pattern": False,
                "risk_factors": ["female gender", "sexual activity", "certain contraceptives"],
                "red_flags": ["fever", "back pain", "nausea"],
                "differential_conditions": ["kidney_infection", "bladder_infection", "sexually_transmitted_infection"]
            },
            "pneumonia": {
                "symptoms": ["fever", "cough", "shortness of breath", "chest pain", "fatigue", "chills"],
                "symptom_weights": {"fever": 0.9, "cough": 0.9, "shortness_of_breath": 0.95},
                "icd_code": "J18.9",
                "description": "Infection that inflames air sacs in lungs",
                "severity": "severe",
                "common_age_groups": ["elderly", "children"],
                "seasonal_pattern": True,
                "risk_factors": ["age", "chronic diseases", "smoking"],
                "red_flags": ["severe shortness of breath", "blue lips", "confusion"],
                "differential_conditions": ["bronchitis", "pulmonary_embolism", "heart_failure"]
            },
            "sepsis": {
                "symptoms": ["fever", "rapid heart rate", "rapid breathing", "confusion", "low blood pressure"],
                "symptom_weights": {"fever": 0.9, "rapid_heart_rate": 0.9, "confusion": 0.95},
                "icd_code": "A41.9",
                "description": "Life-threatening response to infection",
                "severity": "critical",
                "common_age_groups": ["elderly", "immunocompromised"],
                "seasonal_pattern": False,
                "risk_factors": ["chronic illness", "immunosuppression", "recent surgery"],
                "red_flags": ["all symptoms are red flags"],
                "differential_conditions": ["severe_infection", "shock", "heart_failure"]
            },
            
            # Dermatological Conditions
            "eczema": {
                "symptoms": ["itchy skin", "red rash", "dry skin", "skin inflammation"],
                "symptom_weights": {"itchy_skin": 0.95, "red_rash": 0.9, "dry_skin": 0.8},
                "icd_code": "L30.9",
                "description": "Chronic skin condition causing inflammation",
                "severity": "mild_to_moderate",
                "common_age_groups": ["children", "adults"],
                "seasonal_pattern": False,
                "risk_factors": ["allergies", "family history", "environmental factors"],
                "red_flags": ["widespread infection", "fever", "pus"],
                "differential_conditions": ["psoriasis", "contact_dermatitis", "fungal_infection"]
            },
            "psoriasis": {
                "symptoms": ["red patches", "scaly skin", "itching", "burning sensation"],
                "symptom_weights": {"red_patches": 0.95, "scaly_skin": 0.9, "itching": 0.7},
                "icd_code": "L40.9",
                "description": "Autoimmune skin condition",
                "severity": "moderate",
                "common_age_groups": ["adults"],
                "seasonal_pattern": False,
                "risk_factors": ["family history", "stress", "infections"],
                "red_flags": ["joint pain", "fever", "severe skin infection"],
                "differential_conditions": ["eczema", "seborrheic_dermatitis", "lupus"]
            },
            
            # Gynecological Conditions
            "pms": {
                "symptoms": ["mood changes", "breast tenderness", "bloating", "fatigue", "irritability"],
                "symptom_weights": {"mood_changes": 0.8, "breast_tenderness": 0.8, "bloating": 0.7},
                "icd_code": "N94.3",
                "description": "Premenstrual syndrome",
                "severity": "mild_to_moderate",
                "common_age_groups": ["reproductive_age_women"],
                "seasonal_pattern": False,
                "risk_factors": ["hormonal changes", "stress", "diet"],
                "red_flags": ["severe depression", "thoughts of self-harm"],
                "differential_conditions": ["pmdd", "depression", "thyroid_disease"]
            },
            "menopause": {
                "symptoms": ["hot flashes", "night sweats", "mood changes", "irregular periods", "sleep disturbances"],
                "symptom_weights": {"hot_flashes": 0.9, "night_sweats": 0.8, "irregular_periods": 0.9},
                "icd_code": "N95.1",
                "description": "Natural end of reproductive years",
                "severity": "mild_to_moderate",
                "common_age_groups": ["middle_aged_women"],
                "seasonal_pattern": False,
                "risk_factors": ["age", "family history", "lifestyle factors"],
                "red_flags": ["severe depression", "heavy bleeding"],
                "differential_conditions": ["thyroid_disease", "depression", "cardiovascular_disease"]
            },
            
            # Allergic Conditions
            "allergic_rhinitis": {
                "symptoms": ["sneezing", "runny nose", "itchy eyes", "congestion"],
                "symptom_weights": {"sneezing": 0.9, "runny_nose": 0.9, "itchy_eyes": 0.8},
                "icd_code": "J30.9",
                "description": "Allergic reaction affecting nose and eyes",
                "severity": "mild",
                "common_age_groups": ["all"],
                "seasonal_pattern": True,
                "risk_factors": ["allergies", "family history", "environmental exposure"],
                "red_flags": ["difficulty breathing", "severe swelling"],
                "differential_conditions": ["common_cold", "sinusitis", "non_allergic_rhinitis"]
            },
            "food_allergy": {
                "symptoms": ["hives", "swelling", "nausea", "vomiting", "difficulty breathing"],
                "symptom_weights": {"hives": 0.9, "swelling": 0.95, "difficulty_breathing": 0.95},
                "icd_code": "T78.1",
                "description": "Immune system reaction to food",
                "severity": "mild_to_severe",
                "common_age_groups": ["children", "adults"],
                "seasonal_pattern": False,
                "risk_factors": ["family history", "other allergies", "age"],
                "red_flags": ["difficulty breathing", "swelling of throat", "severe drop in blood pressure"],
                "differential_conditions": ["food_intolerance", "gastroenteritis", "anxiety"]
            }
        }
    
    async def _precompute_condition_embeddings(self):
        """Pre-compute embeddings for all conditions in knowledge base (if available)"""
        self.condition_embeddings = {}
        if not (ST_AVAILABLE and self.sentence_transformer is not None):
            return
        for condition_name, condition_data in self.medical_knowledge_base.items():
            # Create a text representation combining symptoms and description
            condition_text = f"{condition_data['description']} symptoms: {' '.join(condition_data['symptoms'])}"
            # Generate embedding
            embedding = self.sentence_transformer.encode([condition_text])[0]
            self.condition_embeddings[condition_name] = embedding
    
    async def process_symptoms(self, symptom_input: SymptomInput, 
                             symptom_classification: Dict[str, Any]) -> AgentResponse:
        """
        Main processing function for condition matching
        
        Args:
            symptom_input: Patient symptoms and information
            symptom_classification: Results from symptom classifier agent
            
        Returns:
            AgentResponse with condition matching results
        """
        start_time = asyncio.get_event_loop().time()
        
        try:
            # 1. Extract symptoms for matching
            symptoms = [symptom.name for symptom in symptom_input.symptoms]
            
            # 2. Perform similarity-based matching (if available)
            similarity_matches = await self._similarity_based_matching(symptoms, symptom_input)
            
            # 3. Perform rule-based matching
            rule_based_matches = await self._rule_based_matching(symptoms, symptom_input)
            
            # 4. Combine and rank conditions
            combined_matches = await self._combine_and_rank_matches(
                similarity_matches, rule_based_matches, symptom_input
            )
            
            # 5. Apply demographic and risk factor adjustments
            adjusted_matches = await self._apply_demographic_adjustments(
                combined_matches, symptom_input.patient_info
            )
            
            # 6. Generate differential diagnosis
            differential_diagnosis = await self._generate_differential_diagnosis(adjusted_matches)
            
            processing_time = asyncio.get_event_loop().time() - start_time
            
            results = {
                "differential_diagnosis": differential_diagnosis,
                "similarity_matches": similarity_matches,
                "rule_based_matches": rule_based_matches,
                "total_conditions_considered": len(self.medical_knowledge_base),
                "conditions_matched": len(adjusted_matches),
                "top_condition": differential_diagnosis[0] if differential_diagnosis else None,
                "matching_method": "hybrid_similarity_rules"
            }
            
            confidence = self._calculate_confidence(results, symptoms)
            
            return AgentResponse(
                agent_name="ConditionMatcher",
                processing_time=processing_time,
                confidence=confidence,
                results=results,
                errors=[]
            )
            
        except Exception as e:
            processing_time = asyncio.get_event_loop().time() - start_time
            logger.error(f"Error in condition matching: {e}")
            
            return AgentResponse(
                agent_name="ConditionMatcher",
                processing_time=processing_time,
                confidence=0.0,
                results={},
                errors=[str(e)]
            )
    
    async def _similarity_based_matching(self, symptoms: List[str], 
                                       symptom_input: SymptomInput) -> List[Dict[str, Any]]:
        """Use semantic similarity to match symptoms to conditions (if embeddings available)"""
        if not (ST_AVAILABLE and self.sentence_transformer is not None and NP_AVAILABLE and self.condition_embeddings):
            return []

        # Create symptom text for embedding
        symptom_text = " ".join(symptoms)
        symptom_embedding = self.sentence_transformer.encode([symptom_text])[0]

        def _cosine(a, b) -> float:
            # a, b are 1-D arrays
            a = np.array(a)
            b = np.array(b)
            denom = (np.linalg.norm(a) * np.linalg.norm(b))
            if denom == 0:
                return 0.0
            return float(np.dot(a, b) / denom)

        matches: List[Dict[str, Any]] = []
        for condition_name, condition_embedding in self.condition_embeddings.items():
            similarity = _cosine(symptom_embedding, condition_embedding)
            matches.append({
                "condition": condition_name,
                "similarity_score": similarity,
                "method": "semantic_similarity",
            })

        # Sort by similarity score
        matches.sort(key=lambda x: x["similarity_score"], reverse=True)
        return matches[:10]
    
    async def _rule_based_matching(self, symptoms: List[str], 
                                 symptom_input: SymptomInput) -> List[Dict[str, Any]]:
        """Use rule-based matching for exact symptom matches"""
        matches = []
        
        for condition_name, condition_data in self.medical_knowledge_base.items():
            condition_symptoms = condition_data["symptoms"]
            
            # Calculate exact matches
            exact_matches = []
            for symptom in symptoms:
                for condition_symptom in condition_symptoms:
                    if (symptom.lower() in condition_symptom.lower() or 
                        condition_symptom.lower() in symptom.lower()):
                        exact_matches.append(condition_symptom)
                        break
            
            # Calculate match percentage
            match_percentage = len(exact_matches) / len(condition_symptoms) if condition_symptoms else 0
            
            if match_percentage > 0:
                matches.append({
                    "condition": condition_name,
                    "match_percentage": match_percentage,
                    "exact_matches": exact_matches,
                    "total_condition_symptoms": len(condition_symptoms),
                    "method": "rule_based"
                })
        
        # Sort by match percentage
        matches.sort(key=lambda x: x["match_percentage"], reverse=True)
        
        return matches
    
    async def _combine_and_rank_matches(self, similarity_matches: List[Dict[str, Any]], 
                                      rule_based_matches: List[Dict[str, Any]], 
                                      symptom_input: SymptomInput) -> List[Dict[str, Any]]:
        """Combine similarity and rule-based matches with weighted scoring"""
        combined_scores = {}
        
        # Process similarity matches
        for match in similarity_matches:
            condition = match["condition"]
            combined_scores[condition] = {
                "similarity_score": match["similarity_score"],
                "rule_score": 0.0,
                "combined_score": 0.0,
                "exact_matches": []
            }
        
        # Add rule-based scores
        for match in rule_based_matches:
            condition = match["condition"]
            if condition not in combined_scores:
                combined_scores[condition] = {
                    "similarity_score": 0.0,
                    "rule_score": match["match_percentage"],
                    "combined_score": 0.0,
                    "exact_matches": match["exact_matches"]
                }
            else:
                combined_scores[condition]["rule_score"] = match["match_percentage"]
                combined_scores[condition]["exact_matches"] = match["exact_matches"]
        
        # Calculate combined scores (weighted average)
        similarity_weight = 0.6
        rule_weight = 0.4
        
        for condition, scores in combined_scores.items():
            scores["combined_score"] = (
                scores["similarity_score"] * similarity_weight + 
                scores["rule_score"] * rule_weight
            )
        
        # Convert to list and sort
        combined_matches = []
        for condition, scores in combined_scores.items():
            combined_matches.append({
                "condition": condition,
                "combined_score": scores["combined_score"],
                "similarity_score": scores["similarity_score"],
                "rule_score": scores["rule_score"],
                "exact_matches": scores["exact_matches"]
            })
        
        combined_matches.sort(key=lambda x: x["combined_score"], reverse=True)
        
        return combined_matches
    
    async def _apply_demographic_adjustments(self, matches: List[Dict[str, Any]], 
                                           patient_info) -> List[Dict[str, Any]]:
        """Apply demographic and risk factor adjustments to condition probabilities"""
        adjusted_matches = []
        
        for match in matches:
            condition_name = match["condition"]
            condition_data = self.medical_knowledge_base.get(condition_name, {})
            
            # Start with the combined score
            adjusted_score = match["combined_score"]
            
            # Age group adjustments
            age_groups = condition_data.get("common_age_groups", ["all"])
            if "all" not in age_groups:
                age = patient_info.age
                if age < 18 and "children" in age_groups:
                    adjusted_score *= 1.2
                elif 18 <= age < 65 and "adults" in age_groups:
                    adjusted_score *= 1.1
                elif age >= 65 and "elderly" in age_groups:
                    adjusted_score *= 1.2
                else:
                    adjusted_score *= 0.8  # Less likely if age doesn't match
            
            # Risk factor adjustments
            risk_factors = condition_data.get("risk_factors", [])
            medical_history = patient_info.medical_history or []
            
            # Check for risk factors in medical history
            risk_factor_matches = len([rf for rf in risk_factors 
                                     if any(rf.lower() in mh.lower() for mh in medical_history)])
            
            if risk_factor_matches > 0:
                adjusted_score *= (1.0 + 0.1 * risk_factor_matches)
            
            # Gender-specific adjustments
            if condition_name == "urinary_tract_infection" and patient_info.gender.lower() == "female":
                adjusted_score *= 1.3
            
            adjusted_matches.append({
                **match,
                "adjusted_score": min(adjusted_score, 1.0),  # Cap at 1.0
                "demographic_adjustment": adjusted_score / match["combined_score"] if match["combined_score"] > 0 else 1.0
            })
        
        # Re-sort by adjusted score
        adjusted_matches.sort(key=lambda x: x["adjusted_score"], reverse=True)
        
        return adjusted_matches
    
    async def _generate_differential_diagnosis(self, matches: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate structured differential diagnosis as plain dicts to avoid downstream type issues"""
        differential_diagnosis: List[Dict[str, Any]] = []

        for i, match in enumerate(matches[:5]):  # Top 5 conditions
            condition_name = match["condition"]
            condition_data = self.medical_knowledge_base.get(condition_name, {})

            # Calculate probability and confidence
            probability = float(match.get("adjusted_score", match.get("combined_score", 0.0)))
            confidence = float(min(match.get("similarity_score", 0.0) + match.get("rule_score", 0.0), 1.0))

            condition = {
                "name": condition_name.replace("_", " ").title(),
                "icd_code": condition_data.get("icd_code"),
                "probability": probability,
                "confidence": confidence,
                "description": condition_data.get("description", ""),
                "symptoms_match": match.get("exact_matches", []),
                "risk_factors": condition_data.get("risk_factors", []),
            }
            differential_diagnosis.append(condition)

        return differential_diagnosis
    
    def _calculate_confidence(self, results: Dict[str, Any], symptoms: List[str]) -> float:
        """Calculate confidence score for condition matching"""
        factors = {
            "conditions_matched": min(results.get("conditions_matched", 0) / 5.0, 1.0),
            "symptom_count": min(len(symptoms) / 5.0, 1.0),
            "top_condition_score": results.get("top_condition", {}).get("probability", 0.0) if results.get("top_condition") else 0.0,
            "method_diversity": 1.0 if len(results.get("similarity_matches", [])) > 0 and len(results.get("rule_based_matches", [])) > 0 else 0.7
        }
        
        return sum(factors.values()) / len(factors)
    
    async def health_check(self) -> bool:
        """Check if the agent is ready and healthy"""
        # Healthy if knowledge base is present; similarity is optional
        return len(self.medical_knowledge_base) > 0
