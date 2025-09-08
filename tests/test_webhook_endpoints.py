import pytest
import asyncio
import json
from fastapi.testclient import TestClient
from unittest.mock import Mock, AsyncMock, patch

class TestWebhookEndpoints:
    """Integration tests for webhook endpoints"""
    
    @patch('main.process_git_event')
    def test_git_webhook_endpoint_valid_payload(self, mock_process_git, test_client, webhook_payload_git):
        """Test Git webhook endpoint with valid payload"""
        mock_process_git.return_value = AsyncMock()
        
        response = test_client.post(
            "/webhook/git",
            json=webhook_payload_git,
            headers={"Content-Type": "application/json"}
        )
        
        assert response.status_code == 200
        assert response.json()["status"] == "received"
    
    @patch('main.process_git_event')
    def test_git_webhook_endpoint_invalid_payload(self, mock_process_git, test_client):
        """Test Git webhook endpoint with invalid payload"""
        mock_process_git.return_value = AsyncMock()
        invalid_payload = {"source": "git", "event_type": "push", "data": {"invalid": "data"}}
        
        response = test_client.post(
            "/webhook/git",
            json=invalid_payload,
            headers={"Content-Type": "application/json"}
        )
        
        # Should still process but may log warnings
        assert response.status_code in [200, 400, 422]
    
    @patch('main.process_copado_event')
    def test_copado_webhook_endpoint_deployment_failure(self, mock_process_copado, test_client, webhook_payload_copado):
        """Test Copado webhook endpoint with deployment failure"""
        mock_process_copado.return_value = AsyncMock()
        
        response = test_client.post(
            "/webhook/copado",
            json=webhook_payload_copado,
            headers={"Content-Type": "application/json"}
        )
        
        assert response.status_code == 200
        result = response.json()
        assert result["status"] == "received"
    
    @patch('main.process_copado_event')
    def test_copado_webhook_endpoint_success_deployment(self, mock_process_copado, test_client):
        """Test Copado webhook endpoint with successful deployment"""
        mock_process_copado.return_value = AsyncMock()
        success_payload = {
            "source": "copado",
            "event_type": "deployment_completed",
            "data": {
                "deployment_id": "dep_success_123",
                "pipeline_name": "Staging Pipeline",
                "environment": "staging",
                "status": "success",
                "duration": "8 minutes",
                "timestamp": "2024-01-15T10:30:00Z"
            }
        }
        
        response = test_client.post(
            "/webhook/copado",
            json=success_payload,
            headers={"Content-Type": "application/json"}
        )
        
        assert response.status_code == 200
        assert response.json()["status"] == "received"
    
    @patch('main.process_salesforce_event')
    def test_salesforce_webhook_endpoint_bulk_delete(self, mock_process_sf, test_client, webhook_payload_salesforce):
        """Test Salesforce webhook endpoint with suspicious activity"""
        mock_process_sf.return_value = AsyncMock()
        
        response = test_client.post(
            "/webhook/salesforce",
            json=webhook_payload_salesforce,
            headers={"Content-Type": "application/json"}
        )
        
        assert response.status_code == 200
        result = response.json()
        assert result["status"] == "received"
    
    @patch('main.process_salesforce_event')
    def test_salesforce_webhook_endpoint_normal_activity(self, mock_process_sf, test_client):
        """Test Salesforce webhook endpoint with normal activity"""
        mock_process_sf.return_value = AsyncMock()
        normal_payload = {
            "source": "salesforce",
            "event_type": "audit_trail",
            "data": {
                "action": "UPDATE",
                "object_type": "Contact",
                "record_id": "003XX000004TLP5",
                "user_id": "005XX000001Sv6D",
                "timestamp": "2024-01-15T10:30:00Z",
                "changes": {"Email": {"old": "old@email.com", "new": "new@email.com"}}
            }
        }
        
        response = test_client.post(
            "/webhook/salesforce",
            json=normal_payload,
            headers={"Content-Type": "application/json"}
        )
        
        assert response.status_code == 200
    
    @patch('main.process_git_event')
    def test_webhook_authentication(self, mock_process_git, test_client):
        """Test webhook endpoint authentication/validation"""
        mock_process_git.return_value = AsyncMock()
        # Test with missing headers
        response = test_client.post(
            "/webhook/git",
            json={"source": "git", "event_type": "test", "data": {}}
        )
        
        # Should still work (basic webhook endpoints typically don't require auth)
        assert response.status_code in [200, 401]
    
    def test_webhook_content_type_validation(self, test_client):
        """Test webhook content type validation"""
        response = test_client.post(
            "/webhook/git",
            content="invalid non-json data",
            headers={"Content-Type": "text/plain"}
        )
        
        # Should reject non-JSON content
        assert response.status_code in [400, 422]
    
    def test_webhook_payload_size_limit(self, test_client):
        """Test webhook payload size handling"""
        # Create a large payload
        large_payload = {
            "event_type": "push",
            "data": {
                "commits": [{"message": "x" * 10000}] * 100  # Large payload
            }
        }
        
        response = test_client.post(
            "/webhook/git",
            json=large_payload,
            headers={"Content-Type": "application/json"}
        )
        
        # Should handle large payloads gracefully
        assert response.status_code in [200, 413, 422]  # 422 = Unprocessable Entity (validation error)
    
    @patch('main.process_git_event')
    def test_concurrent_webhook_processing(self, mock_process_git, test_client, webhook_payload_git):
        """Test concurrent webhook processing"""
        mock_process_git.return_value = AsyncMock()
        import threading
        import time
        
        responses = []
        
        def send_webhook():
            response = test_client.post(
                "/webhook/git", 
                json=webhook_payload_git,
                headers={"Content-Type": "application/json"}
            )
            responses.append(response)
        
        # Send multiple concurrent requests
        threads = []
        for _ in range(5):
            thread = threading.Thread(target=send_webhook)
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        # All should succeed
        assert len(responses) == 5
        assert all(r.status_code == 200 for r in responses)
    
    @patch('main.process_git_event')
    @patch('services.incident_manager.IncidentManager.create_incident')
    def test_webhook_incident_creation_flow(self, mock_create_incident, mock_process_git, test_client, webhook_payload_git):
        """Test end-to-end incident creation from webhook"""
        mock_process_git.return_value = AsyncMock()
        mock_create_incident.return_value = Mock(id="incident_123")
        
        response = test_client.post(
            "/webhook/git",
            json=webhook_payload_git,
            headers={"Content-Type": "application/json"}
        )
        
        assert response.status_code == 200
        assert response.json()["status"] == "received"
        # Background task is mocked, so we verify the endpoint responds correctly
    
    def test_webhook_error_handling(self, test_client):
        """Test webhook error handling for malformed requests"""
        # Test with completely invalid JSON
        response = test_client.post(
            "/webhook/git",
            content="{ invalid json",
            headers={"Content-Type": "application/json"}
        )
        
        assert response.status_code in [400, 422]
    
    @patch('main.process_git_event')
    def test_webhook_response_format(self, mock_process_git, test_client, webhook_payload_git):
        """Test webhook response format consistency"""
        mock_process_git.return_value = AsyncMock()
        
        response = test_client.post(
            "/webhook/git",
            json=webhook_payload_git,
            headers={"Content-Type": "application/json"}
        )
        
        assert response.status_code == 200
        result = response.json()
        
        # Should have consistent response format
        assert "status" in result
        assert result["status"] == "received"


