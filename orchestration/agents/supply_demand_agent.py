"""
Supply & Demand Agent - STUB for Dev 2

Responsibility: Evaluate supply/demand impact based on time, driver availability patterns.

Current state: Logic implemented in backend/app/services/recommendation_service.py
by Dev 1 as compute_supply_demand_factor().
"""
from typing import Any, Dict


def evaluate_supply_demand(context: Dict[str, Any]) -> Dict[str, Any]:
    """
    Evaluate supply/demand impact on pricing.
    
    Args:
        context: Dictionary with time, zone, etc.
    
    Returns:
        Dictionary with 'factor' (float) and 'summary' (str)
    """
    from app.models.recommendation import RecommendationRequest
    from app.services.recommendation_service import compute_supply_demand_factor
    
    req = RecommendationRequest(**context)
    return compute_supply_demand_factor(req)

