"""
Analytics and Monitoring Dashboard System

This module provides comprehensive analytics, trend tracking, system monitoring,
and performance metrics for the AI Healthcare Assistant.
"""

from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from enum import Enum
import logging
import json
import statistics
from dataclasses import dataclass, asdict
from collections import defaultdict, deque
import asyncio

logger = logging.getLogger(__name__)

class MetricType(str, Enum):
    """Types of metrics tracked"""
    SYSTEM_PERFORMANCE = "system_performance"
    DIAGNOSTIC_ACCURACY = "diagnostic_accuracy"
    USER_INTERACTION = "user_interaction"
    SAFETY_METRICS = "safety_metrics"
    CLINICAL_OUTCOMES = "clinical_outcomes"
    ERROR_TRACKING = "error_tracking"
    RESOURCE_UTILIZATION = "resource_utilization"

class AlertLevel(str, Enum):
    """Alert severity levels"""
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"
    EMERGENCY = "emergency"

@dataclass
class PerformanceMetric:
    """Performance metric data structure"""
    timestamp: datetime
    metric_type: MetricType
    metric_name: str
    value: float
    unit: str
    context: Dict[str, Any]
    tags: List[str] = None

@dataclass
class SystemAlert:
    """System alert data structure"""
    timestamp: datetime
    alert_id: str
    level: AlertLevel
    title: str
    description: str
    metric_type: MetricType
    threshold_value: Optional[float] = None
    current_value: Optional[float] = None
    resolution_status: str = "open"
    acknowledged_by: Optional[str] = None

