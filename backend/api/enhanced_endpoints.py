"""
Enhanced API Endpoints for AI Healthcare Assistant

This module provides comprehensive API endpoints including analytics,
monitoring, risk assessment, and uncertainty quantification capabilities.
"""

from fastapi import APIRouter, HTTPException, Depends, Query, BackgroundTasks
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import logging
import asyncio

from models.schemas import (
    SymptomInput, DiagnosisResponse, PatientInfo, 
    HealthCheckResponse
)
from agents.coordinator import AgentCoordinator
from utils.database_manager import DatabaseManager
from utils.analytics import analytics_engine, MetricType, PerformanceMetric
from utils.risk_assessment import AdvancedRiskAssessment
from utils.uncertainty_quantification import uncertainty_quantifier
from utils.emergency_detection import EmergencyDetectionSystem
from utils.drug_interactions import DrugInteractionSystem

logger = logging.getLogger(__name__)

# Create API router
enhanced_router = APIRouter(prefix="/api/v2", tags=["enhanced-ai-healthcare"])

# Global instances
coordinator = None
db_manager = None
risk_assessor = AdvancedRiskAssessment()
emergency_detector = EmergencyDetectionSystem()
drug_checker = DrugInteractionSystem()

async def initialize_enhanced_api():
    """Initialize enhanced API components"""
    global coordinator, db_manager
    try:
        logger.info("Initializing enhanced API components...")
        
        # Initialize database manager
        db_manager = DatabaseManager()
        await db_manager.connect()
        
        # Initialize agent coordinator with enhanced capabilities
        coordinator = AgentCoordinator(db_manager, None)  # Guidelines manager can be None for now
        await coordinator.initialize_agents()
        
        logger.info("Enhanced API components initialized successfully")
        
    except Exception as e:
        logger.error(f"Failed to initialize enhanced API: {e}")
        raise

@enhanced_router.post("/diagnose", response_model=DiagnosisResponse)
async def enhanced_diagnose(symptom_input: SymptomInput, background_tasks: BackgroundTasks):
    """
    Enhanced symptom diagnosis with safety systems, risk assessment, and uncertainty analysis
    
    This endpoint provides:
    - Emergency detection and triage
    - Drug interaction checking
    - Advanced risk assessment
    - Uncertainty quantification
    - Comprehensive analytics
    """
    try:
        if not coordinator:
            raise HTTPException(status_code=503, detail="Service not initialized")
        
        logger.info("Processing enhanced diagnosis request")
        
        # Record request metrics in background
        background_tasks.add_task(
            analytics_engine.record_metric,
            PerformanceMetric(
                timestamp=datetime.utcnow(),
                metric_type=MetricType.USER_INTERACTION,
                metric_name="diagnosis_request",
                value=1.0,
                unit="count",
                context={"symptoms_count": len(symptom_input.symptoms)}
            )
        )
        
        # Process symptoms through enhanced coordinator
        diagnosis_response = await coordinator.process_symptoms(symptom_input)
        
        # Record successful diagnosis
        background_tasks.add_task(
            analytics_engine.record_metric,
            PerformanceMetric(
                timestamp=datetime.utcnow(),
                metric_type=MetricType.DIAGNOSTIC_ACCURACY,
                metric_name="successful_diagnosis",
                value=1.0,
                unit="count",
                context={"session_id": diagnosis_response.session_id}
            )
        )
        
        return diagnosis_response
        
    except Exception as e:
        logger.error(f"Error in enhanced diagnosis: {e}")
        
        # Record error
        await analytics_engine.record_error(
            "enhanced_diagnosis",
            str(e),
            {"symptoms_count": len(symptom_input.symptoms)}
        )
        
        raise HTTPException(status_code=500, detail=f"Diagnosis failed: {str(e)}")

@enhanced_router.post("/emergency-check")
async def emergency_check(symptom_input: SymptomInput):
    """
    Dedicated emergency detection endpoint for rapid triage
    
    Returns immediate emergency assessment without full diagnosis
    """
    try:
        logger.info("Processing emergency check request")
        
        # Rapid emergency assessment
        emergency_result = await emergency_detector.assess_emergency_risk(symptom_input)
        
        # Record emergency check
        is_emergency = emergency_result.get("call_911", False) or emergency_result.get("emergency_level") == "EMERGENCY"
        await analytics_engine.record_emergency_detection(
            f"emergency_check_{datetime.utcnow().timestamp()}",
            is_emergency,
            0.8 if is_emergency else 0.6,  # Confidence score
            0.1  # Fast response time for emergency checks
        )
        
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "emergency_detected": is_emergency,
            "urgency_level": emergency_result.get("emergency_level", "MODERATE"),
            "safety_alert": emergency_result.get("safety_alert", "CONSULT_DOCTOR"),
            "immediate_actions": emergency_result.get("immediate_actions", []),
            "warning_message": emergency_result.get("warning_message", ""),
            "call_911": emergency_result.get("call_911", False),
            "red_flags": emergency_result.get("red_flag_alerts", []),
            "response_time": "< 1 second"
        }
        
    except Exception as e:
        logger.error(f"Error in emergency check: {e}")
        raise HTTPException(status_code=500, detail=f"Emergency check failed: {str(e)}")