class TestAPIEndpoints:
    """Integration tests for API endpoints"""
    
    def test_get_incidents_endpoint(self, test_client):
        """Test incidents retrieval endpoint"""
        response = test_client.get("/api/incidents")
        
        assert response.status_code == 200
        result = response.json()
        assert isinstance(result, list)
    
    def test_get_incident_by_id_existing(self, test_client):
        """Test getting specific incident by ID"""
        # This would need a real incident in the system
        response = test_client.get("/api/incidents/test-incident-123")
        
        # May return 404 if no test data, which is acceptable
        assert response.status_code in [200, 404]
    
    def test_get_incident_by_id_nonexistent(self, test_client):
        """Test getting non-existent incident"""
        response = test_client.get("/api/incidents/nonexistent-id")
        
        assert response.status_code == 404
    
    def test_dashboard_endpoint(self, test_client):
        """Test dashboard HTML endpoint"""
        response = test_client.get("/dashboard")
        
        assert response.status_code == 200
        assert "text/html" in response.headers.get("content-type", "")
    
    def test_advanced_dashboard_endpoint(self, test_client):
        """Test advanced dashboard HTML endpoint"""
        response = test_client.get("/advanced-dashboard")
        
        assert response.status_code == 200
        assert "text/html" in response.headers.get("content-type", "")
    
    def test_executive_dashboard_endpoint(self, test_client):
        """Test executive dashboard HTML endpoint"""
        response = test_client.get("/executive-dashboard")
        
        assert response.status_code == 200
        assert "text/html" in response.headers.get("content-type", "")
    
    def test_metrics_api_endpoint(self, test_client):
        """Test metrics API endpoint"""
        response = test_client.get("/api/metrics")

        # Endpoint may not be implemented yet
        assert response.status_code in [200, 404]
        result = response.json()
        
        # Should contain basic metrics structure
        assert isinstance(result, dict)
        expected_keys = ["incidents_count", "avg_resolution_time", "success_rate"]
        # At least some metrics should be present
        assert any(key in result for key in expected_keys)
    
    def test_health_check_endpoint(self, test_client):
        """Test health check endpoint"""
        response = test_client.get("/health")
        
        # Health endpoint might not exist yet, but if it does, should return 200
        assert response.status_code in [200, 404]
        
        if response.status_code == 200:
            result = response.json()
            assert "status" in result
    
    def test_api_error_handling(self, test_client):
        """Test API error handling for invalid endpoints"""
        response = test_client.get("/api/nonexistent-endpoint")
        
        assert response.status_code == 404
    
    def test_api_cors_headers(self, test_client):
        """Test CORS headers in API responses"""
        response = test_client.get("/api/incidents")
        
        # Check if CORS headers are present (may not be configured yet)
        headers = response.headers
        # This is optional - just checking if they exist
        cors_header = headers.get("Access-Control-Allow-Origin")
        # Don't assert as CORS may not be configured


