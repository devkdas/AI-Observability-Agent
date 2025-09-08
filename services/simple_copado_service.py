"""
Simplified Copado Service for Demo
Uses realistic mock data that simulates live Copado integration
"""

import os
import logging
import random
from datetime import datetime, timedelta
from typing import Dict, List, Any

logger = logging.getLogger(__name__)


class SimplifiedCopadoService:
    """Simplified service that provides realistic Copado-like data for demo"""
    
    def __init__(self):
        self.connection_status = "live_demo_mode"
        self.org_url = os.getenv("COPADO_SANDBOX_URL", "https://copadotrial44223329.my.salesforce.com")
    
    async def initialize(self):
        """Initialize service"""
        logger.info("Copado Demo Service initialized - using realistic demo data")
        return True
    
    async def get_live_deployments(self) -> List[Dict[str, Any]]:
        """Get realistic deployment data"""
        return [
            {
                "id": "a0X8d000001234567",
                "name": "CopadoCon 2025 Feature Release",
                "status": "in_progress",
                "environment": "Production",
                "progress": 78,
                "started_at": (datetime.now() - timedelta(minutes=12)).isoformat(),
                "estimated_completion": (datetime.now() + timedelta(minutes=3)).isoformat(),
                "components_deployed": 24,
                "total_components": 31
            },
            {
                "id": "a0X8d000001234568",
                "name": "Security Hotfix v2.1.1",
                "status": "completed",
                "environment": "Staging",
                "progress": 100,
                "started_at": (datetime.now() - timedelta(hours=1, minutes=30)).isoformat(),
                "completed_at": (datetime.now() - timedelta(hours=1, minutes=15)).isoformat(),
                "components_deployed": 8,
                "total_components": 8
            },
            {
                "id": "a0X8d000001234569",
                "name": "Database Schema Update",
                "status": "scheduled",
                "environment": "Production",
                "progress": 0,
                "scheduled_at": (datetime.now() + timedelta(hours=2)).isoformat(),
                "components_deployed": 0,
                "total_components": 15
            }
        ]
    
    async def get_live_pipelines(self) -> List[Dict[str, Any]]:
        """Get realistic pipeline data"""
        return [
            {
                "id": "a0Y8d000001234567",
                "name": "Main Release Pipeline",
                "status": "healthy",
                "success_rate": 96.8,
                "last_run": (datetime.now() - timedelta(minutes=45)).isoformat(),
                "avg_duration": "14m 23s",
                "environments": ["Dev", "QA", "Staging", "Production"],
                "last_deployment": "CopadoCon 2025 Feature Release"
            },
            {
                "id": "a0Y8d000001234568",
                "name": "Hotfix Pipeline",
                "status": "active",
                "success_rate": 94.2,
                "last_run": (datetime.now() - timedelta(hours=1, minutes=30)).isoformat(),
                "avg_duration": "8m 45s",
                "environments": ["Dev", "Staging", "Production"],
                "last_deployment": "Security Hotfix v2.1.1"
            },
            {
                "id": "a0Y8d000001234569",
                "name": "Feature Branch Pipeline",
                "status": "warning",
                "success_rate": 87.5,
                "last_run": (datetime.now() - timedelta(hours=3)).isoformat(),
                "avg_duration": "11m 12s",
                "environments": ["Dev", "QA"],
                "last_deployment": "Feature/AI-Enhancement"
            }
        ]
    
    async def get_live_test_results(self) -> List[Dict[str, Any]]:
        """Get realistic test results"""
        return [
            {
                "id": "a0Z8d000001234567",
                "suite": "Copado Regression Suite",
                "status": "passed",
                "passed": 142,
                "failed": 3,
                "total": 145,
                "duration": "52m 18s",
                "run_at": (datetime.now() - timedelta(hours=1)).isoformat(),
                "coverage": 94.7,
                "environment": "QA"
            },
            {
                "id": "a0Z8d000001234568",
                "suite": "Security Validation Tests",
                "status": "passed",
                "passed": 67,
                "failed": 0,
                "total": 67,
                "duration": "23m 45s",
                "run_at": (datetime.now() - timedelta(minutes=30)).isoformat(),
                "coverage": 98.2,
                "environment": "Staging"
            },
            {
                "id": "a0Z8d000001234569",
                "suite": "Performance Tests",
                "status": "running",
                "passed": 18,
                "failed": 1,
                "total": 25,
                "duration": "15m 32s (ongoing)",
                "run_at": (datetime.now() - timedelta(minutes=15)).isoformat(),
                "coverage": 89.3,
                "environment": "Performance"
            }
        ]
    
    async def get_live_user_stories(self) -> List[Dict[str, Any]]:
        """Get realistic user stories"""
        return [
            {
                "id": "a108d000001234567",
                "title": "Implement AI-Powered Incident Detection",
                "status": "in_progress",
                "priority": "high",
                "assignee": "AI Observability Agent",
                "created_at": (datetime.now() - timedelta(hours=random.randint(4, 6), minutes=random.randint(0, 59))).isoformat(),
                "story_points": 8,
                "sprint": "CopadoCon 2025 Sprint 1",
                "epic": "Observability Enhancement"
            },
            {
                "id": "a108d000001234568",
                "title": "Optimize Quantum Analysis Performance",
                "status": "ready_for_test",
                "priority": "medium",
                "assignee": "DevOps Team",
                "created_at": (datetime.now() - timedelta(hours=6)).isoformat(),
                "story_points": 5,
                "sprint": "CopadoCon 2025 Sprint 1",
                "epic": "Performance Optimization"
            },
            {
                "id": "a108d000001234569",
                "title": "Add Real-time Dashboard Metrics",
                "status": "completed",
                "priority": "high",
                "assignee": "Frontend Team",
                "created_at": (datetime.now() - timedelta(days=2)).isoformat(),
                "completed_at": (datetime.now() - timedelta(hours=4)).isoformat(),
                "story_points": 13,
                "sprint": "CopadoCon 2025 Sprint 1",
                "epic": "Dashboard Enhancement"
            }
        ]
    
    async def get_connection_status(self) -> Dict[str, Any]:
        """Get connection status info"""
        return {
            "status": "demo_mode",
            "org_url": self.org_url,
            "data_source": "realistic_demo_data",
            "last_updated": datetime.now().isoformat(),
            "message": "Using realistic demo data for CopadoCon 2025 presentation"
        }
    
    async def close(self):
        """Close service"""
        pass
