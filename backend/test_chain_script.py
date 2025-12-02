"""
Standalone script to test the LangChain pricing explanation chain.
Run this script to verify that the LLM integration generates meaningful explanations.

Usage:
    cd backend
    python test_chain_script.py
"""
import asyncio
import os
import sys

# Add the current directory to sys.path so we can import from app
sys.path.append(os.getcwd())

from langchain_openai import ChatOpenAI
from app.core.config import settings
from app.orchestration.chains.pricing_explanation_chain import generate_explanation

async def main():
    print("--- Testing Pricing Explanation Chain ---")
    
    # Check for API Key
    if not settings.openai_api_key or "sk-" not in settings.openai_api_key:
        print("⚠️  WARNING: OPENAI_API_KEY not found or invalid in .env")
        print("   The script will try to run, but likely fail if no key is present.")
    else:
        print(f"✅ API Key detected (starts with {settings.openai_api_key[:3]}...)")

    # 1. Initialize LLM
    print(f"Initializing LLM: {settings.llm_model}...")
    try:
        llm = ChatOpenAI(
            model=settings.llm_model,
            temperature=settings.llm_temperature,
            api_key=settings.openai_api_key
        )
    except Exception as e:
        print(f"❌ Failed to initialize LLM: {e}")
        return

    # 2. Mock Data (Simulating the output from Agents)
    mock_request = {
        "zone": "Downtown Metro",
        "scenario": "Heavy Rain",
        "time": "2023-10-27T18:30:00Z",
        "loyalty_segment": "Gold Tier"
    }

    mock_factors = {
        "environment": "Heavy rain slows traffic and increases difficulty (+8%)",
        "supply_demand": "Evening rush hour with high demand (+15%)",
        "loyalty": "Gold Tier member receives loyalty discount (-5%)",
        "historical": "Historical patterns suggest +5% for this zone/weather",
        "corporate_pressure": "Moderate revenue goal nudges price up (+3%)",
        "guardrails": "MAX SURGE capped at 100% (Not applied here)"
    }

    adjustment = 0.26  # +26%
    goodness = 0.78    # Good balance

    print("\n--- Input Data ---")
    print(f"Request: {mock_request}")
    print(f"Adjustment: {adjustment*100:.0f}%")
    print(f"Goodness: {goodness}")
    print("-" * 30)

    # 3. Generate Explanation
    print("\nInvoking Chain (calling OpenAI)...")
    try:
        explanation = await generate_explanation(
            llm,
            mock_request,
            mock_factors,
            adjustment,
            goodness
        )
        
        print("\n✅ Chain Output Success!")
        print("=" * 60)
        print(explanation)
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Chain Execution Failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())

