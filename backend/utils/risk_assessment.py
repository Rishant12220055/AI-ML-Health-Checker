"""
Advanced Risk Assessment and Predictive Analytics System

This module provides comprehensive risk scoring, predictive health analytics,
uncertainty quantification, and patient-specific risk assessments.
"""

from typing import Dict, List, Any, Optional, Tuple
from enum import Enum
from datetime import datetime, timedelta
import logging
import statistics
from models.schemas import PatientInfo, SymptomInput, Symptom

logger = logging.getLogger(__name__)

class RiskLevel(str, Enum):
    """Risk assessment levels"""
    VERY_LOW = "very_low"      # 0-20%
    LOW = "low"                # 21-40%
    MODERATE = "moderate"      # 41-60%
    HIGH = "high"              # 61-80%
    VERY_HIGH = "very_high"    # 81-100%

class RiskFactor(str, Enum):
    """Types of risk factors"""
    AGE = "age"
    GENDER = "gender"
    MEDICAL_HISTORY = "medical_history"
    LIFESTYLE = "lifestyle"
    ENVIRONMENTAL = "environmental"
    GENETIC = "genetic"
    MEDICATION = "medication"

class AdvancedRiskAssessment:
    """Advanced risk assessment and predictive analytics system"""
    
    def __init__(self):
        self.risk_matrices = self._load_risk_matrices()
        self.comorbidity_weights = self._load_comorbidity_weights()
        self.age_risk_curves = self._load_age_risk_curves()
        self.lifestyle_factors = self._load_lifestyle_factors()
        self.predictive_models = self._load_predictive_models()
        
    def _load_risk_matrices(self) -> Dict[str, Dict[str, Any]]:
        """Load comprehensive risk assessment matrices"""
        return {
            "cardiovascular": {
                "age_weights": {
                    "20-30": 0.1, "31-40": 0.2, "41-50": 0.4, 
                    "51-60": 0.7, "61-70": 1.0, "71+": 1.5
                },
                "gender_weights": {"male": 1.2, "female": 0.8},
                "condition_multipliers": {
                    "diabetes": 2.5, "hypertension": 2.0, "high_cholesterol": 1.8,
                    "smoking": 2.2, "obesity": 1.6, "family_history": 1.4
                },
                "protective_factors": {
                    "regular_exercise": 0.7, "healthy_diet": 0.8, "normal_weight": 0.9
                }
            },
            "diabetes": {
                "age_weights": {
                    "20-30": 0.1, "31-40": 0.3, "41-50": 0.6,
                    "51-60": 1.0, "61-70": 1.3, "71+": 1.5
                },
                "gender_weights": {"male": 1.1, "female": 0.9},
                "condition_multipliers": {
                    "obesity": 3.0, "hypertension": 1.8, "family_history": 2.2,
                    "gestational_diabetes": 2.5, "prediabetes": 4.0
                },
                "protective_factors": {
                    "regular_exercise": 0.6, "healthy_diet": 0.7, "normal_weight": 0.5
                }
            },
            "stroke": {
                "age_weights": {
                    "20-40": 0.1, "41-50": 0.3, "51-60": 0.7,
                    "61-70": 1.2, "71-80": 2.0, "81+": 3.0
                },
                "gender_weights": {"male": 1.3, "female": 1.0},
                "condition_multipliers": {
                    "atrial_fibrillation": 3.0, "hypertension": 2.5, "diabetes": 2.0,
                    "smoking": 2.2, "previous_stroke": 4.0, "carotid_disease": 2.8
                }
            },
            "cancer": {
                "age_weights": {
                    "20-30": 0.1, "31-40": 0.2, "41-50": 0.4,
                    "51-60": 0.8, "61-70": 1.2, "71+": 1.8
                },
                "gender_weights": {"male": 1.1, "female": 1.0},
                "condition_multipliers": {
                    "smoking": 3.0, "family_history": 2.0, "radiation_exposure": 2.5,
                    "chemical_exposure": 1.8, "chronic_inflammation": 1.6
                },
                "protective_factors": {
                    "healthy_diet": 0.8, "regular_exercise": 0.8, "normal_weight": 0.9
                }
            },
            "mental_health": {
                "age_weights": {
                    "15-25": 1.3, "26-35": 1.1, "36-50": 1.0,
                    "51-65": 0.9, "66+": 0.8
                },
                "gender_weights": {"male": 0.8, "female": 1.2},
                "condition_multipliers": {
                    "trauma_history": 2.5, "family_history": 2.0, "chronic_illness": 1.8,
                    "substance_abuse": 2.2, "social_isolation": 1.6
                },
                "protective_factors": {
                    "social_support": 0.7, "regular_exercise": 0.8, "stress_management": 0.8
                }
            }
        }
    
    def _load_comorbidity_weights(self) -> Dict[str, Dict[str, float]]:
        """Load weights for multiple condition interactions"""
        return {
            "diabetes_hypertension": 1.8,
            "diabetes_obesity": 2.2,
            "hypertension_heart_disease": 2.0,
            "depression_anxiety": 1.6,
            "copd_heart_failure": 2.1,
            "diabetes_kidney_disease": 2.5,
            "obesity_sleep_apnea": 1.9
        }
    
    def _load_age_risk_curves(self) -> Dict[str, List[Tuple[int, float]]]:
        """Load age-based risk progression curves"""
        return {
            "cardiovascular": [
                (20, 0.01), (30, 0.02), (40, 0.05), (50, 0.12),
                (60, 0.25), (70, 0.40), (80, 0.60), (90, 0.80)
            ],
            "diabetes": [
                (20, 0.01), (30, 0.03), (40, 0.08), (50, 0.15),
                (60, 0.25), (70, 0.35), (80, 0.45)
            ],
            "cancer": [
                (20, 0.001), (30, 0.003), (40, 0.01), (50, 0.03),
                (60, 0.08), (70, 0.18), (80, 0.35)
            ]
        }
    
    def _load_lifestyle_factors(self) -> Dict[str, Dict[str, float]]:
        """Load lifestyle factor impact on health risks"""
        return {
            "smoking": {
                "cardiovascular": 2.2, "cancer": 3.0, "copd": 4.0,
                "stroke": 1.8, "diabetes": 1.4
            },
            "obesity": {
                "diabetes": 3.0, "cardiovascular": 1.6, "sleep_apnea": 2.5,
                "cancer": 1.3, "arthritis": 2.0
            },
            "sedentary_lifestyle": {
                "cardiovascular": 1.4, "diabetes": 1.8, "depression": 1.5,
                "obesity": 2.0, "osteoporosis": 1.6
            },
            "excessive_alcohol": {
                "liver_disease": 3.5, "cardiovascular": 1.3, "cancer": 1.8,
                "mental_health": 2.0, "accidents": 2.5
            },
            "poor_diet": {
                "diabetes": 1.8, "cardiovascular": 1.5, "cancer": 1.4,
                "obesity": 2.2, "digestive_issues": 1.6
            }
        }
    
    def _load_predictive_models(self) -> Dict[str, Dict[str, Any]]:
        """Load predictive health models"""
        return {
            "hospital_readmission": {
                "risk_factors": ["age", "comorbidities", "previous_admissions", "medication_compliance"],
                "weights": [0.3, 0.4, 0.2, 0.1],
                "threshold": 0.6
            },
            "emergency_visit": {
                "risk_factors": ["chronic_conditions", "medication_count", "age", "recent_symptoms"],
                "weights": [0.4, 0.2, 0.2, 0.2],
                "threshold": 0.5
            },
            "medication_adherence": {
                "risk_factors": ["medication_count", "complexity", "side_effects", "cost"],
                "weights": [0.3, 0.25, 0.25, 0.2],
                "threshold": 0.4
            }
        }
    
    async def comprehensive_risk_assessment(self, patient_info: PatientInfo, 
                                          symptom_input: SymptomInput,
                                          current_conditions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Perform comprehensive risk assessment across multiple health domains
        
        Args:
            patient_info: Patient demographic and medical information
            symptom_input: Current symptoms and complaints
            current_conditions: Probable conditions from diagnosis
            
        Returns:
            Comprehensive risk assessment with predictions and recommendations
        """
        try:
            # Calculate baseline risk scores
            baseline_risks = await self._calculate_baseline_risks(patient_info)
            
            # Assess current condition risks
            condition_risks = await self._assess_condition_risks(current_conditions, patient_info)
            
            # Calculate symptom-based risk modifiers
            symptom_modifiers = await self._calculate_symptom_risk_modifiers(symptom_input)
            
            # Assess comorbidity interactions
            comorbidity_risks = await self._assess_comorbidity_risks(patient_info.medical_history)
            
            # Generate predictive analytics
            predictions = await self._generate_health_predictions(patient_info, current_conditions)
            
            # Calculate uncertainty measures
            uncertainty = await self._calculate_uncertainty(baseline_risks, condition_risks, symptom_modifiers)
            
            # Generate personalized recommendations
            recommendations = await self._generate_risk_recommendations(
                baseline_risks, condition_risks, comorbidity_risks, patient_info
            )
            
            return {
                "patient_id": f"patient_{hash(str(patient_info.model_dump()))}",
                "assessment_timestamp": datetime.utcnow().isoformat(),
                "baseline_risks": baseline_risks,
                "condition_specific_risks": condition_risks,
                "symptom_risk_modifiers": symptom_modifiers,
                "comorbidity_interactions": comorbidity_risks,
                "predictive_analytics": predictions,
                "uncertainty_measures": uncertainty,
                "overall_risk_score": self._calculate_overall_risk(baseline_risks, condition_risks),
                "risk_level": self._determine_risk_level(baseline_risks, condition_risks),
                "recommendations": recommendations,
                "monitoring_schedule": self._generate_monitoring_schedule(baseline_risks, condition_risks),
                "intervention_priorities": self._prioritize_interventions(baseline_risks, condition_risks)
            }
            
        except Exception as e:
            logger.error(f"Error in comprehensive risk assessment: {e}")
            return {
                "error": "Risk assessment failed",
                "default_risk_level": RiskLevel.MODERATE,
                "recommendations": ["Consult healthcare provider for comprehensive evaluation"]
            }
    
    async def _calculate_baseline_risks(self, patient_info: PatientInfo) -> Dict[str, Any]:
        """Calculate baseline risk scores for major health conditions"""
        risks = {}
        
        for condition, risk_data in self.risk_matrices.items():
            # Age-based risk
            age_risk = self._get_age_risk(patient_info.age, risk_data["age_weights"])
            
            # Gender-based risk
            gender_risk = risk_data["gender_weights"].get(patient_info.gender.lower(), 1.0)
            
            # Medical history multipliers
            history_multiplier = 1.0
            for condition_name in patient_info.medical_history or []:
                multiplier = risk_data.get("condition_multipliers", {}).get(condition_name.lower(), 1.0)
                history_multiplier *= multiplier
            
            # Calculate baseline risk
            baseline_risk = min(age_risk * gender_risk * history_multiplier, 1.0)
            
            risks[condition] = {
                "baseline_score": baseline_risk,
                "age_component": age_risk,
                "gender_component": gender_risk,
                "history_component": history_multiplier,
                "risk_level": self._score_to_risk_level(baseline_risk)
            }
        
        return risks
    
    async def _assess_condition_risks(self, current_conditions: List[Dict[str, Any]], 
                                    patient_info: PatientInfo) -> Dict[str, Any]:
        """Assess risks associated with current probable conditions"""
        condition_risks = {}
        
        for condition in current_conditions:
            condition_name = condition.get("name", "").lower()
            probability = condition.get("probability", 0.0)
            confidence = condition.get("confidence", 0.0)
            
            # Base risk from condition probability and confidence
            base_risk = (probability * confidence)
            
            # Age adjustment
            age = patient_info.age
            age_multiplier = 1.0
            if age < 18:
                age_multiplier = 0.8
            elif age > 65:
                age_multiplier = 1.3
            
            # Complication risk based on condition
            complication_risks = self._get_condition_complications(condition_name)
            
            condition_risks[condition_name] = {
                "immediate_risk": base_risk * age_multiplier,
                "complication_risks": complication_risks,
                "severity_adjusted_risk": base_risk * self._get_severity_multiplier(condition_name),
                "requires_monitoring": base_risk > 0.6 or any(risk > 0.4 for risk in complication_risks.values())
            }
        
        return condition_risks
    
    async def _calculate_symptom_risk_modifiers(self, symptom_input: SymptomInput) -> Dict[str, Any]:
        """Calculate risk modifiers based on current symptoms"""
        modifiers = {
            "severity_modifier": 1.0,
            "symptom_count_modifier": 1.0,
            "duration_modifier": 1.0,
            "emergency_flags": []
        }
        
        # Severity-based modifier
        severity_scores = []
        for symptom in symptom_input.symptoms:
            severity_value = self._extract_severity_value(symptom.severity)
            severity_scores.append(severity_value)
        
        if severity_scores:
            avg_severity = statistics.mean(severity_scores)
            max_severity = max(severity_scores)
            
            modifiers["severity_modifier"] = 1.0 + (avg_severity - 5) * 0.1
            modifiers["max_severity"] = max_severity
            modifiers["average_severity"] = avg_severity
        
        # Symptom count modifier
        symptom_count = len(symptom_input.symptoms)
        if symptom_count > 5:
            modifiers["symptom_count_modifier"] = 1.0 + (symptom_count - 5) * 0.05
        
        # Emergency symptom flags
        emergency_symptoms = [
            "severe chest pain", "difficulty breathing", "loss of consciousness",
            "severe bleeding", "severe abdominal pain", "sudden weakness"
        ]
        
        for symptom in symptom_input.symptoms:
            if any(emergency in symptom.name.lower() for emergency in emergency_symptoms):
                modifiers["emergency_flags"].append(symptom.name)
        
        return modifiers
    
    async def _assess_comorbidity_risks(self, medical_history: List[str]) -> Dict[str, Any]:
        """Assess risks from multiple condition interactions"""
        if not medical_history or len(medical_history) < 2:
            return {"comorbidity_multiplier": 1.0, "interactions": []}
        
        interactions = []
        overall_multiplier = 1.0
        
        # Check for known comorbidity combinations
        for i, condition1 in enumerate(medical_history):
            for condition2 in medical_history[i+1:]:
                combo_key = f"{condition1.lower()}_{condition2.lower()}"
                reverse_key = f"{condition2.lower()}_{condition1.lower()}"
                
                weight = self.comorbidity_weights.get(combo_key) or self.comorbidity_weights.get(reverse_key)
                if weight:
                    interactions.append({
                        "conditions": [condition1, condition2],
                        "risk_multiplier": weight,
                        "clinical_significance": "high" if weight > 2.0 else "moderate"
                    })
                    overall_multiplier *= weight
        
        # General comorbidity burden
        condition_count = len(medical_history)
        if condition_count >= 3:
            overall_multiplier *= (1.0 + (condition_count - 2) * 0.1)
        
        return {
            "comorbidity_multiplier": min(overall_multiplier, 3.0),
            "interactions": interactions,
            "condition_count": condition_count,
            "complexity_score": self._calculate_complexity_score(medical_history)
        }
    
    async def _generate_health_predictions(self, patient_info: PatientInfo, 
                                         current_conditions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate predictive health analytics"""
        predictions = {}
        
        for model_name, model_data in self.predictive_models.items():
            risk_factors = model_data["risk_factors"]
            weights = model_data["weights"]
            threshold = model_data["threshold"]
            
            # Calculate weighted risk score
            risk_score = 0.0
            
            if "age" in risk_factors:
                age_normalized = min(patient_info.age / 80.0, 1.0)
                risk_score += age_normalized * weights[risk_factors.index("age")]
            
            if "comorbidities" in risk_factors:
                comorbidity_score = min(len(patient_info.medical_history or []) / 5.0, 1.0)
                risk_score += comorbidity_score * weights[risk_factors.index("comorbidities")]
            
            if "medication_count" in risk_factors:
                med_score = min(len(patient_info.medications or []) / 10.0, 1.0)
                risk_score += med_score * weights[risk_factors.index("medication_count")]
            
            predictions[model_name] = {
                "risk_score": risk_score,
                "probability": risk_score,
                "risk_level": "high" if risk_score > threshold else "low",
                "timeframe": "6_months",
                "confidence": 0.75  # Model confidence
            }
        
        return predictions
    
    async def _calculate_uncertainty(self, baseline_risks: Dict[str, Any], 
                                   condition_risks: Dict[str, Any], 
                                   symptom_modifiers: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate uncertainty measures for risk predictions"""
        
        # Epistemic uncertainty (model uncertainty)
        model_disagreement = self._calculate_model_disagreement(baseline_risks)
        
        # Aleatoric uncertainty (data uncertainty)
        data_completeness = self._assess_data_completeness(baseline_risks, condition_risks)
        
        # Confidence intervals
        confidence_intervals = self._calculate_confidence_intervals(baseline_risks)
        
        return {
            "epistemic_uncertainty": model_disagreement,
            "aleatoric_uncertainty": 1.0 - data_completeness,
            "overall_uncertainty": (model_disagreement + (1.0 - data_completeness)) / 2,
            "confidence_intervals": confidence_intervals,
            "prediction_reliability": "high" if model_disagreement < 0.2 else "moderate" if model_disagreement < 0.4 else "low"
        }
    
    async def _generate_risk_recommendations(self, baseline_risks: Dict[str, Any], 
                                           condition_risks: Dict[str, Any], 
                                           comorbidity_risks: Dict[str, Any],
                                           patient_info: PatientInfo) -> List[Dict[str, Any]]:
        """Generate personalized risk reduction recommendations"""
        recommendations = []
        
        # High-risk condition recommendations
        for condition, risk_data in baseline_risks.items():
            if risk_data["baseline_score"] > 0.6:
                recommendations.append({
                    "category": "prevention",
                    "condition": condition,
                    "priority": "high",
                    "recommendation": f"High risk for {condition} - implement aggressive prevention strategies",
                    "specific_actions": self._get_prevention_actions(condition),
                    "monitoring_frequency": "quarterly"
                })
        
        # Lifestyle modification recommendations
        age = patient_info.age
        if age > 40:
            recommendations.append({
                "category": "screening",
                "priority": "moderate",
                "recommendation": "Age-appropriate screening for cardiovascular disease and diabetes",
                "specific_actions": ["blood pressure monitoring", "cholesterol screening", "diabetes screening"],
                "monitoring_frequency": "annually"
            })
        
        # Medication safety recommendations
        if len(patient_info.medications or []) > 5:
            recommendations.append({
                "category": "medication_safety",
                "priority": "high",
                "recommendation": "Medication review for potential interactions and optimization",
                "specific_actions": ["pharmacist consultation", "medication reconciliation", "deprescribing review"]
            })
        
        return recommendations
    
    def _get_age_risk(self, age: int, age_weights: Dict[str, float]) -> float:
        """Calculate age-based risk factor"""
        for age_range, weight in age_weights.items():
            if self._age_in_range(age, age_range):
                return weight
        return 1.0
    
    def _age_in_range(self, age: int, age_range: str) -> bool:
        """Check if age falls within specified range"""
        if "+" in age_range:
            min_age = int(age_range.replace("+", ""))
            return age >= min_age
        elif "-" in age_range:
            min_age, max_age = map(int, age_range.split("-"))
            return min_age <= age <= max_age
        else:
            return age == int(age_range)
    
    def _score_to_risk_level(self, score: float) -> RiskLevel:
        """Convert numeric risk score to risk level"""
        if score <= 0.2:
            return RiskLevel.VERY_LOW
        elif score <= 0.4:
            return RiskLevel.LOW
        elif score <= 0.6:
            return RiskLevel.MODERATE
        elif score <= 0.8:
            return RiskLevel.HIGH
        else:
            return RiskLevel.VERY_HIGH
    
    def _extract_severity_value(self, severity) -> int:
        """Extract numeric severity value"""
        if hasattr(severity, 'value'):
            severity_map = {"mild": 3, "moderate": 6, "severe": 8, "critical": 10}
            return severity_map.get(severity.value, 5)
        elif isinstance(severity, (int, float)):
            return int(severity)
        elif isinstance(severity, str):
            severity_map = {"mild": 3, "moderate": 6, "severe": 8, "critical": 10}
            return severity_map.get(severity.lower(), 5)
        return 5
    
    def _get_condition_complications(self, condition_name: str) -> Dict[str, float]:
        """Get complication risks for a specific condition"""
        complication_map = {
            "diabetes": {"cardiovascular": 0.4, "kidney_disease": 0.3, "neuropathy": 0.25},
            "hypertension": {"stroke": 0.15, "heart_attack": 0.12, "kidney_damage": 0.1},
            "heart_failure": {"arrhythmia": 0.3, "kidney_failure": 0.2, "stroke": 0.15},
            "pneumonia": {"respiratory_failure": 0.1, "sepsis": 0.08, "complications": 0.05}
        }
        return complication_map.get(condition_name, {})
    
    def _get_severity_multiplier(self, condition_name: str) -> float:
        """Get severity multiplier for a condition"""
        severity_map = {
            "appendicitis": 2.0, "pneumonia": 1.8, "heart_attack": 2.5,
            "stroke": 2.2, "sepsis": 2.8, "diabetes": 1.3, "hypertension": 1.2
        }
        return severity_map.get(condition_name, 1.0)
    
    def _calculate_complexity_score(self, medical_history: List[str]) -> float:
        """Calculate complexity score based on medical history"""
        complexity_weights = {
            "diabetes": 0.3, "heart_disease": 0.4, "kidney_disease": 0.4,
            "cancer": 0.5, "mental_health": 0.2, "autoimmune": 0.3
        }
        
        total_complexity = 0.0
        for condition in medical_history:
            condition_lower = condition.lower()
            for key, weight in complexity_weights.items():
                if key in condition_lower:
                    total_complexity += weight
                    break
        
        return min(total_complexity, 2.0)
    
    def _calculate_model_disagreement(self, baseline_risks: Dict[str, Any]) -> float:
        """Calculate disagreement between different risk models"""
        scores = [risk_data["baseline_score"] for risk_data in baseline_risks.values()]
        if len(scores) < 2:
            return 0.1
        
        variance = statistics.variance(scores)
        return min(variance, 0.5)
    
    def _assess_data_completeness(self, baseline_risks: Dict[str, Any], 
                                condition_risks: Dict[str, Any]) -> float:
        """Assess completeness of available data for risk assessment"""
        total_factors = 10  # Expected data points
        available_factors = 0
        
        if baseline_risks:
            available_factors += 5
        if condition_risks:
            available_factors += 3
        if len(baseline_risks) > 3:
            available_factors += 2
        
        return min(available_factors / total_factors, 1.0)
    
    def _calculate_confidence_intervals(self, baseline_risks: Dict[str, Any]) -> Dict[str, Dict[str, float]]:
        """Calculate confidence intervals for risk predictions"""
        intervals = {}
        
        for condition, risk_data in baseline_risks.items():
            score = risk_data["baseline_score"]
            margin = score * 0.15  # 15% margin of error
            
            intervals[condition] = {
                "lower_bound": max(0.0, score - margin),
                "upper_bound": min(1.0, score + margin),
                "confidence_level": 0.85
            }
        
        return intervals
    
    def _calculate_overall_risk(self, baseline_risks: Dict[str, Any], 
                              condition_risks: Dict[str, Any]) -> float:
        """Calculate overall composite risk score"""
        baseline_scores = [risk_data["baseline_score"] for risk_data in baseline_risks.values()]
        condition_scores = [risk_data["immediate_risk"] for risk_data in condition_risks.values()]
        
        all_scores = baseline_scores + condition_scores
        if not all_scores:
            return 0.3
        
        # Weighted average with emphasis on highest risks
        sorted_scores = sorted(all_scores, reverse=True)
        if len(sorted_scores) >= 3:
            weighted_score = (sorted_scores[0] * 0.5 + sorted_scores[1] * 0.3 + sorted_scores[2] * 0.2)
        elif len(sorted_scores) == 2:
            weighted_score = (sorted_scores[0] * 0.7 + sorted_scores[1] * 0.3)
        else:
            weighted_score = sorted_scores[0]
        
        return min(weighted_score, 1.0)
    
    def _determine_risk_level(self, baseline_risks: Dict[str, Any], 
                            condition_risks: Dict[str, Any]) -> RiskLevel:
        """Determine overall risk level"""
        overall_score = self._calculate_overall_risk(baseline_risks, condition_risks)
        return self._score_to_risk_level(overall_score)
    
    def _generate_monitoring_schedule(self, baseline_risks: Dict[str, Any], 
                                    condition_risks: Dict[str, Any]) -> Dict[str, str]:
        """Generate monitoring schedule based on risk levels"""
        overall_risk = self._calculate_overall_risk(baseline_risks, condition_risks)
        
        if overall_risk > 0.8:
            return {"frequency": "monthly", "type": "intensive_monitoring"}
        elif overall_risk > 0.6:
            return {"frequency": "quarterly", "type": "regular_monitoring"}
        elif overall_risk > 0.4:
            return {"frequency": "semi_annually", "type": "routine_monitoring"}
        else:
            return {"frequency": "annually", "type": "preventive_monitoring"}
    
    def _prioritize_interventions(self, baseline_risks: Dict[str, Any], 
                                condition_risks: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Prioritize interventions based on risk assessment"""
        interventions = []
        
        # Sort risks by score
        all_risks = []
        for condition, risk_data in baseline_risks.items():
            all_risks.append((condition, risk_data["baseline_score"], "prevention"))
        
        for condition, risk_data in condition_risks.items():
            all_risks.append((condition, risk_data["immediate_risk"], "treatment"))
        
        all_risks.sort(key=lambda x: x[1], reverse=True)
        
        for i, (condition, score, intervention_type) in enumerate(all_risks[:5]):
            interventions.append({
                "priority": i + 1,
                "condition": condition,
                "risk_score": score,
                "intervention_type": intervention_type,
                "urgency": "high" if score > 0.7 else "moderate" if score > 0.4 else "low"
            })
        
        return interventions
    
    def _get_prevention_actions(self, condition: str) -> List[str]:
        """Get specific prevention actions for a condition"""
        prevention_map = {
            "cardiovascular": [
                "Regular exercise (150 min/week)", "Heart-healthy diet", "Blood pressure monitoring",
                "Cholesterol management", "Smoking cessation", "Weight management"
            ],
            "diabetes": [
                "Weight management", "Regular physical activity", "Healthy diet",
                "Blood glucose monitoring", "Regular screening", "Stress management"
            ],
            "stroke": [
                "Blood pressure control", "Atrial fibrillation management", "Smoking cessation",
                "Cholesterol management", "Regular exercise", "Medication compliance"
            ],
            "cancer": [
                "Regular screening", "Healthy diet", "Exercise", "Avoid tobacco",
                "Limit alcohol", "Sun protection", "Vaccination (where applicable)"
            ]
        }
        return prevention_map.get(condition, ["Consult healthcare provider", "Regular health monitoring"])
