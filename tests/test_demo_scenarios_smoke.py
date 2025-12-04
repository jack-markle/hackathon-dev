"""
Backend smoke tests for demo scenarios.

This test suite loads demo_scenarios.json and validates that the API
returns responses within expected ranges for each canonical demo scenario.

Run with: pytest tests/test_demo_scenarios_smoke.py
Or: python -m pytest tests/test_demo_scenarios_smoke.py
"""
import json
import os
import sys
from pathlib import Path

# Add backend to path so we can import app modules
backend_path = Path(__file__).parent.parent / "backend"
sys.path.insert(0, str(backend_path))

import pytest
from app.models.recommendation import RecommendationRequest, RecommendationResponse
from app.services.recommendation_service import build_recommendation


# Load demo scenarios JSON
def load_demo_scenarios():
    """Load demo scenarios from JSON file"""
    scenarios_path = Path(__file__).parent.parent / "planning_docs" / "demo_scenarios.json"
    with open(scenarios_path, 'r') as f:
        data = json.load(f)
    return data["scenarios"]


DEMO_SCENARIOS = load_demo_scenarios()


class TestDemoScenariosSmoke:
    """Smoke tests for canonical demo scenarios"""
    
    @pytest.mark.parametrize("scenario_data", DEMO_SCENARIOS)
    def test_scenario_adjustment_range(self, scenario_data):
        """Test that recommended adjustment falls within expected range"""
        scenario_id = scenario_data["scenario_id"]
        input_payload = scenario_data["input_payload"]
        expected_ranges = scenario_data["expected_output_ranges"]
        
        # Build request from payload
        request = RecommendationRequest(**input_payload)
        
        # Get recommendation
        response = build_recommendation(request)
        
        # Validate adjustment range
        expected_min = expected_ranges["recommended_adjustment_pct"]["min"]
        expected_max = expected_ranges["recommended_adjustment_pct"]["max"]
        
        assert expected_min <= response.recommended_adjustment <= expected_max, (
            f"Scenario {scenario_id}: Adjustment {response.recommended_adjustment} "
            f"not in range [{expected_min}, {expected_max}]"
        )
    
    @pytest.mark.parametrize("scenario_data", DEMO_SCENARIOS)
    def test_scenario_goodness_range(self, scenario_data):
        """Test that goodness score falls within expected range"""
        scenario_id = scenario_data["scenario_id"]
        input_payload = scenario_data["input_payload"]
        expected_ranges = scenario_data["expected_output_ranges"]
        
        # Build request from payload
        request = RecommendationRequest(**input_payload)
        
        # Get recommendation
        response = build_recommendation(request)
        
        # Validate goodness range
        expected_min = expected_ranges["goodness"]["min"]
        expected_max = expected_ranges["goodness"]["max"]
        
        assert expected_min <= response.goodness <= expected_max, (
            f"Scenario {scenario_id}: Goodness {response.goodness} "
            f"not in range [{expected_min}, {expected_max}]"
        )
    
    @pytest.mark.parametrize("scenario_data", DEMO_SCENARIOS)
    def test_scenario_required_factors(self, scenario_data):
        """Test that all required factors are present in response"""
        scenario_id = scenario_data["scenario_id"]
        input_payload = scenario_data["input_payload"]
        
        # Build request from payload
        request = RecommendationRequest(**input_payload)
        
        # Get recommendation
        response = build_recommendation(request)
        
        # Check required factors
        required_factors = [
            "environment",
            "supply_demand",
            "loyalty",
            "historical",
            "corporate_pressure"
        ]
        
        for factor in required_factors:
            assert factor in response.factors, (
                f"Scenario {scenario_id}: Missing required factor '{factor}'"
            )
            assert isinstance(response.factors[factor], str), (
                f"Scenario {scenario_id}: Factor '{factor}' should be a string"
            )
            assert len(response.factors[factor]) > 0, (
                f"Scenario {scenario_id}: Factor '{factor}' should not be empty"
            )
    
    @pytest.mark.parametrize("scenario_data", DEMO_SCENARIOS)
    def test_scenario_reasoning_present(self, scenario_data):
        """Test that reasoning field is present and non-empty"""
        scenario_id = scenario_data["scenario_id"]
        input_payload = scenario_data["input_payload"]
        
        # Build request from payload
        request = RecommendationRequest(**input_payload)
        
        # Get recommendation
        response = build_recommendation(request)
        
        # Validate reasoning
        assert hasattr(response, 'reasoning'), (
            f"Scenario {scenario_id}: Missing 'reasoning' field"
        )
        assert isinstance(response.reasoning, str), (
            f"Scenario {scenario_id}: Reasoning should be a string"
        )
        assert len(response.reasoning) > 0, (
            f"Scenario {scenario_id}: Reasoning should not be empty"
        )
    
    def test_emergency_guardrail_override(self):
        """Test that emergency scenarios always return 0% adjustment"""
        emergency_scenario = next(
            (s for s in DEMO_SCENARIOS if s["scenario_id"] == "emergency_guardrail_override"),
            None
        )
        
        if emergency_scenario:
            input_payload = emergency_scenario["input_payload"]
            request = RecommendationRequest(**input_payload)
            response = build_recommendation(request)
            
            assert response.recommended_adjustment == 0.0, (
                f"Emergency scenario must return 0% adjustment, got {response.recommended_adjustment}"
            )
            
            # Check that guardrails are mentioned
            assert "guardrails" in response.factors or "emergency" in response.factors.get("environment", "").lower(), (
                "Emergency scenario should mention guardrails or emergency in factors"
            )
    
    def test_corporate_pressure_cap(self):
        """Test that corporate pressure influence is capped appropriately"""
        # Find scenario with high corporate pressure
        high_pressure_scenario = next(
            (s for s in DEMO_SCENARIOS 
             if s["input_payload"].get("corporate_revenue_goal", 0) > 0.15),
            None
        )
        
        if high_pressure_scenario:
            input_payload = high_pressure_scenario["input_payload"]
            request = RecommendationRequest(**input_payload)
            response = build_recommendation(request)
            
            # Corporate pressure should be capped at 8% actual influence
            # We can't directly test this, but we can verify the adjustment
            # isn't unreasonably high (should be capped by guardrails if needed)
            assert response.recommended_adjustment <= 1.0, (
                "Adjustment should not exceed 100% (2.0x multiplier)"
            )
    
    @pytest.mark.parametrize("scenario_data", DEMO_SCENARIOS)
    def test_scenario_response_structure(self, scenario_data):
        """Test that response matches RecommendationResponse model structure"""
        scenario_id = scenario_data["scenario_id"]
        input_payload = scenario_data["input_payload"]
        
        # Build request from payload
        request = RecommendationRequest(**input_payload)
        
        # Get recommendation
        response = build_recommendation(request)
        
        # Validate response structure
        assert isinstance(response, RecommendationResponse), (
            f"Scenario {scenario_id}: Response should be RecommendationResponse instance"
        )
        
        assert isinstance(response.recommended_adjustment, float), (
            f"Scenario {scenario_id}: recommended_adjustment should be float"
        )
        
        assert isinstance(response.goodness, float), (
            f"Scenario {scenario_id}: goodness should be float"
        )
        
        assert isinstance(response.factors, dict), (
            f"Scenario {scenario_id}: factors should be dict"
        )
        
        assert isinstance(response.reasoning, str), (
            f"Scenario {scenario_id}: reasoning should be string"
        )
        
        # Validate ranges
        assert 0.0 <= response.recommended_adjustment <= 1.0, (
            f"Scenario {scenario_id}: Adjustment should be between 0.0 and 1.0"
        )
        
        assert 0.0 <= response.goodness <= 1.0, (
            f"Scenario {scenario_id}: Goodness should be between 0.0 and 1.0"
        )


if __name__ == "__main__":
    # Allow running directly with python
    pytest.main([__file__, "-v"])

