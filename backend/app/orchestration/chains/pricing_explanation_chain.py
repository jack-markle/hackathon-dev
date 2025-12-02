"""
LangChain-based pricing explanation chain.

Responsibility: Generate natural language reasoning for pricing recommendations.
"""
from typing import Any, Dict
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.language_models import BaseChatModel

async def generate_explanation(
    llm: BaseChatModel,
    request: Dict[str, Any],
    factors: Dict[str, str],
    adjustment: float,
    goodness: float
) -> str:
    """
    Generate a natural language explanation for the pricing recommendation.
    
    Args:
        llm: The Language Model to use
        request: Original request context (zone, scenario, time, etc.)
        factors: Dictionary of factor summaries
        adjustment: Recommended adjustment value (float)
        goodness: Goodness score (float)
    
    Returns:
        Natural language explanation string
    """
    
    # SYSTEM PROMPT
    system_template = """You are a Pricing Advisor for a ride-hailing platform.
Your goal is to explain a pricing recommendation to a Business Analyst.
Your tone should be professional, objective, and clear.

You must consider the following inputs:
1. Environmental conditions (weather, events)
2. Supply and Demand (time of day, driver availability)
3. Customer Loyalty (tiers)
4. Historical Patterns
5. Corporate Strategy (revenue goals)

CRITICAL RULES:
- Market physics (supply/demand) and Safety/Ethics (emergencies) are HARD constraints.
- Corporate Strategy is a SOFT influence. It nudges price but cannot override safety or ethics.
- If Corporate Pressure is high but Guardrails block it, explicitly mention this tension.
- If Goodness Score is low (< 0.6), explain why the recommendation is suboptimal (e.g., conflict between goals).
- Be concise (3-6 sentences).
"""

    # HUMAN PROMPT
    human_template = """Please explain this pricing recommendation:

CONTEXT:
Zone: {zone}
Scenario: {scenario}
Time: {time}
Loyalty Tier: {loyalty}

FACTOR ANALYSIS:
- Environment: {env_summary}
- Supply/Demand: {sd_summary}
- Loyalty: {loyalty_summary}
- Historical: {hist_summary}
- Corporate Pressure: {corp_summary}
{guardrails_info}

OUTCOME:
Recommended Adjustment: {adj_percent}%
Goodness Score: {goodness}/1.0

Explain the reasoning, highlighting the key drivers and any trade-offs.
"""

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_template),
        ("human", human_template),
    ])

    # Prepare input variables
    guardrails_text = ""
    if "guardrails" in factors:
        guardrails_text = f"- GUARDRAILS ACTIVE: {factors['guardrails']}"

    input_vars = {
        "zone": request.get("zone", "Unknown"),
        "scenario": request.get("scenario", "Unknown"),
        "time": request.get("time", "Unknown"),
        "loyalty": request.get("loyalty_segment") or "Standard",
        "env_summary": factors.get("environment", "N/A"),
        "sd_summary": factors.get("supply_demand", "N/A"),
        "loyalty_summary": factors.get("loyalty", "N/A"),
        "hist_summary": factors.get("historical", "N/A"),
        "corp_summary": factors.get("corporate_pressure", "N/A"),
        "guardrails_info": guardrails_text,
        "adj_percent": f"{adjustment * 100:+.0f}",
        "goodness": f"{goodness:.2f}"
    }

    # Direct invocation (No Pipe | Operator)
    messages = prompt.format_messages(**input_vars)
    response = await llm.ainvoke(messages)
    return StrOutputParser().invoke(response)
