from typing import Dict, Any, Optional, List
from langchain_core.tools import tool
from app.models.recommendation import RecommendationRequest
from app.services.recommendation_service import compute_corporate_pressure_factor

@tool
def corporate_pressure_tool(
    origin_zone: str,
    destination_zone: str,
    scenarios: List[str],
    scenario: str,
    time: str,
    loyalty_segment: Optional[str] = None,
    notes: Optional[str] = None,
    corporate_revenue_goal: Optional[float] = None,
    corporate_strategy_notes: Optional[str] = None
) -> Dict[str, Any]:
    """
    Evaluate corporate pressure factors based on the recommendation request.
    Returns a factor adjustment (float) and a summary (string).
    """
    req = RecommendationRequest(
        origin_zone=origin_zone,
        destination_zone=destination_zone,
        scenarios=scenarios,
        scenario=scenario,
        time=time,
        loyalty_segment=loyalty_segment,
        notes=notes,
        corporate_revenue_goal=corporate_revenue_goal,
        corporate_strategy_notes=corporate_strategy_notes
    )
    return compute_corporate_pressure_factor(req)
