# UI Test Checklist for Dev-3

Manual testing checklist for the frontend pricing recommendation interface. Each item should be tested and marked as Pass/Fail.

## Test Environment Setup

- [ ] Backend API is running on `http://localhost:8000`
- [ ] Frontend is accessible and loads without errors
- [ ] Browser console shows no critical errors

---

## 1. Required Fields Validation

### 1.1 Zone Field
- [ ] Zone dropdown is present and functional
- [ ] All zones are available: `downtown`, `airport_corridor`, `stadium`, `suburbs`, `venue`
- [ ] Zone selection is required (form cannot submit without selection)
- [ ] Error message appears if zone is not selected when submitting

**Expected Behavior:** Zone must be selected before form submission

### 1.2 Scenario Field
- [ ] Scenario dropdown is present and functional
- [ ] All scenarios are available: `normal`, `storm`, `road_closure`, `concert`, `holiday`, `emergency`
- [ ] Scenario selection is required (form cannot submit without selection)
- [ ] Error message appears if scenario is not selected when submitting

**Expected Behavior:** Scenario must be selected before form submission

### 1.3 Time Field
- [ ] Time input field is present (datetime picker or text input)
- [ ] Time field accepts ISO 8601 format: `2025-12-01T18:00:00Z`
- [ ] Time selection is required (form cannot submit without value)
- [ ] Error message appears if time is invalid or missing

**Expected Behavior:** Valid time must be provided before form submission

---

## 2. Optional Fields

### 2.1 Loyalty Segment
- [ ] Loyalty segment dropdown is present (optional field)
- [ ] Options available: `standard`, `silver`, `gold`, `platinum`
- [ ] Form can submit without loyalty segment (defaults to `standard`)
- [ ] Selected loyalty segment is included in API request

**Expected Behavior:** Loyalty segment is optional, defaults to `standard` if not provided

### 2.2 Notes Field
- [ ] Notes text area is present (optional field)
- [ ] Notes can be left empty
- [ ] Notes text is included in API request when provided

**Expected Behavior:** Notes are optional and included in request when provided

### 2.3 Corporate Revenue Goal
- [ ] Corporate revenue goal input is present (optional field)
- [ ] Input accepts decimal values (e.g., `0.15` for 15%)
- [ ] Input can be left empty
- [ ] Validation prevents negative values or values > 1.0
- [ ] Value is included in API request when provided

**Expected Behavior:** Corporate revenue goal is optional, validated if provided

### 2.4 Corporate Strategy Notes
- [ ] Corporate strategy notes text area is present (optional field)
- [ ] Notes can be left empty
- [ ] Notes text is included in API request when provided

**Expected Behavior:** Corporate strategy notes are optional

---

## 3. Loading States

### 3.1 Form Submission Loading
- [ ] Submit button shows loading state when API request is in progress
- [ ] Submit button is disabled during API request
- [ ] Loading indicator/spinner is visible during request
- [ ] Form fields are disabled during request (prevents double-submission)

**Expected Behavior:** Clear visual feedback during API call

### 3.2 Results Loading
- [ ] Results area shows loading state while waiting for API response
- [ ] Previous results are hidden or clearly marked as "loading"
- [ ] Loading state disappears when results arrive

**Expected Behavior:** User knows system is processing request

---

## 4. Error Handling

### 4.1 API Error Handling
- [ ] Network errors display user-friendly error message
- [ ] 500 server errors display appropriate error message
- [ ] 400 validation errors display field-specific error messages
- [ ] Error messages are clearly visible and actionable

**Expected Behavior:** Errors are handled gracefully with clear messaging

### 4.2 Form Validation Errors
- [ ] Invalid time format shows error message
- [ ] Invalid corporate revenue goal shows error message
- [ ] Missing required fields show error messages
- [ ] Error messages are displayed near relevant fields

**Expected Behavior:** Validation errors are clear and field-specific

---

## 5. Corporate Pressure UI

### 5.1 Corporate Fields Visibility
- [ ] Corporate revenue goal field is visible and accessible
- [ ] Corporate strategy notes field is visible and accessible
- [ ] Fields can be toggled or shown/hidden appropriately

**Expected Behavior:** Corporate pressure fields are accessible when needed

### 5.2 Corporate Pressure Impact Display
- [ ] Results show corporate pressure factor in factor breakdown
- [ ] Corporate pressure is clearly labeled in results
- [ ] High corporate pressure is visually distinct (if applicable)
- [ ] Corporate strategy notes appear in results (if provided)

**Expected Behavior:** Corporate pressure influence is transparent in results

### 5.3 Corporate Pressure Scenarios
- [ ] Test with high corporate goal (20%+) - verify it appears in factors
- [ ] Test with no corporate goal - verify factors don't show corporate pressure
- [ ] Test with moderate corporate goal (10-15%) - verify balanced display

