

Based on the code analysis, a confidence (goodness) score below 0.80 (80%) occurs when there is a **mismatch between corporate goals and market reality**, or when **severe guardrails** are triggered due to ethical conflicts.

Here is a specific user input combination that will likely trigger a score around **0.65 (65%)**:

### The "Corporate Greed in a Calm Market" Scenario

*   **`corporate_revenue_goal`**: `0.20` (High: 20% revenue uplift goal)
*   **`scenario`**: `"normal"` (No weather/event justification)
*   **`time`**: `"2024-01-15T10:00:00Z"` (Off-peak: Mon 10 AM)
*   **`origin_zone`**: `"suburbs"` (Low historical demand)

#### Why this scores low:
1.  **Base Score**: Starts at `0.80`.
2.  **Penalty Triggered**: The code checks `if corp_factor > 0.05 and market_support < 0.05`.
    *   Your corporate goal (0.20) results in a high pressure factor (capped at 0.08).
    *   The market support (Environment + Supply/Demand) is `0.0` because it's a normal day at off-peak hours.
    *   **Result**: `-0.15` penalty for "Corporate pushing without market justification".
3.  **Final Calculation**: `0.80 - 0.15 = 0.65`.

This combination effectively asks the system to "Jack up prices by 20% just because we want more money," which the system flags as a low-confidence/low-goodness decision.