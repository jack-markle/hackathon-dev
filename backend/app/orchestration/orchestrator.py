"""
Main orchestrator for pricing recommendations.
Integrates conceptual agents and LangChain reasoning.
"""
import json
import re
import logging
from typing import Dict, Any
from app.models.recommendation import RecommendationRequest, RecommendationResponse, FactorReasoning
from app.core.config import settings
from app.orchestration.orchestrator_agent import build_orchestrator_agent
from app.integrations.n8n_notifier import send_pricing_alert

async def orchestrate_pricing_recommendation(
    req: RecommendationRequest,
) -> RecommendationResponse:
    """
    High-level orchestration for pricing recommendation using LangChain Agent.
    
    1. Initializes the Orchestrator Agent.
    2. Invokes the agent with the request details.
    3. Extracts structured data (factors, adjustment, goodness) from tool outputs.
    4. Uses the agent's final text response as the reasoning.
    5. Returns complete response.
    """
    # 1. Initialize Agent
    agent_executor = build_orchestrator_agent(
        model_name=settings.llm_model,
        temperature=settings.llm_temperature,
        api_key=settings.openai_api_key
    )

    # 2. Invoke Agent
    # We pass the request as a JSON string in the input
    req_dict = req.model_dump()
    # Ensure datetime is serializable
    input_text = f"Please generate a pricing recommendation for this request: {json.dumps(req_dict, default=str)}"
    
    try:
        result = await agent_executor.ainvoke({"input": input_text})
    except Exception as e:
        # Log error for debugging
        logger = logging.getLogger(__name__)
        logger.error(f"Agent execution failed: {e}", exc_info=True)
        
        # Return a fallback response with basic factor calculations
        # This ensures the API doesn't crash during demo
        from app.services.recommendation_service import build_recommendation
        fallback_response = build_recommendation(req)
        fallback_response.overall_reasoning = (
            f"AI reasoning temporarily unavailable. "
            f"Recommendation based on factor analysis: {fallback_response.overall_reasoning}"
        )
        
        # Attempt to send alert even in fallback mode
        try:
            flags = []
            if "guardrails" in fallback_response.factors:
                flags = fallback_response.factors["guardrails"].split(" | ")
            
            await send_pricing_alert(
                req=req,
                adjustment=fallback_response.recommended_adjustment,
                goodness=fallback_response.goodness,
                flags=flags
            )
        except Exception:
            pass # Don't let alert failure block response
            
        return fallback_response
    
    # 3. Extract data from intermediate steps
    # AgentExecutor returns intermediate_steps as a list of (AgentAction, observation) tuples
    intermediate_steps = result.get("intermediate_steps", [])
    
    # Containers for extracted data
    factor_summaries = {}
    factor_reasoning = {}  # Agent's reasoning about each factor
    final_adjustment = 0.0
    goodness = 0.0
    guardrail_flags = []
    
    tool_map = {
        "environment_tool": "environment",
        "supply_demand_tool": "supply_demand",
        "loyalty_tool": "loyalty",
        "historical_tool": "historical",
        "corporate_pressure_tool": "corporate_pressure"
    }
    
    # Extract messages to find reasoning between tool calls
    messages = result.get("messages", [])
    current_tool = None
    
    for action, observation in intermediate_steps:
        # Extract tool name from AgentAction
        tool_name = action.tool if hasattr(action, 'tool') else str(action)
        
        # Parse observation if it's a string (JSON)
        if isinstance(observation, str):
            try:
                observation = json.loads(observation)
            except:
                pass
        
        # Extract factor summaries from tool outputs
        if tool_name in tool_map:
            key = tool_map[tool_name]
            current_tool = key
            if isinstance(observation, dict) and "summary" in observation:
                factor_summaries[key] = observation["summary"]
        
        # Extract calculation results
        if tool_name == "calculate_pricing_outcome_tool":
            if isinstance(observation, dict):
                final_adjustment = observation.get("final_adjustment", 0.0)
                goodness = observation.get("goodness", 0.0)
                guardrail_flags = observation.get("guardrail_flags", [])
    
    # Extract reasoning summaries from agent messages
    # Look for structured reasoning markers in messages
    reasoning_markers = {
        "ENVIRONMENT_REASONING": "environment",
        "SUPPLY_DEMAND_REASONING": "supply_demand",
        "LOYALTY_REASONING": "loyalty",
        "HISTORICAL_REASONING": "historical",
        "CORPORATE_PRESSURE_REASONING": "corporate_pressure"
    }
    
    # Helper function to extract reasoning from text
    def extract_reasoning_from_text(text: str, markers: dict, existing_reasoning: dict) -> dict:
        """Extract factor reasoning from text using markers."""
        # Check for each marker (case-insensitive)
        for marker, key in markers.items():
            if key in existing_reasoning:
                continue  # Already extracted
            
            # Try both uppercase and original case
            marker_variants = [marker, marker.upper(), marker.lower()]
            for marker_variant in marker_variants:
                if marker_variant + ":" in text.upper():
                    # Find the marker in the text (case-insensitive)
                    pattern = re.compile(re.escape(marker_variant) + ":", re.IGNORECASE)
                    match = pattern.search(text)
                    if match:
                        # Extract text after the marker
                        start_pos = match.end()
                        reasoning_text = text[start_pos:].strip()
                        
                        # Find the next marker or end of text
                        next_marker_pos = len(reasoning_text)
                        for other_marker, _ in markers.items():
                            if other_marker != marker:
                                other_pattern = re.compile(re.escape(other_marker) + ":", re.IGNORECASE)
                                other_match = other_pattern.search(reasoning_text)
                                if other_match and other_match.start() < next_marker_pos:
                                    next_marker_pos = other_match.start()
                        
                        # Also check for OVERALL_REASONING marker
                        overall_match = re.compile(r"OVERALL_REASONING:", re.IGNORECASE).search(reasoning_text)
                        if overall_match and overall_match.start() < next_marker_pos:
                            next_marker_pos = overall_match.start()
                        
                        reasoning_text = reasoning_text[:next_marker_pos].strip()
                        
                        # Clean up - take first 2 sentences or 300 chars
                        sentences = re.split(r'[.!?]+', reasoning_text)
                        if len(sentences) > 2:
                            reasoning_text = ". ".join(sentences[:2]).strip()
                            if reasoning_text and not reasoning_text.endswith('.'):
                                reasoning_text += "."
                        else:
                            reasoning_text = reasoning_text[:300].strip()
                        
                        if reasoning_text and len(reasoning_text) > 10:
                            existing_reasoning[key] = reasoning_text
                            break  # Found it, move to next marker
        return existing_reasoning
    
    # First, try to extract from individual messages
    last_tool_key = None
    for i, msg in enumerate(messages):
        if not hasattr(msg, 'content') or not msg.content:
            continue
        
        content = msg.content if isinstance(msg.content, str) else str(msg.content)
        if not content or len(content) < 10:  # Skip empty or very short content
            continue

        # Look for structured reasoning markers
        factor_reasoning = extract_reasoning_from_text(content, reasoning_markers, factor_reasoning)
    
    # Also check the final output string for reasoning markers (they might be there)
    output_text = result.get("output", "")
    if output_text:
        factor_reasoning = extract_reasoning_from_text(output_text, reasoning_markers, factor_reasoning)
    
    # If we didn't get individual reasoning, try to parse from the overall reasoning
    # Look for factor mentions in the overall reasoning
    if not any(factor_reasoning.values()):
        overall_reasoning_text = result.get("output", "")
        if overall_reasoning_text:
            # Extract text after "REASONING:" if present
            if "REASONING:" in overall_reasoning_text.upper():
                parts = overall_reasoning_text.split("REASONING:", 1)
                if len(parts) > 1:
                    reasoning_section = parts[1]
                    # Remove "OVERALL_REASONING:" if present
                    if "OVERALL_REASONING:" in reasoning_section.upper():
                        reasoning_section = reasoning_section.upper().split("OVERALL_REASONING:", 1)[-1]
                    overall_reasoning_text = reasoning_section
            
            # Try to extract factor-specific reasoning from the combined text
            # Look for explicit factor mentions
            factor_patterns = {
                "environment": [r"environmental factor", r"environment", r"weather", r"storm.*adjustment"],
                "supply_demand": [r"supply.*demand", r"supply-demand", r"driver availability", r"off-peak"],
                "loyalty": [r"loyalty factor", r"loyalty", r"gold member", r"platinum", r"discount"],
                "historical": [r"historical data", r"historical", r"similar.*events", r"typically"],
                "corporate_pressure": [r"corporate pressure", r"corporate", r"revenue.*q4", r"revenue goals"]
            }
            
            # Split by sentences
            sentences = re.split(r'[.!?]+', overall_reasoning_text)
            
            for sentence in sentences:
                sentence = sentence.strip()
                if not sentence or len(sentence) < 10:
                    continue
                    
                sentence_upper = sentence.upper()
                for factor_key, patterns in factor_patterns.items():
                    if factor_key not in factor_reasoning:
                        for pattern in patterns:
                            if re.search(pattern, sentence_upper, re.IGNORECASE):
                                # Found a sentence related to this factor
                                if len(sentence) > 15 and len(sentence) < 300:
                                    factor_reasoning[factor_key] = sentence.strip()
                                    break
                        if factor_key in factor_reasoning:
                            break

    # Add guardrails to summaries if present
    if guardrail_flags:
        factor_summaries["guardrails"] = " | ".join(guardrail_flags)

    # 4. Get Overall Reasoning from output
    overall_reasoning = result.get("output", "No reasoning generated.")
    
    # Clean up overall reasoning - remove individual factor reasoning markers if present
    if "OVERALL_REASONING:" in overall_reasoning.upper():
        parts = overall_reasoning.upper().split("OVERALL_REASONING:", 1)
        if len(parts) > 1:
            overall_reasoning = parts[1].strip()
    
    # Remove individual reasoning markers from overall reasoning
    for marker in ["ENVIRONMENT_REASONING", "SUPPLY_DEMAND_REASONING", "LOYALTY_REASONING", 
                   "HISTORICAL_REASONING", "CORPORATE_PRESSURE_REASONING", "REASONING:"]:
        if marker in overall_reasoning.upper():
            # Remove everything before the last occurrence of OVERALL_REASONING or keep everything after REASONING:
            if marker == "REASONING:" and "OVERALL_REASONING" not in overall_reasoning.upper():
                # If it's just "REASONING:", take everything after it
                parts = overall_reasoning.upper().split("REASONING:", 1)
                if len(parts) > 1:
                    overall_reasoning = parts[1].strip()
            else:
                # Remove the marker and everything before it if OVERALL_REASONING exists
                if "OVERALL_REASONING:" in overall_reasoning.upper():
                    overall_reasoning = overall_reasoning.upper().split("OVERALL_REASONING:", 1)[1].strip()
    
    # 5. Create structured factor reasoning object
    factor_reasoning_obj = FactorReasoning(
        environment=factor_reasoning.get("environment"),
        supply_demand=factor_reasoning.get("supply_demand"),
        loyalty=factor_reasoning.get("loyalty"),
        historical=factor_reasoning.get("historical"),
        corporate_pressure=factor_reasoning.get("corporate_pressure")
    )

    # 6. Return complete response
    # Send alert to n8n (fire and forget / non-blocking ideally, but await here is fine for now)
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
        factor_reasoning=factor_reasoning_obj
    )
