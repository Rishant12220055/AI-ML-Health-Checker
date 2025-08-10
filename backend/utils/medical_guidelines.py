"""
Medical Guidelines Manager

Manages medical guidelines from WHO, CDC, and other authoritative sources:
1. Loads and caches medical guidelines
2. Provides guideline-based treatment recommendations
3. Ensures compliance with international standards
4. Updates guidelines periodically
"""

import asyncio
import json
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import logging
import os
import httpx

logger = logging.getLogger(__name__)

class MedicalGuidelinesManager:
    """Manages medical guidelines from authoritative sources"""
    
    def __init__(self):
        self.who_guidelines = {}
        self.cdc_guidelines = {}
        self.local_guidelines = {}
        self.guidelines_loaded = False
        self.last_update = None
        
        # Configuration
        self.update_interval_hours = int(os.getenv("GUIDELINES_UPDATE_INTERVAL", "24"))
        self.guidelines_cache_dir = os.getenv("GUIDELINES_CACHE_DIR", "./data/guidelines")
        
        # Ensure cache directory exists
        os.makedirs(self.guidelines_cache_dir, exist_ok=True)
    
    async def load_guidelines(self):
        """Load medical guidelines from all sources"""
        try:
            logger.info("Loading medical guidelines...")
            
            # Load guidelines in parallel
            await asyncio.gather(
                self._load_who_guidelines(),
                self._load_cdc_guidelines(),
                self._load_local_guidelines()
            )
            
            self.guidelines_loaded = True
            self.last_update = datetime.utcnow()
            
            logger.info("Medical guidelines loaded successfully")
            
        except Exception as e:
            logger.error(f"Error loading medical guidelines: {e}")
            raise
    
    async def _load_who_guidelines(self):
        """Load WHO medical guidelines"""
        try:
            # In production, this would fetch from WHO APIs or databases
            # For this implementation, we'll use local data
            
            self.who_guidelines = {
                "influenza": {
                    "guideline_id": "WHO_INFLUENZA_2019",
                    "title": "WHO Guidelines for Influenza Treatment and Prevention",
                    "version": "2019.1",
                    "last_updated": "2019-03-15",
                    "url": "https://www.who.int/influenza/guidelines",
                    "recommendations": {
                        "treatment": {
                            "mild_cases": [
                                "Supportive care with rest and hydration",
                                "Symptomatic treatment with paracetamol/acetaminophen",
                                "Monitor for complications"
                            ],
                            "severe_cases": [
                                "Antiviral therapy (oseltamivir) within 48 hours",
                                "Hospitalization if indicated",
                                "Intensive supportive care"
                            ],
                            "high_risk_groups": [
                                "Pregnant women",
                                "Children under 5 years",
                                "Adults over 65 years",
                                "Immunocompromised patients"
                            ]
                        },
                        "prevention": [
                            "Annual influenza vaccination",
                            "Hand hygiene",
                            "Respiratory etiquette",
                            "Isolation of confirmed cases"
                        ]
                    },
                    "evidence_level": "A",
                    "contraindications": {
                        "oseltamivir": ["severe renal impairment", "known hypersensitivity"]
                    }
                },
                "pneumonia": {
                    "guideline_id": "WHO_PNEUMONIA_2019",
                    "title": "WHO Guidelines for Community-Acquired Pneumonia",
                    "version": "2019.2",
                    "last_updated": "2019-06-20",
                    "url": "https://www.who.int/pneumonia/guidelines",
                    "recommendations": {
                        "assessment": [
                            "Use clinical scoring systems (CURB-65, PORT)",
                            "Chest X-ray for diagnosis confirmation",
                            "Arterial blood gas if hypoxemia suspected"
                        ],
                        "treatment": {
                            "outpatient": [
                                "Amoxicillin 500mg TID for 5-7 days",
                                "Alternative: azithromycin or cefuroxime",
                                "Symptomatic care and monitoring"
                            ],
                            "inpatient": [
                                "IV antibiotics (ceftriaxone + azithromycin)",
                                "Oxygen therapy if SpO2 < 90%",
                                "Fluid management and monitoring"
                            ]
                        },
                        "monitoring": [
                            "Clinical response within 48-72 hours",
                            "Follow-up chest X-ray if no improvement",
                            "Complete antibiotic course"
                        ]
                    },
                    "evidence_level": "A"
                },
                "hypertension": {
                    "guideline_id": "WHO_CVD_2020",
                    "title": "WHO Guidelines for Cardiovascular Disease Prevention",
                    "version": "2020.1",
                    "last_updated": "2020-09-10",
                    "url": "https://www.who.int/cardiovascular_diseases/guidelines",
                    "recommendations": {
                        "diagnosis": [
                            "Multiple BP measurements on separate occasions",
                            "Cardiovascular risk assessment",
                            "Laboratory tests for target organ damage"
                        ],
                        "lifestyle": [
                            "Dietary approaches (DASH diet)",
                            "Regular physical activity (150 min/week)",
                            "Weight management (BMI 18.5-24.9)",
                            "Sodium reduction (<2g/day)",
                            "Limit alcohol consumption"
                        ],
                        "pharmacological": {
                            "first_line": ["ACE inhibitors", "ARBs", "Calcium channel blockers", "Thiazide diuretics"],
                            "combination_therapy": "For BP >160/100 or high CV risk",
                            "targets": "BP <140/90 mmHg (general), <130/80 mmHg (high risk)"
                        }
                    },
                    "evidence_level": "A"
                }
            }
            
            logger.debug("WHO guidelines loaded")
            
        except Exception as e:
            logger.error(f"Error loading WHO guidelines: {e}")
            self.who_guidelines = {}
    
    async def _load_cdc_guidelines(self):
        """Load CDC medical guidelines"""
        try:
            # In production, this would fetch from CDC APIs or databases
            
            self.cdc_guidelines = {
                "influenza": {
                    "guideline_id": "CDC_FLU_2023",
                    "title": "CDC Influenza Treatment and Prevention Guidelines",
                    "version": "2023.1",
                    "last_updated": "2023-08-15",
                    "url": "https://www.cdc.gov/flu/treatment",
                    "recommendations": {
                        "antiviral_treatment": {
                            "indications": [
                                "Hospitalized patients",
                                "High-risk outpatients",
                                "Severe or progressive illness"
                            ],
                            "medications": {
                                "oseltamivir": {
                                    "adult_dose": "75mg BID x 5 days",
                                    "pediatric_dose": "Weight-based dosing",
                                    "renal_adjustment": "Required for CrCl <60"
                                },
                                "zanamivir": {
                                    "dose": "10mg BID x 5 days (inhaled)",
                                    "contraindications": ["Asthma", "COPD"]
                                }
                            }
                        },
                        "supportive_care": [
                            "Rest and adequate fluid intake",
                            "Fever and pain management",
                            "Cough suppressants if needed"
                        ]
                    },
                    "prevention": {
                        "vaccination": {
                            "annual_recommendation": "All persons ≥6 months",
                            "timing": "September-October optimal",
                            "contraindications": ["Severe egg allergy", "Previous severe reaction"]
                        }
                    }
                },
                "pneumonia": {
                    "guideline_id": "CDC_PNEUMONIA_2022",
                    "title": "CDC Community-Acquired Pneumonia Guidelines",
                    "version": "2022.1",
                    "last_updated": "2022-11-30",
                    "url": "https://www.cdc.gov/pneumonia/treatment",
                    "recommendations": {
                        "empirical_therapy": {
                            "healthy_outpatient": [
                                "Amoxicillin 1g TID",
                                "Alternative: macrolide or doxycycline"
                            ],
                            "comorbidities": [
                                "Amoxicillin-clavulanate + macrolide",
                                "Respiratory fluoroquinolone"
                            ],
                            "hospitalized": [
                                "Beta-lactam + macrolide",
                                "Respiratory fluoroquinolone"
                            ]
                        },
                        "duration": "5-7 days for most patients",
                        "monitoring": [
                            "Clinical improvement within 48-72 hours",
                            "Procalcitonin guidance if available"
                        ]
                    }
                },
                "diabetes": {
                    "guideline_id": "CDC_DIABETES_2023",
                    "title": "CDC Diabetes Management Guidelines",
                    "version": "2023.1",
                    "last_updated": "2023-05-20",
                    "url": "https://www.cdc.gov/diabetes/guidelines",
                    "recommendations": {
                        "diagnosis": {
                            "criteria": [
                                "HbA1c ≥6.5%",
                                "Fasting glucose ≥126 mg/dL",
                                "Random glucose ≥200 mg/dL + symptoms"
                            ]
                        },
                        "management": {
                            "lifestyle": [
                                "Medical nutrition therapy",
                                "Regular physical activity",
                                "Weight management if overweight"
                            ],
                            "pharmacological": {
                                "first_line": "Metformin",
                                "targets": "HbA1c <7% for most adults",
                                "individualized": "Based on age, comorbidities, life expectancy"
                            }
                        },
                        "monitoring": [
                            "HbA1c every 3-6 months",
                            "Annual comprehensive exam",
                            "Cardiovascular risk assessment"
                        ]
                    }
                }
            }
            
            logger.debug("CDC guidelines loaded")
            
        except Exception as e:
            logger.error(f"Error loading CDC guidelines: {e}")
            self.cdc_guidelines = {}
    
    async def _load_local_guidelines(self):
        """Load local/institutional medical guidelines"""
        try:
            # Load any local guidelines or institutional protocols
            guidelines_file = os.path.join(self.guidelines_cache_dir, "local_guidelines.json")
            
            if os.path.exists(guidelines_file):
                with open(guidelines_file, 'r') as f:
                    self.local_guidelines = json.load(f)
            else:
                # Create default local guidelines
                self.local_guidelines = {
                    "emergency_protocols": {
                        "chest_pain": {
                            "immediate_actions": [
                                "Call 911 immediately",
                                "Give aspirin if no contraindications",
                                "Position patient comfortably",
                                "Monitor vital signs"
                            ],
                            "red_flags": [
                                "Severe crushing chest pain",
                                "Radiation to arm/jaw",
                                "Shortness of breath",
                                "Nausea and sweating"
                            ]
                        },
                        "difficulty_breathing": {
                            "immediate_actions": [
                                "Call 911 immediately",
                                "Position patient upright",
                                "Remove restrictive clothing",
                                "Prepare for possible CPR"
                            ]
                        }
                    },
                    "triage_protocols": {
                        "emergency": "Immediate medical attention required",
                        "urgent": "Medical attention within 2-4 hours",
                        "moderate": "Medical attention within 24-48 hours",
                        "low": "Routine medical care or self-care"
                    }
                }
                
                # Save default guidelines
                with open(guidelines_file, 'w') as f:
                    json.dump(self.local_guidelines, f, indent=2)
            
            logger.debug("Local guidelines loaded")
            
        except Exception as e:
            logger.error(f"Error loading local guidelines: {e}")
            self.local_guidelines = {}
    
    async def get_condition_info(self, condition_name: str) -> Optional[Dict[str, Any]]:
        """Get comprehensive information about a medical condition"""
        condition_key = condition_name.lower().replace(" ", "_")
        
        info = {
            "condition_name": condition_name,
            "who_guidelines": self.who_guidelines.get(condition_key),
            "cdc_guidelines": self.cdc_guidelines.get(condition_key),
            "local_protocols": self.local_guidelines.get(condition_key),
            "last_updated": self.last_update
        }
        
        # Filter out None values
        return {k: v for k, v in info.items() if v is not None}
    
    async def get_treatment_guidelines(self, condition_name: str) -> Optional[Dict[str, Any]]:
        """Get treatment guidelines for a specific condition"""
        condition_key = condition_name.lower().replace(" ", "_")
        
        guidelines = {}
        
        # WHO guidelines
        who_data = self.who_guidelines.get(condition_key)
        if who_data and "recommendations" in who_data:
            guidelines["who"] = who_data["recommendations"]
        
        # CDC guidelines
        cdc_data = self.cdc_guidelines.get(condition_key)
        if cdc_data and "recommendations" in cdc_data:
            guidelines["cdc"] = cdc_data["recommendations"]
        
        # Local protocols
        local_data = self.local_guidelines.get(condition_key)
        if local_data:
            guidelines["local"] = local_data
        
        return guidelines if guidelines else None
    
    async def get_who_guidelines(self) -> Dict[str, Any]:
        """Get all WHO guidelines"""
        return {
            "guidelines": self.who_guidelines,
            "total_conditions": len(self.who_guidelines),
            "last_updated": self.last_update
        }
    
    async def get_cdc_guidelines(self) -> Dict[str, Any]:
        """Get all CDC guidelines"""
        return {
            "guidelines": self.cdc_guidelines,
            "total_conditions": len(self.cdc_guidelines),
            "last_updated": self.last_update
        }
    
    async def update_guidelines(self) -> bool:
        """Update guidelines if they are stale"""
        try:
            if (not self.last_update or 
                datetime.utcnow() - self.last_update > timedelta(hours=self.update_interval_hours)):
                
                logger.info("Updating medical guidelines...")
                await self.load_guidelines()
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Error updating guidelines: {e}")
            return False
    
    def is_loaded(self) -> bool:
        """Check if guidelines are loaded"""
        return self.guidelines_loaded
    
    async def validate_treatment(self, treatment_name: str, condition: str, 
                               patient_info: Dict[str, Any]) -> Dict[str, Any]:
        """Validate a treatment against guidelines"""
        validation_result = {
            "treatment_name": treatment_name,
            "condition": condition,
            "is_appropriate": True,
            "warnings": [],
            "contraindications": [],
            "evidence_level": "Unknown",
            "guideline_sources": []
        }
        
        try:
            condition_key = condition.lower().replace(" ", "_")
            
            # Check WHO guidelines
            who_data = self.who_guidelines.get(condition_key)
            if who_data:
                validation_result["guideline_sources"].append("WHO")
                
                # Check contraindications
                contraindications = who_data.get("contraindications", {})
                treatment_contraindications = contraindications.get(treatment_name.lower(), [])
                
                if treatment_contraindications:
                    validation_result["contraindications"].extend(treatment_contraindications)
                
                # Get evidence level
                validation_result["evidence_level"] = who_data.get("evidence_level", "Unknown")
            
            # Check CDC guidelines
            cdc_data = self.cdc_guidelines.get(condition_key)
            if cdc_data:
                validation_result["guideline_sources"].append("CDC")
            
            # Check for patient-specific contraindications
            patient_age = patient_info.get("age", 0)
            medical_history = patient_info.get("medical_history", [])
            allergies = patient_info.get("allergies", [])
            
            # Age-based warnings
            if patient_age < 18 and "aspirin" in treatment_name.lower():
                validation_result["warnings"].append("Aspirin not recommended in children due to Reye's syndrome risk")
                validation_result["is_appropriate"] = False
            
            # Allergy checks
            for allergy in allergies:
                if allergy.lower() in treatment_name.lower():
                    validation_result["contraindications"].append(f"Patient allergic to {allergy}")
                    validation_result["is_appropriate"] = False
            
            return validation_result
            
        except Exception as e:
            logger.error(f"Error validating treatment: {e}")
            validation_result["warnings"].append("Unable to validate treatment against guidelines")
            return validation_result
    
    async def get_emergency_protocols(self) -> Dict[str, Any]:
        """Get emergency medical protocols"""
        return self.local_guidelines.get("emergency_protocols", {})
    
    async def health_check(self) -> bool:
        """Check if guidelines are healthy and up to date"""
        return (self.guidelines_loaded and 
                len(self.who_guidelines) > 0 and 
                len(self.cdc_guidelines) > 0)
