"""
Standalone script to test the LangChain Orchestrator Agent.
Run this script to verify that the Agent drives the pricing flow and generates explanations.

Usage:
    cd backend
    python test_chain_script.py
"""
import asyncio
import os
import sys
import json

# Add the current directory to sys.path so we can import from app
sys.path.append(os.getcwd())

from app.core.config import settings
from app.models.recommendation import RecommendationRequest
from app.orchestration.orchestrator import orchestrate_pricing_recommendation

async def main():
    print("--- Testing LangChain Orchestrator Agent ---")
    
    # Check for API Key
    if not settings.openai_api_key or "sk-" not in settings.openai_api_key:
        print("⚠️  WARNING: OPENAI_API_KEY not found or invalid in .env")
        print("   The script will try to run, but likely fail if no key is present.")
    else:
        print(f"✅ API Key detected (starts with {settings.openai_api_key[:3]}...)")

    # 1. Create Request
    req = RecommendationRequest(
        origin_zone="downtown",
        destination_zone="airport_corridor",
        scenarios=["storm", "road_closure"],
        scenario="storm",
        time="2024-01-15T14:30:00.000Z",
        loyalty_segment="gold",
        notes="Storm expected to reduce driver availability by 40%.",
        corporate_revenue_goal=0.03,
        corporate_strategy_notes="Q4 revenue push"
    )
    
    print("\n--- Input Request ---")
    print(json.dumps(req.model_dump(), indent=2, default=str))
    print("-" * 30)

    # 2. Run Orchestrator
    print("\nInvoking Orchestrator Agent (this may take a few seconds)...")
    try:
        response = await orchestrate_pricing_recommendation(req)
        
        print("\n✅ Orchestration Success!")
        print("=" * 60)
        print(f"Recommended Adjustment: +{response.recommended_adjustment*100:.0f}%")
        print(f"Goodness Score: {response.goodness}")
        print("\nFactors:")
        for k, v in response.factors.items():
            print(f"  - {k}: {v}")
            
        print("\nOverall Reasoning:")
        print(response.overall_reasoning)
        
        print("\nFactor Reasoning Summaries:")
        if response.factor_reasoning.environment:
            print(f"  - Environment: {response.factor_reasoning.environment}")
        if response.factor_reasoning.supply_demand:
            print(f"  - Supply/Demand: {response.factor_reasoning.supply_demand}")
        if response.factor_reasoning.loyalty:
            print(f"  - Loyalty: {response.factor_reasoning.loyalty}")
        if response.factor_reasoning.historical:
            print(f"  - Historical: {response.factor_reasoning.historical}")
        if response.factor_reasoning.corporate_pressure:
            print(f"  - Corporate Pressure: {response.factor_reasoning.corporate_pressure}")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Orchestration Failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
