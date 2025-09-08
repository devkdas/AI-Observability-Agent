"""
Signal Detection Service for AI-Powered Observability Agent
Monitors various sources for anomalies and issues
"""

import logging
from datetime import datetime
from typing import Dict, Any
from models.incident import Signal

logger = logging.getLogger(__name__)


class SignalDetector:
    """Watches for trouble signals from different systems - like a smoke detector for your code"""
    
    def __init__(self):
        self.anomaly_patterns = {
            "test_failure": ["failed", "error", "exception", "timeout"],
            "deployment_issue": ["deployment failed", "build failed", "rollback"],
            "performance_degradation": ["slow", "timeout", "high cpu", "memory leak"],
            "security_issue": ["unauthorized", "permission denied", "security violation"]
        }
    
    async def initialize(self):
        """Initialize the signal detector"""
        logger.info("Signal Detector initialized")
    
    async def analyze_git_event(self, payload) -> Signal:
        """Analyze Git events for potential issues"""
        event_data = payload.data
        event_type = payload.event_type
        
        # Look for risky patterns in commits that might indicate problems
        is_anomaly = False
        severity = 0.0
        description = f"Git {event_type} event"
        
        if event_type == "push":
            # Check commit messages and changes for warning signs
            commits = event_data.get("commits", [])
            for commit in commits:
                message = commit.get("message", "").lower()
                if any(pattern in message for pattern in ["fix", "hotfix", "urgent", "critical"]):
                    is_anomaly = True
                    severity = 0.6
                    description = f"Urgent commit detected: {commit.get('message')}"
                    break
        
        elif event_type == "pull_request":
            # Check PR for risk indicators
            pr_data = event_data.get("pull_request", {})
            title = pr_data.get("title", "").lower()
            if any(pattern in title for pattern in ["fix", "bug", "critical", "hotfix"]):
                is_anomaly = True
                severity = 0.5
                description = f"Bug fix PR detected: {pr_data.get('title')}"
        
        elif event_type == "hotfix_commit":
            # Hotfix commits are always anomalies requiring immediate attention
            is_anomaly = True
            severity = 0.8
            commit_message = event_data.get("commit_message", "")
            description = f"Critical hotfix commit: {commit_message}"
        
        return Signal(
            source="git",
            event_type=event_type,
            description=description,
            severity=severity,
            is_anomaly=is_anomaly,
            raw_data=event_data
        )
    
    async def analyze_copado_event(self, payload) -> Signal:
        """Analyze Copado CI/CD events"""
        event_data = payload.data
        event_type = payload.event_type
        
        # Copado events are typically already indicating issues
        is_anomaly = True
        severity = 0.8
        
        severity_map = {
            "deployment_failed": 0.9,
            "test_failed": 0.7,
            "build_failed": 0.8,
            "pipeline_failed": 0.8
        }
        
        severity = severity_map.get(event_type, 0.7)
        description = f"Copado {event_type.replace('_', ' ')}"
        
        # Extract additional context
        if "error_message" in event_data:
            description += f": {event_data['error_message']}"
        
        return Signal(
            source="copado",
            event_type=event_type,
            description=description,
            severity=severity,
            is_anomaly=is_anomaly,
            raw_data=event_data
        )
    
    async def analyze_salesforce_event(self, payload) -> Signal:
        """Analyze Salesforce audit trail events"""
        event_data = payload.data
        event_type = payload.event_type
        
        is_anomaly = False
        severity = 0.0
        description = f"Salesforce {event_type}"
        
        # Check for risky Salesforce operations
        risky_operations = [
            "delete_user",
            "change_permission_set", 
            "modify_profile",
            "delete_custom_object",
            "change_org_settings",
            "audit_alert",
            "permission_change"
        ]
        
        operation = event_data.get("operation", event_data.get("alert_type", ""))
        action = event_data.get("action", "")
        
        # Check for bulk delete operations - high severity
        if action == "DELETE" or "delete" in operation.lower():
            records_count = event_data.get("records_count", 0)
            if records_count > 100:  # Bulk operation
                is_anomaly = True
                severity = 0.8  # High severity for bulk deletes
            elif records_count > 10:
                is_anomaly = True
                severity = 0.7  # Medium-high severity
            else:
                is_anomaly = True
                severity = 0.6  # Standard delete operations
        elif any(risky_op in operation.lower() for risky_op in risky_operations) or event_type == "audit_alert":
            is_anomaly = True
            severity = 0.7
            # Create more detailed description
            user = event_data.get("username", "Unknown user")
            timestamp = event_data.get("timestamp", "")
            business_hours_check = ""
            if timestamp and ("02:" in timestamp or "03:" in timestamp or "01:" in timestamp):
                business_hours_check = " during business hours"
            
            description = f"Risky Salesforce operation: {operation} permissions by {user}{business_hours_check}"
        
        # Check for unusual activity patterns
        user_id = event_data.get("user_id")
        timestamp = event_data.get("timestamp")
        
        # Simple anomaly detection (in production, use more sophisticated ML models)
        # For demo purposes, always flag audit alerts as anomalies
        if event_type == "audit_alert" and not is_anomaly:
            is_anomaly = True
            severity = 0.6
            description += " (unusual activity pattern detected)"
        
        return Signal(
            source="salesforce",
            event_type=event_type,
            description=description,
            severity=severity,
            is_anomaly=is_anomaly,
            raw_data=event_data
        )
    
    def _is_unusual_activity(self, user_id: str, timestamp: str, operation: str) -> bool:
        """Simple heuristic for unusual activity detection"""
        # In production, this would use ML models and historical data
        # For demo, we'll use simple rules
        
        try:
            event_time = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            current_time = datetime.now(event_time.tzinfo)
            
            # Check if operation is happening outside business hours
            if event_time.hour < 6 or event_time.hour > 22:
                return True
                
            # Check for rapid successive operations (would need state tracking)
            # This is simplified for demo
            
        except Exception:
            pass
        
        return False
