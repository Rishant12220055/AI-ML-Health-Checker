"""
Uncertainty Quantification and Confidence Analysis System

This module provides advanced uncertainty estimation, confidence analysis,
and reliability assessment for AI-generated medical recommendations.
"""

from typing import Dict, List, Any, Optional, Tuple, Union
from enum import Enum
from datetime import datetime
import logging
import statistics
import math
from dataclasses import dataclass
from models.schemas import Symptom, Condition, Treatment

# Optional numpy import
try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False
    np = None

logger = logging.getLogger(__name__)

class UncertaintyType(str, Enum):
    """Types of uncertainty in medical AI systems"""
    EPISTEMIC = "epistemic"          # Model uncertainty (lack of knowledge)
    ALEATORIC = "aleatoric"          # Data uncertainty (inherent randomness)
    LINGUISTIC = "linguistic"        # Language/interpretation uncertainty
    DIAGNOSTIC = "diagnostic"        # Medical diagnosis uncertainty
    TREATMENT = "treatment"          # Treatment recommendation uncertainty

class ConfidenceLevel(str, Enum):
    """Confidence levels for medical recommendations"""
    VERY_HIGH = "very_high"      # 90-100%
    HIGH = "high"                # 75-89%
    MODERATE = "moderate"        # 60-74%
    LOW = "low"                  # 40-59%
    VERY_LOW = "very_low"        # 0-39%

@dataclass
class UncertaintyEstimate:
    """Uncertainty estimation result"""
    uncertainty_type: UncertaintyType
    value: float                     # 0.0 (certain) to 1.0 (completely uncertain)
    confidence_interval: Tuple[float, float]
    explanation: str
    factors: List[str]
    recommendations: List[str]

@dataclass
class ConfidenceAnalysis:
    """Confidence analysis result"""
    overall_confidence: float
    confidence_level: ConfidenceLevel
    confidence_factors: Dict[str, float]
    uncertainty_breakdown: Dict[UncertaintyType, float]
    reliability_score: float
    calibration_score: float
    explanation: str

