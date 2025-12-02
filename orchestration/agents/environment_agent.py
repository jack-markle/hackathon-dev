"""
Environment Agent - STUB for Dev 2

Responsibility: Evaluate environmental factors (storms, road closures, emergencies)
and express them as a pricing adjustment factor.

Current state: Logic implemented in backend/app/services/recommendation_service.py
by Dev 1 as compute_environment_factor().

Dev 2 can:
- Keep using the service function directly, OR
- Wrap it as a formal LangChain tool/agent if desired for the architecture demo
"""
from typing import Any, Dict


def evaluate_environment(context: Dict[str, Any]) -> Dict[str, Any]:
    """
    Evaluate environmental impact on pricing.
    
    Args:
        context: Dictionary with zone, scenario, time, etc.
    
    Returns:
        Dictionary with 'factor' (float) and 'summary' (str)
    
    TODO (Dev 2): Decide if you want to use this as a wrapper or use
    the service function directly.
    """
    # Option 1: Delegate to Dev 1's implementation
    from app.models.recommendation import RecommendationRequest
    from app.services.recommendation_service import compute_environment_factor
    
    # Convert context to request object
    req = RecommendationRequest(**context)
    return compute_environment_factor(req)
    
    # Option 2: Implement as a separate LangChain tool
    # (Dev 2's choice based on architecture needs)

