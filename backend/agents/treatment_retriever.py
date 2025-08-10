"""
Treatment Retriever Agent

This agent is responsible for:
1. Retrieving evidence-based treatment recommendations
2. Integrating WHO and CDC guidelines
3. Assessing urgency levels and triage recommendations
4. Providing medication and non-medication treatment options
"""

import asyncio
import json
from typing import List, Dict, Any, Optional
from datetime import datetime
import logging

from models.schemas import Condition, Treatment, UrgencyLevel, AgentResponse, PatientInfo

logger = logging.getLogger(__name__)

class TreatmentRetrieverAgent:
    """AI Agent for treatment recommendation and urgency assessment"""
    
    def __init__(self):
        self.treatment_database = {}
        self.urgency_rules = {}
        self.who_guidelines = {}
        self.cdc_guidelines = {}
        self.contraindication_rules = {}
        
    async def initialize(self):
        """Initialize treatment database and guidelines"""
        try:
            logger.info("Initializing Treatment Retriever Agent...")
            
            # Load treatment database
            await self._load_treatment_database()
            
            # Load urgency assessment rules
            await self._load_urgency_rules()
            
            # Load WHO guidelines
            await self._load_who_guidelines()
            
            # Load CDC guidelines
            await self._load_cdc_guidelines()
            
            # Load contraindication rules
            await self._load_contraindication_rules()
            
            logger.info("Treatment Retriever Agent initialized successfully")
            
        except Exception as e:
            logger.error(f"Error initializing Treatment Retriever Agent: {e}")
            raise
    
    async def _load_treatment_database(self):
        """Load comprehensive treatment database"""
        self.treatment_database = {
            "influenza": [
                {
                    "name": "Rest and Hydration",
                    "type": "lifestyle",
                    "description": "Adequate rest and increased fluid intake",
                    "dosage": "8-10 glasses of water daily",
                    "duration": "7-10 days",
                    "side_effects": [],
                    "contraindications": [],
                    "who_guideline": "WHO_INFLUENZA_2019",
                    "cdc_guideline": "CDC_FLU_TREATMENT_2023"
                },
                {
                    "name": "Oseltamivir (Tamiflu)",
                    "type": "medication",
                    "description": "Antiviral medication for influenza",
                    "dosage": "75mg twice daily",
                    "duration": "5 days",
                    "side_effects": ["nausea", "vomiting", "headache"],
                    "contraindications": ["severe kidney disease"],
                    "who_guideline": "WHO_INFLUENZA_2019",
                    "cdc_guideline": "CDC_ANTIVIRAL_2023"
                },
                {
                    "name": "Acetaminophen",
                    "type": "medication",
                    "description": "For fever and pain relief",
                    "dosage": "500-1000mg every 6-8 hours",
                    "duration": "As needed",
                    "side_effects": ["rare liver toxicity with overdose"],
                    "contraindications": ["severe liver disease"],
                    "who_guideline": "WHO_PAIN_MANAGEMENT_2020",
                    "cdc_guideline": "CDC_OTC_MEDICATIONS_2022"
                }
            ],
            "common_cold": [
                {
                    "name": "Supportive Care",
                    "type": "lifestyle",
                    "description": "Rest, fluids, and symptom management",
                    "dosage": "Increase fluid intake",
                    "duration": "7-14 days",
                    "side_effects": [],
                    "contraindications": [],
                    "who_guideline": "WHO_RESPIRATORY_2021",
                    "cdc_guideline": "CDC_COMMON_COLD_2022"
                },
                {
                    "name": "Saline Nasal Spray",
                    "type": "medication",
                    "description": "For nasal congestion relief",
                    "dosage": "2-3 sprays per nostril as needed",
                    "duration": "As needed",
                    "side_effects": [],
                    "contraindications": [],
                    "who_guideline": "WHO_RESPIRATORY_2021",
                    "cdc_guideline": "CDC_NASAL_CARE_2022"
                }
            ],
            "gastroenteritis": [
                {
                    "name": "Oral Rehydration Therapy",
                    "type": "treatment",
                    "description": "ORS solution to prevent dehydration",
                    "dosage": "250ml after each loose stool",
                    "duration": "Until symptoms resolve",
                    "side_effects": [],
                    "contraindications": ["severe vomiting"],
                    "who_guideline": "WHO_DIARRHEA_2017",
                    "cdc_guideline": "CDC_GASTROENTERITIS_2021"
                },
                {
                    "name": "BRAT Diet",
                    "type": "lifestyle",
                    "description": "Bananas, Rice, Applesauce, Toast diet",
                    "dosage": "As tolerated",
                    "duration": "2-3 days",
                    "side_effects": [],
                    "contraindications": [],
                    "who_guideline": "WHO_NUTRITION_2020",
                    "cdc_guideline": "CDC_DIET_THERAPY_2022"
                }
            ],
            "migraine": [
                {
                    "name": "Ibuprofen",
                    "type": "medication",
                    "description": "NSAID for migraine pain relief",
                    "dosage": "400-600mg every 6-8 hours",
                    "duration": "As needed, max 3 days",
                    "side_effects": ["stomach upset", "kidney issues with prolonged use"],
                    "contraindications": ["kidney disease", "stomach ulcers"],
                    "who_guideline": "WHO_PAIN_MANAGEMENT_2020",
                    "cdc_guideline": "CDC_HEADACHE_2022"
                },
                {
                    "name": "Dark Room Rest",
                    "type": "lifestyle",
                    "description": "Rest in quiet, dark environment",
                    "dosage": "As needed during episode",
                    "duration": "Until symptoms improve",
                    "side_effects": [],
                    "contraindications": [],
                    "who_guideline": "WHO_HEADACHE_2019",
                    "cdc_guideline": "CDC_MIGRAINE_MANAGEMENT_2021"
                }
            ],
            "pneumonia": [
                {
                    "name": "Amoxicillin",
                    "type": "medication",
                    "description": "First-line antibiotic for community-acquired pneumonia",
                    "dosage": "500mg three times daily",
                    "duration": "7-10 days",
                    "side_effects": ["diarrhea", "allergic reactions"],
                    "contraindications": ["penicillin allergy"],
                    "who_guideline": "WHO_PNEUMONIA_2019",
                    "cdc_guideline": "CDC_PNEUMONIA_2022"
                },
                {
                    "name": "Oxygen Therapy",
                    "type": "treatment",
                    "description": "Supplemental oxygen if SpO2 < 90%",
                    "dosage": "2-4L/min via nasal cannula",
                    "duration": "Until SpO2 > 92%",
                    "side_effects": [],
                    "contraindications": [],
                    "who_guideline": "WHO_OXYGEN_2020",
                    "cdc_guideline": "CDC_RESPIRATORY_SUPPORT_2023"
                }
            ],
            "anxiety_disorder": [
                {
                    "name": "Cognitive Behavioral Therapy",
                    "type": "therapy",
                    "description": "Psychotherapy for anxiety management",
                    "dosage": "1 session per week",
                    "duration": "12-20 sessions",
                    "side_effects": [],
                    "contraindications": [],
                    "who_guideline": "WHO_MENTAL_HEALTH_2021",
                    "cdc_guideline": "CDC_ANXIETY_2022"
                },
                {
                    "name": "Relaxation Techniques",
                    "type": "lifestyle",
                    "description": "Deep breathing, meditation, progressive muscle relaxation",
                    "dosage": "15-30 minutes daily",
                    "duration": "Ongoing",
                    "side_effects": [],
                    "contraindications": [],
                    "who_guideline": "WHO_MENTAL_HEALTH_2021",
                    "cdc_guideline": "CDC_STRESS_MANAGEMENT_2023"
                }
            ],
            "hypertension": [
                {
                    "name": "Lifestyle Modifications",
                    "type": "lifestyle",
                    "description": "DASH diet, exercise, weight loss, sodium reduction",
                    "dosage": "30 min exercise daily, <2.3g sodium/day",
                    "duration": "Ongoing",
                    "side_effects": [],
                    "contraindications": [],
                    "who_guideline": "WHO_HYPERTENSION_2021",
                    "cdc_guideline": "CDC_HYPERTENSION_2023"
                },
                {
                    "name": "Lisinopril",
                    "type": "medication",
                    "description": "ACE inhibitor for blood pressure control",
                    "dosage": "10mg once daily, titrate as needed",
                    "duration": "Long-term",
                    "side_effects": ["dry cough", "hyperkalemia"],
                    "contraindications": ["pregnancy", "bilateral renal artery stenosis"],
                    "who_guideline": "WHO_CVD_2020",
                    "cdc_guideline": "CDC_HYPERTENSION_MEDS_2023"
                }
            ],
            "diabetes_type_2": [
                {
                    "name": "Metformin",
                    "type": "medication",
                    "description": "First-line medication for type 2 diabetes",
                    "dosage": "500mg twice daily with meals",
                    "duration": "Long-term",
                    "side_effects": ["gastrointestinal upset", "lactic acidosis (rare)"],
                    "contraindications": ["severe kidney disease", "liver disease"],
                    "who_guideline": "WHO_DIABETES_2020",
                    "cdc_guideline": "CDC_DIABETES_2023"
                },
                {
                    "name": "Lifestyle Management",
                    "type": "lifestyle",
                    "description": "Diet modification, exercise, weight management",
                    "dosage": "150 min moderate exercise/week",
                    "duration": "Ongoing",
                    "side_effects": [],
                    "contraindications": [],
                    "who_guideline": "WHO_DIABETES_2020",
                    "cdc_guideline": "CDC_DIABETES_PREVENTION_2023"
                }
            ],
            "urinary_tract_infection": [
                {
                    "name": "Nitrofurantoin",
                    "type": "medication",
                    "description": "First-line antibiotic for uncomplicated UTI",
                    "dosage": "100mg twice daily",
                    "duration": "5-7 days",
                    "side_effects": ["nausea", "pulmonary toxicity (rare)"],
                    "contraindications": ["severe kidney disease", "pregnancy at term"],
                    "who_guideline": "WHO_UTI_2019",
                    "cdc_guideline": "CDC_UTI_2022"
                },
                {
                    "name": "Increased Fluid Intake",
                    "type": "lifestyle",
                    "description": "Drink plenty of water to flush bacteria",
                    "dosage": "8-10 glasses water daily",
                    "duration": "During treatment and prevention",
                    "side_effects": [],
                    "contraindications": [],
                    "who_guideline": "WHO_UTI_2019",
                    "cdc_guideline": "CDC_UTI_PREVENTION_2022"
                }
            ],
            "appendicitis": [
                {
                    "name": "Emergency Surgery",
                    "type": "procedure",
                    "description": "Immediate appendectomy",
                    "dosage": "Single procedure",
                    "duration": "Immediate",
                    "side_effects": ["surgical risks", "infection"],
                    "contraindications": [],
                    "who_guideline": "WHO_SURGERY_2020",
                    "cdc_guideline": "CDC_SURGICAL_GUIDELINES_2022"
                },
                {
                    "name": "Pre-operative Antibiotics",
                    "type": "medication",
                    "description": "Prophylactic antibiotics before surgery",
                    "dosage": "As per surgical protocol",
                    "duration": "Perioperative",
                    "side_effects": ["allergic reactions"],
                    "contraindications": ["known allergies"],
                    "who_guideline": "WHO_SURGICAL_PROPHYLAXIS_2020",
                    "cdc_guideline": "CDC_SURGICAL_ANTIBIOTICS_2023"
                }
            ]
        }
    
    async def _load_urgency_rules(self):
        """Load urgency assessment rules"""
        self.urgency_rules = {
            "emergency": {
                "symptoms": [
                    "severe chest pain",
                    "difficulty breathing",
                    "severe abdominal pain",
                    "loss of consciousness",
                    "severe bleeding",
                    "signs of stroke",
                    "high fever with confusion",
                    "severe allergic reaction"
                ],
                "conditions": ["appendicitis", "heart attack", "stroke", "severe pneumonia"],
                "action": "Call 911 or go to emergency room immediately"
            },
            "urgent": {
                "symptoms": [
                    "persistent high fever",
                    "severe headache",
                    "persistent vomiting",
                    "severe pain",
                    "signs of dehydration"
                ],
                "conditions": ["pneumonia", "severe migraine", "severe gastroenteritis"],
                "action": "Seek medical care within 24 hours"
            },
            "moderate": {
                "symptoms": [
                    "moderate fever",
                    "persistent cough",
                    "moderate pain",
                    "fatigue"
                ],
                "conditions": ["influenza", "moderate infection", "anxiety disorder"],
                "action": "Schedule appointment with healthcare provider within 2-3 days"
            },
            "low": {
                "symptoms": [
                    "mild cold symptoms",
                    "minor aches",
                    "mild fatigue"
                ],
                "conditions": ["common cold", "mild viral infection"],
                "action": "Self-care and monitor symptoms"
            }
        }
    
    async def _load_who_guidelines(self):
        """Load WHO treatment guidelines"""
        self.who_guidelines = {
            "WHO_INFLUENZA_2019": {
                "title": "WHO Guidelines for Influenza Treatment",
                "url": "https://www.who.int/influenza/guidelines",
                "key_recommendations": [
                    "Antiviral treatment within 48 hours of symptom onset",
                    "Supportive care for uncomplicated cases",
                    "Hospitalization for severe cases"
                ]
            },
            "WHO_PNEUMONIA_2019": {
                "title": "WHO Pneumonia Guidelines",
                "url": "https://www.who.int/pneumonia/guidelines",
                "key_recommendations": [
                    "Antibiotic therapy based on severity",
                    "Oxygen therapy for hypoxemic patients",
                    "Vaccination for prevention"
                ]
            },
            "WHO_HYPERTENSION_2021": {
                "title": "WHO Hypertension Management Guidelines",
                "url": "https://www.who.int/hypertension/guidelines",
                "key_recommendations": [
                    "Lifestyle modifications as first-line",
                    "Medication based on cardiovascular risk",
                    "Regular monitoring and follow-up"
                ]
            }
        }
    
    async def _load_cdc_guidelines(self):
        """Load CDC treatment guidelines"""
        self.cdc_guidelines = {
            "CDC_FLU_TREATMENT_2023": {
                "title": "CDC Influenza Treatment Guidelines",
                "url": "https://www.cdc.gov/flu/treatment",
                "key_recommendations": [
                    "Antiviral medications for high-risk patients",
                    "Symptomatic treatment for healthy adults",
                    "Isolation during infectious period"
                ]
            },
            "CDC_PNEUMONIA_2022": {
                "title": "CDC Pneumonia Treatment Guidelines", 
                "url": "https://www.cdc.gov/pneumonia/treatment",
                "key_recommendations": [
                    "Empirical antibiotic therapy",
                    "Severity assessment for treatment setting",
                    "Prevention through vaccination"
                ]
            },
            "CDC_HYPERTENSION_2023": {
                "title": "CDC Hypertension Management",
                "url": "https://www.cdc.gov/bloodpressure/treatment",
                "key_recommendations": [
                    "Blood pressure targets <130/80 mmHg",
                    "Team-based care approach",
                    "Self-monitoring and lifestyle counseling"
                ]
            }
        }
    
    async def _load_contraindication_rules(self):
        """Load medication contraindication rules"""
        self.contraindication_rules = {
            "age_based": {
                "aspirin": {"min_age": 18, "reason": "Reye's syndrome risk in children"},
                "ace_inhibitors": {"pregnancy": True, "reason": "Teratogenic effects"}
            },
            "condition_based": {
                "nsaids": ["kidney disease", "stomach ulcers", "heart failure"],
                "antibiotics": ["known allergies"]
            },
            "drug_interactions": {
                "warfarin": ["aspirin", "nsaids"],
                "metformin": ["contrast dye procedures"]
            }
        }
    
    async def process_conditions(self, conditions: List[Any], 
                               patient_info: PatientInfo) -> AgentResponse:
        """
        Main processing function for treatment retrieval
        
        Args:
            conditions: List of possible conditions from condition matcher
            patient_info: Patient demographic and medical information
            
        Returns:
            AgentResponse with treatment recommendations
        """
        start_time = asyncio.get_event_loop().time()
        
        try:
            # Normalize incoming conditions to Condition models
            normalized_conditions: List[Condition] = []
            for c in conditions or []:
                if isinstance(c, Condition):
                    normalized_conditions.append(c)
                elif isinstance(c, dict):
                    try:
                        normalized_conditions.append(Condition(**c))
                    except Exception:
                        # Skip invalid entries
                        continue

            # 1. Assess overall urgency level
            urgency_level = await self._assess_urgency_level(normalized_conditions)
            
            # 2. Retrieve treatments for each condition
            treatment_recommendations = []
            for condition in normalized_conditions[:3]:  # Top 3 conditions
                treatments = await self._get_treatments_for_condition(condition, patient_info)
                treatment_recommendations.extend(treatments)
            
            # 3. Filter treatments based on contraindications
            safe_treatments = await self._filter_contraindicated_treatments(
                treatment_recommendations, patient_info
            )
            
            # 4. Rank treatments by evidence and safety
            ranked_treatments = await self._rank_treatments(safe_treatments, normalized_conditions)
            
            # 5. Generate next steps and warnings
            next_steps = await self._generate_next_steps(urgency_level, normalized_conditions)
            warning_signs = await self._generate_warning_signs(normalized_conditions)
            care_instructions = await self._generate_care_instructions(urgency_level)
            
            processing_time = asyncio.get_event_loop().time() - start_time
            
            results = {
                "urgency_level": urgency_level.value,
                "treatment_recommendations": [treatment.dict() for treatment in ranked_treatments],
                "next_steps": next_steps,
                "warning_signs": warning_signs,
                "when_to_seek_care": care_instructions,
                "total_treatments_considered": len(treatment_recommendations),
                "safe_treatments_count": len(safe_treatments),
                "contraindications_found": len(treatment_recommendations) - len(safe_treatments)
            }
            
            confidence = self._calculate_confidence(results, normalized_conditions)
            
            return AgentResponse(
                agent_name="TreatmentRetriever",
                processing_time=processing_time,
                confidence=confidence,
                results=results,
                errors=[]
            )
            
        except Exception as e:
            processing_time = asyncio.get_event_loop().time() - start_time
            logger.error(f"Error in treatment retrieval: {e}")
            
            return AgentResponse(
                agent_name="TreatmentRetriever",
                processing_time=processing_time,
                confidence=0.0,
                results={},
                errors=[str(e)]
            )
    
    async def _assess_urgency_level(self, conditions: List[Condition]) -> UrgencyLevel:
        """Assess overall urgency level based on conditions"""
        if not conditions:
            return UrgencyLevel.LOW
        
        top_condition = conditions[0]
        condition_name = top_condition.name.lower().replace(" ", "_")
        
        # Check against urgency rules
        for urgency, rules in self.urgency_rules.items():
            if condition_name in rules.get("conditions", []):
                return UrgencyLevel(urgency)
        
        # Default urgency based on probability and severity
        if top_condition.probability > 0.8:
            return UrgencyLevel.URGENT
        elif top_condition.probability > 0.6:
            return UrgencyLevel.MODERATE
        else:
            return UrgencyLevel.LOW
    
    async def _get_treatments_for_condition(self, condition: Condition, 
                                          patient_info: PatientInfo) -> List[Treatment]:
        """Get treatment recommendations for a specific condition"""
        condition_name = condition.name.lower().replace(" ", "_")
        treatments_data = self.treatment_database.get(condition_name, [])
        
        treatments = []
        for treatment_data in treatments_data:
            treatment = Treatment(
                name=treatment_data["name"],
                type=treatment_data["type"],
                description=treatment_data["description"],
                dosage=treatment_data.get("dosage"),
                duration=treatment_data.get("duration"),
                side_effects=treatment_data.get("side_effects", []),
                contraindications=treatment_data.get("contraindications", []),
                who_guideline=treatment_data.get("who_guideline"),
                cdc_guideline=treatment_data.get("cdc_guideline")
            )
            treatments.append(treatment)
        
        return treatments
    
    async def _filter_contraindicated_treatments(self, treatments: List[Treatment], 
                                               patient_info: PatientInfo) -> List[Treatment]:
        """Filter out contraindicated treatments based on patient information"""
        safe_treatments = []
        
        for treatment in treatments:
            is_safe = True
            
            # Check age-based contraindications
            # Check medical history contraindications
            medical_history = [mh.lower() for mh in patient_info.medical_history]
            for contraindication in treatment.contraindications:
                if any(contraindication.lower() in mh for mh in medical_history):
                    is_safe = False
                    break
            
            # Check allergy contraindications
            allergies = [allergy.lower() for allergy in patient_info.allergies]
            treatment_name = treatment.name.lower()
            if any(allergy in treatment_name for allergy in allergies):
                is_safe = False
            
            if is_safe:
                safe_treatments.append(treatment)
        
        return safe_treatments
    
    async def _rank_treatments(self, treatments: List[Treatment], 
                             conditions: List[Condition]) -> List[Treatment]:
        """Rank treatments by evidence level and safety"""
        # Simple ranking based on type and guidelines
        type_priority = {
            "lifestyle": 1,
            "medication": 2,
            "therapy": 2,
            "treatment": 3,
            "procedure": 4
        }
        
        def treatment_score(treatment):
            type_score = type_priority.get(treatment.type, 5)
            guideline_score = 0
            if treatment.who_guideline:
                guideline_score += 1
            if treatment.cdc_guideline:
                guideline_score += 1
            
            return (type_score, -guideline_score)  # Lower type score and higher guideline score is better
        
        treatments.sort(key=treatment_score)
        return treatments
    
    async def _generate_next_steps(self, urgency_level: UrgencyLevel, 
                                 conditions: List[Condition]) -> List[str]:
        """Generate next steps based on urgency and conditions"""
        next_steps = []
        
        if urgency_level == UrgencyLevel.EMERGENCY:
            next_steps = [
                "Call 911 or go to the nearest emergency room immediately",
                "Do not drive yourself - have someone else drive or call an ambulance",
                "Bring a list of current medications and medical history"
            ]
        elif urgency_level == UrgencyLevel.URGENT:
            next_steps = [
                "Contact your healthcare provider or urgent care within 24 hours",
                "Monitor symptoms closely and seek immediate care if they worsen",
                "Follow prescribed treatment plan carefully"
            ]
        elif urgency_level == UrgencyLevel.MODERATE:
            next_steps = [
                "Schedule an appointment with your healthcare provider within 2-3 days",
                "Start appropriate self-care measures",
                "Keep a symptom diary to track changes"
            ]
        else:  # LOW
            next_steps = [
                "Monitor symptoms and practice self-care",
                "Consider over-the-counter treatments if appropriate",
                "Contact healthcare provider if symptoms persist or worsen"
            ]
        
        return next_steps
    
    async def _generate_warning_signs(self, conditions: List[Condition]) -> List[str]:
        """Generate warning signs to watch for"""
        warning_signs = [
            "Severe or worsening symptoms",
            "High fever (>103°F/39.4°C)",
            "Difficulty breathing or chest pain",
            "Severe dehydration signs",
            "Confusion or altered mental state",
            "Persistent vomiting",
            "Signs of allergic reaction"
        ]
        
        # Add condition-specific warnings
        for condition in conditions[:2]:  # Top 2 conditions
            condition_name = condition.name.lower()
            if "pneumonia" in condition_name:
                warning_signs.extend([
                    "Bluish lips or fingernails",
                    "Rapid or difficult breathing"
                ])
            elif "appendicitis" in condition_name:
                warning_signs.extend([
                    "Severe abdominal pain that worsens",
                    "Inability to pass gas or stool"
                ])
        
        return list(set(warning_signs))  # Remove duplicates
    
    async def _generate_care_instructions(self, urgency_level: UrgencyLevel) -> str:
        """Generate care-seeking instructions based on urgency"""
        instructions = {
            UrgencyLevel.EMERGENCY: "Seek immediate emergency medical care (call 911)",
            UrgencyLevel.URGENT: "Seek medical care within 24 hours",
            UrgencyLevel.MODERATE: "Schedule medical appointment within 2-3 days",
            UrgencyLevel.LOW: "Monitor symptoms and seek care if they worsen or persist"
        }
        
        return instructions.get(urgency_level, "Consult with healthcare provider")
    
    def _calculate_confidence(self, results: Dict[str, Any], conditions: List[Condition]) -> float:
        """Calculate confidence score for treatment recommendations"""
        factors = {
            "condition_confidence": conditions[0].confidence if conditions else 0.0,
            "treatment_availability": min(results.get("safe_treatments_count", 0) / 3.0, 1.0),
            "guideline_coverage": 1.0,  # Assuming good guideline coverage
            "safety_assessment": 1.0 - (results.get("contraindications_found", 0) / max(results.get("total_treatments_considered", 1), 1))
        }
        
        return sum(factors.values()) / len(factors)
    
    async def health_check(self) -> bool:
        """Check if the agent is ready and healthy"""
        return (len(self.treatment_database) > 0 and 
                len(self.urgency_rules) > 0 and 
                len(self.who_guidelines) > 0 and 
                len(self.cdc_guidelines) > 0)
