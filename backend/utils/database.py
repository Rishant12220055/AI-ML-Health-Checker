"""
Database Manager

Handles all database operations including:
1. MongoDB connection management
2. Patient consultation logging
3. Medical data storage and retrieval
4. Analytics and reporting

This module is resilient: if MongoDB or the motor driver isn't available, it
degrades gracefully into a disabled/no-op mode so the app can still run the
demo backend without hard failures.
"""

import asyncio
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import logging
import os

# Optional motor/pymongo imports (graceful fallback if missing)
try:
    from motor.motor_asyncio import AsyncIOMotorClient  # type: ignore
    from pymongo.errors import ConnectionFailure, OperationFailure  # type: ignore
    MOTOR_AVAILABLE = True
except Exception:  # pragma: no cover - import-time environment dependent
    AsyncIOMotorClient = object  # type: ignore
    ConnectionFailure = Exception  # type: ignore
    OperationFailure = Exception  # type: ignore
    MOTOR_AVAILABLE = False
from models.schemas import SymptomInput, DiagnosisResponse, ConsultationLog

logger = logging.getLogger(__name__)

class DatabaseManager:
    """Manages MongoDB database operations for the healthcare assistant"""
    
    def __init__(self):
        self.client = None
        self.database = None
        self.collections = {}
        self.enabled = False

        # Database configuration
        self.connection_string = os.getenv(
            "MONGODB_CONNECTION_STRING",
            "mongodb://localhost:27017",
        )
        self.database_name = os.getenv(
            "MONGODB_DATABASE", "healthcare_assistant"
        )

        # Collection names
        self.collection_names = {
            "consultations": "consultations",
            "patients": "patients",
            "medical_data": "medical_data",
            "guidelines": "guidelines",
            "analytics": "analytics",
            "feedback": "feedback",
        }
    
    async def connect(self) -> bool:
        """Establish connection to MongoDB. Returns True if enabled/connected.

        Respects env var DISABLE_DB to skip connecting. If motor is missing or
        connection fails, stays in disabled mode instead of raising.
        """
        if os.getenv("DISABLE_DB", "").strip().lower() in {"1", "true", "yes"}:
            logger.warning("Database disabled via DISABLE_DB env var; running in no-op mode")
            self.enabled = False
            return False

        if not MOTOR_AVAILABLE:
            logger.warning("motor/pymongo not available; DatabaseManager running in no-op mode")
            self.enabled = False
            return False

        try:
            logger.info("Connecting to MongoDB...")

            self.client = AsyncIOMotorClient(
                self.connection_string,
                serverSelectionTimeoutMS=5000,
                maxPoolSize=50,
                minPoolSize=5,
            )

            # Test connection
            await self.client.admin.command("ping")

            # Get database
            self.database = self.client[self.database_name]

            # Initialize collections
            for collection_key, collection_name in self.collection_names.items():
                self.collections[collection_key] = self.database[collection_name]

            # Create indexes for better performance
            await self._create_indexes()

            self.enabled = True
            logger.info("Successfully connected to MongoDB")
            return True

        except ConnectionFailure as e:
            logger.error(f"Failed to connect to MongoDB: {e}")
            self.enabled = False
            return False
        except Exception as e:
            logger.error(f"Unexpected error connecting to MongoDB: {e}")
            self.enabled = False
            return False
    
    async def disconnect(self):
        """Close MongoDB connection"""
        if self.client:
            self.client.close()
            logger.info("Disconnected from MongoDB")
    
    async def _create_indexes(self):
        """Create database indexes for optimal performance"""
        if not self.enabled:
            return
        try:
            # Consultations collection indexes
            consultations = self.collections["consultations"]
            await consultations.create_index("session_id", unique=True)
            await consultations.create_index("timestamp")
            await consultations.create_index("patient_info.age")
            await consultations.create_index("urgency_level")
            
            # Patients collection indexes
            patients = self.collections["patients"]
            await patients.create_index("patient_id", unique=True)
            await patients.create_index("last_consultation")
            
            # Medical data collection indexes
            medical_data = self.collections["medical_data"]
            await medical_data.create_index("condition_name")
            await medical_data.create_index("icd_code")
            
            # Analytics collection indexes
            analytics = self.collections["analytics"]
            await analytics.create_index("date")
            await analytics.create_index("metric_type")
            
            logger.debug("Database indexes created successfully")
            
        except OperationFailure as e:
            logger.warning(f"Some indexes may already exist: {e}")
        except Exception as e:
            logger.error(f"Error creating indexes: {e}")
    
    async def log_consultation(self, symptom_input: SymptomInput, 
                             diagnosis_response: DiagnosisResponse) -> bool:
        """Log a consultation to the database"""
        if not self.enabled:
            logger.debug("DB disabled; skipping log_consultation (no-op)")
            return True
        try:
            consultation_log = ConsultationLog(
                session_id=diagnosis_response.session_id,
                symptoms_input=symptom_input,
                diagnosis_response=diagnosis_response
            )
            
            # Insert into consultations collection
            result = await self.collections["consultations"].insert_one(
                consultation_log.model_dump()
            )
            
            # Update analytics
            # diagnosis_response.timestamp may be str; coerce to datetime
            ts = diagnosis_response.timestamp
            dt: datetime
            if isinstance(ts, datetime):
                dt = ts
            else:
                try:
                    # Handle ISO format (may not include timezone)
                    dt = datetime.fromisoformat(str(ts))
                except Exception:
                    dt = datetime.utcnow()
            await self._update_analytics("consultation_logged", dt)
            
            logger.debug(f"Consultation logged with ID: {result.inserted_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error logging consultation: {e}")
            return False
    
    async def get_consultation(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve a consultation by session ID"""
        if not self.enabled:
            logger.debug("DB disabled; get_consultation returns None")
            return None
        try:
            consultation = await self.collections["consultations"].find_one(
                {"session_id": session_id}
            )
            return consultation
            
        except Exception as e:
            logger.error(f"Error retrieving consultation: {e}")
            return None
    
    async def get_patient_history(self, patient_criteria: Dict[str, Any], 
                                limit: int = 10) -> List[Dict[str, Any]]:
        """Get patient consultation history based on criteria"""
        if not self.enabled:
            logger.debug("DB disabled; get_patient_history returns []")
            return []
        try:
            cursor = self.collections["consultations"].find(
                patient_criteria
            ).sort("timestamp", -1).limit(limit)
            
            consultations = await cursor.to_list(length=limit)
            return consultations
            
        except Exception as e:
            logger.error(f"Error retrieving patient history: {e}")
            return []
    
    async def store_medical_data(self, condition_name: str, medical_data: Dict[str, Any]) -> bool:
        """Store or update medical condition data"""
        if not self.enabled:
            logger.debug("DB disabled; skipping store_medical_data (no-op)")
            return True
        try:
            # Upsert medical data
            result = await self.collections["medical_data"].update_one(
                {"condition_name": condition_name},
                {"$set": {
                    **medical_data,
                    "last_updated": datetime.utcnow()
                }},
                upsert=True
            )
            
            logger.debug(f"Medical data updated for condition: {condition_name}")
            return True
            
        except Exception as e:
            logger.error(f"Error storing medical data: {e}")
            return False
    
    async def get_medical_data(self, condition_name: str) -> Optional[Dict[str, Any]]:
        """Retrieve medical data for a condition"""
        if not self.enabled:
            logger.debug("DB disabled; get_medical_data returns None")
            return None
        try:
            medical_data = await self.collections["medical_data"].find_one(
                {"condition_name": condition_name}
            )
            return medical_data
            
        except Exception as e:
            logger.error(f"Error retrieving medical data: {e}")
            return None
    
    async def store_guidelines(self, guideline_type: str, guidelines: Dict[str, Any]) -> bool:
        """Store medical guidelines (WHO, CDC, etc.)"""
        if not self.enabled:
            logger.debug("DB disabled; skipping store_guidelines (no-op)")
            return True
        try:
            result = await self.collections["guidelines"].update_one(
                {"guideline_type": guideline_type},
                {"$set": {
                    **guidelines,
                    "last_updated": datetime.utcnow()
                }},
                upsert=True
            )
            
            logger.debug(f"Guidelines updated for type: {guideline_type}")
            return True
            
        except Exception as e:
            logger.error(f"Error storing guidelines: {e}")
            return False
    
    async def get_guidelines(self, guideline_type: str) -> Optional[Dict[str, Any]]:
        """Retrieve medical guidelines by type"""
        if not self.enabled:
            logger.debug("DB disabled; get_guidelines returns None")
            return None
        try:
            guidelines = await self.collections["guidelines"].find_one(
                {"guideline_type": guideline_type}
            )
            return guidelines
            
        except Exception as e:
            logger.error(f"Error retrieving guidelines: {e}")
            return None
    
    async def log_user_feedback(self, session_id: str, feedback: Dict[str, Any]) -> bool:
        """Log user feedback for a consultation"""
        if not self.enabled:
            logger.debug("DB disabled; skipping log_user_feedback (no-op)")
            return True
        try:
            feedback_doc = {
                "session_id": session_id,
                "feedback": feedback,
                "timestamp": datetime.utcnow()
            }
            
            result = await self.collections["feedback"].insert_one(feedback_doc)
            
            # Update analytics
            await self._update_analytics("feedback_received", datetime.utcnow())
            
            logger.debug(f"Feedback logged for session: {session_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error logging feedback: {e}")
            return False
    
    async def get_analytics_summary(self, days: int = 30) -> Dict[str, Any]:
        """Get analytics summary for the specified number of days"""
        if not self.enabled:
            logger.debug("DB disabled; get_analytics_summary returns {}")
            return {}
        try:
            start_date = datetime.utcnow() - timedelta(days=days)
            
            # Get consultation counts
            consultation_count = await self.collections["consultations"].count_documents(
                {"timestamp": {"$gte": start_date}}
            )
            
            # Get urgency level distribution
            urgency_pipeline = [
                {"$match": {"timestamp": {"$gte": start_date}}},
                {"$group": {
                    "_id": "$urgency_level",
                    "count": {"$sum": 1}
                }}
            ]
            urgency_distribution = await self.collections["consultations"].aggregate(
                urgency_pipeline
            ).to_list(length=None)
            
            # Get top conditions
            conditions_pipeline = [
                {"$match": {"timestamp": {"$gte": start_date}}},
                {"$unwind": "$possible_conditions"},
                {"$group": {
                    "_id": "$possible_conditions.name",
                    "count": {"$sum": 1}
                }},
                {"$sort": {"count": -1}},
                {"$limit": 10}
            ]
            top_conditions = await self.collections["consultations"].aggregate(
                conditions_pipeline
            ).to_list(length=None)
            
            # Get feedback summary
            feedback_count = await self.collections["feedback"].count_documents(
                {"timestamp": {"$gte": start_date}}
            )
            
            return {
                "period_days": days,
                "total_consultations": consultation_count,
                "urgency_distribution": {item["_id"]: item["count"] for item in urgency_distribution},
                "top_conditions": top_conditions,
                "total_feedback": feedback_count,
                "generated_at": datetime.utcnow()
            }
            
        except Exception as e:
            logger.error(f"Error generating analytics summary: {e}")
            return {}
    
    async def _update_analytics(self, metric_type: str, timestamp: datetime):
        """Update analytics metrics"""
        if not self.enabled:
            return
        try:
            date_key = timestamp.strftime("%Y-%m-%d")
            
            await self.collections["analytics"].update_one(
                {"date": date_key, "metric_type": metric_type},
                {"$inc": {"count": 1}},
                upsert=True
            )
            
        except Exception as e:
            logger.warning(f"Error updating analytics: {e}")
    
    async def health_check(self) -> bool:
        """Check database connection health"""
        try:
            if not self.client or not self.enabled:
                return False
            
            # Ping the database
            await self.client.admin.command('ping')
            return True
            
        except Exception as e:
            logger.error(f"Database health check failed: {e}")
            return False
    
    async def cleanup_old_data(self, days_to_keep: int = 90):
        """Clean up old consultation data (for GDPR compliance)"""
        if not self.enabled:
            logger.debug("DB disabled; cleanup_old_data returns 0")
            return 0
        try:
            cutoff_date = datetime.utcnow() - timedelta(days=days_to_keep)
            
            # Remove old consultations
            result = await self.collections["consultations"].delete_many(
                {"timestamp": {"$lt": cutoff_date}}
            )
            
            # Remove old analytics
            analytics_cutoff = cutoff_date.strftime("%Y-%m-%d")
            await self.collections["analytics"].delete_many(
                {"date": {"$lt": analytics_cutoff}}
            )
            
            logger.info(f"Cleaned up {result.deleted_count} old consultation records")
            return result.deleted_count
            
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")
            return 0
    
    async def export_consultation_data(self, start_date: datetime, 
                                     end_date: datetime) -> List[Dict[str, Any]]:
        """Export consultation data for analysis (anonymized)"""
        if not self.enabled:
            logger.debug("DB disabled; export_consultation_data returns []")
            return []
        try:
            pipeline = [
                {"$match": {
                    "timestamp": {"$gte": start_date, "$lte": end_date}
                }},
                {"$project": {
                    "_id": 0,
                    "session_id": 1,
                    "timestamp": 1,
                    "urgency_level": 1,
                    "symptom_count": {"$size": "$symptoms_input.symptoms"},
                    "patient_age": "$symptoms_input.patient_info.age",
                    "patient_gender": "$symptoms_input.patient_info.gender",
                    "top_condition": {"$arrayElemAt": ["$possible_conditions", 0]},
                    "treatment_count": {"$size": "$recommended_treatments"}
                }}
            ]
            
            consultations = await self.collections["consultations"].aggregate(
                pipeline
            ).to_list(length=None)
            
            return consultations
            
        except Exception as e:
            logger.error(f"Error exporting consultation data: {e}")
            return []