class UncertaintyQuantifier:
    """Advanced uncertainty quantification system"""
    
    def __init__(self):
        self.uncertainty_models = self._initialize_uncertainty_models()
        self.confidence_calibrators = self._initialize_confidence_calibrators()
        self.reliability_assessors = self._initialize_reliability_assessors()
        self.historical_performance = {}
        
    def _initialize_uncertainty_models(self) -> Dict[str, Any]:
        """Initialize uncertainty estimation models"""
        return {
            "symptom_uncertainty": {
                "vague_symptoms": ["fatigue", "discomfort", "feeling unwell", "pain"],
                "specific_symptoms": ["chest pain", "shortness of breath", "fever", "nausea"],
                "uncertainty_weights": {
                    "symptom_specificity": 0.3,
                    "symptom_count": 0.2,
                    "symptom_severity": 0.2,
                    "symptom_duration": 0.15,
                    "symptom_consistency": 0.15
                }
            },
            "diagnosis_uncertainty": {
                "differential_overlap": 0.25,      # Uncertainty from overlapping conditions
                "rare_conditions": 0.20,           # Uncertainty from rare diagnoses
                "incomplete_information": 0.30,    # Missing patient information
                "model_confidence": 0.25           # AI model uncertainty
            },
            "treatment_uncertainty": {
                "contraindications": 0.35,         # Drug/treatment contraindications
                "individual_variation": 0.25,      # Patient-specific responses
                "evidence_quality": 0.25,          # Quality of supporting evidence
                "side_effect_profile": 0.15        # Known side effects
            }
        }
    
    def _initialize_confidence_calibrators(self) -> Dict[str, Any]:
        """Initialize confidence calibration systems"""
        return {
            "diagnosis_calibration": {
                "high_confidence_threshold": 0.85,
                "moderate_confidence_threshold": 0.65,
                "low_confidence_threshold": 0.45,
                "calibration_factors": {
                    "model_agreement": 0.3,
                    "evidence_strength": 0.25,
                    "symptom_match": 0.25,
                    "prevalence_adjustment": 0.2
                }
            },
            "treatment_calibration": {
                "safety_weight": 0.4,
                "efficacy_weight": 0.3,
                "patient_suitability": 0.2,
                "evidence_quality": 0.1
            }
        }
    
    def _initialize_reliability_assessors(self) -> Dict[str, Any]:
        """Initialize reliability assessment criteria"""
        return {
            "data_quality_factors": {
                "completeness": 0.25,
                "consistency": 0.25,
                "accuracy": 0.25,
                "timeliness": 0.25
            },
            "model_reliability_factors": {
                "validation_performance": 0.3,
                "cross_validation_stability": 0.25,
                "domain_applicability": 0.25,
                "bias_assessment": 0.2
            }
        }
    
    async def comprehensive_uncertainty_analysis(self, 
                                               symptoms: List[Symptom],
                                               predicted_conditions: List[Dict[str, Any]],
                                               recommended_treatments: List[Dict[str, Any]],
                                               patient_context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform comprehensive uncertainty analysis across all AI outputs
        
        Args:
            symptoms: Patient symptoms
            predicted_conditions: AI-predicted conditions with probabilities
            recommended_treatments: AI-recommended treatments
            patient_context: Patient demographic and medical context
            
        Returns:
            Comprehensive uncertainty analysis
        """
        try:
            # Analyze symptom uncertainty
            symptom_uncertainty = await self._analyze_symptom_uncertainty(symptoms)
            
            # Analyze diagnostic uncertainty
            diagnostic_uncertainty = await self._analyze_diagnostic_uncertainty(
                symptoms, predicted_conditions, patient_context
            )
            
            # Analyze treatment uncertainty
            treatment_uncertainty = await self._analyze_treatment_uncertainty(
                recommended_treatments, predicted_conditions, patient_context
            )
            
            # Calculate overall confidence
            overall_confidence = await self._calculate_overall_confidence(
                symptom_uncertainty, diagnostic_uncertainty, treatment_uncertainty
            )
            
            # Generate uncertainty recommendations
            recommendations = await self._generate_uncertainty_recommendations(
                symptom_uncertainty, diagnostic_uncertainty, treatment_uncertainty
            )
            
            # Calculate reliability metrics
            reliability_metrics = await self._calculate_reliability_metrics(
                symptoms, predicted_conditions, patient_context
            )
            
            return {
                "analysis_timestamp": datetime.utcnow().isoformat(),
                "overall_confidence": overall_confidence,
                "uncertainty_breakdown": {
                    "symptom_uncertainty": symptom_uncertainty,
                    "diagnostic_uncertainty": diagnostic_uncertainty,
                    "treatment_uncertainty": treatment_uncertainty
                },
                "reliability_metrics": reliability_metrics,
                "uncertainty_recommendations": recommendations,
                "confidence_intervals": await self._calculate_confidence_intervals(
                    predicted_conditions, treatment_uncertainty
                ),
                "calibration_assessment": await self._assess_calibration_quality(
                    predicted_conditions, overall_confidence
                ),
                "decision_support": await self._generate_decision_support(
                    overall_confidence, uncertainty_breakdown={
                        "symptom": symptom_uncertainty,
                        "diagnostic": diagnostic_uncertainty,
                        "treatment": treatment_uncertainty
                    }
                )
            }
            
        except Exception as e:
            logger.error(f"Error in comprehensive uncertainty analysis: {e}")
            return {
                "error": "Uncertainty analysis failed",
                "fallback_confidence": 0.5,
                "recommendation": "Exercise additional caution due to analysis limitations"
            }
    
    async def _analyze_symptom_uncertainty(self, symptoms: List[Symptom]) -> UncertaintyEstimate:
        """Analyze uncertainty in symptom reporting and interpretation"""
        try:
            if not symptoms:
                return UncertaintyEstimate(
                    uncertainty_type=UncertaintyType.LINGUISTIC,
                    value=0.9,
                    confidence_interval=(0.8, 1.0),
                    explanation="No symptoms provided - extremely high uncertainty",
                    factors=["missing_symptoms"],
                    recommendations=["Gather comprehensive symptom history"]
                )
            
            uncertainty_factors = []
            uncertainty_scores = []
            
            # Analyze symptom specificity
            vague_symptoms = self.uncertainty_models["symptom_uncertainty"]["vague_symptoms"]
            vague_count = sum(1 for symptom in symptoms 
                            if any(vague in symptom.name.lower() for vague in vague_symptoms))
            specificity_uncertainty = vague_count / len(symptoms)
            uncertainty_scores.append(specificity_uncertainty)
            
            if specificity_uncertainty > 0.5:
                uncertainty_factors.append("high_proportion_vague_symptoms")
            
            # Analyze symptom count adequacy
            symptom_count = len(symptoms)
            if symptom_count < 3:
                count_uncertainty = 0.4
                uncertainty_factors.append("insufficient_symptom_detail")
            elif symptom_count > 10:
                count_uncertainty = 0.3
                uncertainty_factors.append("symptom_overload_complexity")
            else:
                count_uncertainty = 0.1
            uncertainty_scores.append(count_uncertainty)
            
            # Analyze severity consistency
            severity_scores = []
            for symptom in symptoms:
                if hasattr(symptom, 'severity'):
                    if hasattr(symptom.severity, 'value'):
                        severity_map = {"mild": 1, "moderate": 2, "severe": 3, "critical": 4}
                        severity_scores.append(severity_map.get(symptom.severity.value, 2))
                    elif isinstance(symptom.severity, (int, float)):
                        severity_scores.append(symptom.severity)
            
            if severity_scores:
                severity_variance = statistics.variance(severity_scores) if len(severity_scores) > 1 else 0
                severity_uncertainty = min(severity_variance / 2.0, 0.5)
                uncertainty_scores.append(severity_uncertainty)
                
                if severity_variance > 1.5:
                    uncertainty_factors.append("inconsistent_severity_reporting")
            else:
                uncertainty_scores.append(0.3)
                uncertainty_factors.append("missing_severity_information")
            
            # Calculate weighted uncertainty
            weights = self.uncertainty_models["symptom_uncertainty"]["uncertainty_weights"]
            weighted_uncertainty = (
                uncertainty_scores[0] * weights["symptom_specificity"] +
                uncertainty_scores[1] * weights["symptom_count"] +
                uncertainty_scores[2] * weights["symptom_severity"]
            )
            
            # Generate recommendations
            recommendations = []
            if specificity_uncertainty > 0.4:
                recommendations.append("Request more specific symptom descriptions")
            if symptom_count < 3:
                recommendations.append("Gather additional symptom information")
            if "missing_severity_information" in uncertainty_factors:
                recommendations.append("Assess and document symptom severity")
            
            return UncertaintyEstimate(
                uncertainty_type=UncertaintyType.LINGUISTIC,
                value=weighted_uncertainty,
                confidence_interval=(max(0, weighted_uncertainty - 0.1), min(1, weighted_uncertainty + 0.1)),
                explanation=f"Symptom uncertainty based on specificity, count, and severity consistency",
                factors=uncertainty_factors,
                recommendations=recommendations
            )
            
        except Exception as e:
            logger.error(f"Error analyzing symptom uncertainty: {e}")
            return UncertaintyEstimate(
                uncertainty_type=UncertaintyType.LINGUISTIC,
                value=0.5,
                confidence_interval=(0.4, 0.6),
                explanation="Error in symptom uncertainty analysis",
                factors=["analysis_error"],
                recommendations=["Manual symptom review recommended"]
            )
    
    async def _analyze_diagnostic_uncertainty(self, symptoms: List[Symptom],
                                            predicted_conditions: List[Dict[str, Any]],
                                            patient_context: Dict[str, Any]) -> UncertaintyEstimate:
        """Analyze uncertainty in diagnostic predictions"""
        try:
            if not predicted_conditions:
                return UncertaintyEstimate(
                    uncertainty_type=UncertaintyType.DIAGNOSTIC,
                    value=1.0,
                    confidence_interval=(0.9, 1.0),
                    explanation="No diagnostic predictions available",
                    factors=["no_predictions"],
                    recommendations=["Run diagnostic analysis"]
                )
            
            uncertainty_factors = []
            
            # Analyze prediction confidence distribution
            confidences = [condition.get("confidence", 0.5) for condition in predicted_conditions]
            probabilities = [condition.get("probability", 0.0) for condition in predicted_conditions]
            
            # Model confidence uncertainty
            avg_confidence = statistics.mean(confidences) if confidences else 0.5
            confidence_variance = statistics.variance(confidences) if len(confidences) > 1 else 0
            model_uncertainty = 1 - avg_confidence + (confidence_variance * 0.5)
            
            if avg_confidence < 0.6:
                uncertainty_factors.append("low_model_confidence")
            if confidence_variance > 0.1:
                uncertainty_factors.append("inconsistent_prediction_confidence")
            
            # Differential diagnosis overlap
            top_probabilities = sorted(probabilities, reverse=True)[:3]
            if len(top_probabilities) >= 2:
                prob_gap = top_probabilities[0] - top_probabilities[1]
                if prob_gap < 0.2:
                    differential_uncertainty = 0.4
                    uncertainty_factors.append("close_differential_diagnosis")
                else:
                    differential_uncertainty = max(0, 0.3 - prob_gap)
            else:
                differential_uncertainty = 0.2
            
            # Rare condition uncertainty
            rare_conditions = ["rare_disease", "orphan_disease", "uncommon"]
            rare_condition_penalty = 0
            for condition in predicted_conditions:
                condition_name = condition.get("name", "").lower()
                if any(rare in condition_name for rare in rare_conditions):
                    rare_condition_penalty += 0.2
                    uncertainty_factors.append("rare_condition_prediction")
            
            rare_condition_penalty = min(rare_condition_penalty, 0.4)
            
            # Information completeness
            required_info = ["age", "gender", "medical_history", "medications"]
            available_info = sum(1 for info in required_info if patient_context.get(info))
            completeness_score = available_info / len(required_info)
            information_uncertainty = 1 - completeness_score
            
            if completeness_score < 0.5:
                uncertainty_factors.append("incomplete_patient_information")
            
            # Calculate weighted diagnostic uncertainty
            weights = self.uncertainty_models["diagnosis_uncertainty"]
            weighted_uncertainty = (
                differential_uncertainty * weights["differential_overlap"] +
                rare_condition_penalty * weights["rare_conditions"] +
                information_uncertainty * weights["incomplete_information"] +
                model_uncertainty * weights["model_confidence"]
            )
            
            # Clamp to [0, 1]
            weighted_uncertainty = max(0, min(1, weighted_uncertainty))
            
            # Generate recommendations
            recommendations = []
            if model_uncertainty > 0.5:
                recommendations.append("Consider additional diagnostic testing")
            if differential_uncertainty > 0.3:
                recommendations.append("Review differential diagnosis carefully")
            if information_uncertainty > 0.4:
                recommendations.append("Gather additional patient history")
            if rare_condition_penalty > 0.1:
                recommendations.append("Verify rare condition diagnosis with specialist")
            
            return UncertaintyEstimate(
                uncertainty_type=UncertaintyType.DIAGNOSTIC,
                value=weighted_uncertainty,
                confidence_interval=(max(0, weighted_uncertainty - 0.15), min(1, weighted_uncertainty + 0.15)),
                explanation=f"Diagnostic uncertainty from model confidence, differential overlap, and information completeness",
                factors=uncertainty_factors,
                recommendations=recommendations
            )
            
        except Exception as e:
            logger.error(f"Error analyzing diagnostic uncertainty: {e}")
            return UncertaintyEstimate(
                uncertainty_type=UncertaintyType.DIAGNOSTIC,
                value=0.6,
                confidence_interval=(0.5, 0.7),
                explanation="Error in diagnostic uncertainty analysis",
                factors=["analysis_error"],
                recommendations=["Manual diagnostic review recommended"]
            )
    
    async def _analyze_treatment_uncertainty(self, recommended_treatments: List[Dict[str, Any]],
                                           predicted_conditions: List[Dict[str, Any]],
                                           patient_context: Dict[str, Any]) -> UncertaintyEstimate:
        """Analyze uncertainty in treatment recommendations"""
        try:
            if not recommended_treatments:
                return UncertaintyEstimate(
                    uncertainty_type=UncertaintyType.TREATMENT,
                    value=0.8,
                    confidence_interval=(0.7, 0.9),
                    explanation="No treatment recommendations available",
                    factors=["no_treatments"],
                    recommendations=["Generate treatment recommendations"]
                )
            
            uncertainty_factors = []
            
            # Contraindication uncertainty
            contraindications = 0
            for treatment in recommended_treatments:
                # Check for potential contraindications based on patient context
                treatment_name = treatment.get("name", "").lower()
                patient_allergies = patient_context.get("allergies", [])
                patient_medications = patient_context.get("medications", [])
                
                # Simple contraindication checks (would be more sophisticated in practice)
                if any(allergy in treatment_name for allergy in patient_allergies):
                    contraindications += 1
                    uncertainty_factors.append("potential_allergy_contraindication")
                
                # Check for drug interactions (simplified)
                if "anticoagulant" in treatment_name and any("aspirin" in med for med in patient_medications):
                    contraindications += 1
                    uncertainty_factors.append("potential_drug_interaction")
            
            contraindication_uncertainty = min(contraindications * 0.3, 0.6)
            
            # Individual variation uncertainty
            age = patient_context.get("age", 50)
            if age < 18 or age > 75:
                age_uncertainty = 0.2
                uncertainty_factors.append("age_related_treatment_variation")
            else:
                age_uncertainty = 0.05
            
            # Comorbidity complexity
            medical_history = patient_context.get("medical_history", [])
            comorbidity_count = len(medical_history)
            if comorbidity_count >= 3:
                comorbidity_uncertainty = min(comorbidity_count * 0.1, 0.4)
                uncertainty_factors.append("complex_comorbidity_profile")
            else:
                comorbidity_uncertainty = 0.1
            
            individual_variation_uncertainty = age_uncertainty + comorbidity_uncertainty
            
            # Evidence quality uncertainty (simplified assessment)
            evidence_uncertainty = 0.2  # Default evidence uncertainty
            for treatment in recommended_treatments:
                confidence = treatment.get("confidence", 0.5)
                if confidence < 0.6:
                    evidence_uncertainty += 0.1
                    uncertainty_factors.append("low_evidence_confidence")
            
            evidence_uncertainty = min(evidence_uncertainty, 0.5)
            
            # Side effect profile uncertainty
            side_effect_uncertainty = 0.15  # Default side effect uncertainty
            for treatment in recommended_treatments:
                # Check for treatments with known high side effect profiles
                treatment_name = treatment.get("name", "").lower()
                high_risk_treatments = ["chemotherapy", "immunosuppressant", "anticoagulant"]
                if any(risk_treatment in treatment_name for risk_treatment in high_risk_treatments):
                    side_effect_uncertainty += 0.1
                    uncertainty_factors.append("high_side_effect_risk")
            
            side_effect_uncertainty = min(side_effect_uncertainty, 0.4)
            
            # Calculate weighted treatment uncertainty
            weights = self.uncertainty_models["treatment_uncertainty"]
            weighted_uncertainty = (
                contraindication_uncertainty * weights["contraindications"] +
                individual_variation_uncertainty * weights["individual_variation"] +
                evidence_uncertainty * weights["evidence_quality"] +
                side_effect_uncertainty * weights["side_effect_profile"]
            )
            
            # Clamp to [0, 1]
            weighted_uncertainty = max(0, min(1, weighted_uncertainty))
            
            # Generate recommendations
            recommendations = []
            if contraindication_uncertainty > 0.2:
                recommendations.append("Review contraindications and drug interactions")
            if individual_variation_uncertainty > 0.3:
                recommendations.append("Consider patient-specific factors for treatment selection")
            if evidence_uncertainty > 0.3:
                recommendations.append("Review treatment evidence and guidelines")
            if side_effect_uncertainty > 0.25:
                recommendations.append("Discuss potential side effects with patient")
            
            return UncertaintyEstimate(
                uncertainty_type=UncertaintyType.TREATMENT,
                value=weighted_uncertainty,
                confidence_interval=(max(0, weighted_uncertainty - 0.1), min(1, weighted_uncertainty + 0.1)),
                explanation=f"Treatment uncertainty from contraindications, individual variation, and evidence quality",
                factors=uncertainty_factors,
                recommendations=recommendations
            )
            
        except Exception as e:
            logger.error(f"Error analyzing treatment uncertainty: {e}")
            return UncertaintyEstimate(
                uncertainty_type=UncertaintyType.TREATMENT,
                value=0.5,
                confidence_interval=(0.4, 0.6),
                explanation="Error in treatment uncertainty analysis",
                factors=["analysis_error"],
                recommendations=["Manual treatment review recommended"]
            )
    
    async def _calculate_overall_confidence(self, symptom_uncertainty: UncertaintyEstimate,
                                          diagnostic_uncertainty: UncertaintyEstimate,
                                          treatment_uncertainty: UncertaintyEstimate) -> ConfidenceAnalysis:
        """Calculate overall confidence from uncertainty estimates"""
        try:
            # Convert uncertainties to confidences
            symptom_confidence = 1 - symptom_uncertainty.value
            diagnostic_confidence = 1 - diagnostic_uncertainty.value
            treatment_confidence = 1 - treatment_uncertainty.value
            
            # Weighted overall confidence
            confidence_weights = {"symptom": 0.25, "diagnostic": 0.45, "treatment": 0.30}
            overall_confidence = (
                symptom_confidence * confidence_weights["symptom"] +
                diagnostic_confidence * confidence_weights["diagnostic"] +
                treatment_confidence * confidence_weights["treatment"]
            )
            
            # Determine confidence level
            if overall_confidence >= 0.9:
                confidence_level = ConfidenceLevel.VERY_HIGH
            elif overall_confidence >= 0.75:
                confidence_level = ConfidenceLevel.HIGH
            elif overall_confidence >= 0.6:
                confidence_level = ConfidenceLevel.MODERATE
            elif overall_confidence >= 0.4:
                confidence_level = ConfidenceLevel.LOW
            else:
                confidence_level = ConfidenceLevel.VERY_LOW
            
            # Reliability score (consistency of confidence across domains)
            confidence_values = [symptom_confidence, diagnostic_confidence, treatment_confidence]
            confidence_variance = statistics.variance(confidence_values)
            reliability_score = max(0, 1 - (confidence_variance * 2))
            
            # Calibration score (how well-calibrated our confidence estimates are)
            calibration_score = self._calculate_calibration_score(overall_confidence)
            
            return ConfidenceAnalysis(
                overall_confidence=overall_confidence,
                confidence_level=confidence_level,
                confidence_factors={
                    "symptom_confidence": symptom_confidence,
                    "diagnostic_confidence": diagnostic_confidence,
                    "treatment_confidence": treatment_confidence
                },
                uncertainty_breakdown={
                    UncertaintyType.LINGUISTIC: symptom_uncertainty.value,
                    UncertaintyType.DIAGNOSTIC: diagnostic_uncertainty.value,
                    UncertaintyType.TREATMENT: treatment_uncertainty.value
                },
                reliability_score=reliability_score,
                calibration_score=calibration_score,
                explanation=f"Overall confidence: {confidence_level.value} ({overall_confidence:.2f}). "
                          f"Based on symptom clarity, diagnostic certainty, and treatment confidence."
            )
            
        except Exception as e:
            logger.error(f"Error calculating overall confidence: {e}")
            return ConfidenceAnalysis(
                overall_confidence=0.5,
                confidence_level=ConfidenceLevel.MODERATE,
                confidence_factors={},
                uncertainty_breakdown={},
                reliability_score=0.5,
                calibration_score=0.5,
                explanation="Error in confidence calculation"
            )
    
    async def _generate_uncertainty_recommendations(self, symptom_uncertainty: UncertaintyEstimate,
                                                  diagnostic_uncertainty: UncertaintyEstimate,
                                                  treatment_uncertainty: UncertaintyEstimate) -> List[Dict[str, Any]]:
        """Generate actionable recommendations based on uncertainty analysis"""
        recommendations = []
        
        # High symptom uncertainty recommendations
        if symptom_uncertainty.value > 0.5:
            recommendations.append({
                "category": "symptom_clarification",
                "priority": "high",
                "action": "Gather more detailed symptom information",
                "rationale": "High uncertainty in symptom interpretation",
                "specific_steps": symptom_uncertainty.recommendations
            })
        
        # High diagnostic uncertainty recommendations
        if diagnostic_uncertainty.value > 0.6:
            recommendations.append({
                "category": "diagnostic_verification",
                "priority": "high",
                "action": "Seek additional diagnostic confirmation",
                "rationale": "High uncertainty in diagnostic predictions",
                "specific_steps": diagnostic_uncertainty.recommendations
            })
        
        # High treatment uncertainty recommendations
        if treatment_uncertainty.value > 0.5:
            recommendations.append({
                "category": "treatment_review",
                "priority": "moderate",
                "action": "Review treatment recommendations carefully",
                "rationale": "Uncertainty in treatment safety or efficacy",
                "specific_steps": treatment_uncertainty.recommendations
            })
        
        # Overall uncertainty management
        max_uncertainty = max(symptom_uncertainty.value, diagnostic_uncertainty.value, treatment_uncertainty.value)
        if max_uncertainty > 0.7:
            recommendations.append({
                "category": "expert_consultation",
                "priority": "high",
                "action": "Consider expert medical consultation",
                "rationale": "High overall uncertainty requires human expertise",
                "specific_steps": ["Consult specialist", "Review with senior physician", "Consider second opinion"]
            })
        
        return recommendations
    
    async def _calculate_confidence_intervals(self, predicted_conditions: List[Dict[str, Any]],
                                            treatment_uncertainty: UncertaintyEstimate) -> Dict[str, Dict[str, float]]:
        """Calculate confidence intervals for predictions"""
        intervals = {}
        
        for condition in predicted_conditions:
            condition_name = condition.get("name", "unknown")
            probability = condition.get("probability", 0.5)
            confidence = condition.get("confidence", 0.5)
            
            # Calculate margin of error based on uncertainty
            margin_of_error = (1 - confidence) * 0.2 + treatment_uncertainty.value * 0.1
            
            intervals[condition_name] = {
                "probability_lower": max(0, probability - margin_of_error),
                "probability_upper": min(1, probability + margin_of_error),
                "confidence_level": 0.9  # 90% confidence interval
            }
        
        return intervals
    
    async def _assess_calibration_quality(self, predicted_conditions: List[Dict[str, Any]],
                                        overall_confidence: ConfidenceAnalysis) -> Dict[str, Any]:
        """Assess how well-calibrated our confidence estimates are"""
        # This would typically use historical validation data
        # For now, we provide a simplified assessment
        
        confidences = [condition.get("confidence", 0.5) for condition in predicted_conditions]
        if not confidences:
            return {"calibration_status": "unknown", "reason": "no_predictions"}
        
        avg_confidence = statistics.mean(confidences)
        confidence_std = statistics.stdev(confidences) if len(confidences) > 1 else 0
        
        # Simple calibration assessment
        if abs(avg_confidence - overall_confidence.overall_confidence) < 0.1:
            calibration_status = "well_calibrated"
        elif avg_confidence > overall_confidence.overall_confidence + 0.2:
            calibration_status = "overconfident"
        elif avg_confidence < overall_confidence.overall_confidence - 0.2:
            calibration_status = "underconfident"
        else:
            calibration_status = "moderately_calibrated"
        
        return {
            "calibration_status": calibration_status,
            "average_prediction_confidence": avg_confidence,
            "overall_system_confidence": overall_confidence.overall_confidence,
            "confidence_consistency": 1 - confidence_std,
            "reliability_indicator": calibration_status in ["well_calibrated", "moderately_calibrated"]
        }
    
    async def _generate_decision_support(self, overall_confidence: ConfidenceAnalysis,
                                       uncertainty_breakdown: Dict[str, UncertaintyEstimate]) -> Dict[str, Any]:
        """Generate decision support recommendations"""
        decision_support = {
            "recommended_action": "",
            "caution_level": "",
            "next_steps": [],
            "monitoring_requirements": [],
            "consultation_recommendations": []
        }
        
        confidence_value = overall_confidence.overall_confidence
        
        if confidence_value >= 0.8:
            decision_support["recommended_action"] = "Proceed with recommendations"
            decision_support["caution_level"] = "low"
            decision_support["next_steps"] = ["Implement treatment plan", "Schedule follow-up"]
        elif confidence_value >= 0.6:
            decision_support["recommended_action"] = "Proceed with caution"
            decision_support["caution_level"] = "moderate"
            decision_support["next_steps"] = ["Verify key assumptions", "Monitor closely", "Be prepared to adjust"]
            decision_support["monitoring_requirements"] = ["Regular symptom monitoring", "Response assessment"]
        elif confidence_value >= 0.4:
            decision_support["recommended_action"] = "Seek additional information"
            decision_support["caution_level"] = "high"
            decision_support["next_steps"] = ["Gather more data", "Consider additional testing", "Reassess"]
            decision_support["consultation_recommendations"] = ["Consider specialist consultation"]
        else:
            decision_support["recommended_action"] = "Exercise extreme caution"
            decision_support["caution_level"] = "very_high"
            decision_support["next_steps"] = ["Comprehensive reevaluation required"]
            decision_support["consultation_recommendations"] = ["Immediate expert consultation required"]
        
        return decision_support
    
    async def _calculate_reliability_metrics(self, symptoms: List[Symptom],
                                           predicted_conditions: List[Dict[str, Any]],
                                           patient_context: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate reliability metrics for the analysis"""
        reliability_metrics = {}
        
        # Data quality assessment
        data_completeness = self._assess_data_completeness(symptoms, patient_context)
        data_consistency = self._assess_data_consistency(symptoms, predicted_conditions)
        
        # Model reliability assessment
        prediction_consistency = self._assess_prediction_consistency(predicted_conditions)
        
        reliability_metrics = {
            "data_quality": {
                "completeness": data_completeness,
                "consistency": data_consistency,
                "overall_quality": (data_completeness + data_consistency) / 2
            },
            "prediction_quality": {
                "consistency": prediction_consistency,
                "confidence_distribution": self._analyze_confidence_distribution(predicted_conditions)
            },
            "overall_reliability": (data_completeness + data_consistency + prediction_consistency) / 3
        }
        
        return reliability_metrics
    
    def _calculate_calibration_score(self, confidence: float) -> float:
        """Calculate calibration score for confidence estimate"""
        # Simplified calibration score
        # In practice, this would use historical validation data
        if 0.7 <= confidence <= 0.9:
            return 0.9  # Well-calibrated range
        elif 0.5 <= confidence <= 0.95:
            return 0.7  # Moderately calibrated
        else:
            return 0.5  # Poorly calibrated
    
    def _assess_data_completeness(self, symptoms: List[Symptom], patient_context: Dict[str, Any]) -> float:
        """Assess completeness of available data"""
        total_factors = 6
        available_factors = 0
        
        if symptoms and len(symptoms) >= 2:
            available_factors += 1
        if patient_context.get("age"):
            available_factors += 1
        if patient_context.get("gender"):
            available_factors += 1
        if patient_context.get("medical_history"):
            available_factors += 1
        if patient_context.get("medications"):
            available_factors += 1
        if any(hasattr(s, 'severity') for s in symptoms):
            available_factors += 1
        
        return available_factors / total_factors
    
    def _assess_data_consistency(self, symptoms: List[Symptom], predicted_conditions: List[Dict[str, Any]]) -> float:
        """Assess consistency of data"""
        # Simplified consistency check
        if not symptoms or not predicted_conditions:
            return 0.5
        
        # Check if number of symptoms is reasonable for number of conditions
        symptom_condition_ratio = len(symptoms) / len(predicted_conditions)
        if 0.5 <= symptom_condition_ratio <= 3.0:
            ratio_consistency = 1.0
        else:
            ratio_consistency = 0.6
        
        return ratio_consistency
    
    def _assess_prediction_consistency(self, predicted_conditions: List[Dict[str, Any]]) -> float:
        """Assess consistency of predictions"""
        if not predicted_conditions:
            return 0.5
        
        confidences = [condition.get("confidence", 0.5) for condition in predicted_conditions]
        probabilities = [condition.get("probability", 0.5) for condition in predicted_conditions]
        
        # Check if confidences and probabilities are reasonably aligned
        if len(confidences) == len(probabilities):
            alignment_scores = [abs(c - p) for c, p in zip(confidences, probabilities)]
            avg_alignment = statistics.mean(alignment_scores)
            consistency = max(0, 1 - (avg_alignment * 2))
        else:
            consistency = 0.5
        
        return consistency
    
    def _analyze_confidence_distribution(self, predicted_conditions: List[Dict[str, Any]]) -> Dict[str, float]:
        """Analyze distribution of confidence scores"""
        if not predicted_conditions:
            return {"mean": 0.5, "std": 0.0, "range": 0.0}
        
        confidences = [condition.get("confidence", 0.5) for condition in predicted_conditions]
        
        return {
            "mean": statistics.mean(confidences),
            "std": statistics.stdev(confidences) if len(confidences) > 1 else 0.0,
            "range": max(confidences) - min(confidences) if confidences else 0.0,
            "distribution_quality": "good" if statistics.stdev(confidences) < 0.3 else "poor" if len(confidences) > 1 else "insufficient_data"
        }

# Global uncertainty quantifier instance
uncertainty_quantifier = UncertaintyQuantifier()
