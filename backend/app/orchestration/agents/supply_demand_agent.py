from typing import Dict, Any
from app.models.recommendation import RecommendationRequest
from app.services.recommendation_service import compute_supply_demand_factor

def evaluate_supply_demand(req: RecommendationRequest) -> Dict[str, Any]:
    """
    Evaluate supply and demand factors.
    Wrapper for recommendation_service.compute_supply_demand_factor.
    """
    return compute_supply_demand_factor(req)
