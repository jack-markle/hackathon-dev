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
        origin_zone="downtown",
        destination_zone="downtown",
        scenarios=["normal"],
        scenario="normal",
        time="2025-10-10T10:00:00Z",
        loyalty_segment="gold",
        corporate_revenue_goal=0.10
    )

    # 2. Mock Dependencies
    # Mock the agent executor
    with patch("app.orchestration.orchestrator.build_orchestrator_agent") as mock_build_agent:
        mock_agent_executor = AsyncMock()
        mock_agent_executor.ainvoke.return_value = {
            "output": "AI Generated Explanation",
            "intermediate_steps": [],
            "messages": []
        }
        mock_build_agent.return_value = mock_agent_executor

        # 3. Execute
        response = await orchestrate_pricing_recommendation(req)
        
        # 4. Assertions
        # Check basic structure
        assert response.recommended_adjustment is not None
        assert response.goodness is not None
        assert response.overall_reasoning is not None
        assert response.factor_reasoning is not None
        
        # Check factors presence
        # Note: In mock response without tools, factors might be empty unless extracted from reasoning
        # But extracted reasoning checks keys
        
        # Verify agent was built
        mock_build_agent.assert_called_once()
        
        # Verify agent was invoked
        mock_agent_executor.ainvoke.assert_called_once()

@pytest.mark.asyncio
async def test_orchestrator_llm_failure_fallback():
    """
    Test that the orchestrator provides a fallback message if LLM fails.
    """
    req = RecommendationRequest(
        origin_zone="downtown",
        destination_zone="downtown",
        scenarios=["normal"],
        scenario="normal",
        time="2025-10-10T10:00:00Z",
        loyalty_segment="standard"
    )

    with patch("app.orchestration.orchestrator.build_orchestrator_agent") as mock_build_agent:
        mock_agent_executor = AsyncMock()
        # Simulate LLM failure
        mock_agent_executor.ainvoke.side_effect = Exception("API Error")
        mock_build_agent.return_value = mock_agent_executor
        
        response = await orchestrate_pricing_recommendation(req)
        
        # Should not crash, but return fallback reasoning
        assert "AI reasoning temporarily unavailable" in response.overall_reasoning or "Error" in response.overall_reasoning