class AnalyticsEngine:
    """Advanced analytics and monitoring system"""
    
    def __init__(self, retention_days: int = 90):
        self.retention_days = retention_days
        self.metrics_buffer = defaultdict(lambda: deque(maxlen=10000))
        self.alerts_buffer = deque(maxlen=1000)
        self.performance_baselines = {}
        self.alert_thresholds = self._initialize_alert_thresholds()
        self.diagnostic_patterns = {}
        self.trend_analyzers = {}
        self._initialize_trend_analyzers()
        
    def _initialize_alert_thresholds(self) -> Dict[str, Dict[str, Any]]:
        """Initialize alert thresholds for various metrics"""
        return {
            "response_time": {
                "warning": 2.0,    # seconds
                "critical": 5.0,
                "emergency": 10.0
            },
            "error_rate": {
                "warning": 0.05,   # 5%
                "critical": 0.10,  # 10%
                "emergency": 0.20  # 20%
            },
            "diagnostic_confidence": {
                "warning": 0.60,   # Below 60% confidence
                "critical": 0.40,  # Below 40% confidence
                "emergency": 0.20  # Below 20% confidence
            },
            "emergency_detection_accuracy": {
                "warning": 0.90,   # Below 90% accuracy
                "critical": 0.85,  # Below 85% accuracy
                "emergency": 0.80  # Below 80% accuracy
            },
            "system_cpu_usage": {
                "warning": 0.70,   # 70% CPU
                "critical": 0.85,  # 85% CPU
                "emergency": 0.95  # 95% CPU
            },
            "memory_usage": {
                "warning": 0.80,   # 80% memory
                "critical": 0.90,  # 90% memory
                "emergency": 0.95  # 95% memory
            },
            "concurrent_users": {
                "warning": 100,
                "critical": 200,
                "emergency": 300
            }
        }
    
    def _initialize_trend_analyzers(self):
        """Initialize trend analysis modules"""
        self.trend_analyzers = {
            "diagnostic_accuracy": TrendAnalyzer("diagnostic_accuracy", window_size=100),
            "response_times": TrendAnalyzer("response_times", window_size=500),
            "error_patterns": TrendAnalyzer("error_patterns", window_size=200),
            "user_satisfaction": TrendAnalyzer("user_satisfaction", window_size=50),
            "system_performance": TrendAnalyzer("system_performance", window_size=1000)
        }
    
    async def record_metric(self, metric: PerformanceMetric):
        """Record a performance metric"""
        try:
            # Store metric
            metric_key = f"{metric.metric_type}_{metric.metric_name}"
            self.metrics_buffer[metric_key].append(metric)
            
            # Update trend analyzer
            if metric.metric_name in self.trend_analyzers:
                self.trend_analyzers[metric.metric_name].add_data_point(metric.value)
            
            # Check for alerts
            await self._check_alert_conditions(metric)
            
            # Update baselines periodically
            await self._update_performance_baselines(metric_key)
            
        except Exception as e:
            logger.error(f"Error recording metric: {e}")
    
    async def record_diagnosis_result(self, patient_id: str, symptoms: List[str], 
                                    predicted_conditions: List[Dict[str, Any]], 
                                    response_time: float, confidence_scores: List[float]):
        """Record diagnosis session results for analytics"""
        try:
            timestamp = datetime.utcnow()
            
            # Record response time
            await self.record_metric(PerformanceMetric(
                timestamp=timestamp,
                metric_type=MetricType.SYSTEM_PERFORMANCE,
                metric_name="response_time",
                value=response_time,
                unit="seconds",
                context={"patient_id": patient_id, "symptom_count": len(symptoms)}
            ))
            
            # Record diagnostic confidence
            avg_confidence = statistics.mean(confidence_scores) if confidence_scores else 0.0
            await self.record_metric(PerformanceMetric(
                timestamp=timestamp,
                metric_type=MetricType.DIAGNOSTIC_ACCURACY,
                metric_name="diagnostic_confidence",
                value=avg_confidence,
                unit="probability",
                context={"patient_id": patient_id, "conditions_found": len(predicted_conditions)}
            ))
            
            # Record symptom complexity
            await self.record_metric(PerformanceMetric(
                timestamp=timestamp,
                metric_type=MetricType.USER_INTERACTION,
                metric_name="symptom_complexity",
                value=len(symptoms),
                unit="count",
                context={"patient_id": patient_id, "symptoms": symptoms}
            ))
            
            # Update diagnostic patterns
            await self._update_diagnostic_patterns(symptoms, predicted_conditions)
            
        except Exception as e:
            logger.error(f"Error recording diagnosis result: {e}")
    
    async def record_emergency_detection(self, patient_id: str, emergency_detected: bool, 
                                       emergency_confidence: float, response_time: float):
        """Record emergency detection metrics"""
        try:
            timestamp = datetime.utcnow()
            
            # Record emergency detection accuracy
            await self.record_metric(PerformanceMetric(
                timestamp=timestamp,
                metric_type=MetricType.SAFETY_METRICS,
                metric_name="emergency_detection_accuracy",
                value=emergency_confidence if emergency_detected else 1.0 - emergency_confidence,
                unit="probability",
                context={"patient_id": patient_id, "emergency_detected": emergency_detected}
            ))
            
            # Record emergency response time
            await self.record_metric(PerformanceMetric(
                timestamp=timestamp,
                metric_type=MetricType.SAFETY_METRICS,
                metric_name="emergency_response_time",
                value=response_time,
                unit="seconds",
                context={"patient_id": patient_id, "emergency_detected": emergency_detected}
            ))
            
        except Exception as e:
            logger.error(f"Error recording emergency detection: {e}")
    
    async def record_system_metrics(self, cpu_usage: float, memory_usage: float, 
                                  concurrent_users: int, disk_usage: float):
        """Record system resource metrics"""
        try:
            timestamp = datetime.utcnow()
            
            metrics = [
                ("system_cpu_usage", cpu_usage, "percentage"),
                ("memory_usage", memory_usage, "percentage"),
                ("concurrent_users", concurrent_users, "count"),
                ("disk_usage", disk_usage, "percentage")
            ]
            
            for metric_name, value, unit in metrics:
                await self.record_metric(PerformanceMetric(
                    timestamp=timestamp,
                    metric_type=MetricType.RESOURCE_UTILIZATION,
                    metric_name=metric_name,
                    value=value,
                    unit=unit,
                    context={"server_instance": "main"}
                ))
            
        except Exception as e:
            logger.error(f"Error recording system metrics: {e}")
    
    async def record_error(self, error_type: str, error_message: str, 
                         context: Dict[str, Any], severity: str = "error"):
        """Record system errors for tracking"""
        try:
            timestamp = datetime.utcnow()
            
            await self.record_metric(PerformanceMetric(
                timestamp=timestamp,
                metric_type=MetricType.ERROR_TRACKING,
                metric_name=f"error_{error_type}",
                value=1.0,
                unit="count",
                context={
                    "error_message": error_message,
                    "severity": severity,
                    **context
                }
            ))
            
            # Calculate error rate
            await self._calculate_error_rate()
            
        except Exception as e:
            logger.error(f"Error recording error: {e}")
    
    async def generate_dashboard_data(self, time_range: timedelta = timedelta(hours=24)) -> Dict[str, Any]:
        """Generate comprehensive dashboard data"""
        try:
            end_time = datetime.utcnow()
            start_time = end_time - time_range
            
            # System performance overview
            system_overview = await self._generate_system_overview(start_time, end_time)
            
            # Diagnostic analytics
            diagnostic_analytics = await self._generate_diagnostic_analytics(start_time, end_time)
            
            # Safety metrics
            safety_metrics = await self._generate_safety_metrics(start_time, end_time)
            
            # Trend analysis
            trend_analysis = await self._generate_trend_analysis()
            
            # Active alerts
            active_alerts = await self._get_active_alerts()
            
            # Performance summary
            performance_summary = await self._generate_performance_summary(start_time, end_time)
            
            # Usage statistics
            usage_statistics = await self._generate_usage_statistics(start_time, end_time)
            
            return {
                "generated_at": end_time.isoformat(),
                "time_range": {
                    "start": start_time.isoformat(),
                    "end": end_time.isoformat(),
                    "duration_hours": time_range.total_seconds() / 3600
                },
                "system_overview": system_overview,
                "diagnostic_analytics": diagnostic_analytics,
                "safety_metrics": safety_metrics,
                "trend_analysis": trend_analysis,
                "active_alerts": active_alerts,
                "performance_summary": performance_summary,
                "usage_statistics": usage_statistics,
                "health_score": await self._calculate_system_health_score()
            }
            
        except Exception as e:
            logger.error(f"Error generating dashboard data: {e}")
            return {"error": "Failed to generate dashboard data"}
    
    async def _check_alert_conditions(self, metric: PerformanceMetric):
        """Check if metric values trigger alerts"""
        try:
            metric_thresholds = self.alert_thresholds.get(metric.metric_name)
            if not metric_thresholds:
                return
            
            current_value = metric.value
            
            # Check thresholds in order of severity
            alert_level = None
            threshold_value = None
            
            if current_value >= metric_thresholds.get("emergency", float('inf')):
                alert_level = AlertLevel.EMERGENCY
                threshold_value = metric_thresholds["emergency"]
            elif current_value >= metric_thresholds.get("critical", float('inf')):
                alert_level = AlertLevel.CRITICAL
                threshold_value = metric_thresholds["critical"]
            elif current_value >= metric_thresholds.get("warning", float('inf')):
                alert_level = AlertLevel.WARNING
                threshold_value = metric_thresholds["warning"]
            
            # For metrics where lower is worse (like confidence)
            if metric.metric_name in ["diagnostic_confidence", "emergency_detection_accuracy"]:
                if current_value <= metric_thresholds.get("emergency", 0):
                    alert_level = AlertLevel.EMERGENCY
                    threshold_value = metric_thresholds["emergency"]
                elif current_value <= metric_thresholds.get("critical", 0):
                    alert_level = AlertLevel.CRITICAL
                    threshold_value = metric_thresholds["critical"]
                elif current_value <= metric_thresholds.get("warning", 0):
                    alert_level = AlertLevel.WARNING
                    threshold_value = metric_thresholds["warning"]
            
            if alert_level:
                await self._create_alert(metric, alert_level, threshold_value, current_value)
                
        except Exception as e:
            logger.error(f"Error checking alert conditions: {e}")
    
    async def _create_alert(self, metric: PerformanceMetric, level: AlertLevel, 
                          threshold: float, current_value: float):
        """Create a system alert"""
        try:
            alert = SystemAlert(
                timestamp=metric.timestamp,
                alert_id=f"alert_{hash(f'{metric.metric_name}_{metric.timestamp}')}",
                level=level,
                title=f"{metric.metric_name.replace('_', ' ').title()} {level.value.title()}",
                description=f"{metric.metric_name} value {current_value} exceeded {level.value} threshold {threshold}",
                metric_type=metric.metric_type,
                threshold_value=threshold,
                current_value=current_value
            )
            
            self.alerts_buffer.append(alert)
            
            # Log alert
            logger.warning(f"Alert created: {alert.title} - {alert.description}")
            
        except Exception as e:
            logger.error(f"Error creating alert: {e}")
    
    async def _generate_system_overview(self, start_time: datetime, end_time: datetime) -> Dict[str, Any]:
        """Generate system performance overview"""
        try:
            # Get recent metrics
            response_times = self._get_metrics_in_range("system_performance_response_time", start_time, end_time)
            error_metrics = self._get_metrics_in_range("error_tracking", start_time, end_time)
            
            # Calculate averages
            avg_response_time = statistics.mean([m.value for m in response_times]) if response_times else 0
            total_errors = len(error_metrics)
            total_requests = len(response_times)
            error_rate = (total_errors / total_requests) if total_requests > 0 else 0
            
            return {
                "avg_response_time": round(avg_response_time, 3),
                "total_requests": total_requests,
                "total_errors": total_errors,
                "error_rate": round(error_rate, 4),
                "uptime_percentage": 99.9,  # Placeholder - would be calculated from actual uptime data
                "system_status": "healthy" if error_rate < 0.05 and avg_response_time < 2.0 else "degraded"
            }
            
        except Exception as e:
            logger.error(f"Error generating system overview: {e}")
            return {}
    
    async def _generate_diagnostic_analytics(self, start_time: datetime, end_time: datetime) -> Dict[str, Any]:
        """Generate diagnostic performance analytics"""
        try:
            confidence_metrics = self._get_metrics_in_range("diagnostic_accuracy_diagnostic_confidence", start_time, end_time)
            
            if not confidence_metrics:
                return {"message": "No diagnostic data available"}
            
            confidence_values = [m.value for m in confidence_metrics]
            
            return {
                "total_diagnoses": len(confidence_metrics),
                "avg_confidence": round(statistics.mean(confidence_values), 3),
                "min_confidence": round(min(confidence_values), 3),
                "max_confidence": round(max(confidence_values), 3),
                "confidence_std_dev": round(statistics.stdev(confidence_values) if len(confidence_values) > 1 else 0, 3),
                "high_confidence_percentage": round(len([c for c in confidence_values if c > 0.8]) / len(confidence_values) * 100, 1),
                "low_confidence_percentage": round(len([c for c in confidence_values if c < 0.6]) / len(confidence_values) * 100, 1)
            }
            
        except Exception as e:
            logger.error(f"Error generating diagnostic analytics: {e}")
            return {}
    
    async def _generate_safety_metrics(self, start_time: datetime, end_time: datetime) -> Dict[str, Any]:
        """Generate safety-related metrics"""
        try:
            emergency_metrics = self._get_metrics_in_range("safety_metrics_emergency_detection_accuracy", start_time, end_time)
            emergency_response_metrics = self._get_metrics_in_range("safety_metrics_emergency_response_time", start_time, end_time)
            
            if not emergency_metrics:
                return {"message": "No emergency detection data available"}
            
            accuracy_values = [m.value for m in emergency_metrics]
            response_times = [m.value for m in emergency_response_metrics] if emergency_response_metrics else []
            
            return {
                "emergency_detections": len(emergency_metrics),
                "avg_detection_accuracy": round(statistics.mean(accuracy_values), 3),
                "avg_emergency_response_time": round(statistics.mean(response_times), 3) if response_times else 0,
                "detection_accuracy_threshold_met": len([a for a in accuracy_values if a > 0.9]) / len(accuracy_values) * 100 if accuracy_values else 0,
                "fast_response_percentage": len([t for t in response_times if t < 1.0]) / len(response_times) * 100 if response_times else 0
            }
            
        except Exception as e:
            logger.error(f"Error generating safety metrics: {e}")
            return {}
    
    async def _generate_trend_analysis(self) -> Dict[str, Any]:
        """Generate trend analysis for key metrics"""
        try:
            trends = {}
            
            for analyzer_name, analyzer in self.trend_analyzers.items():
                trend_data = analyzer.get_trend_analysis()
                trends[analyzer_name] = trend_data
            
            return trends
            
        except Exception as e:
            logger.error(f"Error generating trend analysis: {e}")
            return {}
    
    async def _get_active_alerts(self) -> List[Dict[str, Any]]:
        """Get currently active alerts"""
        try:
            # Get alerts from last 24 hours that are still open
            cutoff_time = datetime.utcnow() - timedelta(hours=24)
            active_alerts = [
                asdict(alert) for alert in self.alerts_buffer 
                if alert.timestamp > cutoff_time and alert.resolution_status == "open"
            ]
            
            # Sort by severity and timestamp
            severity_order = {AlertLevel.EMERGENCY: 0, AlertLevel.CRITICAL: 1, AlertLevel.WARNING: 2, AlertLevel.INFO: 3}
            active_alerts.sort(key=lambda x: (severity_order.get(AlertLevel(x["level"]), 4), x["timestamp"]))
            
            return active_alerts
            
        except Exception as e:
            logger.error(f"Error getting active alerts: {e}")
            return []
    
    async def _generate_performance_summary(self, start_time: datetime, end_time: datetime) -> Dict[str, Any]:
        """Generate performance summary"""
        try:
            # Get resource utilization metrics
            cpu_metrics = self._get_metrics_in_range("resource_utilization_system_cpu_usage", start_time, end_time)
            memory_metrics = self._get_metrics_in_range("resource_utilization_memory_usage", start_time, end_time)
            
            cpu_values = [m.value for m in cpu_metrics] if cpu_metrics else [0]
            memory_values = [m.value for m in memory_metrics] if memory_metrics else [0]
            
            return {
                "avg_cpu_usage": round(statistics.mean(cpu_values), 2),
                "max_cpu_usage": round(max(cpu_values), 2),
                "avg_memory_usage": round(statistics.mean(memory_values), 2),
                "max_memory_usage": round(max(memory_values), 2),
                "resource_efficiency": "optimal" if max(cpu_values) < 0.7 and max(memory_values) < 0.8 else "suboptimal"
            }
            
        except Exception as e:
            logger.error(f"Error generating performance summary: {e}")
            return {}
    
    async def _generate_usage_statistics(self, start_time: datetime, end_time: datetime) -> Dict[str, Any]:
        """Generate usage statistics"""
        try:
            # Get user interaction metrics
            user_metrics = []
            for key, metrics in self.metrics_buffer.items():
                if "user_interaction" in key:
                    user_metrics.extend([m for m in metrics if start_time <= m.timestamp <= end_time])
            
            concurrent_user_metrics = self._get_metrics_in_range("resource_utilization_concurrent_users", start_time, end_time)
            
            return {
                "total_interactions": len(user_metrics),
                "peak_concurrent_users": max([m.value for m in concurrent_user_metrics]) if concurrent_user_metrics else 0,
                "avg_concurrent_users": round(statistics.mean([m.value for m in concurrent_user_metrics]), 1) if concurrent_user_metrics else 0,
                "interaction_patterns": await self._analyze_interaction_patterns(user_metrics)
            }
            
        except Exception as e:
            logger.error(f"Error generating usage statistics: {e}")
            return {}
    
    async def _calculate_system_health_score(self) -> Dict[str, Any]:
        """Calculate overall system health score"""
        try:
            # Get recent metrics for health calculation
            end_time = datetime.utcnow()
            start_time = end_time - timedelta(hours=1)
            
            # Performance score (40%)
            response_times = self._get_metrics_in_range("system_performance_response_time", start_time, end_time)
            avg_response_time = statistics.mean([m.value for m in response_times]) if response_times else 2.0
            performance_score = max(0, 1 - (avg_response_time / 5.0))  # Normalize to 0-1
            
            # Reliability score (30%)
            error_metrics = self._get_metrics_in_range("error_tracking", start_time, end_time)
            total_requests = len(response_times)
            error_rate = len(error_metrics) / total_requests if total_requests > 0 else 0
            reliability_score = max(0, 1 - (error_rate / 0.1))  # Normalize to 0-1
            
            # Safety score (20%)
            emergency_metrics = self._get_metrics_in_range("safety_metrics_emergency_detection_accuracy", start_time, end_time)
            avg_safety = statistics.mean([m.value for m in emergency_metrics]) if emergency_metrics else 0.9
            safety_score = avg_safety
            
            # Resource efficiency score (10%)
            cpu_metrics = self._get_metrics_in_range("resource_utilization_system_cpu_usage", start_time, end_time)
            avg_cpu = statistics.mean([m.value for m in cpu_metrics]) if cpu_metrics else 0.5
            efficiency_score = max(0, 1 - avg_cpu)
            
            # Calculate weighted health score
            health_score = (
                performance_score * 0.4 +
                reliability_score * 0.3 +
                safety_score * 0.2 +
                efficiency_score * 0.1
            )
            
            # Determine health status
            if health_score >= 0.9:
                status = "excellent"
            elif health_score >= 0.7:
                status = "good"
            elif health_score >= 0.5:
                status = "fair"
            else:
                status = "poor"
            
            return {
                "overall_score": round(health_score, 3),
                "status": status,
                "component_scores": {
                    "performance": round(performance_score, 3),
                    "reliability": round(reliability_score, 3),
                    "safety": round(safety_score, 3),
                    "efficiency": round(efficiency_score, 3)
                }
            }
            
        except Exception as e:
            logger.error(f"Error calculating system health score: {e}")
            return {"overall_score": 0.5, "status": "unknown"}
    
    def _get_metrics_in_range(self, metric_key: str, start_time: datetime, end_time: datetime) -> List[PerformanceMetric]:
        """Get metrics within a specific time range"""
        try:
            metrics = self.metrics_buffer.get(metric_key, [])
            return [m for m in metrics if start_time <= m.timestamp <= end_time]
        except Exception as e:
            logger.error(f"Error getting metrics in range: {e}")
            return []
    
    async def _update_performance_baselines(self, metric_key: str):
        """Update performance baselines for metrics"""
        try:
            if len(self.metrics_buffer[metric_key]) >= 100:  # Need sufficient data
                values = [m.value for m in list(self.metrics_buffer[metric_key])[-100:]]
                self.performance_baselines[metric_key] = {
                    "mean": statistics.mean(values),
                    "median": statistics.median(values),
                    "std_dev": statistics.stdev(values) if len(values) > 1 else 0,
                    "p95": sorted(values)[int(len(values) * 0.95)] if len(values) > 20 else max(values),
                    "updated_at": datetime.utcnow()
                }
        except Exception as e:
            logger.error(f"Error updating baselines: {e}")
    
    async def _update_diagnostic_patterns(self, symptoms: List[str], predicted_conditions: List[Dict[str, Any]]):
        """Update diagnostic pattern analysis"""
        try:
            # Track symptom-condition correlations
            for condition in predicted_conditions:
                condition_name = condition.get("name", "unknown")
                if condition_name not in self.diagnostic_patterns:
                    self.diagnostic_patterns[condition_name] = {"symptoms": defaultdict(int), "count": 0}
                
                self.diagnostic_patterns[condition_name]["count"] += 1
                for symptom in symptoms:
                    self.diagnostic_patterns[condition_name]["symptoms"][symptom] += 1
                    
        except Exception as e:
            logger.error(f"Error updating diagnostic patterns: {e}")
    
    async def _calculate_error_rate(self):
        """Calculate current error rate"""
        try:
            end_time = datetime.utcnow()
            start_time = end_time - timedelta(hours=1)
            
            # Get error and request metrics
            error_metrics = []
            request_metrics = []
            
            for key, metrics in self.metrics_buffer.items():
                if "error_tracking" in key:
                    error_metrics.extend([m for m in metrics if start_time <= m.timestamp <= end_time])
                elif "response_time" in key:
                    request_metrics.extend([m for m in metrics if start_time <= m.timestamp <= end_time])
            
            total_requests = len(request_metrics)
            total_errors = len(error_metrics)
            
            error_rate = total_errors / total_requests if total_requests > 0 else 0
            
            # Record error rate metric
            await self.record_metric(PerformanceMetric(
                timestamp=end_time,
                metric_type=MetricType.SYSTEM_PERFORMANCE,
                metric_name="error_rate",
                value=error_rate,
                unit="percentage",
                context={"calculation_window": "1_hour"}
            ))
            
        except Exception as e:
            logger.error(f"Error calculating error rate: {e}")
    
    async def _analyze_interaction_patterns(self, user_metrics: List[PerformanceMetric]) -> Dict[str, Any]:
        """Analyze user interaction patterns"""
        try:
            if not user_metrics:
                return {}
            
            # Group by hour to find usage patterns
            hourly_usage = defaultdict(int)
            for metric in user_metrics:
                hour = metric.timestamp.hour
                hourly_usage[hour] += 1
            
            peak_hour = max(hourly_usage.items(), key=lambda x: x[1])[0] if hourly_usage else 0
            
            return {
                "peak_usage_hour": peak_hour,
                "usage_distribution": dict(hourly_usage),
                "total_unique_hours": len(hourly_usage)
            }
            
        except Exception as e:
            logger.error(f"Error analyzing interaction patterns: {e}")
            return {}

