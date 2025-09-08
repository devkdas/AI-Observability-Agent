import pytest
import asyncio
from unittest.mock import Mock, AsyncMock, patch
from fastapi.testclient import TestClient
import os
import sys

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from models.incident import Incident, AIAnalysis, Signal, ActionTaken
from services.ai_analyzer import AIAnalyzer
from services.signal_detector import SignalDetector
from services.ml_predictor import AdvancedMLPredictor
from services.github_monitor import GitHubMonitor
from services.quantum_analyzer import QuantumInspiredAnalyzer
from services.incident_manager import IncidentManager
from services.copado_intelligence import CopadoIntelligenceEngine
from services.action_executor import ActionExecutor

@pytest.fixture
def mock_env():
    """Mock environment variables for testing"""
    env_vars = {
        'COPADO_AI_API_KEY': 'test-copado-key',
        'COPADO_AI_API_URL': 'https://test-copado-api.com',
        'COPADO_WORKSPACE_ID': 'test-workspace-123',
        'GITHUB_TOKEN': 'test-github-token',
        'JIRA_BASE_URL': 'https://test.atlassian.net',
        'JIRA_EMAIL': 'test@example.com',
        'JIRA_API_TOKEN': 'test-jira-token',
        'SLACK_WEBHOOK_URL': 'https://hooks.slack.com/test',
        'TEAMS_WEBHOOK_URL': 'https://outlook.office.com/webhook/test',
        'SALESFORCE_INSTANCE_URL': 'https://test.salesforce.com',
        'SALESFORCE_ACCESS_TOKEN': 'test-sf-token',
        'DATABASE_URL': 'sqlite:///test.db'
    }
    
    with patch.dict(os.environ, env_vars, clear=False):
        yield env_vars

@pytest.fixture
def sample_incident():
    """Create a sample incident for testing"""
    return Incident(
        id="test-incident-123",
        source="git",
        event_type="push",
        severity="high",
        title="Critical deployment failure detected",
        description="Multiple failed commits with urgent fixes",
        raw_data={"commits": [{"message": "urgent hotfix for production"}]},
        status="open"
    )

@pytest.fixture
def sample_signal():
    """Create a sample signal for testing"""
    return Signal(
        source="git",
        event_type="push",
        severity=0.7,
        is_anomaly=True,
        description="Urgent commit pattern detected",
        confidence=0.85,
        raw_data={"commit_message": "hotfix: critical production issue"}
    )

@pytest.fixture
def sample_ai_analysis():
    """Create a sample AI analysis for testing"""
    return AIAnalysis(
        incident_id="test-incident-123",
        root_cause="Deployment pipeline misconfiguration",
        confidence=0.92,
        suggested_actions=["Create rollback plan", "Update pipeline config"],
        analysis_duration=2.5,
        severity_assessment="high",
        business_impact="High revenue risk",
        technical_details={
            "affected_services": ["payment-api", "user-service"],
            "error_patterns": ["timeout", "connection_refused"]
        }
    )

@pytest.fixture
def mock_aiohttp_session():
    """Mock aiohttp session for external API calls"""
    session = AsyncMock()
    
    # Mock successful API responses
    mock_response = AsyncMock()
    mock_response.status = 200
    mock_response.json = AsyncMock(return_value={
        "analysis": "System detected critical deployment issues",
        "confidence": 0.89,
        "recommendations": ["Rollback deployment", "Check configuration"]
    })
    mock_response.__aenter__ = AsyncMock(return_value=mock_response)
    mock_response.__aexit__ = AsyncMock(return_value=None)
    
    session.post.return_value = mock_response
    session.get.return_value = mock_response
    
    return session

@pytest.fixture
def ai_analyzer(mock_env, mock_aiohttp_session):
    """Create AIAnalyzer instance for testing"""
    with patch('aiohttp.ClientSession', return_value=mock_aiohttp_session):
        analyzer = AIAnalyzer()
        # Set up the session directly for synchronous tests
        analyzer.session = mock_aiohttp_session
        return analyzer

@pytest.fixture
def signal_detector(mock_env):
    """Create SignalDetector instance for testing"""
    return SignalDetector()

@pytest.fixture
def ml_predictor(mock_env):
    """Create AdvancedMLPredictor instance for testing"""
    return AdvancedMLPredictor()

@pytest.fixture
def github_monitor(mock_env):
    """Create GitHubMonitor instance for testing"""
    return GitHubMonitor()

@pytest.fixture
def quantum_analyzer(mock_env):
    """Create QuantumInspiredAnalyzer instance for testing"""
    return QuantumInspiredAnalyzer()

@pytest.fixture
def copado_intelligence(mock_env, mock_aiohttp_session):
    """Create CopadoIntelligenceEngine instance for testing"""
    with patch('aiohttp.ClientSession', return_value=mock_aiohttp_session):
        return CopadoIntelligenceEngine()

@pytest.fixture
async def incident_manager(mock_env):
    """Create IncidentManager instance for testing"""
    manager = IncidentManager()
    await manager.initialize()
    return manager

@pytest.fixture
def action_executor(mock_env, mock_aiohttp_session):
    """Create ActionExecutor instance for testing"""
    with patch('aiohttp.ClientSession', return_value=mock_aiohttp_session):
        return ActionExecutor()

@pytest.fixture
def webhook_payload_git():
    """Sample Git webhook payload for testing"""
    return {
        "source": "git",
        "event_type": "push",
        "data": {
            "commits": [
                {
                    "id": "abc123",
                    "message": "urgent: fix critical production bug",
                    "author": {"name": "John Doe", "email": "john@company.com"},
                    "timestamp": "2024-01-15T10:30:00Z"
                }
            ],
            "repository": {"name": "payment-service", "full_name": "company/payment-service"},
            "ref": "refs/heads/main"
        }
    }

@pytest.fixture
def webhook_payload_copado():
    """Sample Copado webhook payload for testing"""
    return {
        "source": "copado",
        "event_type": "deployment_failed",
        "data": {
            "deployment_id": "dep_123",
            "pipeline_name": "Production Pipeline",
            "environment": "production",
            "status": "failed",
            "error_message": "Deployment timeout after 30 minutes",
            "user_story": "US-456",
            "timestamp": "2024-01-15T10:30:00Z"
        }
    }

@pytest.fixture
def webhook_payload_salesforce():
    """Sample Salesforce webhook payload for testing"""
    return {
        "source": "salesforce",
        "event_type": "audit_trail",
        "data": {
            "action": "DELETE",
            "object_type": "Account",
            "record_id": "001XX000004TLP5",
            "user_id": "005XX000001Sv6D",
            "timestamp": "2024-01-15T10:30:00Z",
            "ip_address": "192.168.1.100"
        }
    }

@pytest.fixture
def test_client():
    """Create FastAPI test client"""
    # Import here to avoid circular dependencies
    from main import app
    return TestClient(app)
