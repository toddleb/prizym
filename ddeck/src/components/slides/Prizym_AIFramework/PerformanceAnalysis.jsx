import React from 'react';
import { LineChart, Line, BarChart, Bar, PieChart, Pie, Cell, ScatterChart, Scatter, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, Label } from 'recharts';

const PerformanceAnalysis = () => {
  // Sample data for visualizations
  const salesTrendData = [
    { month: 'Jan', actual: 2.1, target: 2.4, industry: 2.3 },
    { month: 'Feb', actual: 2.3, target: 2.4, industry: 2.3 },
    { month: 'Mar', actual: 2.0, target: 2.5, industry: 2.4 },
    { month: 'Apr', actual: 2.2, target: 2.5, industry: 2.4 },
    { month: 'May', actual: 2.5, target: 2.6, industry: 2.4 },
    { month: 'Jun', actual: 2.1, target: 2.6, industry: 2.5 }
  ];
  
  const productMixData = [
    { name: 'Product A', value: 35 },
    { name: 'Product B', value: 25 },
    { name: 'Product C', value: 20 },
    { name: 'Product D', value: 15 },
    { name: 'Other', value: 5 }
  ];
  
  const salesCycleData = [
    { name: 'Lead Gen', avgDays: 12, bestPerformer: 7 },
    { name: 'Qualification', avgDays: 9, bestPerformer: 5 },
    { name: 'Discovery', avgDays: 14, bestPerformer: 8 },
    { name: 'Proposal', avgDays: 18, bestPerformer: 12 },
    { name: 'Negotiation', avgDays: 15, bestPerformer: 9 },
    { name: 'Closing', avgDays: 8, bestPerformer: 4 }
  ];
  
  const salesRepData = [
    { rep: 'Team A', deals: 42, avgValue: 78000, winRate: 32 },
    { rep: 'Team B', deals: 38, avgValue: 92000, winRate: 28 },
    { rep: 'Team C', deals: 29, avgValue: 115000, winRate: 24 },
    { rep: 'Team D', deals: 52, avgValue: 65000, winRate: 38 },
    { rep: 'Team E', deals: 34, avgValue: 88000, winRate: 29 }
  ];
  
  const keyFindings = [
    {
      title: "Inconsistent Pipeline Velocity",
      description: "76% longer sales cycles in EMEA vs. North America",
      insight: "Process bottlenecks identified in qualification and proposal stages"
    },
    {
      title: "Product Mix Optimization",
      description: "Over-reliance on Product A despite higher margins on C & D",
      insight: "Cross-selling opportunity with 35% of customers buying only one product"
    },
    {
      title: "Performance Distribution",
      description: "Top 20% of reps generate 53% of total revenue",
      insight: "Significant skill gap between top and bottom performers"
    },
    {
      title: "Activity vs. Outcomes",
      description: "High activity metrics don't correlate with success in 42% of reps",
      insight: "Quality of engagement more important than quantity"
    }
  ];
  
  const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884d8'];

  return (
    <div className="w-full h-full bg-white p-4 font-sans">
      <div className="flex justify-between items-center mb-4">
        <h1 className="text-2xl font-bold">Sales Performance Analysis</h1>
        <div className="flex items-center">
          <div className="h-8 w-8 bg-purple-600 rounded-full mr-2"></div>
          <div className="h-8 w-8 bg-blue-600 rounded-full"></div>
        </div>
      </div>
      
      <div className="grid grid-cols-2 gap-4">
        {/* Analysis Context & Methodology */}
        <div className="border-2 border-gray-300 rounded-lg p-3">
          <h2 className="text-lg font-bold mb-2">Analysis Context</h2>
          <div className="text-sm space-y-1 mb-3">
            <p>Global B2B technology provider with 150+ sales professionals</p>
            <p>Declining win rates and growing sales cycles over past 3 quarters</p>
            <p>Significant performance variance across regions and teams</p>
            <p>Preparing for compensation plan redesign initiative</p>
          </div>
          
          <h2 className="text-lg font-bold mb-2">AI-Powered Analysis Approach</h2>
          <div className="flex items-start mb-1">
            <div className="w-6 h-6 rounded-full bg-purple-600 text-white flex items-center justify-center font-bold mr-2 flex-shrink-0">1</div>
            <p className="text-sm">Deep analysis of 18 months of CRM data (15,000+ opportunities)</p>
          </div>
          <div className="flex items-start mb-1">
            <div className="w-6 h-6 rounded-full bg-purple-600 text-white flex items-center justify-center font-bold mr-2 flex-shrink-0">2</div>
            <p className="text-sm">Pattern recognition across sales stages, rep behaviors, and outcomes</p>
          </div>
          <div className="flex items-start mb-1">
            <div className="w-6 h-6 rounded-full bg-purple-600 text-white flex items-center justify-center font-bold mr-2 flex-shrink-0">3</div>
            <p className="text-sm">Integration with call transcripts, email sentiment, and customer feedback</p>
          </div>
          <div className="flex items-start">
            <div className="w-6 h-6 rounded-full bg-purple-600 text-white flex items-center justify-center font-bold mr-2 flex-shrink-0">4</div>
            <p className="text-sm">Benchmarking against industry standards and internal top performers</p>
          </div>
          
          <div className="mt-3 bg-blue-50 p-2 rounded-lg">
            <p className="text-sm font-bold">Data Sources Analyzed:</p>
            <div className="grid grid-cols-2 gap-2 text-xs mt-1">
              <div>• CRM opportunity data</div>
              <div>• Sales activity metrics</div>
              <div>• Call & meeting transcripts</div>
              <div>• Email communications</div>
              <div>• Product usage data</div>
              <div>• Customer support interactions</div>
              <div>• Win/loss interview reports</div>
              <div>• Competitor intelligence data</div>
            </div>
          </div>
        </div>
        
        {/* Sales Performance Visualizations */}
        <div className="border-2 border-gray-300 rounded-lg p-3">
          <h2 className="text-lg font-bold mb-2">Performance Analysis</h2>
          <div className="grid grid-cols-2 gap-3">
            {/* Sales Trends Chart */}
            <div className="h-40">
              <p className="text-sm font-bold mb-1 text-center">Sales Performance Trends</p>
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={salesTrendData} margin={{ top: 5, right: 5, left: 5, bottom: 5 }}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="month" tick={{ fontSize: 10 }} />
                  <YAxis tick={{ fontSize: 10 }}>
                    <Label value="$ Millions" angle={-90} position="insideLeft" style={{ textAnchor: 'middle', fontSize: 10 }} />
                  </YAxis>
                  <Tooltip />
                  <Legend wrapperStyle={{ fontSize: 8 }} />
                  <Line type="monotone" dataKey="actual" stroke="#8884d8" activeDot={{ r: 8 }} name="Actual" />
                  <Line type="monotone" dataKey="target" stroke="#82ca9d" strokeDasharray="5 5" name="Target" />
                  <Line type="monotone" dataKey="industry" stroke="#ffc658" strokeDasharray="3 3" name="Industry Avg" />
                </LineChart>
              </ResponsiveContainer>
            </div>
            
            {/* Product Mix Pie Chart */}
            <div className="h-40">
              <p className="text-sm font-bold mb-1 text-center">Revenue by Product</p>
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={productMixData}
                    cx="50%"
                    cy="50%"
                    innerRadius={30}
                    outerRadius={50}
                    fill="#8884d8"
                    paddingAngle={2}
                    dataKey="value"
                    label={({name, percent}) => `${name}: ${(percent * 100).toFixed(0)}%`}
                    labelLine={false}
                  >
                    {productMixData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
            </div>
          </div>
          
          <div className="grid grid-cols-2 gap-3 mt-3">
            {/* Sales Cycle Comparison */}
            <div className="h-40">
              <p className="text-sm font-bold mb-1 text-center">Sales Cycle Analysis (Days)</p>
              <ResponsiveContainer width="100%" height="100%">
                <BarChart
                  data={salesCycleData}
                  margin={{ top: 5, right: 5, left: 5, bottom: 5 }}
                >
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="name" tick={{ fontSize: 8 }} />
                  <YAxis tick={{ fontSize: 10 }} />
                  <Tooltip />
                  <Legend wrapperStyle={{ fontSize: 8 }} />
                  <Bar dataKey="avgDays" name="Avg. Days" fill="#8884d8" />
                  <Bar dataKey="bestPerformer" name="Top Performers" fill="#82ca9d" />
                </BarChart>
              </ResponsiveContainer>
            </div>
            
            {/* Sales Rep Performance */}
            <div className="h-40">
              <p className="text-sm font-bold mb-1 text-center">Team Performance Analysis</p>
              <ResponsiveContainer width="100%" height="100%">
                <ScatterChart
                  margin={{ top: 5, right: 5, left: 5, bottom: 5 }}
                >
                  <CartesianGrid />
                  <XAxis dataKey="winRate" name="Win Rate %" tick={{ fontSize: 10 }} />
                  <YAxis dataKey="avgValue" name="Avg Deal Value" tick={{ fontSize: 10 }} />
                  <Tooltip cursor={{ strokeDasharray: '3 3' }} />
                  <Scatter name="Teams" data={salesRepData} fill="#8884d8">
                    {salesRepData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                    ))}
                  </Scatter>
                </ScatterChart>
              </ResponsiveContainer>
            </div>
          </div>
        </div>
        
        {/* AI Pattern Recognition */}
        <div className="border-2 border-gray-300 rounded-lg p-3">
          <h2 className="text-lg font-bold mb-2">AI Pattern Recognition Insights</h2>
          
          <div className="bg-purple-50 rounded-lg p-2 mb-3">
            <h3 className="font-bold text-sm">Customer Engagement Patterns</h3>
            <div className="mt-1 flex items-center justify-center">
              <div className="relative h-28 w-full">
                {/* Visualization of engagement pattern recognition */}
                <div className="absolute top-1/4 left-1/5 h-4 w-20 bg-green-200 rounded"></div>
                <div className="absolute top-1/4 left-1/2 h-4 w-16 bg-yellow-200 rounded"></div>
                <div className="absolute top-1/4 left-4/5 h-4 w-8 bg-red-200 rounded"></div>
                
                <div className="absolute top-2/4 left-1/5 h-4 w-12 bg-green-300 rounded"></div>
                <div className="absolute top-2/4 left-1/2 h-4 w-20 bg-yellow-300 rounded"></div>
                <div className="absolute top-2/4 left-4/5 h-4 w-14 bg-red-300 rounded"></div>
                
                <div className="absolute top-3/4 left-1/5 h-4 w-8 bg-green-400 rounded"></div>
                <div className="absolute top-3/4 left-1/2 h-4 w-10 bg-yellow-400 rounded"></div>
                <div className="absolute top-3/4 left-4/5 h-4 w-24 bg-red-400 rounded"></div>
                
                {/* Labels */}
                <div className="absolute top-0 left-1/5 text-xs font-bold">Won Deals</div>
                <div className="absolute top-0 left-1/2 text-xs font-bold">Stalled Deals</div>
                <div className="absolute top-0 left-4/5 text-xs font-bold">Lost Deals</div>
                
                <div className="absolute left-0 top-1/4 text-xs font-bold">Discovery</div>
                <div className="absolute left-0 top-2/4 text-xs font-bold">Proposal</div>
                <div className="absolute left-0 top-3/4 text-xs font-bold">Negotiation</div>
              </div>
            </div>
            <p className="text-xs mt-1">AI identified distinct engagement patterns in successful deals: higher early-stage discovery engagement, more collaborative proposal development, and shorter negotiation phases.</p>
          </div>
          
          <div className="mb-3">
            <h3 className="font-bold text-sm mb-1">Critical Success Factors Identified</h3>
            <div className="grid grid-cols-2 gap-2">
              <div className="bg-blue-50 p-2 rounded-lg">
                <p className="text-xs font-bold">Executive Engagement</p>
                <p className="text-xs">Win rate increases 42% with C-suite involvement before proposal stage</p>
              </div>
              <div className="bg-green-50 p-2 rounded-lg">
                <p className="text-xs font-bold">Solution Demonstration</p>
                <p className="text-xs">Interactive demos increase conversion by 37% vs. presentation-only</p>
              </div>
              <div className="bg-yellow-50 p-2 rounded-lg">
                <p className="text-xs font-bold">Multi-threading</p>
                <p className="text-xs">Deals with 3+ stakeholder relationships close 28% faster</p>
              </div>
              <div className="bg-purple-50 p-2 rounded-lg">
                <p className="text-xs font-bold">Follow-up Timing</p>
                <p className="text-xs">24-hour response time increases progression rates by 35%</p>
              </div>
            </div>
          </div>
          
          <h3 className="font-bold text-sm mb-1">Communication Analysis</h3>
          <div className="border border-gray-300 rounded-lg p-2">
            <div className="flex justify-between text-xs font-bold border-b border-gray-200 pb-1 mb-1">
              <div>Top Performer Language Patterns</div>
              <div>Low Performer Language Patterns</div>
            </div>
            <div className="flex justify-between text-xs">
              <ul className="list-disc pl-4 pr-2">
                <li>Value-oriented discussions (ROI, outcomes)</li>
                <li>Active listening indicators (follow-up questions)</li>
                <li>Collaborative language ("we", "together")</li>
                <li>Specific next steps with timeframes</li>
              </ul>
              <ul className="list-disc pl-4">
                <li>Feature-focused presentations</li>
                <li>Overuse of technical jargon</li>
                <li>Self-referential language ("I", "our product")</li>
                <li>Vague or absent action commitments</li>
              </ul>
            </div>
          </div>
        </div>
        
        {/* Key Findings & Next Steps */}
        <div className="border-2 border-gray-300 rounded-lg p-3">
          <h2 className="text-lg font-bold mb-2">Key Findings & Recommendations</h2>
          
          <div className="space-y-2 mb-3">
            {keyFindings.map((finding, index) => (
              <div key={index} className="border-l-4 border-blue-500 pl-2">
                <p className="font-bold text-sm">{finding.title}</p>
                <p className="text-xs">{finding.description}</p>
                <p className="text-xs italic">Insight: {finding.insight}</p>
              </div>
            ))}
          </div>
          
          <h2 className="text-lg font-bold mb-2">Recommended Actions Before Compensation Redesign</h2>
          <div className="bg-gray-100 rounded-lg p-2">
            <ul className="text-sm list-disc pl-4 space-y-1">
              <li><span className="font-bold">Process Standardization:</span> Implement structured discovery and proposal processes based on top performer patterns</li>
              <li><span className="font-bold">Enablement Focus:</span> Develop training on identified success factors before changing compensation</li>
              <li><span className="font-bold">Activity Alignment:</span> Redefine KPIs to track quality metrics that correlate with success</li>
              <li><span className="font-bold">Product Strategy:</span> Address product mix imbalance through targeted enablement and incentives</li>
            </ul>
          </div>
          
          <div className="mt-3 bg-purple-100 rounded-lg p-2">
            <p className="text-sm font-bold">Next Phase: Compensation Plan Analysis</p>
            <p className="text-xs">This foundational sales performance analysis provides critical context for the compensation plan review. Findings will inform incentive structure design to reward behaviors that drive success rather than just activities.</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PerformanceAnalysis;