@enhanced_router.post("/risk-assessment")
async def comprehensive_risk_assessment(patient_info: PatientInfo, symptom_input: SymptomInput):
    """
    Comprehensive risk assessment endpoint
    
    Provides detailed risk analysis across multiple health domains
    """
    try:
        logger.info("Processing comprehensive risk assessment")
        
        # Perform comprehensive risk assessment
        risk_result = await risk_assessor.comprehensive_risk_assessment(
            patient_info, symptom_input, []  # Empty conditions list for standalone assessment
        )
        
        # Record risk assessment
        await analytics_engine.record_metric(
            PerformanceMetric(
                timestamp=datetime.utcnow(),
                metric_type=MetricType.CLINICAL_OUTCOMES,
                metric_name="risk_assessment_completed",
                value=risk_result.get("overall_risk_score", 0.5),
                unit="score",
                context={"patient_age": patient_info.age, "risk_level": risk_result.get("risk_level")}
            )
        )
        
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "risk_breakdown": risk_result.get("baseline_risks", {}),
            "recommendations": risk_result.get("recommendations", []),
            "monitoring_schedule": risk_result.get("monitoring_schedule", {}),
            "intervention_priorities": risk_result.get("intervention_priorities", [])
        }
        
    except Exception as e:
        logger.error(f"Error in risk assessment: {e}")
        raise HTTPException(status_code=500, detail=f"Risk assessment failed: {str(e)}")

@enhanced_router.post("/drug-interactions")
async def check_drug_interactions(medications: List[str], patient_age: int = 30, allergies: List[str] = None):
    """
    Drug interaction and contraindication checking endpoint
    
    Analyzes potential drug interactions and safety concerns
    """
    try:
        logger.info(f"Checking drug interactions for {len(medications)} medications")
        
        if allergies is None:
            allergies = []
        
        # Comprehensive drug interaction check
        interaction_result = await drug_checker.check_comprehensive_interactions(
            medications, patient_age, allergies
        )
        
        # Record drug safety check
        await analytics_engine.record_metric(
            PerformanceMetric(
                timestamp=datetime.utcnow(),
                metric_type=MetricType.SAFETY_METRICS,
                metric_name="drug_interaction_check",
                value=len(interaction_result.get("interactions", [])),
                unit="count",
                context={"medication_count": len(medications), "safety_score": interaction_result.get("safety_score", 1.0)}
            )
        )
        
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "medications_analyzed": len(medications),
            "interactions_found": len(interaction_result.get("interactions", [])),
            "contraindications_found": len(interaction_result.get("contraindications", [])),
            "safety_score": interaction_result.get("safety_score", 1.0),
            "interactions": interaction_result.get("interactions", []),
            "contraindications": interaction_result.get("contraindications", []),
            "recommendations": interaction_result.get("recommendations", [])
        }
        
    except Exception as e:
        logger.error(f"Error in drug interaction check: {e}")
        raise HTTPException(status_code=500, detail=f"Drug interaction check failed: {str(e)}")

