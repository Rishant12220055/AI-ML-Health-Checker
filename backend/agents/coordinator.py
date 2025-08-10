"""
Agent Coordinator

This module coordinates the multi-agent AI system:
1. Orchestrates the three specialized agents
2. Manages workflow between agents
3. Combines results into comprehensive diagnosis
4. Provides explainable AI output
"""

import asyncio
import uuid
from datetime import datetime
from typing import Dict, Any, List
import logging
import time

from models.schemas import (
    SymptomInput, DiagnosisResponse, DiagnosisExplanation, 
    UrgencyLevel, AgentResponse
)
from agents.symptom_classifier import SymptomClassifierAgent
from agents.condition_matcher import ConditionMatcherAgent
from agents.treatment_retriever import TreatmentRetrieverAgent
from utils.emergency_detection import detect_emergency_conditions
from utils.drug_interactions import DrugInteractionSystem
from utils.risk_assessment import AdvancedRiskAssessment
from utils.analytics import analytics_engine, PerformanceMetric, MetricType
from utils.uncertainty_quantification import uncertainty_quantifier

logger = logging.getLogger(__name__)

class AgentCoordinator:
    """Enhanced coordinator for the multi-agent AI system with safety and analytics"""
    
    def __init__(self, database_manager, guidelines_manager):
        self.database_manager = database_manager
        self.guidelines_manager = guidelines_manager
        
        # Initialize core agents
        self.symptom_classifier = SymptomClassifierAgent()
        self.condition_matcher = ConditionMatcherAgent()
        self.treatment_retriever = TreatmentRetrieverAgent()
        
        # Initialize safety and analytics systems
        self.drug_interaction_checker = DrugInteractionSystem()
        self.risk_assessor = AdvancedRiskAssessment()
        
        self.agents_initialized = False
    
    async def initialize_agents(self):
        """Initialize all AI agents"""
        try:
            logger.info("Initializing multi-agent system...")
            
            # Initialize agents in parallel for better performance
            await asyncio.gather(
                self.symptom_classifier.initialize(),
                self.condition_matcher.initialize(),
                self.treatment_retriever.initialize()
            )
            
            self.agents_initialized = True
            logger.info("Multi-agent system initialized successfully")
            
        except Exception as e:
            logger.error(f"Error initializing agents: {e}")
            raise
    
    async def process_symptoms(self, symptom_input: SymptomInput) -> DiagnosisResponse:
        """
        Process symptoms through the multi-agent system
        
        Args:
            symptom_input: Patient symptoms and information
            
        Returns:
            Complete diagnosis response with recommendations
        """
        if not self.agents_initialized:
            raise RuntimeError("Agents not initialized. Call initialize_agents() first.")
        
        session_id = str(uuid.uuid4())
        start_time = datetime.utcnow()
        
        try:
            logger.info(f"Processing symptoms for session {session_id}")
            
            # Step 1: Symptom Classification
            logger.debug("Running symptom classification...")
            symptom_response = await self.symptom_classifier.process_symptoms(symptom_input)
            
            if symptom_response.errors:
                logger.warning(f"Symptom classifier errors: {symptom_response.errors}")
            
            # Step 2: Condition Matching (depends on symptom classification)
            logger.debug("Running condition matching...")
            condition_response = await self.condition_matcher.process_symptoms(
                symptom_input, symptom_response.results
            )
            
            if condition_response.errors:
                logger.warning(f"Condition matcher errors: {condition_response.errors}")
            
            # Step 3: Treatment Retrieval (depends on condition matching)
            logger.debug("Running treatment retrieval...")
            conditions = condition_response.results.get("differential_diagnosis", [])
            treatment_response = await self.treatment_retriever.process_conditions(
                conditions, symptom_input.patient_info
            )
            
            if treatment_response.errors:
                logger.warning(f"Treatment retriever errors: {treatment_response.errors}")
            
            # Step 4: Combine results and generate comprehensive response
            logger.debug("Generating comprehensive diagnosis response...")
            diagnosis_response = await self._generate_diagnosis_response(
                session_id,
                start_time,
                symptom_input,
                symptom_response,
                condition_response,
                treatment_response
            )
            
            logger.info(f"Successfully processed symptoms for session {session_id}")
            return diagnosis_response
            
        except Exception as e:
            logger.error(f"Error processing symptoms for session {session_id}: {e}")
            
            # Return error response
            return DiagnosisResponse(
                session_id=session_id,
                timestamp=start_time,
                urgency_level=UrgencyLevel.MODERATE,
                symptom_classification={"error": "Symptom classification failed"},
                possible_conditions=[],
                recommended_treatments=[],
                next_steps=["Contact healthcare provider for evaluation"],
                warning_signs=["Monitor symptoms closely"],
                when_to_seek_care="If symptoms persist or worsen",
                explanation=DiagnosisExplanation(
                    reasoning_steps=["Error occurred during analysis"],
                    evidence_supporting=["System error"],
                    evidence_against=[],
                    alternative_diagnoses=[],
                    confidence_factors={"system_error": 0.0},
                    guidelines_used=[]
                )
            )
    
    async def _generate_diagnosis_response(self, session_id: str, start_time: datetime,
                                         symptom_input: SymptomInput,
                                         symptom_response: AgentResponse,
                                         condition_response: AgentResponse,
                                         treatment_response: AgentResponse) -> DiagnosisResponse:
        """Generate comprehensive diagnosis response from agent results"""
        
        # Extract results from each agent
        symptom_results = symptom_response.results
        condition_results = condition_response.results
        treatment_results = treatment_response.results
        
        # Determine overall urgency level
        urgency_level = UrgencyLevel(treatment_results.get("urgency_level", "moderate"))
        
        # Get differential diagnosis
        possible_conditions = condition_results.get("differential_diagnosis", [])
        
        # Get treatment recommendations
        recommended_treatments = treatment_results.get("treatment_recommendations", [])
        
        # Generate next steps
        next_steps = treatment_results.get("next_steps", [])
        
        # Generate warning signs
        warning_signs = treatment_results.get("warning_signs", [])
        
        # Generate care instructions
        when_to_seek_care = treatment_results.get("when_to_seek_care", "Consult healthcare provider")
        
        # Generate explainable AI output
        explanation = await self._generate_explanation(
            symptom_input, symptom_response, condition_response, treatment_response
        )
        
        return DiagnosisResponse(
            session_id=session_id,
            timestamp=start_time,
            urgency_level=urgency_level,
            symptom_classification=symptom_results,
            possible_conditions=possible_conditions,
            recommended_treatments=recommended_treatments,
            next_steps=next_steps,
            warning_signs=warning_signs,
            when_to_seek_care=when_to_seek_care,
            explanation=explanation
        )
    
    async def _generate_explanation(self, symptom_input: SymptomInput,
                                  symptom_response: AgentResponse,
                                  condition_response: AgentResponse,
                                  treatment_response: AgentResponse) -> DiagnosisExplanation:
        """Generate explainable AI output for regulatory compliance"""
        
        # Build reasoning steps
        reasoning_steps = [
            f"Analyzed {len(symptom_input.symptoms)} reported symptoms",
            f"Classified symptoms into {len(symptom_response.results.get('system_classification', {}))} body systems",
            f"Identified {len(condition_response.results.get('differential_diagnosis', []))} possible conditions",
            f"Generated {len(treatment_response.results.get('treatment_recommendations', []))} treatment recommendations",
            f"Assessed urgency level as {treatment_response.results.get('urgency_level', 'moderate')}"
        ]
        
        # Gather supporting evidence
        evidence_supporting = []
        top_condition = condition_response.results.get("differential_diagnosis", [])
        if top_condition:
            top_condition = top_condition[0]
            evidence_supporting.extend([
                f"Primary condition probability: {top_condition.get('probability', 0):.2f}",
                f"Matching symptoms: {', '.join(top_condition.get('symptoms_match', []))}",
                f"Patient age group compatibility: {symptom_input.patient_info.age} years"
            ])
        
        # Identify alternative diagnoses
        alternative_diagnoses = []
        all_conditions = condition_response.results.get("differential_diagnosis", [])
        if len(all_conditions) > 1:
            for condition in all_conditions[1:3]:  # Top 2 alternatives
                alternative_diagnoses.append(
                    f"{condition.get('name', 'Unknown')} (probability: {condition.get('probability', 0):.2f})"
                )
        
        # Calculate confidence factors
        confidence_factors = {
            "symptom_classification": symptom_response.confidence,
            "condition_matching": condition_response.confidence,
            "treatment_retrieval": treatment_response.confidence,
            "overall_confidence": (symptom_response.confidence + 
                                 condition_response.confidence + 
                                 treatment_response.confidence) / 3
        }
        
        # Identify guidelines used
        guidelines_used = []
        treatments = treatment_response.results.get("treatment_recommendations", [])
        for treatment in treatments:
            if treatment.get("who_guideline"):
                guidelines_used.append(f"WHO: {treatment['who_guideline']}")
            if treatment.get("cdc_guideline"):
                guidelines_used.append(f"CDC: {treatment['cdc_guideline']}")
        
        return DiagnosisExplanation(
            reasoning_steps=reasoning_steps,
            evidence_supporting=evidence_supporting,
            evidence_against=[],  # Could be enhanced with contradictory evidence
            alternative_diagnoses=alternative_diagnoses,
            confidence_factors=confidence_factors,
            guidelines_used=list(set(guidelines_used))  # Remove duplicates
        )
    
    async def assess_urgency(self, symptoms: List[str]) -> str:
        """Quick urgency assessment for triage purposes"""
        # Emergency keywords
        emergency_keywords = [
            "severe chest pain", "difficulty breathing", "loss of consciousness",
            "severe bleeding", "severe abdominal pain", "stroke symptoms"
        ]
        
        # Urgent keywords
        urgent_keywords = [
            "high fever", "severe headache", "persistent vomiting",
            "severe pain", "dehydration"
        ]
        
        # Check for emergency symptoms
        for symptom in symptoms:
            symptom_lower = symptom.lower()
            if any(keyword in symptom_lower for keyword in emergency_keywords):
                return "emergency"
        
        # Check for urgent symptoms
        for symptom in symptoms:
            symptom_lower = symptom.lower()
            if any(keyword in symptom_lower for keyword in urgent_keywords):
                return "urgent"
        
        # Default to moderate
        return "moderate"
    
    async def explain_diagnosis(self, diagnosis_id: str) -> Dict[str, Any]:
        """Generate detailed explanation for a specific diagnosis"""
        # This would typically retrieve the diagnosis from database
        # For now, return a template explanation
        return {
            "diagnosis_id": diagnosis_id,
            "explanation_type": "detailed_reasoning",
            "ai_models_used": [
                "ClinicalBERT for symptom understanding",
                "Sentence Transformers for semantic similarity",
                "Rule-based medical knowledge matching"
            ],
            "confidence_breakdown": {
                "symptom_recognition": "High - Clear symptom patterns identified",
                "condition_matching": "Medium - Multiple conditions possible",
                "treatment_selection": "High - Evidence-based guidelines followed"
            },
            "medical_guidelines_referenced": [
                "WHO Treatment Guidelines 2023",
                "CDC Clinical Recommendations 2023",
                "Evidence-based medicine protocols"
            ],
            "limitations": [
                "AI assessment is not a substitute for professional medical evaluation",
                "Individual patient factors may not be fully captured",
                "Emergency situations require immediate medical attention"
            ]
        }
    
    async def health_check(self) -> Dict[str, bool]:
        """Check health status of all agents"""
        if not self.agents_initialized:
            return {
                "symptom_classifier": False,
                "condition_matcher": False,
                "treatment_retriever": False,
                "overall": False
            }
        
        try:
            # Check each agent in parallel
            health_checks = await asyncio.gather(
                self.symptom_classifier.health_check(),
                self.condition_matcher.health_check(),
                self.treatment_retriever.health_check(),
                return_exceptions=True
            )
            
            symptom_health = health_checks[0] if not isinstance(health_checks[0], Exception) else False
            condition_health = health_checks[1] if not isinstance(health_checks[1], Exception) else False
            treatment_health = health_checks[2] if not isinstance(health_checks[2], Exception) else False
            
            return {
                "symptom_classifier": symptom_health,
                "condition_matcher": condition_health,
                "treatment_retriever": treatment_health,
                "overall": all([symptom_health, condition_health, treatment_health])
            }
            
        except Exception as e:
            logger.error(f"Error during health check: {e}")
            return {
                "symptom_classifier": False,
                "condition_matcher": False,
                "treatment_retriever": False,
                "overall": False
            }
    
    async def _generate_enhanced_diagnosis_response(self, session_id: str, start_time: datetime,
                                                  symptom_input: SymptomInput,
                                                  symptom_response: AgentResponse,
                                                  condition_response: AgentResponse,
                                                  treatment_response: AgentResponse,
                                                  emergency_assessment: Dict[str, Any],
                                                  drug_interactions: Dict[str, Any],
                                                  risk_assessment: Dict[str, Any],
                                                  uncertainty_analysis: Dict[str, Any]) -> DiagnosisResponse:
        """Generate comprehensive enhanced diagnosis response with safety and analytics"""
        
        try:
            # Extract base results from each agent
            symptom_results = symptom_response.results
            condition_results = condition_response.results
            treatment_results = treatment_response.results
            
            # Determine urgency level (emergency takes precedence)
            if emergency_assessment.get("is_emergency", False):
                urgency_level = UrgencyLevel.CRITICAL
            else:
                urgency_level = UrgencyLevel(treatment_results.get("urgency_level", "moderate"))
            
            # Get differential diagnosis with enhanced information
            possible_conditions = condition_results.get("differential_diagnosis", [])
            
            # Enhance conditions with risk assessment
            enhanced_conditions = []
            for condition in possible_conditions:
                condition_name = condition.get("name", "").lower()
                enhanced_condition = condition.copy()
                
                # Add risk information
                if "condition_specific_risks" in risk_assessment:
                    condition_risks = risk_assessment["condition_specific_risks"].get(condition_name, {})
                    enhanced_condition["risk_assessment"] = condition_risks
                
                # Add uncertainty information
                if "uncertainty_breakdown" in uncertainty_analysis:
                    enhanced_condition["uncertainty"] = uncertainty_analysis["uncertainty_breakdown"]
                
                enhanced_conditions.append(enhanced_condition)
            
            # Get treatment recommendations with safety enhancements
            base_treatments = treatment_results.get("treatment_recommendations", [])
            enhanced_treatments = []
            
            for treatment in base_treatments:
                enhanced_treatment = treatment.copy()
                
                # Add drug interaction warnings
                treatment_name = treatment.get("name", "").lower()
                for interaction in drug_interactions.get("interactions", []):
                    if treatment_name in interaction.get("description", "").lower():
                        enhanced_treatment["drug_interaction_warning"] = interaction
                
                # Add contraindication warnings
                for contraindication in drug_interactions.get("contraindications", []):
                    if treatment_name in contraindication.get("medication", "").lower():
                        enhanced_treatment["contraindication_warning"] = contraindication
                
                enhanced_treatments.append(enhanced_treatment)
            
            # Generate enhanced next steps
            next_steps = treatment_results.get("next_steps", [])
            
            # Add emergency-specific steps
            if emergency_assessment.get("is_emergency", False):
                emergency_steps = emergency_assessment.get("recommendations", [])
                next_steps = emergency_steps + next_steps
            
            # Add uncertainty-based recommendations
            if "uncertainty_recommendations" in uncertainty_analysis:
                uncertainty_steps = [rec.get("action", "") for rec in uncertainty_analysis["uncertainty_recommendations"]]
                next_steps.extend(uncertainty_steps)
            
            # Generate enhanced warning signs
            warning_signs = treatment_results.get("warning_signs", [])
            
            # Add emergency warning signs
            if emergency_assessment.get("red_flags"):
                warning_signs.extend(emergency_assessment["red_flags"])
            
            # Add risk-based warning signs
            if "recommendations" in risk_assessment:
                risk_warnings = [rec.get("recommendation", "") for rec in risk_assessment["recommendations"] 
                               if rec.get("category") == "monitoring"]
                warning_signs.extend(risk_warnings)
            
            # Enhanced care instructions
            when_to_seek_care = treatment_results.get("when_to_seek_care", "Consult healthcare provider")
            
            if emergency_assessment.get("is_emergency", False):
                when_to_seek_care = "SEEK IMMEDIATE EMERGENCY CARE"
            elif emergency_assessment.get("urgency_level") == "high":
                when_to_seek_care = "Seek urgent medical attention within 24 hours"
            
            # Generate enhanced explanation
            explanation = await self._generate_enhanced_explanation(
                symptom_input, symptom_response, condition_response, treatment_response,
                emergency_assessment, risk_assessment, uncertainty_analysis
            )
            
            # Create enhanced response with additional fields
            response_data = {
                "session_id": session_id,
                "timestamp": start_time,
                "urgency_level": urgency_level,
                "symptom_classification": symptom_results,
                "possible_conditions": enhanced_conditions,
                "recommended_treatments": enhanced_treatments,
                "next_steps": next_steps,
                "warning_signs": warning_signs,
                "when_to_seek_care": when_to_seek_care,
                "explanation": explanation
            }
            
            # Add enhanced analytics if available
            if emergency_assessment:
                response_data["emergency_assessment"] = emergency_assessment
            
            if drug_interactions.get("interactions") or drug_interactions.get("contraindications"):
                response_data["drug_safety"] = drug_interactions
            
            if risk_assessment:
                response_data["risk_assessment"] = {
                    "overall_risk_score": risk_assessment.get("overall_risk_score"),
                    "risk_level": risk_assessment.get("risk_level"),
                    "high_priority_risks": [r for r in risk_assessment.get("recommendations", []) 
                                          if r.get("priority") == "high"]
                }
            
            if uncertainty_analysis:
                response_data["confidence_analysis"] = {
                    "overall_confidence": uncertainty_analysis.get("overall_confidence", {}).get("overall_confidence"),
                    "confidence_level": uncertainty_analysis.get("overall_confidence", {}).get("confidence_level"),
                    "reliability_score": uncertainty_analysis.get("reliability_metrics", {}).get("overall_reliability"),
                    "uncertainty_recommendations": uncertainty_analysis.get("uncertainty_recommendations", [])
                }
            
            return DiagnosisResponse(**response_data)
            
        except Exception as e:
            logger.error(f"Error generating enhanced diagnosis response: {e}")
            # Fallback to basic response
            return await self._generate_diagnosis_response(
                session_id, start_time, symptom_input, 
                symptom_response, condition_response, treatment_response
            )
    
    async def _generate_enhanced_explanation(self, symptom_input: SymptomInput,
                                           symptom_response: AgentResponse,
                                           condition_response: AgentResponse,
                                           treatment_response: AgentResponse,
                                           emergency_assessment: Dict[str, Any],
                                           risk_assessment: Dict[str, Any],
                                           uncertainty_analysis: Dict[str, Any]) -> DiagnosisExplanation:
        """Generate enhanced explainable AI output with safety and confidence information"""
        
        try:
            # Build enhanced reasoning steps
            reasoning_steps = [
                f"Analyzed {len(symptom_input.symptoms)} reported symptoms",
                f"Classified symptoms into {len(symptom_response.results.get('system_classification', {}))} body systems"
            ]
            
            # Add emergency assessment step
            if emergency_assessment.get("is_emergency", False):
                reasoning_steps.append(f"EMERGENCY DETECTED with {emergency_assessment.get('confidence', 0):.2f} confidence")
            else:
                reasoning_steps.append("No emergency conditions detected")
            
            reasoning_steps.extend([
                f"Identified {len(condition_response.results.get('differential_diagnosis', []))} possible conditions",
                f"Generated {len(treatment_response.results.get('treatment_recommendations', []))} treatment recommendations",
                f"Assessed overall risk level as {risk_assessment.get('risk_level', 'moderate')}",
                f"Calculated uncertainty and confidence metrics"
            ])
            
            # Enhanced supporting evidence
            evidence_supporting = []
            top_condition = condition_response.results.get("differential_diagnosis", [])
            if top_condition:
                top_condition = top_condition[0]
                evidence_supporting.extend([
                    f"Primary condition probability: {top_condition.get('probability', 0):.2f}",
                    f"Matching symptoms: {', '.join(top_condition.get('symptoms_match', []))}",
                    f"Patient age group compatibility: {symptom_input.patient_info.age} years"
                ])
                
                # Add risk factors
                if risk_assessment.get("baseline_risks"):
                    evidence_supporting.append(f"Risk assessment completed for {len(risk_assessment['baseline_risks'])} conditions")
            
            # Enhanced confidence factors
            confidence_factors = {
                "symptom_classification": symptom_response.confidence,
                "condition_matching": condition_response.confidence,
                "treatment_retrieval": treatment_response.confidence,
                "emergency_detection": emergency_assessment.get("confidence", 0.5),
                "overall_confidence": uncertainty_analysis.get("overall_confidence", {}).get("overall_confidence", 0.5),
                "uncertainty_level": 1 - uncertainty_analysis.get("overall_confidence", {}).get("overall_confidence", 0.5)
            }
            
            # Alternative diagnoses with uncertainty
            alternative_diagnoses = []
            all_conditions = condition_response.results.get("differential_diagnosis", [])
            if len(all_conditions) > 1:
                for condition in all_conditions[1:3]:  # Top 2 alternatives
                    uncertainty_info = ""
                    if "uncertainty_breakdown" in uncertainty_analysis:
                        uncertainty_info = f" (uncertainty: {uncertainty_analysis['uncertainty_breakdown'].get('diagnostic', 0):.2f})"
                    alternative_diagnoses.append(
                        f"{condition.get('name', 'Unknown')} (probability: {condition.get('probability', 0):.2f}){uncertainty_info}"
                    )
            
            # Enhanced guidelines used
            guidelines_used = []
            treatments = treatment_response.results.get("treatment_recommendations", [])
            for treatment in treatments:
                if "guideline" in treatment:
                    guidelines_used.append(treatment["guideline"])
            
            # Add safety guidelines
            if emergency_assessment.get("safety_protocols"):
                guidelines_used.extend(emergency_assessment["safety_protocols"])
            
            return DiagnosisExplanation(
                reasoning_steps=reasoning_steps,
                evidence_supporting=evidence_supporting,
                evidence_against=[],  # Could be enhanced with contradictory evidence
                alternative_diagnoses=alternative_diagnoses,
                confidence_factors=confidence_factors,
                guidelines_used=guidelines_used
            )
            
        except Exception as e:
            logger.error(f"Error generating enhanced explanation: {e}")
            # Fallback to basic explanation
            return await self._generate_explanation(
                symptom_input, symptom_response, condition_response, treatment_response
            )
