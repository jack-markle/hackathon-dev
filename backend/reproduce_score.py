
import asyncio
from app.services.recommendation_service import build_recommendation, compute_corporate_pressure_factor, compute_environment_factor, compute_supply_demand_factor
from app.models.recommendation import RecommendationRequest

def test_low_confidence():
    req = RecommendationRequest(
        origin_zone="suburbs",
        destination_zone="suburbs", 
        scenarios=["normal"],
        scenario="normal",
        time="2024-01-15T10:00:00Z", # Off-peak Monday 10am
        loyalty_segment="standard",
        notes="Testing low confidence",
        corporate_revenue_goal=0.20, # High goal
        corporate_strategy_notes="Aggressive growth"
    )

    # Debug individual factors
    env = compute_environment_factor(req)
    supply = compute_supply_demand_factor(req)
    corp = compute_corporate_pressure_factor(req)
    
    print(f"Environment Factor: {env['factor']}")
    print(f"Supply/Demand Factor: {supply['factor']}")
    print(f"Corporate Factor: {corp['factor']}")
    
    market_support = env['factor'] + supply['factor']
    print(f"Market Support: {market_support}")

    # Run full recommendation
    result = build_recommendation(req)
    
    print(f"\n--- Result ---")
    print(f"Recommended Adjustment: {result.recommended_adjustment}")
    print(f"Goodness Score: {result.goodness}")
    print(f"Reasoning: {result.overall_reasoning}")

if __name__ == "__main__":
    test_low_confidence()

