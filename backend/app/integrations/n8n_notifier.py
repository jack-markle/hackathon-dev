"""
N8N webhook integration for alerting.
"""
from typing import List, Optional
import httpx
from datetime import datetime
from app.core.config import settings
from app.models.recommendation import RecommendationRequest

async def send_pricing_alert(
    req: RecommendationRequest,
    adjustment: float,
    goodness: float,
    flags: List[str]
) -> bool:
    """
    Send a pricing alert to n8n webhook with full context.
    
    Args:
        req: The original recommendation request with all context
        adjustment: Recommended price adjustment
        goodness: Goodness score
        flags: List of guardrail flags
    
    Returns:
        bool: True if alert sent successfully (or disabled), False on failure
    """
    if not settings.n8n_webhook_enabled or not settings.n8n_webhook_url:
        return True
    
    # Ensure flags is always a list/array, never a string or other type
    if not isinstance(flags, list):
        if isinstance(flags, str):
            # If flags is a string, convert to list (split by delimiter if needed)
            flags = [flags] if flags else []
        else:
            # For any other type, convert to empty list
            flags = []
    
    # Ensure all items in flags are strings
    flags = [str(flag) for flag in flags if flag]
    
    payload = {
        "origin_zone": req.origin_zone,
        "destination_zone": req.destination_zone,
        "recommended_adjustment": adjustment,
        "goodness": goodness,
        "flags": flags,  # Always a list of strings
        "scenarios": req.scenarios if isinstance(req.scenarios, list) else [req.scenarios] if req.scenarios else [],
        "scenario": req.scenario,
        "time": req.time,
        "loyalty_segment": req.loyalty_segment,
        "notes": req.notes,
        "corporate_revenue_goal": req.corporate_revenue_goal,
        "corporate_strategy_notes": req.corporate_strategy_notes
    }
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(settings.n8n_webhook_url, json=payload, timeout=5.0)
            if response.status_code == 200:
                return True
            else:
                print(f"[N8N] Error sending alert: Status {response.status_code}")
                return False
    except Exception as e:
        print(f"[N8N] Exception sending alert: {e}")
        return False
