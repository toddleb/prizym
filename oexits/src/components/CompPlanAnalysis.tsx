// Save this as components/CompPlanAnalysis.tsx
import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, Cell, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar, ReferenceLine } from 'recharts';
import { AlertTriangle, BarChart3, Award, Target } from 'lucide-react';

const CompPlanAnalysis = () => {
  // Theme colors based on OEXITS logo
  const colors = {
    primary: '#645994',        // Medium purple (base)
    secondary: '#4E4E4E',      // Dark gray
    accent1: '#8070b5',        // Lighter purple
    accent2: '#a596d4',        // Even lighter purple
    accent3: '#463e68',        // Darker purple
    light: '#d8d0f0',          // Very light purple
    textDark: '#333333',
    textLight: '#777777',
    background: '#f8f7fc',     // Super light purple background
    success: '#8070b5',        // Using purple instead of green
    warning: '#a596d4',        // Using lighter purple instead of yellow
    danger: '#463e68'          // Using darker purple instead of red
  };

  // Plan complexity score
  const complexityScore = 72;
  const industryAvg = 65;

  // Red flags data
  const redFlags = [
    { id: 1, issue: "Stack ranking methodology (top 75%)", severity: "high", impact: "Creates unhealthy internal competition; 25% of Sales Reps get no payout" },
    { id: 2, issue: "High dependency on qualitative assessment", severity: "medium", impact: "Year-end award lacks objective criteria and measurable goals" },
    { id: 3, issue: "Multi-tiered goal structure", severity: "medium", impact: "Complex structure with varying targets adds unnecessary complexity" }
  ];

  // Payout curve data for heatmap
  const payoutCurveData = [
    { name: "Below 75th percentile", percentile: "0-74th", multiplier: 0, color: "#e5e7eb" },
    { name: "Quartile 4", percentile: "75-81st", multiplier: 1.0, color: colors.light },
    { name: "Quartile 4", percentile: "82-87th", multiplier: 1.5, color: colors.accent2 },
    { name: "Quartile 3", percentile: "88-93rd", multiplier: 2.5, color: colors.accent1 },
    { name: "Quartile 2", percentile: "94-96th", multiplier: 3.5, color: colors.primary },
    { name: "Quartile 1", percentile: "97-99th", multiplier: 7.0, color: colors.accent3 },
    { name: "Quartile 1 (Top)", percentile: "100th", multiplier: 9.0, color: "#2d274d" }
  ];

  // Benchmark comparison data
  const benchmarkData = [
    { category: "Plan Simplicity", score: 4, industry: 7, topPerformer: 9, fullMark: 10 },
    { category: "Performance Linkage", score: 7, industry: 6, topPerformer: 9, fullMark: 10 },
    { category: "Objective Criteria", score: 5, industry: 7, topPerformer: 9, fullMark: 10 },
    { category: "Balanced Incentives", score: 6, industry: 6, topPerformer: 8, fullMark: 10 },
    { category: "Transparent Payouts", score: 5, industry: 7, topPerformer: 9, fullMark: 10 }
  ];

  // Get color for complexity score
  const getComplexityColor = (score: number) => {
    if (score < 40) return colors.light;
    if (score < 70) return colors.accent1;
    return colors.accent3;
  };

  // Severity colors for red flags - purple theme
  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case "low": return "bg-purple-100 text-purple-800";
      case "medium": return "bg-purple-200 text-purple-800";
      case "high": return "bg-purple-300 text-purple-900";
      default: return "bg-gray-100 text-gray-800";
    }
  };

  // Format multiplier for tooltip
  const formatMultiplier = (value: any) => {
    const numValue = Number(value);
    return isNaN(numValue) ? "Invalid" : numValue === 0 ? "No Payout" : `${numValue.toFixed(1)}x Base`;
  };

  return (
    <div className="p-6" style={{ backgroundColor: colors.background, fontFamily: 'Inter, system-ui, sans-serif' }}>
      <div className="grid grid-cols-2 gap-6">
        {/* Quadrant 1: Plan Complexity Score */}
        <div className="bg-white p-6 rounded-lg shadow-lg flex flex-col">
          <div className="flex items-center mb-4">
            <Target style={{ color: colors.primary }} className="mr-2" size={24} />
            <h2 className="text-2xl font-bold" style={{ color: colors.primary }}>Plan Complexity Score</h2>
          </div>
          
          <div className="flex-1 flex flex-col justify-center items-center">
            <div className="relative w-64 h-64 mb-4">
              <div className="absolute inset-0 flex items-center justify-center">
                <div className="text-center">
                  <div className="text-6xl font-bold mb-2" style={{ color: getComplexityColor(complexityScore) }}>
                    {complexityScore}
                  </div>
                  <div className="text-lg" style={{ color: colors.textDark }}>
                    <span className="font-medium">Moderately Complex</span>
                  </div>
                </div>
              </div>
              <svg className="w-full h-full" viewBox="0 0 42 42">
                <circle
                  cx="21"
                  cy="21"
                  r="15.91549430918954"
                  fill="transparent"
                  stroke="#e6e6e6"
                  strokeWidth="3"
                ></circle>
                <circle
                  cx="21"
                  cy="21"
                  r="15.91549430918954"
                  fill="transparent"
                  stroke={getComplexityColor(complexityScore)}
                  strokeWidth="3"
                  strokeDasharray={`${complexityScore} ${100 - complexityScore}`}
                  strokeDashoffset="25"
                ></circle>
              </svg>
            </div>
            
            <div className="w-full max-w-md space-y-3">
              <div>
                <div className="flex justify-between mb-1 text-sm">
                  <span style={{ color: colors.textLight }}>Industry Average</span>
                  <span className="font-medium" style={{ color: colors.primary }}>{industryAvg}/100</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2 mb-4">
                  <div 
                    className="rounded-full h-2" 
                    style={{ 
                      width: `${industryAvg}%`, 
                      backgroundColor: colors.primary
                    }}
                  ></div>
                </div>
              </div>
              
              <div className="bg-gray-50 p-3 rounded-lg mb-3">
                <p className="text-sm font-medium mb-2" style={{ color: colors.primary }}>Complex Components:</p>
                <ul className="list-disc pl-5 text-xs space-y-1" style={{ color: colors.textDark }}>
                  <li>Three-tiered goal structure with multiple metrics</li>
                  <li>Stack ranking methodology requires constant comparison</li>
                  <li>Subjective year-end qualitative assessment</li>
                </ul>
              </div>
              
              <div className="bg-purple-50 p-3 rounded-lg mb-3">
                <p className="text-sm font-medium mb-2" style={{ color: colors.primary }}>Administrative Burden:</p>
                <div className="grid grid-cols-2 gap-2">
                  <div className="bg-white p-2 rounded text-center">
                    <p className="text-xs text-gray-500">Manual Processes</p>
                    <p className="text-lg font-bold" style={{ color: colors.accent3 }}>High</p>
                  </div>
                  <div className="bg-white p-2 rounded text-center">
                    <p className="text-xs text-gray-500">Calculation Time</p>
                    <p className="text-lg font-bold" style={{ color: colors.accent3 }}>12+ hrs</p>
                  </div>
                </div>
              </div>
              
              <div className="bg-purple-50 p-3 rounded-lg">
                <p className="text-sm font-medium mb-2" style={{ color: colors.primary }}>Plan Structure Impact:</p>
                <div className="flex justify-between items-center mb-1">
                  <span className="text-xs" style={{ color: colors.textLight }}>Rep Understanding</span>
                  <span className="text-xs font-medium" style={{ color: colors.accent3 }}>Low</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-1.5 mb-2">
                  <div className="rounded-full h-1.5" style={{ width: '35%', backgroundColor: colors.accent3 }}></div>
                </div>
                
                <div className="flex justify-between items-center mb-1">
                  <span className="text-xs" style={{ color: colors.textLight }}>Administration Efficiency</span>
                  <span className="text-xs font-medium" style={{ color: colors.accent3 }}>Low</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-1.5 mb-2">
                  <div className="rounded-full h-1.5" style={{ width: '30%', backgroundColor: colors.accent3 }}></div>
                </div>
                
                <div className="flex justify-between items-center mb-1">
                  <span className="text-xs" style={{ color: colors.textLight }}>Sales Rep Satisfaction</span>
                  <span className="text-xs font-medium" style={{ color: colors.accent1 }}>Medium</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-1.5">
                  <div className="rounded-full h-1.5" style={{ width: '55%', backgroundColor: colors.accent1 }}></div>
                </div>
              </div>
            </div>
            
            <div className="w-full flex justify-between text-xs font-medium mt-3">
              <span style={{ color: colors.light }}>Simple (0-40)</span>
              <span style={{ color: colors.accent1 }}>Moderate (41-70)</span>
              <span style={{ color: colors.accent3 }}>Complex (71-100)</span>
            </div>
          </div>
        </div>

        {/* Quadrant 2: Red Flags & Risk Markers */}
        <div className="bg-white p-6 rounded-lg shadow-lg flex flex-col">
          <div className="flex items-center mb-4">
            <AlertTriangle style={{ color: colors.primary }} className="mr-2" size={24} />
            <h2 className="text-2xl font-bold" style={{ color: colors.primary }}>Risk Markers & Red Flags</h2>
          </div>
          
          <div className="flex-1 overflow-auto">
            <div className="space-y-4">
              {redFlags.map(flag => (
                <div key={flag.id} className="p-4 rounded-lg shadow-sm border-l-4" 
                  style={{ 
                    borderLeftColor: flag.severity === 'high' ? colors.accent3 : flag.severity === 'medium' ? colors.accent1 : colors.light,
                    backgroundColor: flag.severity === 'high' ? '#f5f3ff' : flag.severity === 'medium' ? '#f9f7ff' : '#fbfaff'
                  }}>
                  <div className="flex items-start">
                    <span className={`px-2 py-1 text-xs font-medium rounded-full ${getSeverityColor(flag.severity)} mr-2`}>
                      {flag.severity}
                    </span>
                    <div>
                      <h3 className="font-semibold" style={{ color: colors.textDark }}>{flag.issue}</h3>
                      <p className="text-sm mt-1" style={{ color: colors.textLight }}>{flag.impact}</p>
                    </div>
                  </div>
                </div>
              ))}
            </div>
            
            <div className="mt-6">
              <h3 className="font-semibold mb-3 flex items-center" style={{ color: colors.primary }}>
                <Award size={18} className="mr-2" />
                Improvement Recommendations
              </h3>
              <ul className="space-y-2">
                <li className="flex items-start p-2 bg-gray-50 rounded">
                  <div className="mr-2 w-5 h-5 flex items-center justify-center rounded-full text-xs font-bold" style={{ backgroundColor: '#f3f0ff', color: colors.primary }}>
                    1
                  </div>
                  <div>
                    <p className="text-sm" style={{ color: colors.textDark }}>
                      <span className="font-medium">Simplify tier structure</span> — Reduce from three tiers to two, with clearer advancement criteria
                    </p>
                  </div>
                </li>
                <li className="flex items-start p-2 bg-gray-50 rounded">
                  <div className="mr-2 w-5 h-5 flex items-center justify-center rounded-full text-xs font-bold" style={{ backgroundColor: '#f3f0ff', color: colors.primary }}>
                    2
                  </div>
                  <div>
                    <p className="text-sm" style={{ color: colors.textDark }}>
                      <span className="font-medium">Replace stack ranking</span> — Implement absolute goal-based payouts rather than relative performance
                    </p>
                  </div>
                </li>
                <li className="flex items-start p-2 bg-gray-50 rounded">
                  <div className="mr-2 w-5 h-5 flex items-center justify-center rounded-full text-xs font-bold" style={{ backgroundColor: '#f3f0ff', color: colors.primary }}>
                    3
                  </div>
                  <div>
                    <p className="text-sm" style={{ color: colors.textDark }}>
                      <span className="font-medium">Objectify qualitative metrics</span> — Add measurable KPIs for the year-end qualitative assessment
                    </p>
                  </div>
                </li>
              </ul>
            </div>
          </div>
        </div>

        {/* Quadrant 3: Payout Curve Heatmap */}
        <div className="bg-white p-6 rounded-lg shadow-lg flex flex-col">
          <div className="flex items-center mb-4">
            <BarChart3 style={{ color: colors.primary }} className="mr-2" size={24} />
            <h2 className="text-2xl font-bold" style={{ color: colors.primary }}>Payout Curve Analysis</h2>
          </div>
          
          <div className="flex-1">
            <div className="mb-4 bg-gray-50 p-3 rounded border-l-4" style={{ borderLeftColor: colors.primary }}>
              <p className="text-sm" style={{ color: colors.textDark }}>
                <span className="font-medium">Steep Incentive Curve Analysis:</span> The plan creates significant payout differentials between top performers and others.
              </p>
            </div>
            
            <ResponsiveContainer width="100%" height={250}>
              <BarChart
                data={payoutCurveData}
                margin={{ top: 20, right: 30, left: 20, bottom: 30 }}
              >
                <CartesianGrid strokeDasharray="3 3" stroke="#e0e0e0" />
                <XAxis dataKey="percentile" tick={{ fill: colors.textDark }} />
                <YAxis tick={{ fill: colors.textDark }} label={{ value: 'Payout Multiplier', angle: -90, position: 'insideLeft', style: { fill: colors.textDark } }} />
                <Tooltip 
                  formatter={(value) => [formatMultiplier(value as number), 'Payout']}
                  contentStyle={{ backgroundColor: 'white', borderColor: colors.primary }}
                  labelStyle={{ color: colors.primary }}
                />
                <Bar dataKey="multiplier" name="Payout Multiplier">
                  {payoutCurveData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Bar>
                <ReferenceLine y={industryAvg/20} stroke={colors.accent3} strokeDasharray="3 3" />
              </BarChart>
            </ResponsiveContainer>
            
            <div className="mt-4 space-y-3">
              <p className="text-sm" style={{ color: colors.textDark }}>
                <span className="font-medium">Analysis:</span> The distribution follows a power curve with extreme rewards for top 5% performers.
              </p>
              
              <div className="grid grid-cols-2 gap-4 text-center">
                <div className="bg-gray-50 p-2 rounded">
                  <p className="text-xs" style={{ color: colors.textLight }}>Bottom 25% of Sales Reps</p>
                  <p className="text-xl font-bold" style={{ color: colors.accent3 }}>$0</p>
                  <p className="text-xs" style={{ color: colors.textLight }}>No incentive payout</p>
                </div>
                <div className="bg-gray-50 p-2 rounded">
                  <p className="text-xs" style={{ color: colors.textLight }}>Top 3% of Sales Reps</p>
                  <p className="text-xl font-bold" style={{ color: colors.primary }}>$7-9K</p>
                  <p className="text-xs" style={{ color: colors.textLight }}>Quarterly payout</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Quadrant 4: Benchmark Comparison */}
        <div className="bg-white p-6 rounded-lg shadow-lg flex flex-col">
          <div className="flex items-center mb-4">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" className="mr-2">
              <path d="M12 2L4 6V12C4 15.31 7.58 19.8 12 22C16.42 19.8 20 15.31 20 12V6L12 2Z" stroke={colors.primary} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
            </svg>
            <h2 className="text-2xl font-bold" style={{ color: colors.primary }}>Industry Benchmarking</h2>
          </div>
          
          <div className="flex-1 flex flex-col">
            <div className="flex-1">
              <ResponsiveContainer width="100%" height="100%">
                <RadarChart outerRadius={90} data={benchmarkData}>
                  <PolarGrid />
                  <PolarAngleAxis dataKey="category" tick={{ fill: colors.textDark, fontSize: 12 }} />
                  <PolarRadiusAxis angle={30} domain={[0, 10]} />
                  <Radar name="Your Plan" dataKey="score" stroke={colors.primary} fill={colors.primary} fillOpacity={0.5} />
                  <Radar name="Industry Average" dataKey="industry" stroke={colors.accent2} fill={colors.accent2} fillOpacity={0.3} />
                  <Radar name="Top Performer" dataKey="topPerformer" stroke={colors.light} fill={colors.light} fillOpacity={0.2} />
                  <Legend />
                  <Tooltip />
                </RadarChart>
              </ResponsiveContainer>
            </div>
            
            <div>
              <p className="text-sm font-medium mb-2" style={{ color: colors.primary }}>Key Findings:</p>
              <ul className="text-xs space-y-2" style={{ color: colors.textDark }}>
                <li className="flex items-start">
                  <span className="inline-block w-3 h-3 mr-2 mt-1 rounded-full" style={{ backgroundColor: colors.accent3 }}></span>
                  <p>Plan simplicity scores <span className="font-medium">43% below</span> industry average with complex tiering</p>
                </li>
                <li className="flex items-start">
                  <span className="inline-block w-3 h-3 mr-2 mt-1 rounded-full" style={{ backgroundColor: colors.accent2 }}></span>
                  <p>Performance linkage scores <span className="font-medium">17% above</span> industry average with focus on sales metrics</p>
                </li>
                <li className="flex items-start">
                  <span className="inline-block w-3 h-3 mr-2 mt-1 rounded-full" style={{ backgroundColor: colors.accent1 }}></span>
                  <p>Objective criteria scores <span className="font-medium">29% below</span> industry average due to qualitative components</p>
                </li>
                <li className="flex items-start">
                  <span className="inline-block w-3 h-3 mr-2 mt-1 rounded-full" style={{ backgroundColor: colors.primary }}></span>
                  <p>Overall assessment: Current structure has moderate competitive gaps versus industry best practices</p>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default CompPlanAnalysis;