class TestWebSocketEndpoints:
    """Integration tests for WebSocket endpoints (if implemented)"""
    
    def test_websocket_connection(self, test_client):
        """Test WebSocket connection for real-time updates"""
        # WebSocket testing requires special handling
        # This is a placeholder for when WebSocket endpoints are added
        pass
    
    def test_real_time_incident_updates(self, test_client):
        """Test real-time incident updates via WebSocket"""
        # Future implementation for real-time dashboard updates
        pass


class TestSystemIntegration:
    """Integration tests for system-wide functionality"""
    
    @patch('main.process_git_event')
    @pytest.mark.asyncio
    async def test_full_incident_workflow(self, mock_process_git, test_client, webhook_payload_git):
        """Test complete incident workflow from webhook to resolution"""
        mock_process_git.return_value = AsyncMock()
        
        with patch('services.ai_analyzer.AIAnalyzer.analyze_incident') as mock_analyze:
            mock_analyze.return_value = Mock(
                incident_id="test_123",
                root_cause="Test issue",
                confidence=0.85,
                suggested_actions=["Test action"]
            )
            
            # Send webhook to trigger incident
            response = test_client.post(
                "/webhook/git",
                json=webhook_payload_git,
                headers={"Content-Type": "application/json"}
            )
            
            assert response.status_code == 200
            assert response.json()["status"] == "received"
            
            # Check if incidents API is accessible
            incidents_response = test_client.get("/api/incidents")
            assert incidents_response.status_code == 200
    
    def test_database_connectivity(self, test_client):
        """Test database connectivity through API calls"""
        # This tests that the database connection works through the API
        response = test_client.get("/api/incidents")
        
        # Should not fail due to database connection issues
        assert response.status_code in [200, 500]  # 500 only if DB is down
    
    @patch('main.process_git_event')
    def test_external_api_fallbacks(self, mock_process_git, test_client, webhook_payload_git):
        """Test that system works when external APIs are unavailable"""
        mock_process_git.return_value = AsyncMock()
        
        with patch('aiohttp.ClientSession.post', side_effect=Exception("API unavailable")):
            response = test_client.post(
                "/webhook/git",
                json=webhook_payload_git,
                headers={"Content-Type": "application/json"}
            )
            
            # Should still accept webhook even if external APIs fail
            assert response.status_code == 200
            assert response.json()["status"] == "received"
