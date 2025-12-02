"""
Main orchestrator for pricing recommendations.
Integrates conceptual agents and LangChain reasoning.
"""
from typing import Dict, Any
from app.models.recommendation import RecommendationRequest, RecommendationResponse
from app.services.recommendation_service import combine_factors, apply_guardrails

# Import Agents
from app.orchestration.agents.environment_agent import evaluate_environment
from app.orchestration.agents.supply_demand_agent import evaluate_supply_demand
from app.orchestration.agents.loyalty_agent import evaluate_loyalty
from app.orchestration.agents.historical_agent import evaluate_historical
from app.orchestration.agents.corporate_pressure_agent import evaluate_corporate_pressure

# Import Chain
from app.orchestration.chains.pricing_explanation_chain import generate_explanation

# LangChain & Config
from langchain_openai import ChatOpenAI
from app.core.config import settings

async def orchestrate_pricing_recommendation(
    req: RecommendationRequest,
) -> RecommendationResponse:
    """
    High-level orchestration for pricing recommendation.
    
    1. Calls all conceptual agents to gather factors.
    2. Combines factors and applies guardrails.
    3. Invokes LangChain to generate natural language reasoning.
    4. Returns complete response.
    """
    # 1. Initialize LLM
    # Note: In production, this might be injected or singleton
    llm = ChatOpenAI(
        model=settings.llm_model,
        temperature=settings.llm_temperature,
        api_key=settings.openai_api_key
    )

    # 2. Call conceptual agents
    env = evaluate_environment(req)
    supply_demand = evaluate_supply_demand(req)
    loyalty = evaluate_loyalty(req)
    historical = evaluate_historical(req)
    corporate_pressure = evaluate_corporate_pressure(req)

    # Store factors for guardrails
    all_factors = {
        "environment": env,
        "supply_demand": supply_demand,
        "loyalty": loyalty,
        "historical": historical,
        "corporate_pressure": corporate_pressure
    }

    # 3. Combine factors & Apply Guardrails
    # (Reusing Dev 1's robust logic for math/rules)
    combination = combine_factors(env, supply_demand, loyalty, historical, corporate_pressure)
    raw_adjustment = combination["recommended_adjustment"]
    goodness = combination["goodness"]

    guardrail_result = apply_guardrails(
        raw_adjustment,
        req.scenario,
        req.loyalty_segment,
        all_factors
    )

    final_adjustment = guardrail_result["adjusted_value"]
    guardrail_flags = guardrail_result["flags"]

    # Adjust goodness if guardrails applied
    if abs(final_adjustment - raw_adjustment) > 0.05:
        if guardrail_result["guardrail_applied"] == "emergency":
            goodness = max(goodness, 0.85)  # Ethical pricing is good
        elif guardrail_flags:
            goodness = max(0.60, goodness - 0.10)  # Tension exists

    # Prepare summaries for explanation
    factor_summaries = {
        "environment": env["summary"],
        "supply_demand": supply_demand["summary"],
        "loyalty": loyalty["summary"],
        "historical": historical["summary"],
        "corporate_pressure": corporate_pressure["summary"]
    }
    if guardrail_flags:
        factor_summaries["guardrails"] = " | ".join(guardrail_flags)

    # 4. Generate reasoning via LangChain (Async)
    try:
        # Use model_dump() for Pydantic v2 compatibility
        req_dict = req.model_dump()
        
        reasoning = await generate_explanation(
            llm,
            req_dict,
            factor_summaries,
            final_adjustment,
            goodness
        )
    except Exception as e:
        # Graceful fallback if LLM service is down or key is missing
        print(f"LLM Generation Error: {e}")
        reasoning = (
            "Pricing Recommendation Generated (AI Explanation Unavailable)\n"
            f"Error: {str(e)}\n\n"
            f"Factors: {str(factor_summaries)}"
        )

    # 5. Return complete response
    return RecommendationResponse(
        recommended_adjustment=round(final_adjustment, 2),
        goodness=round(goodness, 2),
        factors=factor_summaries,
        reasoning=reasoning
    )