class TrendAnalyzer:
    """Trend analysis for time series data"""
    
    def __init__(self, metric_name: str, window_size: int = 100):
        self.metric_name = metric_name
        self.window_size = window_size
        self.data_points = deque(maxlen=window_size)
        self.timestamps = deque(maxlen=window_size)
    
    def add_data_point(self, value: float, timestamp: datetime = None):
        """Add a data point for trend analysis"""
        if timestamp is None:
            timestamp = datetime.utcnow()
        
        self.data_points.append(value)
        self.timestamps.append(timestamp)
    
    def get_trend_analysis(self) -> Dict[str, Any]:
        """Get comprehensive trend analysis"""
        try:
            if len(self.data_points) < 2:
                return {"trend": "insufficient_data"}
            
            values = list(self.data_points)
            
            # Calculate basic statistics
            mean_value = statistics.mean(values)
            median_value = statistics.median(values)
            std_dev = statistics.stdev(values) if len(values) > 1 else 0
            
            # Calculate trend direction
            if len(values) >= 10:
                recent_avg = statistics.mean(values[-10:])
                older_avg = statistics.mean(values[:10])
                trend_direction = "increasing" if recent_avg > older_avg else "decreasing" if recent_avg < older_avg else "stable"
                trend_strength = abs(recent_avg - older_avg) / older_avg if older_avg != 0 else 0
            else:
                trend_direction = "stable"
                trend_strength = 0
            
            # Detect anomalies (values > 2 standard deviations from mean)
            anomaly_threshold = mean_value + (2 * std_dev)
            anomalies = [i for i, v in enumerate(values) if abs(v - mean_value) > 2 * std_dev]
            
            return {
                "trend_direction": trend_direction,
                "trend_strength": round(trend_strength, 3),
                "current_value": values[-1],
                "mean_value": round(mean_value, 3),
                "median_value": round(median_value, 3),
                "std_deviation": round(std_dev, 3),
                "anomaly_count": len(anomalies),
                "data_points": len(values),
                "volatility": "high" if std_dev > mean_value * 0.3 else "moderate" if std_dev > mean_value * 0.1 else "low"
            }
            
        except Exception as e:
            logger.error(f"Error in trend analysis: {e}")
            return {"trend": "analysis_error"}

# Global analytics instance
analytics_engine = AnalyticsEngine()
