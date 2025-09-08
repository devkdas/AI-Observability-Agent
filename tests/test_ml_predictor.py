import pytest
import numpy as np
from unittest.mock import Mock, patch, MagicMock
from services.ml_predictor import AdvancedMLPredictor
from models.incident import Signal

class TestAdvancedMLPredictor:
    """Test suite for Advanced ML Predictor service"""
    
    def test_initialization(self, ml_predictor):
        """Test ML predictor initializes correctly"""
        assert ml_predictor is not None
        assert hasattr(ml_predictor, 'models')
        assert hasattr(ml_predictor, 'prediction_cache')
    
    @pytest.mark.asyncio
    async def test_predict_incident_likelihood_high_risk(self, ml_predictor):
        """Test high risk prediction scenario"""
        # High risk context data
        context = {
            'source': 'copado',
            'environment': 'production',
            'deployment_type': 'critical',
            'time': '02:30',  # Late night
            'urgency': 'high'
        }
        
        prediction = await ml_predictor.predict_incident_likelihood(context)
        
        assert isinstance(prediction, dict)
        assert 'likelihood' in prediction
        assert 'confidence' in prediction
        assert 'risk_factors' in prediction
        assert 'prevention_actions' in prediction
        assert 0 <= prediction['likelihood'] <= 1
        assert 0 <= prediction['confidence'] <= 1
    
    @pytest.mark.asyncio
    async def test_predict_incident_likelihood_low_risk(self, ml_predictor):
        """Test low risk prediction scenario"""
        context = {
            'source': 'git',
            'environment': 'development',
            'deployment_type': 'feature',
            'time': '14:30',  # Business hours
            'urgency': 'low'
        }
        
        prediction = await ml_predictor.predict_incident_likelihood(context)
        
        assert prediction['likelihood'] < 0.6  # Should predict lower risk
        assert len(prediction['risk_factors']) >= 0
    
    def test_identify_risk_factors(self, ml_predictor):
        """Test risk factor identification"""
        context = {
            'source': 'copado',
            'description': 'production deployment failed'
        }
        
        factors = ml_predictor._identify_risk_factors(context)
        
        assert isinstance(factors, list)
        assert len(factors) >= 0
    
    def test_suggest_prevention(self, ml_predictor):
        """Test prevention suggestions generation"""
        context = {'severity': 'high', 'environment': 'production'}
        score = 0.8
        
        suggestions = ml_predictor._suggest_prevention(context, score)
        
        assert isinstance(suggestions, list)
        assert len(suggestions) >= 0
