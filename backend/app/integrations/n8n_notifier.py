"""
N8N webhook integration for alerting.
"""
from typing import List, Optional
import httpx
import logging
from datetime import datetime
from app.core.config import settings
from app.models.recommendation import RecommendationRequest

logger = logging.getLogger(__name__)

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
        logger.debug("N8N webhook disabled or URL not configured - skipping alert")
        return True
    
    # Check if this would trigger n8n workflow (goodness < 0.7 OR flags present)
    will_trigger = goodness < 0.7 or len(flags) > 0
    trigger_reason = []
    if goodness < 0.7:
        trigger_reason.append(f"goodness={goodness:.2f} < 0.7")
    if len(flags) > 0:
        trigger_reason.append(f"{len(flags)} flag(s) present")
    
    logger.info(
        f"[N8N] Triggering webhook alert - Route: {req.origin_zone} → {req.destination_zone} | "
        f"Goodness: {goodness:.2f} | Flags: {len(flags)} | "
        f"Will trigger workflow: {will_trigger} ({', '.join(trigger_reason) if trigger_reason else 'N/A'})"
    )
    
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
        "corporate_strategy_notes": req.corporate_strategy_notes,
        "email_address": settings.n8n_alert_email
    }
    
    try:
        async with httpx.AsyncClient() as client:
            logger.debug(f"[N8N] Sending POST request to {settings.n8n_webhook_url}")
            response = await client.post(settings.n8n_webhook_url, json=payload, timeout=5.0)
            if response.status_code == 200:
                logger.info(f"[N8N] ✅ Alert sent successfully - Status: {response.status_code}")
                return True
            else:
                logger.warning(f"[N8N] ❌ Error sending alert: Status {response.status_code}")
                return False
    except Exception as e:
        logger.error(f"[N8N] ❌ Exception sending alert: {e}", exc_info=True)
        return False
