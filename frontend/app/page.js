'use client';

import { useState, useRef } from 'react';

const zones = {
  downtown: { label: 'Downtown Core', price: 18.50, icon: 'M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4' },
  airport_corridor: { label: 'Airport Corridor', price: 22.75, icon: 'M12 19l9 2-9-18-9 18 9-2zm0 0v-8' },
  suburbs: { label: 'Suburban Areas', price: 15.25, icon: 'M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6' },
  stadium_district: { label: 'Stadium District', price: 19.90, icon: 'M13 10V3L4 14h7v7l9-11h-7z' }
};

// Route-specific base pricing matrix (origin -> destination)
// Same-zone trips are shorter/local trips with lower pricing
const routePricing = {
  downtown: {
    downtown: 12.00,  // Same zone - short local trip
    airport_corridor: 24.50,  // Higher for airport trips from downtown
    suburbs: 16.75,
    stadium_district: 20.25
  },
  airport_corridor: {
    downtown: 26.00,  // Higher for downtown trips from airport
    airport_corridor: 15.00,  // Same zone - short local trip
    suburbs: 28.50,   // Long distance from airport
    stadium_district: 25.00
  },
  suburbs: {
    downtown: 17.50,
    airport_corridor: 29.00,  // Long distance to airport
    suburbs: 10.00,  // Same zone - short local trip
    stadium_district: 18.00
  },
  stadium_district: {
    downtown: 19.50,
    airport_corridor: 24.00,
    suburbs: 17.25,
    stadium_district: 13.00  // Same zone - short local trip
  }
};

const scenarios = {
  normal_day: { label: 'Normal Operations', description: 'Standard day with typical demand' },
  storm: { label: 'Severe Weather', description: 'Storm conditions reducing driver availability' },
  road_closure: { label: 'Road Closure', description: 'Major route disruption affecting traffic' },
  concert: { label: 'Major Event', description: 'Concert or sporting event driving demand' },
  holiday: { label: 'Holiday Period', description: 'Holiday affecting normal patterns' }
};

const adjustments = {
  storm: { adjustment: 0.25, goodness: 0.85 },
  concert: { adjustment: 0.18, goodness: 0.72 },
  road_closure: { adjustment: 0.15, goodness: 0.78 },
  holiday: { adjustment: 0.12, goodness: 0.91 },
  normal_day: { adjustment: 0.05, goodness: 0.94 }
};

const loyaltySegments = {
  gold: { label: 'Gold', description: 'Premium tier customers' },
  silver: { label: 'Silver', description: 'Regular tier customers' },
  bronze: { label: 'Bronze', description: 'Basic tier customers' }
};

