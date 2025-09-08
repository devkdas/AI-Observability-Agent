"""
Incident data models for the AI-Powered Observability Agent
"""

import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, ConfigDict, field_serializer


class IncidentSeverity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class IncidentStatus(str, Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    CLOSED = "closed"
    FAILED = "failed"


class AIAnalysis(BaseModel):
    root_cause: str
    confidence: float = Field(ge=0.0, le=1.0)
    suggested_actions: List[str]
    related_incidents: List[str] = []
    analysis_duration: float  # seconds
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    risk_level: str = "medium"
    impact_scope: str = "unknown"
    analysis_engine: str = "multi-engine-ai"
    analysis_time: float = 1.0  # seconds - alias for analysis_duration
    
    @field_serializer('created_at', when_used='json')
    def serialize_datetime(self, value):
        if value is not None:
            return value.isoformat()
        return value


class ActionTaken(BaseModel):
    action_type: str
    description: str
    status: str
    details: Optional[str] = None  # Additional details about the action
    result: Optional[Dict[str, Any]] = None
    executed_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    @field_serializer('executed_at', when_used='json')
    def serialize_datetime(self, value):
        if value is not None:
            return value.isoformat()
        return value


class Signal(BaseModel):
    source: str
    event_type: str
    description: str
    severity: float = Field(ge=0.0, le=1.0)
    is_anomaly: bool
    raw_data: Dict[str, Any]
    detected_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    @field_serializer('detected_at', when_used='json')
    def serialize_datetime(self, value):
        if value is not None:
            return value.isoformat()
        return value


class Incident(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    description: str
    severity: IncidentSeverity
    status: IncidentStatus = IncidentStatus.OPEN
    source: str
    raw_data: Dict[str, Any]
    detected_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    resolved_at: Optional[datetime] = None
    
    # AI Analysis results
    ai_analysis: Optional[AIAnalysis] = None
    root_cause: Optional[str] = None
    confidence_score: Optional[float] = None
    suggested_actions: List[str] = []
    
    # Advanced AI insights from multiple engines
    ml_insights: List[str] = []
    copado_insights: List[str] = []
    quantum_insights: List[str] = []
    
    # Actions taken
    actions_taken: List[ActionTaken] = []
    
    # Metadata
    tags: List[str] = []
    assignee: Optional[str] = None
    related_incidents: List[str] = []
    slack_message_ts: Optional[str] = None
    
    @field_serializer('detected_at', 'resolved_at', when_used='json')
    def serialize_datetime(self, value):
        if value is not None:
            return value.isoformat()
        return value
