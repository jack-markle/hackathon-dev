"""
Test script for N8N webhook alert functionality.

This script tests the send_pricing_alert function without modifying any existing code.
It creates a sample recommendation request and sends it to the configured n8n webhook.

Usage:
    python test_n8n_alert.py
"""
import asyncio
from datetime import datetime
from app.models.recommendation import RecommendationRequest
from app.integrations.n8n_notifier import send_pricing_alert
from app.core.config import settings


async def test_n8n_alert():
    """Test the n8n webhook alert functionality."""
    print("=" * 60)
    print("N8N Webhook Alert Test")
    print("=" * 60)
    print()
    
    # Check configuration
    print("Configuration Check:")
    print(f"  N8N Webhook Enabled: {settings.n8n_webhook_enabled}")
    print(f"  N8N Webhook URL: {settings.n8n_webhook_url}")
    print(f"  N8N Alert Email: {settings.n8n_alert_email}")
    print()
    
    if not settings.n8n_webhook_enabled or not settings.n8n_webhook_url:
        print("⚠️  WARNING: N8N webhook is not enabled or URL is not set.")
        print("   The test will return True (success) but no webhook will be sent.")
        print("   To enable, set N8N_WEBHOOK_ENABLED=true and N8N_WEBHOOK_URL in .env")
        print()
    
    # Create a sample recommendation request matching the n8n_payload.json structure
    test_request = RecommendationRequest(
        origin_zone="stadium_district",
        destination_zone="downtown",
        scenarios=["storm", "normal_day", "road_closure", "concert"],
        scenario="storm",
        time=datetime.utcnow().isoformat() + "Z",
        loyalty_segment="silver",
        notes="Storm expected to reduce driver availability by 80%.",
        corporate_revenue_goal=0.5,
        corporate_strategy_notes="Make tons of money, all of it"
    )
    
    # Test parameters
    test_adjustment = 0.18
    test_goodness = 0.82
    test_flags = [
        "LOYALTY_GUARDRAIL: Surge capped at 18% for silver members.",
        "TENSION: Corporate revenue goals conflict with fair-pricing during disruption."
    ]
    
    print("Test Request Details:")
    print(f"  Origin Zone: {test_request.origin_zone}")
    print(f"  Destination Zone: {test_request.destination_zone}")
    print(f"  Scenario: {test_request.scenario}")
    print(f"  Scenarios: {test_request.scenarios}")
    print(f"  Loyalty Segment: {test_request.loyalty_segment}")
    print(f"  Corporate Revenue Goal: {test_request.corporate_revenue_goal}")
    print(f"  Notes: {test_request.notes}")
    print()
    
    print("Test Parameters:")
    print(f"  Recommended Adjustment: {test_adjustment}")
    print(f"  Goodness Score: {test_goodness}")
    print(f"  Flags: {len(test_flags)} flag(s)")
    for i, flag in enumerate(test_flags, 1):
        print(f"    {i}. {flag}")
    print()
    
    # Send the alert
    print("Sending alert to n8n webhook...")
    try:
        result = await send_pricing_alert(
            req=test_request,
            adjustment=test_adjustment,
            goodness=test_goodness,
            flags=test_flags
        )
        
        if result:
            print("✅ SUCCESS: Alert sent successfully (or webhook disabled)")
        else:
            print("❌ FAILURE: Alert failed to send")
    except Exception as e:
        print(f"❌ ERROR: Exception occurred: {e}")
        import traceback
        traceback.print_exc()
    
    print()
    print("=" * 60)
    print("Test Complete")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(test_n8n_alert())

