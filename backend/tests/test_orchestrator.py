import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from app.models.recommendation import RecommendationRequest
from app.orchestration.orchestrator import orchestrate_pricing_recommendation

@pytest.mark.asyncio
async def test_orchestrator_flow():
    """
    Test that the orchestrator correctly calls agents, calculates factors,
    and invokes the explanation chain.
    """
    # 1. Prepare Request
    req = RecommendationRequest(
        zone="downtown",
        scenario="normal",
        time="2025-10-10T10:00:00Z",
        loyalty_segment="gold",
        corporate_revenue_goal=0.10
    )

    # 2. Mock Dependencies
    # Mock the explanation generation to avoid LLM calls
    with patch("app.orchestration.orchestrator.generate_explanation", new_callable=AsyncMock) as mock_gen:
        mock_gen.return_value = "AI Generated Explanation"
        
        # Mock ChatOpenAI to avoid API key validation/init
        with patch("app.orchestration.orchestrator.ChatOpenAI") as mock_llm_cls:
            mock_llm_instance = MagicMock()
            mock_llm_cls.return_value = mock_llm_instance
            
            # 3. Execute
            response = await orchestrate_pricing_recommendation(req)
            
            # 4. Assertions
            # Check basic structure
            assert response.recommended_adjustment is not None
            assert response.goodness is not None
            assert response.reasoning == "AI Generated Explanation"
            
            # Check factors presence
            assert "environment" in response.factors
            assert "supply_demand" in response.factors
            assert "loyalty" in response.factors
            assert "historical" in response.factors
            assert "corporate_pressure" in response.factors

            # Verify LLM was initialized
            mock_llm_cls.assert_called_once()
            
            # Verify explanation chain was called
            mock_gen.assert_called_once()
            args = mock_gen.call_args
            # args[0][0] is llm, args[0][1] is req_dict
            assert args[0][1]["zone"] == "downtown"

@pytest.mark.asyncio
async def test_orchestrator_llm_failure_fallback():
    """
    Test that the orchestrator provides a fallback message if LLM fails.
    """
    req = RecommendationRequest(
        zone="downtown",
        scenario="normal",
        time="2025-10-10T10:00:00Z",
        loyalty_segment="standard"
    )

    with patch("app.orchestration.orchestrator.generate_explanation", new_callable=AsyncMock) as mock_gen:
        # Simulate LLM failure
        mock_gen.side_effect = Exception("API Error")
        
        with patch("app.orchestration.orchestrator.ChatOpenAI"):
            response = await orchestrate_pricing_recommendation(req)
            
            # Should not crash, but return fallback reasoning
            assert "AI Explanation Unavailable" in response.reasoning
            assert "Error: API Error" in response.reasoning