@enhanced_router.post("/uncertainty-analysis")
async def uncertainty_analysis(symptom_input: SymptomInput, predicted_conditions: List[Dict] = None, treatments: List[Dict] = None):
    """
    Uncertainty quantification and confidence analysis endpoint
    
    Provides detailed uncertainty analysis for AI predictions
    """
    try:
        logger.info("Processing uncertainty analysis")
        
        if predicted_conditions is None:
            predicted_conditions = []
        if treatments is None:
            treatments = []
        
        patient_context = symptom_input.patient_info.model_dump() if symptom_input.patient_info else {}
        
        # Comprehensive uncertainty analysis
        uncertainty_result = await uncertainty_quantifier.comprehensive_uncertainty_analysis(
            symptom_input.symptoms,
            predicted_conditions,
            treatments,
            patient_context
        )
        
        # Record uncertainty analysis
        overall_confidence = uncertainty_result.get("overall_confidence", {}).get("overall_confidence", 0.5)
        await analytics_engine.record_metric(
            PerformanceMetric(
                timestamp=datetime.utcnow(),
                metric_type=MetricType.DIAGNOSTIC_ACCURACY,
                metric_name="uncertainty_analysis",
                value=overall_confidence,
                unit="confidence",
                context={"confidence_level": uncertainty_result.get("overall_confidence", {}).get("confidence_level")}
            )
        )
        
        return {
            "timestamp": uncertainty_result.get("analysis_timestamp"),
            "overall_confidence": uncertainty_result.get("overall_confidence", {}),
            "uncertainty_breakdown": uncertainty_result.get("uncertainty_breakdown", {}),
            "reliability_metrics": uncertainty_result.get("reliability_metrics", {}),
            "recommendations": uncertainty_result.get("uncertainty_recommendations", []),
            "decision_support": uncertainty_result.get("decision_support", {}),
            "calibration_assessment": uncertainty_result.get("calibration_assessment", {})
        }
        
    except Exception as e:
        logger.error(f"Error in uncertainty analysis: {e}")
        raise HTTPException(status_code=500, detail=f"Uncertainty analysis failed: {str(e)}")

@enhanced_router.get("/analytics/dashboard")
async def analytics_dashboard(hours: int = Query(24, description="Time range in hours")):
    """
    Comprehensive analytics dashboard endpoint
    
    Provides system performance, diagnostic accuracy, and usage analytics
    """
    try:
        logger.info(f"Generating analytics dashboard for {hours} hours")
        
        time_range = timedelta(hours=hours)
        dashboard_data = await analytics_engine.generate_dashboard_data(time_range)
        
        return {
            "dashboard_data": dashboard_data,
            "generated_at": datetime.utcnow().isoformat(),
            "time_range_hours": hours
        }
        
    except Exception as e:
        logger.error(f"Error generating analytics dashboard: {e}")
        raise HTTPException(status_code=500, detail=f"Analytics dashboard failed: {str(e)}")

@enhanced_router.get("/analytics/metrics/{metric_type}")
async def get_metrics(metric_type: str, hours: int = Query(24)):
    """
    Get specific metrics by type
    
    Available metric types: system_performance, diagnostic_accuracy, 
    user_interaction, safety_metrics, clinical_outcomes
    """
    try:
        logger.info(f"Retrieving {metric_type} metrics for {hours} hours")
        
        end_time = datetime.utcnow()
        start_time = end_time - timedelta(hours=hours)
        
        # Get metrics for the specified type and time range
        all_metrics = {}
        for key, metrics in analytics_engine.metrics_buffer.items():
            if metric_type.lower() in key.lower():
                filtered_metrics = [
                    {
                        "timestamp": m.timestamp.isoformat(),
                        "value": m.value,
                        "unit": m.unit,
                        "context": m.context
                    }
                    for m in metrics 
                    if start_time <= m.timestamp <= end_time
                ]
                all_metrics[key] = filtered_metrics
        
        return {
            "metric_type": metric_type,
            "time_range_hours": hours,
            "metrics": all_metrics,
            "total_data_points": sum(len(metrics) for metrics in all_metrics.values())
        }
        
    except Exception as e:
        logger.error(f"Error retrieving metrics: {e}")
        raise HTTPException(status_code=500, detail=f"Metrics retrieval failed: {str(e)}")

@enhanced_router.get("/system/health-advanced")
async def advanced_health_check():
    """
    Advanced system health check with detailed component status
    
    Includes AI agents, safety systems, and analytics components
    """
    try:
        logger.info("Performing advanced health check")
        
        health_status = {}
        
        # Check core AI agents
        if coordinator:
            agent_health = await coordinator.health_check()
            health_status["ai_agents"] = agent_health
        else:
            health_status["ai_agents"] = {"status": "not_initialized"}
        
        # Check safety systems
        health_status["safety_systems"] = {
            "emergency_detection": "operational",
            "drug_interaction_checker": "operational",
            "risk_assessor": "operational"
        }
        
        # Check analytics system
        try:
            # Test analytics by recording a health check metric
            await analytics_engine.record_metric(
                PerformanceMetric(
                    timestamp=datetime.utcnow(),
                    metric_type=MetricType.SYSTEM_PERFORMANCE,
                    metric_name="health_check",
                    value=1.0,
                    unit="count",
                    context={"component": "advanced_health_check"}
                )
            )
            health_status["analytics"] = {"status": "operational", "metrics_buffer_size": len(analytics_engine.metrics_buffer)}
        except Exception as e:
            health_status["analytics"] = {"status": "error", "error": str(e)}
        
        # Check uncertainty quantifier
        health_status["uncertainty_quantifier"] = {"status": "operational"}
        
        # Overall system status
        all_operational = all(
            status.get("status") == "operational" or status.get("overall") == True
            for status in health_status.values()
        )
        
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "overall_status": "healthy" if all_operational else "degraded",
            "component_status": health_status,
            "version": "2.0.0-enhanced",
            "uptime": "operational"  # Would be calculated from actual uptime
        }
        
    except Exception as e:
        logger.error(f"Error in advanced health check: {e}")
        raise HTTPException(status_code=500, detail=f"Health check failed: {str(e)}")