export default function Home() {
  const [originZone, setOriginZone] = useState('downtown');
  const [currentZone, setCurrentZone] = useState('airport_corridor');
  const [selectedScenarios, setSelectedScenarios] = useState(['storm']);
  const [loyaltySegment, setLoyaltySegment] = useState('gold');
  const [revenueGoal, setRevenueGoal] = useState(3);
  const [strategyNotes, setStrategyNotes] = useState('Q4 revenue push');
  const [additionalContext, setAdditionalContext] = useState('Storm expected to reduce driver availability by 40%.');
  const [isLoading, setIsLoading] = useState(false);
  // New fields from gap analysis
  const [numberOfRiders, setNumberOfRiders] = useState('');
  const [numberOfDrivers, setNumberOfDrivers] = useState('');
  const [historicalCost, setHistoricalCost] = useState('');
  const [vehicleType, setVehicleType] = useState('');
  const [expectedDuration, setExpectedDuration] = useState('');
  
  // Use DOM refs to directly access input elements at submission time
  const revenueGoalInputRef = useRef(null);
  const strategyNotesInputRef = useRef(null);
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);
  const [showZoneHint, setShowZoneHint] = useState(false);
  const [showScenarioHint, setShowScenarioHint] = useState(false);
  const [showLoyaltyHint, setShowLoyaltyHint] = useState(false);
  const [showCorporateHint, setShowCorporateHint] = useState(false);
  const [showContextHint, setShowContextHint] = useState(false);
  const [showEmptyStateHint, setShowEmptyStateHint] = useState(false);

  // Calculate route-specific base price from pricing matrix
  const calculateRoutePrice = (origin, destination) => {
    if (routePricing[origin] && routePricing[origin][destination] !== undefined) {
      return routePricing[origin][destination];
    }
    // Fallback to average if route not found
    return (zones[origin].price + zones[destination].price) / 2;
  };

  const currentPrice = calculateRoutePrice(originZone, currentZone);

  const selectOriginZone = (zone) => {
    setOriginZone(zone);
  };

  const selectZone = (zone) => {
    setCurrentZone(zone);
  };

  const toggleScenario = (scenarioKey) => {
    setSelectedScenarios(prev => {
      if (prev.includes(scenarioKey)) {
        // Remove if already selected (but keep at least one)
        if (prev.length > 1) {
          return prev.filter(s => s !== scenarioKey);
        }
        return prev; // Keep at least one selected
      } else {
        // Add if not selected
        return [...prev, scenarioKey];
      }
    });
  };

  const generateRecommendation = async () => {
    // Read current values directly from DOM inputs first (before any state updates)
    // This ensures we get the latest values even if React state hasn't updated yet
    const currentRevenueGoal = revenueGoalInputRef.current ? Number(revenueGoalInputRef.current.value) || 0 : revenueGoal;
    const currentStrategyNotes = strategyNotesInputRef.current ? strategyNotesInputRef.current.value : strategyNotes;
    
    // Sync React state with DOM values to ensure form fields persist after submission
    // Use a small delay to avoid state update conflicts
    if (currentRevenueGoal !== revenueGoal) {
      setRevenueGoal(currentRevenueGoal);
    }
    if (currentStrategyNotes !== strategyNotes) {
      setStrategyNotes(currentStrategyNotes);
    }
    
    setIsLoading(true);
    setResults(null);
    setError(null);

    // Generate ISO 8601 timestamp
    const time = new Date().toISOString();

    // Build payload matching RecommendationRequest structure
    // Note: Backend may need to be updated to accept origin_zone, destination_zone, and scenarios array
    const payload = {
      origin_zone: originZone,
      destination_zone: currentZone,
      scenarios: selectedScenarios, // Array of selected scenarios
      scenario: selectedScenarios[0], // Keep for backward compatibility if backend still expects single scenario
      time: time,
      loyalty_segment: loyaltySegment,
      notes: additionalContext,
      corporate_revenue_goal: currentRevenueGoal / 100, // Convert percentage to decimal (3% -> 0.03)
      corporate_strategy_notes: currentStrategyNotes
    };
    
    // Add new optional fields if provided
    if (numberOfRiders !== '' && numberOfRiders !== null) {
      payload.number_of_riders = parseInt(numberOfRiders, 10);
    }
    if (numberOfDrivers !== '' && numberOfDrivers !== null) {
      payload.number_of_drivers = parseInt(numberOfDrivers, 10);
    }
    if (historicalCost !== '' && historicalCost !== null) {
      payload.historical_cost_of_ride = parseFloat(historicalCost);
    }
    if (vehicleType !== '' && vehicleType !== null) {
      payload.vehicle_type = vehicleType;
    }
    if (expectedDuration !== '' && expectedDuration !== null) {
      payload.expected_ride_duration = parseInt(expectedDuration, 10);
    }

    // Log payload for debugging
    console.log('Payload:', payload);

    try {
      // Call backend API
      const response = await fetch('http://localhost:8000/api/v1/recommendation', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({ detail: 'Failed to get recommendation' }));
        throw new Error(errorData.detail || errorData.message || `HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      
      // Map backend response to frontend state structure
      // Backend returns: recommended_adjustment, goodness, overall_reasoning, factors, factor_reasoning
      const adjustment = data.recommended_adjustment || 0;
      const goodness = data.goodness || 0;
      const newPrice = currentPrice * (1 + adjustment);

      // Calculate goodness label and colors based on goodness score
      let goodnessLabel, goodnessColor, circleColor;
      if (goodness >= 0.8) {
        goodnessLabel = 'Excellent';
        goodnessColor = 'text-cyan-600 bg-cyan-50 border border-cyan-200';
        circleColor = '#06b6d4';
      } else if (goodness >= 0.6) {
        goodnessLabel = 'Good';
        goodnessColor = 'text-blue-600 bg-blue-50 border border-blue-200';
        circleColor = '#3b82f6';
      } else {
        goodnessLabel = 'Needs Review';
        goodnessColor = 'text-red-600 bg-red-50 border border-red-200';
        circleColor = '#ef4444';
      }

      // Use backend's overall_reasoning, fallback to a default message if not provided
      const reasoning = data.overall_reasoning || 'No reasoning provided.';

      // Map factor_reasoning from backend to display format
      const factorReasoning = data.factor_reasoning || {};
      const factorMapping = {
        environment: { title: 'Environmental Conditions', color: 'bg-red-500' },
        supply_demand: { title: 'Supply & Demand', color: 'bg-amber-500' },
        loyalty: { title: 'Customer Loyalty', color: 'bg-blue-500' },
        historical: { title: 'Historical Data', color: 'bg-emerald-500' },
        corporate_pressure: { title: 'Corporate Pressure', color: 'bg-purple-500' }
      };

      // Convert factor_reasoning object to array format for display
      const mappedFactors = Object.entries(factorMapping)
        .map(([key, config]) => {
          const description = factorReasoning[key];
          // Only include factors that have reasoning text
          if (description && description.trim()) {
            return {
              title: config.title,
              color: config.color,
              description: description.trim()
            };
          }
          return null;
        })
        .filter(factor => factor !== null); // Remove null entries

      setResults({
        adjustment,
        newPrice,
        goodness,
        goodnessLabel,
        goodnessColor,
        circleColor,
        reasoning,
        factors: mappedFactors
      });
      setIsLoading(false);
    } catch (err) {
      // Handle errors - preserve form inputs
      setError(err.message || 'An unexpected error occurred. Please try again.');
      setIsLoading(false);
      setResults(null);
    }
  };

  // Default factors array (fallback if backend doesn't provide factor_reasoning)
  const defaultFactors = [
    { color: 'bg-red-500', title: 'Environmental Conditions', description: 'Severe weather reducing driver availability by 35%' },
    { color: 'bg-amber-500', title: 'Supply & Demand', description: 'High demand zone with 1.8x typical requests during storm' },
    { color: 'bg-blue-500', title: 'Customer Loyalty', description: 'Gold-tier customer segment showing high price acceptance during emergencies' },
    { color: 'bg-emerald-500', title: 'Historical Data', description: 'Similar weather conditions typically see 20-30% adjustment success in downtown' },
    { color: 'bg-purple-500', title: 'Corporate Pressure', description: 'Revenue goals driving moderate upward pressure while maintaining ethical constraints' }
  ];

  return (
    <div className="min-h-screen flow-gradient">
      {/* Header */}
      <div className="sticky top-0 z-10 bg-white/90 backdrop-blur-xl border-b border-blue-100">
        <div className="max-w-7xl mx-auto px-4 py-3">
          <div className="grid grid-cols-3 items-center">
            {/* Company Logo & Name */}
            <div className="flex items-center gap-3">
              <div className="p-2 bg-gradient-to-br from-blue-500 to-blue-700 rounded-lg shadow-lg">
                <svg className="w-5 h-5 text-white" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M18.92 6.01C18.72 5.42 18.16 5 17.5 5h-11c-.66 0-1.22.42-1.42 1.01L3 12v8c0 .55.45 1 1 1h1c.55 0 1-.45 1-1v-1h12v1c0 .55.45 1 1 1h1c.55 0 1-.45 1-1v-8l-2.08-5.99zM6.5 16c-.83 0-1.5-.67-1.5-1.5S5.67 13 6.5 13s1.5.67 1.5 1.5S7.33 16 6.5 16zm11 0c-.83 0-1.5-.67-1.5-1.5s.67-1.5 1.5-1.5 1.5.67 1.5 1.5-.67 1.5-1.5 1.5zM5 11l1.5-4.5h11L19 11H5z"/>
                </svg>
              </div>
              <div>
                <h1 className="text-xl font-bold bg-gradient-to-r from-blue-600 via-blue-500 to-cyan-500 bg-clip-text text-transparent" style={{
                  backgroundSize: '300% 300%',
                  animation: 'flow-text 12s ease-in-out infinite'
                }}>
                  RideFlow
                </h1>
                <p className="text-xs text-slate-500">Hop in and go with the flow...</p>
              </div>
            </div>

            {/* App Title - Centered */}
            <div className="text-center">
              <h2 className="text-lg font-semibold bg-gradient-to-r from-blue-700 via-blue-500 to-cyan-500 bg-clip-text text-transparent">
                AI Pricing Monitor & Advisor
              </h2>
              <p className="text-xs text-slate-600">
                Dynamic pricing intelligence
              </p>
            </div>

            {/* Menu Button - Right aligned */}
            <div className="flex justify-end">
              <button className="p-2 hover:bg-slate-100 rounded-lg transition-colors">
                <svg className="w-5 h-5 text-slate-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 6h16M4 12h16M4 18h16"></path>
                </svg>
              </button>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 py-4">
        <div className="grid lg:grid-cols-2 gap-6">
          {/* Input Panel */}
          <div className="space-y-4">
            <div className="bg-white rounded-xl overflow-hidden shadow-lg border border-blue-100">
              <div className="bg-gradient-to-r from-blue-600 to-blue-800 px-4 py-3">
                <h2 className="text-xl font-bold text-white flex items-center gap-2">
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path>
                  </svg>
                  Scenario Configuration
                </h2>
              </div>
              
              <div className="p-4 space-y-4">
                {/* Origin Zone Selection */}
                <div className="space-y-2">
                  <div className="flex items-center gap-2 mb-3">
                    <label className="text-sm font-bold text-slate-800 uppercase tracking-wide">
                      Origin Zone
                    </label>
                    <button
                      onClick={() => setShowZoneHint(!showZoneHint)}
                      className="flex-shrink-0 text-blue-500 hover:text-blue-600 transition-colors"
                      title="Click or tap for more info"
                    >
                      <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                      </svg>
                    </button>
                  </div>
                  {showZoneHint && (
                    <p className="text-xs text-blue-500 italic mb-2">
                      Tip: Select where the ride starts. Base price varies by route (origin to destination).
                    </p>
                  )}
                  <div className="grid grid-cols-2 gap-2">
                    {Object.entries(zones).map(([key, zone]) => (
                      <button
                        key={key}
                        onClick={() => selectOriginZone(key)}
                        className={`p-3 rounded-lg border-2 text-left transition-all ${
                          originZone === key
                            ? 'border-blue-400 bg-gradient-to-br from-blue-50 to-blue-100 shadow-sm'
                            : 'border-slate-200 hover:border-slate-300 hover:bg-slate-50'
                        }`}
                      >
                        <div className="flex items-center gap-2">
                          <div className={`p-1.5 rounded ${originZone === key ? 'bg-blue-200' : 'bg-slate-100'}`}>
                            <svg className={`w-4 h-4 ${originZone === key ? 'text-blue-700' : 'text-slate-600'}`} fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d={zone.icon}></path>
                            </svg>
                          </div>
                          <div>
                            <div className="font-semibold text-sm text-slate-800">{zone.label}</div>
                          </div>
                        </div>
                      </button>
                    ))}
                  </div>
                </div>

                {/* Destination Zone Selection */}
                <div className="space-y-2">
                  <div className="flex items-center gap-2 mb-3">
                    <label className="text-sm font-bold text-slate-800 uppercase tracking-wide">
                      Destination Zone
                    </label>
                    <button
                      onClick={() => setShowZoneHint(!showZoneHint)}
                      className="flex-shrink-0 text-blue-500 hover:text-blue-600 transition-colors"
                      title="Click or tap for more info"
                    >
                      <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                      </svg>
                    </button>
                  </div>
                  {showZoneHint && (
                    <p className="text-xs text-blue-500 italic mb-2">
                      Tip: Select where the ride ends. Base price varies by route (origin to destination).
                    </p>
                  )}
                  <div className="grid grid-cols-2 gap-2">
                    {Object.entries(zones).map(([key, zone]) => (
                      <button
                        key={key}
                        onClick={() => selectZone(key)}
                        className={`p-3 rounded-lg border-2 text-left transition-all ${
                          currentZone === key
                            ? 'border-blue-400 bg-gradient-to-br from-blue-50 to-blue-100 shadow-sm'
                            : 'border-slate-200 hover:border-slate-300 hover:bg-slate-50'
                        }`}
                      >
                        <div className="flex items-center gap-2">
                          <div className={`p-1.5 rounded ${currentZone === key ? 'bg-blue-200' : 'bg-slate-100'}`}>
                            <svg className={`w-4 h-4 ${currentZone === key ? 'text-blue-700' : 'text-slate-600'}`} fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d={zone.icon}></path>
                            </svg>
                          </div>
                          <div>
                            <div className="font-semibold text-sm text-slate-800">{zone.label}</div>
                            {currentZone === key && (
                              <div className="text-xs text-blue-600 font-semibold">
                                Route: ${calculateRoutePrice(originZone, key).toFixed(2)}
                              </div>
                            )}
                          </div>
                        </div>
                      </button>
                    ))}
                  </div>
                </div>

                {/* Scenario Selection */}
                <div className="space-y-2">
                  <div className="flex items-center gap-2 mb-3">
                    <label className="text-sm font-bold text-slate-800 uppercase tracking-wide">
                      Market Scenarios
                    </label>
                    <button
                      onClick={() => setShowScenarioHint(!showScenarioHint)}
                      className="flex-shrink-0 text-blue-500 hover:text-blue-600 transition-colors"
                      title="Click or tap for more info"
                    >
                      <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                      </svg>
                    </button>
                  </div>
                  {showScenarioHint && (
                    <p className="text-xs text-blue-500 italic mb-2">
                      Tip: Select multiple scenarios to analyze combined conditions. At least one scenario must be selected.
                    </p>
                  )}
                  <div className="space-y-2 border-2 border-slate-200 rounded-lg p-3 bg-white">
                    {Object.entries(scenarios).map(([key, scen]) => (
                      <label
                        key={key}
                        className="flex items-start gap-3 p-2 rounded hover:bg-slate-50 cursor-pointer"
                      >
                        <input
                          type="checkbox"
                          checked={selectedScenarios.includes(key)}
                          onChange={() => toggleScenario(key)}
                          className="mt-1 w-4 h-4 text-blue-600 border-slate-300 rounded focus:ring-blue-500"
                        />
                        <div className="flex-1">
                          <div className="text-sm font-semibold text-slate-800">{scen.label}</div>
                          <div className="text-xs text-slate-600">{scen.description}</div>
                        </div>
                      </label>
                    ))}
                  </div>
                  {selectedScenarios.length > 0 && (
                    <p className="text-xs text-slate-600">
                      Selected: {selectedScenarios.map(key => scenarios[key].label).join(', ')}
                    </p>
                  )}
        </div>

                {/* Loyalty Segment Selection */}
                <div className="space-y-2">
                  <div className="flex items-center gap-2 mb-3">
                    <label className="text-sm font-bold text-slate-800 uppercase tracking-wide">
                      Customer Loyalty Segment
                    </label>
                    <button
                      onClick={() => setShowLoyaltyHint(!showLoyaltyHint)}
                      className="flex-shrink-0 text-blue-500 hover:text-blue-600 transition-colors"
                      title="Click or tap for more info"
                    >
                      <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                      </svg>
                    </button>
                  </div>
                  {showLoyaltyHint && (
                    <p className="text-xs text-blue-500 italic mb-2">
                      Tip: Different loyalty segments may show varying price acceptance levels.
                    </p>
                  )}
                  <select
                    value={loyaltySegment}
                    onChange={(e) => setLoyaltySegment(e.target.value)}
                    className="w-full p-3 border-2 border-slate-200 rounded-lg focus:border-indigo-500 focus:outline-none bg-white text-sm font-semibold text-slate-800"
                  >
                    {Object.entries(loyaltySegments).map(([key, segment]) => (
                      <option key={key} value={key}>
                        {segment.label} - {segment.description}
                      </option>
                    ))}
                  </select>
                  <p className="text-xs text-slate-600">
                    {loyaltySegments[loyaltySegment].description}
                  </p>
                </div>

                {/* Supply & Demand Data Section */}
                <div className="bg-amber-50 border border-amber-200 rounded-lg p-4 space-y-3">
                  <h3 className="font-bold text-amber-800 text-sm flex items-center gap-2">
                    <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"></path>
                    </svg>
                    Supply & Demand Data (Optional)
                  </h3>
                  <div className="grid grid-cols-2 gap-3">
                    <div>
                      <label className="text-xs font-semibold text-amber-800">
                        Number of Riders
                      </label>
                      <input
                        type="number"
                        value={numberOfRiders}
                        onChange={(e) => setNumberOfRiders(e.target.value)}
                        className="w-full p-2 border border-amber-300 rounded text-sm focus:border-amber-500 focus:outline-none bg-white text-slate-800 mt-1"
                        min="0"
                        placeholder="e.g., 90"
                      />
                    </div>
                    <div>
                      <label className="text-xs font-semibold text-amber-800">
                        Number of Drivers
                      </label>
                      <input
                        type="number"
                        value={numberOfDrivers}
                        onChange={(e) => setNumberOfDrivers(e.target.value)}
                        className="w-full p-2 border border-amber-300 rounded text-sm focus:border-amber-500 focus:outline-none bg-white text-slate-800 mt-1"
                        min="0"
                        placeholder="e.g., 45"
                      />
                    </div>
                  </div>
                  <p className="text-xs text-amber-700 italic">
                    Provide real-time supply/demand data for more accurate pricing recommendations.
                  </p>
                </div>

                {/* Trip Details Section */}
                <div className="bg-emerald-50 border border-emerald-200 rounded-lg p-4 space-y-3">
                  <h3 className="font-bold text-emerald-800 text-sm flex items-center gap-2">
                    <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                    </svg>
                    Trip Details (Optional)
                  </h3>
                  <div className="grid grid-cols-2 gap-3">
                    <div>
                      <label className="text-xs font-semibold text-emerald-800">
                        Vehicle Type
                      </label>
                      <select
                        value={vehicleType}
                        onChange={(e) => setVehicleType(e.target.value)}
                        className="w-full p-2 border border-emerald-300 rounded text-sm focus:border-emerald-500 focus:outline-none bg-white text-slate-800 mt-1"
                      >
                        <option value="">Select...</option>
                        <option value="Economy">Economy</option>
                        <option value="Premium">Premium</option>
                      </select>
                    </div>
                    <div>
                      <label className="text-xs font-semibold text-emerald-800">
                        Expected Duration (min)
                      </label>
                      <input
                        type="number"
                        value={expectedDuration}
                        onChange={(e) => setExpectedDuration(e.target.value)}
                        className="w-full p-2 border border-emerald-300 rounded text-sm focus:border-emerald-500 focus:outline-none bg-white text-slate-800 mt-1"
                        min="0"
                        placeholder="e.g., 90"
                      />
                    </div>
                  </div>
                  <div>
                    <label className="text-xs font-semibold text-emerald-800">
                      Historical Cost ($)
                    </label>
                    <input
                      type="number"
                      value={historicalCost}
                      onChange={(e) => setHistoricalCost(e.target.value)}
                      className="w-full p-2 border border-emerald-300 rounded text-sm focus:border-emerald-500 focus:outline-none bg-white text-slate-800 mt-1"
                      min="0"
                      step="0.01"
                      placeholder="e.g., 284.26"
                    />
                  </div>
                  <p className="text-xs text-emerald-700 italic">
                    Provide trip-specific details to refine pricing recommendations.
                  </p>
                </div>

                {/* Current Price Display */}
                <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                  <h3 className="font-bold text-blue-800 text-sm flex items-center gap-2 mb-2">
                    <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1"></path>
                    </svg>
                    Current Base Price
                  </h3>
                  <div className="flex items-center justify-between">
                    <div>
                      <div className="text-xl font-bold text-blue-900">
                        ${currentPrice.toFixed(2)}
                      </div>
                      <p className="text-xs text-blue-600">
                        {zones[originZone].label} → {zones[currentZone].label} • {selectedScenarios.map(key => scenarios[key].label).join(', ')}
                      </p>
                    </div>
                    <div className="text-right">
                      <div className="text-xs font-semibold text-blue-800">Base Rate</div>
                      <div className="text-xs text-blue-600">Before adjustment</div>
                    </div>
                  </div>
                </div>

                {/* Corporate Strategy Section */}
                <div className="bg-cyan-50 border border-cyan-200 rounded-lg p-4 space-y-3">
                  <div className="flex items-center gap-2 mb-2">
                    <h3 className="font-bold text-cyan-800 text-sm flex items-center gap-2">
                      <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"></path>
                      </svg>
                      Corporate Strategy
                    </h3>
                    <button
                      onClick={() => setShowCorporateHint(!showCorporateHint)}
                      className="flex-shrink-0 text-blue-500 hover:text-blue-600 transition-colors"
                      title="Click or tap for more info"
                    >
                      <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                      </svg>
                    </button>
                  </div>
                  {showCorporateHint && (
                    <p className="text-xs text-blue-500 italic mb-2">
                      Try changing the corporate revenue goal to see how the recommendation changes (within guardrails).
                    </p>
                  )}
                  <div className="grid grid-cols-2 gap-3">
                    <div>
                      <label className="text-xs font-semibold text-cyan-800">
                        Revenue Goal (%)
                      </label>
                      <input
                        ref={revenueGoalInputRef}
                        type="number"
                        value={revenueGoal}
                        onChange={(e) => {
                          const value = Number(e.target.value) || 0;
                          setRevenueGoal(value);
                        }}
                        className="w-full p-2 border border-cyan-300 rounded text-sm focus:border-cyan-500 focus:outline-none bg-white text-slate-800 mt-1"
                        min="0"
                        max="50"
                      />
                    </div>
                    <div>
                      <label className="text-xs font-semibold text-cyan-800">
                        Strategy Notes
                      </label>
                      <textarea
                        ref={strategyNotesInputRef}
                        value={strategyNotes}
                        onChange={(e) => {
                          setStrategyNotes(e.target.value);
                        }}
                        className="w-full p-2 border border-cyan-300 rounded text-xs focus:border-cyan-500 focus:outline-none bg-white text-slate-800 mt-1"
                        rows="2"
                      />
                    </div>
                  </div>
                </div>

                {/* Analyst Notes */}
                <div className="space-y-2">
                  <div className="flex items-center gap-2 mb-3">
                    <label className="text-sm font-bold text-slate-800 uppercase tracking-wide">
                      Additional Context
                    </label>
                    <button
                      onClick={() => setShowContextHint(!showContextHint)}
                      className="flex-shrink-0 text-blue-500 hover:text-blue-600 transition-colors"
                      title="Click or tap for more info"
                    >
                      <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                      </svg>
                    </button>
                  </div>
                  {showContextHint && (
                    <p className="text-xs text-blue-500 italic mb-2">
                      Tip: Provide additional context about market conditions or special circumstances.
                    </p>
                  )}
                  <textarea
                    value={additionalContext}
                    onChange={(e) => setAdditionalContext(e.target.value)}
                    className="w-full p-3 border-2 border-slate-200 rounded-lg focus:border-indigo-500 focus:outline-none resize-none text-sm bg-white text-slate-800"
                    rows="2"
                    placeholder="Storm expected to reduce driver availability by 40%."
                  />
                </div>

                {/* Submit Button */}
                <button
                  onClick={generateRecommendation}
                  disabled={isLoading}
                  className="w-full py-3 bg-gradient-to-r from-blue-600 via-blue-700 to-blue-800 text-white font-bold rounded-lg shadow-lg hover:shadow-xl transition-all hover:-translate-y-0.5 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {isLoading ? (
                    <div className="flex items-center justify-center gap-2">
                      <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin"></div>
                      Analyzing Market Conditions...
                    </div>
                  ) : (
                    <div className="flex items-center justify-center gap-2">
                      <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path>
                      </svg>
                      Generate Recommendation
                    </div>
                  )}
                </button>
              </div>
            </div>
          </div>

          {/* Results Panel */}
          <div className="space-y-4">
            {/* Error State */}
            {error && (
              <div className="bg-red-50 border-2 border-red-200 rounded-xl p-4 shadow-lg">
                <div className="flex items-start gap-3">
                  <div className="flex-shrink-0">
                    <svg className="w-5 h-5 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                    </svg>
                  </div>
                  <div className="flex-1">
                    <h3 className="text-sm font-bold text-red-800 mb-1">Error Generating Recommendation</h3>
                    <p className="text-sm text-red-700 mb-3">{error}</p>
                    <button
                      onClick={() => {
                        setError(null);
                        generateRecommendation();
                      }}
                      className="text-xs font-semibold text-red-800 hover:text-red-900 underline"
                    >
                      Try Again
                    </button>
                  </div>
                  <button
                    onClick={() => setError(null)}
                    className="flex-shrink-0 text-red-600 hover:text-red-800"
                  >
                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12"></path>
                    </svg>
                  </button>
                </div>
              </div>
            )}

            {/* Empty State */}
            {!isLoading && !results && !error && (
              <div className="bg-white rounded-xl p-6 text-center shadow-lg border border-blue-100">
                <div className="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-3">
                  <svg className="w-6 h-6 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"></path>
                  </svg>
                </div>
                <h3 className="text-lg font-bold text-slate-800 mb-2">Ready for Analysis</h3>
                <p className="text-sm text-slate-600 mb-3">
                  Configure your scenario to receive AI-powered pricing recommendations.
                </p>
                <div className="flex items-start justify-center gap-2">
                  <button
                    onClick={() => setShowEmptyStateHint(!showEmptyStateHint)}
                    className="flex-shrink-0 mt-0.5 text-blue-500 hover:text-blue-600 transition-colors"
                    title="Click or tap for more info"
                  >
                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                    </svg>
                  </button>
                  {showEmptyStateHint && (
                    <p className="text-xs text-blue-500 italic flex-1 text-center">
                      Quick start: Select a zone, choose a scenario, and click &quot;Generate Recommendation&quot; to see AI-powered pricing insights.
                    </p>
                  )}
                </div>
              </div>
            )}

            {/* Loading State */}
            {isLoading && (
              <div className="bg-white rounded-xl p-6 text-center shadow-lg border border-blue-100">
                <div className="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-3">
                  <div className="w-6 h-6 border-2 border-blue-300 border-t-blue-600 rounded-full animate-spin"></div>
                </div>
                <h3 className="text-lg font-bold text-slate-800 mb-2">Analyzing Conditions</h3>
                <p className="text-sm text-slate-600">Processing factors and generating recommendations...</p>
              </div>
            )}

            {/* Results */}
            {results && !error && (
              <div className="space-y-4 animate-[slideUp_0.6s_ease-out]">
                {/* Main Recommendation */}
                <div className="bg-white rounded-xl overflow-hidden shadow-lg border border-blue-100">
                  <div className="bg-gradient-to-r from-blue-600 to-blue-800 px-4 py-3">
                    <h3 className="text-lg font-bold text-white flex items-center gap-2">
                      <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path>
                      </svg>
                      Pricing Recommendation
                    </h3>
                  </div>
                  <div className="p-4">
                    <div className="text-center">
                      <div className="text-4xl font-bold text-blue-800 mb-2">
                        {results.adjustment > 0 ? '+' : ''}{Math.round(results.adjustment * 100)}%
                      </div>
                      <p className="text-sm text-blue-600 font-semibold mb-3">
                        Recommended adjustment for {zones[originZone].label} → {zones[currentZone].label}
                      </p>
                      <div className="flex items-center justify-center gap-3 text-sm">
                        <div className="bg-blue-50 border border-blue-200 px-2 py-1 rounded">
                          <span className="text-blue-600">Current: </span>
                          <span className="font-bold text-blue-800">${currentPrice.toFixed(2)}</span>
                        </div>
                        <div className="text-blue-400">→</div>
                        <div className="bg-cyan-50 border border-cyan-200 px-2 py-1 rounded">
                          <span className="text-cyan-600">New: </span>
                          <span className="font-bold text-cyan-800">${results.newPrice.toFixed(2)}</span>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>

                {/* Goodness Score */}
                <div className="bg-white rounded-xl overflow-hidden shadow-lg border border-blue-100">
                  <div className="bg-gradient-to-r from-blue-600 to-blue-800 px-4 py-3">
                    <h3 className="text-lg font-bold text-white flex items-center gap-2">
                      <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path>
                      </svg>
                      Confidence Score
                    </h3>
                  </div>
                  <div className="p-4">
                    <div className="flex items-center justify-center gap-6">
                      <div className={`inline-block px-2 py-1 rounded-full text-xs font-bold ${results.goodnessColor}`}>
                        {results.goodnessLabel}
                      </div>
                      <div className="text-2xl font-bold text-blue-800">
                        {Math.round(results.goodness * 100)}/100
                      </div>
                      <div className="w-16 h-16 relative">
                        <svg className="w-16 h-16 transform -rotate-90" viewBox="0 0 100 100">
                          <circle cx="50" cy="50" r="40" fill="transparent" stroke="#bae6fd" strokeWidth="8"/>
                          <circle
                            cx="50"
                            cy="50"
                            r="40"
                            fill="transparent"
                            stroke={results.circleColor}
                            strokeWidth="8"
                            strokeDasharray={`${results.goodness * 251.2} 251.2`}
                            className="transition-all duration-1000"
                          />
                        </svg>
                      </div>
                    </div>
                  </div>
                </div>

                {/* AI Reasoning */}
                <div className="bg-white rounded-xl overflow-hidden shadow-lg border border-blue-100">
                  <div className="bg-gradient-to-r from-blue-600 to-blue-800 px-4 py-3">
                    <h3 className="text-lg font-bold text-white flex items-center gap-2">
                      <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"></path>
                      </svg>
                      AI-Generated Analysis & Reasoning
                    </h3>
                    <p className="text-blue-200 text-xs mt-1">
                      Machine learning insights and recommendation logic
                    </p>
                  </div>
                  <div className="p-6 space-y-6">
                    <div className="prose max-w-none">
                      <p className="text-slate-700 leading-relaxed font-medium">
                        {results.reasoning}
                      </p>
                    </div>

                    {/* Factor Breakdown */}
                    <div className="pt-4 border-t border-slate-200">
                      <h4 className="font-bold text-slate-800 mb-4">Contributing Factors:</h4>
                      <div className="space-y-3">
                        {(results.factors && results.factors.length > 0 ? results.factors : defaultFactors).map((factor, index) => (
                          <div key={index} className="flex items-start gap-3 p-3 bg-slate-50 rounded-lg">
                            <div className={`w-2 h-2 ${factor.color} rounded-full mt-2 flex-shrink-0`}></div>
                            <div>
                              <div className="font-semibold text-slate-800 mb-1">{factor.title}</div>
                              <p className="text-sm text-slate-600">{factor.description}</p>
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
