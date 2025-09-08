import pytest
import asyncio
from unittest.mock import Mock, AsyncMock, patch
from services.quantum_analyzer import QuantumInspiredAnalyzer
from models.incident import Incident

class TestQuantumInspiredAnalyzer:
    """Test suite for Quantum Inspired Analyzer"""
    
    def test_initialization(self, quantum_analyzer):
        """Test quantum analyzer initializes correctly"""
        assert quantum_analyzer is not None
        assert hasattr(quantum_analyzer, 'quantum_states')
        assert hasattr(quantum_analyzer, 'entanglement_matrix')
        assert hasattr(quantum_analyzer, 'superposition_cache')
    
    @pytest.mark.asyncio
    async def test_quantum_parallel_analysis(self, quantum_analyzer):
        """Test quantum parallel analysis"""
        incident_data = {
            'severity': 0.8,
            'source': 'git',
            'event_type': 'push',
            'description': 'Multiple concurrent deployment failures'
        }
        
        analysis = await quantum_analyzer.quantum_parallel_analysis(incident_data)
        
        assert isinstance(analysis, dict)
        assert 'quantum_confidence' in analysis
        assert 'parallel_insights' in analysis
        assert 'entangled_patterns' in analysis
        assert 'superposition_analysis' in analysis
        assert 'quantum_recommendations' in analysis
    
    def test_basic_quantum_functionality(self, quantum_analyzer):
        """Test basic quantum analyzer functionality"""
        assert quantum_analyzer.quantum_states == {}
        assert quantum_analyzer.entanglement_matrix.shape == (10, 10)
        assert quantum_analyzer.superposition_cache == {}
    
    