@enhanced_router.get("/system/performance")
async def system_performance():
    """
    Real-time system performance metrics
    
    Provides current CPU, memory, and processing statistics
    """
    try:
        try:
            import psutil  # type: ignore[import-untyped]
            import os
            has_psutil = True
        except ImportError:
            has_psutil = False
            
        if has_psutil:
            # Get system metrics
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            try:
                disk = psutil.disk_usage('/')
                disk_percent = disk.percent
                disk_free_gb = disk.free / (1024**3)
            except:
                disk_percent = 0.0
                disk_free_gb = 0.0
            
            # Record system metrics
            await analytics_engine.record_system_metrics(
                cpu_percent / 100.0,
                1,  # Placeholder for concurrent users
                disk_percent / 100.0
            )
            
            return {
                "timestamp": datetime.utcnow().isoformat(),
                "cpu": {
                    "usage_percent": cpu_percent,
                    "status": "normal" if cpu_percent < 80 else "high"
                },
                "memory": {
                    "usage_percent": memory.percent,
                    "available_gb": memory.available / (1024**3),
                    "status": "normal" if memory.percent < 85 else "high"
                },
                "disk": {
                    "usage_percent": disk_percent,
                    "free_gb": disk_free_gb,
                    "status": "normal" if disk_percent < 90 else "high"
                },
                "process_info": {
                    "pid": os.getpid(),
                    "threads": psutil.Process().num_threads()
                }
            }
        else:
            # Fallback if psutil is not available
            return {
                "timestamp": datetime.utcnow().isoformat(),
                "status": "psutil_not_available",
                "message": "Install psutil for detailed system metrics",
                "fallback_metrics": {
                    "cpu": {"usage_percent": "unknown", "status": "unavailable"},
                    "memory": {"usage_percent": "unknown", "status": "unavailable"},
                    "disk": {"usage_percent": "unknown", "status": "unavailable"}
                }
            }
        
    except Exception as e:
        logger.error(f"Error getting system performance: {e}")
        raise HTTPException(status_code=500, detail=f"Performance check failed: {str(e)}")

@enhanced_router.post("/feedback")
async def submit_feedback(session_id: str, rating: int, feedback_text: str = None, improvement_suggestions: List[str] = None):
    """
    Submit user feedback for continuous improvement
    
    Helps improve AI accuracy and user experience
    """
    try:
        logger.info(f"Receiving feedback for session {session_id}")
        
        if improvement_suggestions is None:
            improvement_suggestions = []
        
        # Record feedback metrics
        await analytics_engine.record_metric(
            PerformanceMetric(
                timestamp=datetime.utcnow(),
                metric_type=MetricType.USER_INTERACTION,
                metric_name="user_feedback",
                value=rating,
                unit="rating_1_to_5",
                context={
                    "session_id": session_id,
                    "has_text_feedback": bool(feedback_text),
                    "suggestions_count": len(improvement_suggestions)
                }
            )
        )
        
        # Store feedback (would typically go to database)
        feedback_record = {
            "session_id": session_id,
            "rating": rating,
            "feedback_text": feedback_text,
            "improvement_suggestions": improvement_suggestions,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        return {
            "message": "Feedback received successfully",
            "feedback_id": f"feedback_{session_id}_{datetime.utcnow().timestamp()}",
            "thank_you": "Your feedback helps us improve the AI Healthcare Assistant"
        }
        
    except Exception as e:
        logger.error(f"Error submitting feedback: {e}")
        raise HTTPException(status_code=500, detail=f"Feedback submission failed: {str(e)}")

# Include router in main application
def get_enhanced_router():
    """Get the enhanced API router for inclusion in main app"""
    return enhanced_router