**Expected Behavior:** Corporate pressure is accurately reflected in results

---

## 6. Empty States

### 6.1 Initial State
- [ ] Page loads with empty form (no pre-filled values)
- [ ] Results area is empty or shows placeholder message
- [ ] No errors shown on initial load

**Expected Behavior:** Clean initial state

### 6.2 After Clear/Reset
- [ ] Form can be cleared/reset to initial state
- [ ] Results are cleared when form is reset
- [ ] No stale data remains after reset

**Expected Behavior:** Form can be reset cleanly

---

## 7. Factor Display

### 7.1 Factor Breakdown
- [ ] All five factors are displayed: `environment`, `supply_demand`, `loyalty`, `historical`, `corporate_pressure`
- [ ] Each factor shows a clear label and description
- [ ] Factor descriptions match API response format
- [ ] Factors are visually organized (list, cards, or sections)

**Expected Behavior:** All factors are clearly displayed with descriptions

### 7.2 Factor Formatting
- [ ] Factor percentages are clearly formatted (e.g., "+5%", "-10%")
- [ ] Positive adjustments are visually distinct from negative
- [ ] Factor text is readable and not truncated
- [ ] Long factor descriptions wrap appropriately

**Expected Behavior:** Factors are easy to read and understand

### 7.3 Guardrails Display
- [ ] Guardrails are displayed when applied (e.g., emergency scenarios)
- [ ] Guardrail messages are clearly visible
- [ ] Guardrails are visually distinct from regular factors

**Expected Behavior:** Guardrails are prominently displayed when active

---

## 8. Explanation Rendering

### 8.1 Reasoning Display
- [ ] Reasoning/explanation text is displayed prominently
- [ ] Reasoning text is readable and well-formatted
- [ ] Long reasoning text wraps appropriately
- [ ] Reasoning matches API response

**Expected Behavior:** Explanation is clear and readable

### 8.2 Explanation Formatting
- [ ] Explanation uses appropriate typography (headings, paragraphs, lists)
- [ ] Key values (adjustment %, goodness) are emphasized
- [ ] Explanation is scannable and easy to read

**Expected Behavior:** Explanation is well-formatted and scannable

---

## 9. Recommended Adjustment Display

### 9.1 Adjustment Value
- [ ] Recommended adjustment percentage is prominently displayed
- [ ] Value is clearly formatted (e.g., "+12%" or "12% increase")
- [ ] Value matches API response `recommended_adjustment` field
- [ ] Large adjustments are visually distinct from small ones

**Expected Behavior:** Adjustment value is clear and prominent

### 9.2 Goodness Score
- [ ] Goodness score is displayed (e.g., "0.78" or "78/100")
- [ ] Goodness score is visually distinct from adjustment
- [ ] Score range is clear (0.0 to 1.0)
- [ ] High scores are visually distinct from low scores (optional: color coding)

**Expected Behavior:** Goodness score is clearly displayed

---

## 10. Demo Scenario Integration

### 10.1 Scenario Quick-Select
- [ ] Demo scenarios can be quickly loaded (if implemented)
- [ ] Pre-filled forms match demo scenario payloads
- [ ] Quick-select doesn't break form validation

**Expected Behavior:** Demo scenarios can be easily tested

### 10.2 Scenario Results Validation
- [ ] Results match expected ranges from `demo_scenarios.json`
- [ ] Factor breakdowns match expected factors
- [ ] Goodness scores fall within expected ranges

**Expected Behavior:** Demo scenarios produce expected results

---

## 11. Responsive Design (if applicable)

### 11.1 Mobile View
- [ ] Form is usable on mobile devices
- [ ] Results display appropriately on small screens
- [ ] Touch interactions work correctly

**Expected Behavior:** UI is functional on mobile devices

### 11.2 Tablet View
- [ ] Form layout adapts to tablet screen size
- [ ] Results are readable on tablet
- [ ] All interactions work correctly

**Expected Behavior:** UI is functional on tablets

---

## 12. Accessibility

### 12.1 Keyboard Navigation
- [ ] All form fields are keyboard accessible
- [ ] Submit button can be activated with keyboard
- [ ] Tab order is logical

**Expected Behavior:** UI is fully keyboard navigable

### 12.2 Screen Reader Support
- [ ] Form fields have appropriate labels
- [ ] Error messages are announced
- [ ] Results are announced appropriately

**Expected Behavior:** UI is accessible to screen readers

---

## Test Results Summary

**Tester Name:** ________________  
**Date:** ________________  
**Browser:** ________________  
**Backend Version:** ________________  

**Total Tests:** ___  
**Passed:** ___  
**Failed:** ___  

**Critical Issues:**
1. 
2. 
3. 

**Notes:**
_Add any additional observations or issues here_

