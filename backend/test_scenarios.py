"""
Test scenarios for pricing recommendation system.

This file contains predefined scenarios for testing and demo purposes.
Dev 1 implementation - validates factor computation and guardrails.
"""
import asyncio
from app.models.recommendation import RecommendationRequest
from app.services.recommendation_service import build_recommendation


# ===== TEST SCENARIOS =====

SCENARIOS = {
    "emergency_no_surge": {
        "description": "Emergency situation should result in zero surge",
        "request": RecommendationRequest(
            origin_zone="downtown",
            destination_zone="downtown",
            scenarios=["emergency"],
            scenario="emergency",
            time="2025-12-01T14:00:00Z",
            loyalty_segment="standard",
            corporate_revenue_goal=0.20  # Even with high corporate pressure
        ),
        "expected": {
            "adjustment_range": (0.0, 0.0),
            "goodness_min": 0.80,
            "guardrails": True
        }
    },
    
    "concert_platinum_loyalty": {
        "description": "Concert event with platinum member - loyalty softens surge",
        "request": RecommendationRequest(
            origin_zone="downtown",
            destination_zone="stadium",
            scenarios=["concert"],
            scenario="concert",
            time="2025-12-01T20:00:00Z",
            loyalty_segment="platinum",
            corporate_revenue_goal=0.15
        ),
        "expected": {
            "adjustment_range": (0.10, 0.25),
            "goodness_min": 0.70,
            "guardrails": False
        }
    },
    
    "storm_gold_morning_rush": {
        "description": "Storm during morning rush at airport with gold member",
        "request": RecommendationRequest(
            origin_zone="downtown",
            destination_zone="airport_corridor",
            scenarios=["storm"],
            scenario="storm",
            time="2025-12-02T07:30:00Z",
            loyalty_segment="gold",
            corporate_revenue_goal=0.10
        ),
        "expected": {
            "adjustment_range": (0.15, 0.30),
            "goodness_min": 0.65,
            "guardrails": False
        }
    },
    
    "road_closure_evening": {
        "description": "Road closure during evening commute",
        "request": RecommendationRequest(
            origin_zone="downtown",
            destination_zone="airport_corridor",
            scenarios=["road_closure"],
            scenario="road_closure",
            time="2025-12-01T18:00:00Z",
            loyalty_segment="gold",
            notes="partial freeway closure",
            corporate_revenue_goal=0.15,
            corporate_strategy_notes="End-of-quarter revenue push"
        ),
        "expected": {
            "adjustment_range": (0.08, 0.20),
            "goodness_min": 0.70,
            "guardrails": False
        }
    },
    
    "weekend_night_downtown": {
        "description": "Weekend night entertainment demand",
        "request": RecommendationRequest(
            origin_zone="suburbs",
            destination_zone="downtown",
            scenarios=["normal"],
            scenario="normal",
            time="2025-12-06T22:00:00Z",  # Saturday night
            loyalty_segment="silver"
        ),
        "expected": {
            "adjustment_range": (0.12, 0.22),
            "goodness_min": 0.75,
            "guardrails": False
        }
    },
    
    "off_peak_suburban": {
        "description": "Off-peak suburban area - minimal adjustment",
        "request": RecommendationRequest(
            origin_zone="suburbs",
            destination_zone="suburbs",
            scenarios=["normal"],
            scenario="normal",
            time="2025-12-02T14:00:00Z",
            loyalty_segment="standard"
        ),
        "expected": {
            "adjustment_range": (0.0, 0.05),
            "goodness_min": 0.80,
            "guardrails": False
        }
    },
    
    "high_corporate_pressure_no_market": {
        "description": "High corporate pressure without market justification - should flag tension",
        "request": RecommendationRequest(
            origin_zone="suburbs",
            destination_zone="suburbs",
            scenarios=["normal"],
            scenario="normal",
            time="2025-12-02T14:00:00Z",
            loyalty_segment="standard",
            corporate_revenue_goal=0.25,  # Very high goal
            corporate_strategy_notes="Aggressive revenue targets for Q4"
        ),
        "expected": {
            "adjustment_range": (0.05, 0.12),
            "goodness_max": 0.70,  # Lower goodness due to tension
            "guardrails": False
        }
    },
    
    "holiday_airport": {
        "description": "Holiday travel at airport",
        "request": RecommendationRequest(
            origin_zone="downtown",
            destination_zone="airport_corridor",
            scenarios=["holiday"],
            scenario="holiday",
            time="2025-12-25T16:00:00Z",
            loyalty_segment="gold"
        ),
        "expected": {
            "adjustment_range": (0.08, 0.18),
            "goodness_min": 0.75,
            "guardrails": False
        }
    }
}


