import React from 'react';
import { LineChart, Line, BarChart, Bar, ComposedChart, Area, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, Label, RadarChart, Radar, PolarGrid, PolarAngleAxis, PolarRadiusAxis } from 'recharts';

const RealTimeAnalysis = () => {
  // Sample data for visualizations
  const quotaAttainmentTrend = [
    { period: 'Jan', attainment: 86, projected: null },
    { period: 'Feb', attainment: 92, projected: null },
    { period: 'Mar', attainment: 78, projected: null },
    { period: 'Apr', attainment: 81, projected: null },
    { period: 'May', attainment: 85, projected: null },
    { period: 'Jun', attainment: null, projected: 88 },
    { period: 'Jul', attainment: null, projected: 93 },
    { period: 'Aug', attainment: null, projected: 95 }
  ];
  
  const payoutDistribution = [
    { range: '0-50%', count: 18, color: '#FF8042' },
    { range: '50-75%', count: 32, color: '#FFBB28' },
    { range: '75-100%', count: 45, color: '#00C49F' },
    { range: '100-125%', count: 37, color: '#0088FE' },
    { range: '125%+', count: 15, color: '#8884d8' }
  ];
  
  const kpiPerformance = [
    { subject: 'Revenue', actual: 87, target: 100, fullMark: 150 },
    { subject: 'New Logos', actual: 92, target: 100, fullMark: 150 },
    { subject: 'Profit Margin', actual: 102, target: 100, fullMark: 150 },
    { subject: 'Retention', actual: 96, target: 100, fullMark: 150 },
    { subject: 'Upsell', actual: 79, target: 100, fullMark: 150 },
    { subject: 'Strategic Products', actual: 65, target: 100, fullMark: 150 }
  ];
  
  const anomalyData = [
    { 
      id: 1,
      rep: "Thomas Wilson",
      metric: "Commission Calculation",
      expected: "$18,250",
      actual: "$26,780",
      severity: "High",
      recommendation: "Review multi-tier qualification criteria; appears to be double-counting enterprise deals"
    },
    { 
      id: 2,
      rep: "Regions: EMEA",
      metric: "Attainment Distribution",
      expected: "Normal bell curve",
      actual: "Bi-modal clustering",
      severity: "Medium",
      recommendation: "Investigate quota setting disparity between sub-regions"
    },
    { 
      id: 3,
      rep: "Product Team B",
      metric: "SPIFFs Effectiveness",
      expected: "30% lift in promotion",
      actual: "8% lift in promotion",
      severity: "Medium",
      recommendation: "Reassess SPIFF timing and communication strategy; awareness is low"
    },
    { 
      id: 4,
      rep: "New Hire Cohort",
      metric: "Ramp Period",
      expected: "90 days",
      actual: "142 days average",
      severity: "High",
      recommendation: "Modify compensation ramp structure to reflect realistic productivity curve"
    }
  ];
  
  const insightCards = [
    {
      title: "Plan Misalignment",
      description: "Current plan drives individual performance but undervalues team collaboration",
      impact: "42% of enterprise deals show delayed handoffs between pre/post sales",
      action: "Introduce shared success metrics for complex deal teams"
    },
    {
      title: "Timing Optimization",
      description: "Monthly vs quarterly payout comparison shows significant behavior change",
      impact: "28% less end-of-quarter discounting with monthly measurement",
      action: "Transition key metrics to monthly cadence with accelerators"
    },
    {
      title: "Component Weighting",
      description: "Weighting analysis shows overemphasis on volume vs. strategic objectives",
      impact: "Strategic product mix is 22% below target despite overall quota attainment",
      action: "Rebalance component weights from 70/30 to 50/50 core/strategic"
    },
    {
      title: "Territory Equity",
      description: "Significant earning potential variance identified across equal-level territories",
      impact: "37% difference in OTE achievement potential due to market maturity",
      action: "Implement market adjustment factors in quota setting process"
    }
  ];

  return (
    <div className="w-full h-full bg-white p-4 font-sans">
      <div className="flex justify-between items-center mb-4">
        <h1 className="text-2xl font-bold">Real-Time Sales Compensation Monitoring & Analysis</h1>
        <div className="flex items-center">
          <div className="h-8 w-8 bg-purple-600 rounded-full mr-2"></div>
          <div className="h-8 w-8 bg-blue-600 rounded-full"></div>
        </div>
      </div>
      
      <div className="grid grid-cols-2 gap-4">
        {/* Live Monitoring Platform */}
        <div className="border-2 border-gray-300 rounded-lg p-3">
          <h2 className="text-lg font-bold mb-2">Real-Time Compensation Intelligence</h2>
          <div className="text-sm space-y-1 mb-3">
            <p>Global medical device manufacturer with 450+ sales professionals</p>
            <p>Complex compensation structure with 12+ plan components per rep</p>
            <p>Multiple data sources from CRM, ERP, and commission systems</p>
            <p>Delayed insights causing compensation disputes and sales behavior lag</p>
          </div>
          
          <h2 className="text-lg font-bold mb-2">Prizym.ai LENS Monitoring Solution</h2>
          <div className="flex items-start mb-1">
            <div className="w-6 h-6 rounded-full bg-purple-600 text-white flex items-center justify-center font-bold mr-2 flex-shrink-0">1</div>
            <p className="text-sm">Real-time data integration from 8 disparate systems (sales, finance, HR)</p>
          </div>
          <div className="flex items-start mb-1">
            <div className="w-6 h-6 rounded-full bg-purple-600 text-white flex items-center justify-center font-bold mr-2 flex-shrink-0">2</div>
            <p className="text-sm">Automated anomaly detection using AI pattern recognition</p>
          </div>
          <div className="flex items-start mb-1">
            <div className="w-6 h-6 rounded-full bg-purple-600 text-white flex items-center justify-center font-bold mr-2 flex-shrink-0">3</div>
            <p className="text-sm">Predictive attainment modeling and payout forecasting</p>
          </div>
          <div className="flex items-start">
            <div className="w-6 h-6 rounded-full bg-purple-600 text-white flex items-center justify-center font-bold mr-2 flex-shrink-0">4</div>
            <p className="text-sm">Continuous plan effectiveness analysis and optimization</p>
          </div>
          
          <div className="mt-3 p-2 bg-purple-50 rounded-lg">
            <p className="text-sm font-bold">System Integration Architecture:</p>
            <div className="mt-1 flex justify-center">
              <div className="relative h-24 w-3/4">
                {/* Data Source Integration */}
                <div className="absolute top-0 left-0 right-0 flex justify-between">
                  <div className="bg-blue-100 border border-blue-300 rounded px-1 text-xs">CRM</div>
                  <div className="bg-green-100 border border-green-300 rounded px-1 text-xs">ERP</div>
                  <div className="bg-yellow-100 border border-yellow-300 rounded px-1 text-xs">HRIS</div>
                  <div className="bg-red-100 border border-red-300 rounded px-1 text-xs">Orders</div>
                  <div className="bg-purple-100 border border-purple-300 rounded px-1 text-xs">Contracts</div>
                </div>
                
                {/* Arrows down */}
                <div className="absolute top-4 left-0 right-0 flex justify-around">
                  <div className="h-4 border-l border-gray-400"></div>
                  <div className="h-4 border-l border-gray-400"></div>
                  <div className="h-4 border-l border-gray-400"></div>
                  <div className="h-4 border-l border-gray-400"></div>
                  <div className="h-4 border-l border-gray-400"></div>
                </div>
                
                {/* Processing layer */}
                <div className="absolute top-8 left-1/4 right-1/4">
                  <div className="bg-purple-500 text-white rounded px-2 py-1 text-xs text-center font-bold">
                    LENS AI Processing Engine
                  </div>
                </div>
                
                {/* Arrow down */}
                <div className="absolute top-15 left-1/2 h-4 border-l border-gray-400 transform -translate-x-1/2"></div>
                
                {/* Output layer */}
                <div className="absolute bottom-0 left-0 right-0 flex justify-center space-x-2">
                  <div className="bg-blue-500 text-white rounded px-1 text-xs">Dashboards</div>
                  <div className="bg-green-500 text-white rounded px-1 text-xs">Alerts</div>
                  <div className="bg-yellow-500 text-white rounded px-1 text-xs">Reports</div>
                  <div className="bg-red-500 text-white rounded px-1 text-xs">API</div>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        {/* Real-time Monitoring Visualizations */}
        <div className="border-2 border-gray-300 rounded-lg p-3">
          <h2 className="text-lg font-bold mb-2">Live Performance Metrics</h2>
          <div className="grid grid-cols-2 gap-3">
            {/* Quota Attainment Trend */}
            <div className="h-40">
              <p className="text-sm font-bold mb-1 text-center">Quota Attainment & Projection</p>
              <ResponsiveContainer width="100%" height="100%">
                <ComposedChart data={quotaAttainmentTrend} margin={{ top: 5, right: 5, left: 5, bottom: 5 }}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="period" tick={{ fontSize: 10 }} />
                  <YAxis tick={{ fontSize: 10 }}>
                    <Label value="% Attainment" angle={-90} position="insideLeft" style={{ textAnchor: 'middle', fontSize: 10 }} />
                  </YAxis>
                  <Tooltip />
                  <Legend wrapperStyle={{ fontSize: 8 }} />
                  <Line type="monotone" dataKey="attainment" stroke="#8884d8" name="Actual" />
                  <Line type="monotone" dataKey="projected" stroke="#82ca9d" strokeDasharray="5 5" name="Projected" />
                  <Area type="monotone" dataKey="attainment" fill="#8884d8" stroke="none" opacity={0.2} />
                </ComposedChart>
              </ResponsiveContainer>
            </div>
            
            {/* KPI Performance Radar */}
            <div className="h-40">
              <p className="text-sm font-bold mb-1 text-center">KPI Performance vs Target</p>
              <ResponsiveContainer width="100%" height="100%">
                <RadarChart cx="50%" cy="50%" outerRadius="80%" data={kpiPerformance}>
                  <PolarGrid />
                  <PolarAngleAxis dataKey="subject" tick={{ fontSize: 8 }} />
                  <PolarRadiusAxis angle={30} domain={[0, 150]} tick={{ fontSize: 8 }} />
                  <Radar name="Target" dataKey="target" stroke="#8884d8" fill="#8884d8" fillOpacity={0.1} />
                  <Radar name="Actual" dataKey="actual" stroke="#82ca9d" fill="#82ca9d" fillOpacity={0.6} />
                  <Legend wrapperStyle={{ fontSize: 8 }} />
                  <Tooltip />
                </RadarChart>
              </ResponsiveContainer>
            </div>
          </div>
          
          <div className="grid grid-cols-2 gap-3 mt-3">
            {/* Payout Distribution */}
            <div className="h-40">
              <p className="text-sm font-bold mb-1 text-center">Current Payout Distribution</p>
              <ResponsiveContainer width="100%" height="100%">
                <BarChart
                  data={payoutDistribution}
                  margin={{ top: 5, right: 5, left: 5, bottom: 5 }}
                >
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="range" tick={{ fontSize: 10 }} />
                  <YAxis tick={{ fontSize: 10 }} />
                  <Tooltip />
                  <Bar dataKey="count" name="Reps">
                    {payoutDistribution.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
                    ))}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            </div>
            
            {/* Plan Component Visualization */}
            <div className="h-40 border border-gray-200 rounded-lg p-2">
              <p className="text-sm font-bold mb-1 text-center">Plan Component Analysis</p>
              <div className="flex flex-col h-full justify-center">
                <div className="relative h-6 rounded-lg overflow-hidden mb-1">
                  <div className="absolute left-0 top-0 h-full w-1/2 bg-blue-500 flex items-center">
                    <span className="text-white text-xs pl-1">Revenue (50%)</span>
                  </div>
                  <div className="absolute left-1/2 top-0 h-full w-1/5 bg-green-500 flex items-center">
                    <span className="text-white text-xs pl-1">Margin (20%)</span>
                  </div>
                  <div className="absolute left-7/10 top-0 h-full w-1/5 bg-purple-500 flex items-center">
                    <span className="text-white text-xs pl-1">Strat (20%)</span>
                  </div>
                  <div className="absolute left-9/10 top-0 h-full w-1/10 bg-yellow-500 flex items-center">
                    <span className="text-white text-xs pl-1">MBO (10%)</span>
                  </div>
                </div>
                <div className="text-xs italic text-center mt-1">Current weighting drives 82% focus on volume metrics</div>
                
                <div className="relative h-6 rounded-lg overflow-hidden mt-2 mb-1">
                  <div className="absolute left-0 top-0 h-full w-4/10 bg-blue-500 flex items-center">
                    <span className="text-white text-xs pl-1">Revenue (40%)</span>
                  </div>
                  <div className="absolute left-4/10 top-0 h-full w-2/10 bg-green-500 flex items-center">
                    <span className="text-white text-xs pl-1">Margin (20%)</span>
                  </div>
                  <div className="absolute left-6/10 top-0 h-full w-3/10 bg-purple-500 flex items-center">
                    <span className="text-white text-xs pl-1">Strategic (30%)</span>
                  </div>
                  <div className="absolute left-9/10 top-0 h-full w-1/10 bg-yellow-500 flex items-center">
                    <span className="text-white text-xs pl-1">MBO (10%)</span>
                  </div>
                </div>
                <div className="text-xs italic text-center">Recommended weighting to balance volume and value</div>
              </div>
            </div>
          </div>
        </div>
        
        {/* Anomaly Detection */}
        <div className="border-2 border-gray-300 rounded-lg p-3">
          <h2 className="text-lg font-bold mb-2">AI-Detected Compensation Anomalies</h2>
          
          <div className="overflow-auto max-h-52">
            <table className="w-full text-xs border-collapse">
              <thead className="bg-gray-100">
                <tr>
                  <th className="border border-gray-300 p-1 text-left">Rep/Group</th>
                  <th className="border border-gray-300 p-1 text-left">Metric</th>
                  <th className="border border-gray-300 p-1 text-left">Expected</th>
                  <th className="border border-gray-300 p-1 text-left">Actual</th>
                  <th className="border border-gray-300 p-1 text-left">Severity</th>
                </tr>
              </thead>
              <tbody>
                {anomalyData.map((item) => (
                  <tr key={item.id} className="hover:bg-gray-50">
                    <td className="border border-gray-300 p-1">{item.rep}</td>
                    <td className="border border-gray-300 p-1">{item.metric}</td>
                    <td className="border border-gray-300 p-1">{item.expected}</td>
                    <td className="border border-gray-300 p-1">{item.actual}</td>
                    <td className="border border-gray-300 p-1">
                      <span className={`px-1 py-0.5 rounded-full text-white ${
                        item.severity === "High" ? "bg-red-500" : "bg-yellow-500"
                      }`}>
                        {item.severity}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          
          <div className="mt-3">
            <h3 className="font-bold text-sm mb-1">Recommended Actions</h3>
            <div className="text-xs italic bg-gray-50 p-2 rounded border border-gray-200">
              <p className="font-bold">Commission Calculation Issue:</p>
              <p>{anomalyData[0].recommendation}</p>
              <div className="border-t border-gray-200 my-1"></div>
              <p className="font-bold">New Hire Ramp Period:</p>
              <p>{anomalyData[3].recommendation}</p>
            </div>
          </div>
          
          <div className="mt-3">
            <h3 className="font-bold text-sm mb-1">Automated Root Cause Analysis</h3>
            <div className="border border-gray-200 rounded-lg p-2">
              <div className="flex items-start">
                <div className="w-8 h-8 rounded-full bg-purple-100 border border-purple-500 flex items-center justify-center text-purple-800 font-bold text-xl mr-2">
                  AI
                </div>
                <div className="text-xs">
                  <p><span className="font-bold">SPIFF Effectiveness Issue:</span> Analysis of sales activity logs shows only 28% of reps were aware of the current SPIFF program. The communication was primarily done through email announcements that were not reinforced in sales meetings or CRM dashboards. Additionally, timing coincided with end-of-quarter focus, diminishing attention to new initiatives.</p>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        {/* Key Insights & Recommendations */}
        <div className="border-2 border-gray-300 rounded-lg p-3">
          <h2 className="text-lg font-bold mb-2">Real-Time Insights & Actions</h2>
          
          <div className="grid grid-cols-2 gap-2 mb-3">
            {insightCards.map((insight, index) => (
              <div key={index} className="bg-gray-50 rounded-lg p-2 border border-gray-200">
                <div className="flex items-start">
                  <div className="w-6 h-6 rounded-full bg-purple-600 text-white flex items-center justify-center font-bold text-sm mr-2 flex-shrink-0">
                    {index + 1}
                  </div>
                  <div>
                    <p className="font-bold text-sm">{insight.title}</p>
                    <p className="text-xs">{insight.description}</p>
                    <p className="text-xs mt-1"><span className="font-bold">Impact:</span> {insight.impact}</p>
                    <p className="text-xs italic mt-1"><span className="font-bold">Action:</span> {insight.action}</p>
                  </div>
                </div>
              </div>
            ))}
          </div>
          
          <h2 className="text-lg font-bold mb-2">Continuous Improvement Cycle</h2>
          <div className="border border-gray-300 rounded-lg p-2">
            <div className="flex justify-around items-center">
              <div className="text-center">
                <div className="w-16 h-16 rounded-full mx-auto flex items-center justify-center bg-blue-100 border-2 border-blue-500">
                  <p className="text-xs font-bold">Monitor</p>
                </div>
                <p className="text-xs mt-1">Real-time tracking</p>
              </div>
              <div className="h-0.5 w-8 bg-gray-400"></div>
              <div className="text-center">
                <div className="w-16 h-16 rounded-full mx-auto flex items-center justify-center bg-purple-100 border-2 border-purple-500">
                  <p className="text-xs font-bold">Analyze</p>
                </div>
                <p className="text-xs mt-1">Pattern detection</p>
              </div>
              <div className="h-0.5 w-8 bg-gray-400"></div>
              <div className="text-center">
                <div className="w-16 h-16 rounded-full mx-auto flex items-center justify-center bg-green-100 border-2 border-green-500">
                  <p className="text-xs font-bold">Recommend</p>
                </div>
                <p className="text-xs mt-1">Action guidance</p>
              </div>
              <div className="h-0.5 w-8 bg-gray-400"></div>
              <div className="text-center">
                <div className="w-16 h-16 rounded-full mx-auto flex items-center justify-center bg-yellow-100 border-2 border-yellow-500">
                  <p className="text-xs font-bold">Implement</p>
                </div>
                <p className="text-xs mt-1">Rapid deployment</p>
              </div>
            </div>
          </div>
          
          <div className="mt-3 bg-blue-50 rounded-lg p-2">
            <h3 className="font-bold text-sm">Value Delivery</h3>
            <div className="grid grid-cols-3 gap-2 mt-1">
              <div className="text-center">
                <p className="text-lg font-bold text-blue-700">82%</p>
                <p className="text-xs">Reduction in calculation errors</p>
              </div>
              <div className="text-center">
                <p className="text-lg font-bold text-blue-700">3.2x</p>
                <p className="text-xs">Faster issue resolution</p>
              </div>
              <div className="text-center">
                <p className="text-lg font-bold text-blue-700">$1.8M</p>
                <p className="text-xs">Saved in overpayments</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default RealTimeAnalysis;
