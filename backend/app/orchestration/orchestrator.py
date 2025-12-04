"""
Main orchestrator for pricing recommendations.
OPTIMIZED: Uses Code-First Orchestration instead of Agent Loop.
1. Calculates all factors deterministically (Python).
2. Uses LLM only for the final reasoning/explanation step.
"""
import re
import logging
from typing import Dict, Any

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

from app.models.recommendation import RecommendationRequest, RecommendationResponse, FactorReasoning
from app.core.config import settings
from app.integrations.n8n_notifier import send_pricing_alert

# Import the deterministic service logic directly
from app.services.recommendation_service import (
    compute_environment_factor,
    compute_supply_demand_factor,
    compute_loyalty_factor,
    compute_historical_factor,
    compute_corporate_pressure_factor,
    combine_factors,
    apply_guardrails
)

logger = logging.getLogger(__name__)

async def orchestrate_pricing_recommendation(
    req: RecommendationRequest,
) -> RecommendationResponse:
    """
    Optimized orchestration:
    1. Compute all factors immediately (Python).
    2. Apply guardrails and calculations (Python).
    3. Send data to LLM to generate the explanation (Reasoning).
    """
    
    # --- STEP 1: Deterministic Calculation (Fast) ---
    # Run all factor computations
    env = compute_environment_factor(req)
    supply = compute_supply_demand_factor(req)
    loyalty = compute_loyalty_factor(req)
    historical = compute_historical_factor(req)
    corp = compute_corporate_pressure_factor(req)
    
    all_factors = {
        "environment": env,
        "supply_demand": supply,
        "loyalty": loyalty,
        "historical": historical,
        "corporate_pressure": corp
    }

    # Calculate initial mix
    combination = combine_factors(env, supply, loyalty, historical, corp)
    raw_adjustment = combination["recommended_adjustment"]
    goodness = combination["goodness"]

    # Apply Guardrails
    guardrail_result = apply_guardrails(
        raw_adjustment,
        req.scenario,
        req.loyalty_segment,
        all_factors
    )
    
    final_adjustment = guardrail_result["adjusted_value"]
    guardrail_flags = guardrail_result["flags"]

    # Adjust goodness if guardrails were active
    if abs(final_adjustment - raw_adjustment) > 0.05:
        if guardrail_result["guardrail_applied"] == "emergency":
            goodness = max(goodness, 0.85)
        elif guardrail_flags:
            goodness = max(0.60, goodness - 0.10)

    # Prepare factor summaries for response
    factor_summaries = {k: v["summary"] for k, v in all_factors.items()}
    if guardrail_flags:
        factor_summaries["guardrails"] = " | ".join(guardrail_flags)


    # --- STEP 2: LLM Reasoning Generation ---
    
    # Construct prompt with the pre-calculated data
    system_prompt = """You are a Pricing Advisor for a ride-hailing platform.
Your goal is to explain a pre-calculated pricing recommendation to a Business Analyst.
Your tone should be professional, objective, and clear.

DATA PROVIDED:
- Request: {request_json}
- Calculated Factors: {factors_json}
- Final Adjustment: {adjustment:.2f}
- Goodness Score: {goodness:.2f}
- Guardrails Triggered: {guardrails}

TASK:
Provide reasoning for each factor and an overall summary.
You MUST use the following format EXACTLY:

ENVIRONMENT_REASONING: [1-2 sentences explaining the environment impact based on the data]
SUPPLY_DEMAND_REASONING: [1-2 sentences explaining supply/demand impact]
LOYALTY_REASONING: [1-2 sentences explaining loyalty impact]
HISTORICAL_REASONING: [1-2 sentences explaining historical context]
CORPORATE_PRESSURE_REASONING: [1-2 sentences explaining corporate goals impact]
OVERALL_REASONING: [3-4 sentences summarizing the recommendation, mentioning key drivers and any guardrails/tensions]
"""

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
    ])

    llm = ChatOpenAI(
        model=settings.llm_model,
        temperature=settings.llm_temperature,
        api_key=settings.openai_api_key
    )

    chain = prompt | llm

    # Format inputs for the prompt
    import json
    chain_input = {
        "request_json": json.dumps(req.model_dump(), default=str),
        "factors_json": json.dumps(factor_summaries, indent=2),
        "adjustment": final_adjustment,
        "goodness": goodness,
        "guardrails": str(guardrail_flags) if guardrail_flags else "None"
    }

    try:
        # Invoke LLM - Single call!
        result_msg = await chain.ainvoke(chain_input)
        output_text = result_msg.content
        
        # Parse the output (Reuse existing regex logic or similar)
        factor_reasoning = parse_llm_reasoning(output_text)
        overall_reasoning = extract_overall_reasoning(output_text)

    except Exception as e:
        logger.error(f"LLM generation failed: {e}", exc_info=True)
        # Fallback if LLM fails
        factor_reasoning = FactorReasoning()
        overall_reasoning = "Automated calculation (LLM unavailable). " + \
                            f"Adjustment: {final_adjustment:.2f}, Goodness: {goodness:.2f}"

    # --- STEP 3: Return Response ---
    
    # Send alert (non-blocking)
    await send_pricing_alert(
        req=req,
        adjustment=round(final_adjustment, 2),
        goodness=round(goodness, 2),
        flags=guardrail_flags
    )

    return RecommendationResponse(
        recommended_adjustment=round(final_adjustment, 2),
        goodness=round(goodness, 2),
        factors=factor_summaries,
        overall_reasoning=overall_reasoning,
        factor_reasoning=factor_reasoning
    )

# --- Helpers for Parsing ---

def parse_llm_reasoning(text: str) -> FactorReasoning:
    """Extracts structured reasoning from LLM output text."""
    reasoning = {}
    markers = {
        "ENVIRONMENT_REASONING": "environment",
        "SUPPLY_DEMAND_REASONING": "supply_demand",
        "LOYALTY_REASONING": "loyalty",
        "HISTORICAL_REASONING": "historical",
        "CORPORATE_PRESSURE_REASONING": "corporate_pressure"
    }
    
    for marker, key in markers.items():
        # Regex to capture text between this marker and the next marker (or end of string)
        # format: MARKER: ... text ... (next marker or end)
        pattern = re.compile(f"{marker}:(.*?)(?=(?:[A-Z_]+_REASONING:)|$)", re.DOTALL)
        match = pattern.search(text)
        if match:
            reasoning[key] = match.group(1).strip()
            
    return FactorReasoning(**reasoning)

def extract_overall_reasoning(text: str) -> str:
    """Extracts the overall reasoning section."""
    pattern = re.compile(r"OVERALL_REASONING:(.*)", re.DOTALL)
    match = pattern.search(text)
    if match:
        return match.group(1).strip()
    return text[:200] # Fallback if format broke