def run_scenario(scenario_name: str, scenario_data: dict) -> dict:
    """Run a single test scenario and return results"""
    print(f"\n{'='*80}")
    print(f"SCENARIO: {scenario_name}")
    print(f"Description: {scenario_data['description']}")
    print(f"{'='*80}")
    
    request = scenario_data["request"]
    expected = scenario_data["expected"]
    
    # Generate recommendation
    result = build_recommendation(request)
    
    # Display request details
    print(f"\nRequest Details:")
    print(f"  Origin Zone: {request.origin_zone}")
    print(f"  Destination Zone: {request.destination_zone}")
    print(f"  Scenarios: {request.scenarios}")
    print(f"  Primary Scenario: {request.scenario}")
    print(f"  Time: {request.time}")
    print(f"  Loyalty: {request.loyalty_segment or 'standard'}")
    if request.corporate_revenue_goal:
        print(f"  Corporate Goal: {request.corporate_revenue_goal*100:.0f}%")
    
    # Display results
    print(f"\nResults:")
    print(f"  Recommended Adjustment: {result.recommended_adjustment*100:+.1f}%")
    print(f"  Goodness Score: {result.goodness:.2f}")
    print(f"\n  Factor Breakdown:")
    for factor_name, factor_summary in result.factors.items():
        print(f"    • {factor_name}: {factor_summary}")
    
    # Validate expectations
    print(f"\nValidation:")
    passed_checks = []
    failed_checks = []
    
    # Check adjustment range
    adj_min, adj_max = expected.get("adjustment_range", (0, 1))
    if adj_min <= result.recommended_adjustment <= adj_max:
        passed_checks.append(f"✓ Adjustment in range [{adj_min}, {adj_max}]")
    else:
        failed_checks.append(f"✗ Adjustment {result.recommended_adjustment} NOT in range [{adj_min}, {adj_max}]")
    
    # Check goodness minimum
    if "goodness_min" in expected:
        if result.goodness >= expected["goodness_min"]:
            passed_checks.append(f"✓ Goodness >= {expected['goodness_min']}")
        else:
            failed_checks.append(f"✗ Goodness {result.goodness} < {expected['goodness_min']}")
    
    # Check goodness maximum
    if "goodness_max" in expected:
        if result.goodness <= expected["goodness_max"]:
            passed_checks.append(f"✓ Goodness <= {expected['goodness_max']}")
        else:
            failed_checks.append(f"✗ Goodness {result.goodness} > {expected['goodness_max']}")
    
    # Check guardrails
    has_guardrails = "guardrails" in result.factors
    if expected.get("guardrails", False):
        if has_guardrails:
            passed_checks.append("✓ Guardrails applied as expected")
        else:
            failed_checks.append("✗ Expected guardrails but none applied")
    
    for check in passed_checks:
        print(f"  {check}")
    for check in failed_checks:
        print(f"  {check}")
    
    success = len(failed_checks) == 0
    status = "PASSED ✓" if success else "FAILED ✗"
    print(f"\nStatus: {status}")
    
    return {
        "scenario": scenario_name,
        "passed": success,
        "result": result,
        "failed_checks": failed_checks
    }


def run_all_scenarios():
    """Run all test scenarios"""
    print("\n" + "="*80)
    print("RUNNING ALL TEST SCENARIOS")
    print("="*80)
    
    results = []
    for scenario_name, scenario_data in SCENARIOS.items():
        result = run_scenario(scenario_name, scenario_data)
        results.append(result)
    
    # Summary
    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    
    passed = sum(1 for r in results if r["passed"])
    total = len(results)
    
    print(f"\nTotal Scenarios: {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {total - passed}")
    print(f"Success Rate: {passed/total*100:.1f}%")
    
    if passed < total:
        print("\nFailed Scenarios:")
        for r in results:
            if not r["passed"]:
                print(f"\n  {r['scenario']}:")
                for check in r["failed_checks"]:
                    print(f"    {check}")
    else:
        print("\n🎉 All scenarios passed!")
    
    return results


if __name__ == "__main__":
    # Run all scenarios
    run_all_scenarios()

