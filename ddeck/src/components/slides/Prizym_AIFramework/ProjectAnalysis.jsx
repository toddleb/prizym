import React from 'react';
import { LineChart, Line, BarChart, Bar, ComposedChart, Area, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, Label, ScatterChart, Scatter } from 'recharts';
import { ArrowRight, AlertTriangle, CheckCircle, Clock, Calendar, Activity, Users, FileText, Briefcase } from 'lucide-react';

const ProjectAnalysis = () => {
  // Sample data for visualizations
  const projectTimeline = [
    { phase: 'Kickoff', planned: 10, actual: 12, complete: 100 },
    { phase: 'Discovery', planned: 25, actual: 32, complete: 100 },
    { phase: 'Requirements', planned: 20, actual: 24, complete: 100 },
    { phase: 'Design', planned: 30, actual: 35, complete: 80 },
    { phase: 'Build', planned: 45, actual: 22, complete: 45 },
    { phase: 'Test', planned: 30, actual: 0, complete: 0 },
    { phase: 'Deploy', planned: 15, actual: 0, complete: 0 }
  ];
  
  const resourceAllocation = [
    { role: 'Project Manager', planned: 120, actual: 145, variance: 25 },
    { role: 'Business Analyst', planned: 280, actual: 315, variance: 35 },
    { role: 'Solution Architect', planned: 160, actual: 185, variance: 25 },
    { role: 'Developer', planned: 450, actual: 380, variance: -70 },
    { role: 'Data Scientist', planned: 180, actual: 95, variance: -85 },
    { role: 'QA Engineer', planned: 200, actual: 85, variance: -115 }
  ];
  
  const deliverableStatus = [
    { name: 'Requirements Doc', progress: 100, status: 'Complete', riskLevel: 'Low' },
    { name: 'Architecture Design', progress: 95, status: 'In Review', riskLevel: 'Low' },
    { name: 'Data Models', progress: 85, status: 'In Progress', riskLevel: 'Medium' },
    { name: 'Core Engine', progress: 60, status: 'In Progress', riskLevel: 'High' },
    { name: 'UI Components', progress: 40, status: 'In Progress', riskLevel: 'Medium' },
    { name: 'API Integration', progress: 25, status: 'In Progress', riskLevel: 'High' },
    { name: 'Documentation', progress: 30, status: 'In Progress', riskLevel: 'Low' }
  ];
  
  const riskAnalysis = [
    { 
      id: 1,
      category: "Resource",
      issue: "Developer Availability",
      impact: "Potential 2-week delay in core components",
      probability: "High",
      mitigation: "Reassign 2 developers from Team B to address critical path items"
    },
    { 
      id: 2,
      category: "Technical",
      issue: "API Integration Complexity",
      impact: "Additional effort for legacy system integration",
      probability: "Medium",
      mitigation: "Create adapter layer to simplify integration points"
    },
    { 
      id: 3,
      category: "Client",
      issue: "Requirements Expansion",
      impact: "Scope creep in reporting module",
      probability: "High",
      mitigation: "Document change requests and propose Phase 2 additions"
    },
    { 
      id: 4,
      category: "Timeline",
      issue: "Testing Environment Readiness",
      impact: "Delayed QA start",
      probability: "Medium",
      mitigation: "Develop containerized test environment independent of client infrastructure"
    }
  ];
  
  const qualityMetrics = [
    { metric: 'Requirements Coverage', score: 92, benchmark: 85 },
    { metric: 'Design Reviews Completed', score: 88, benchmark: 90 },
    { metric: 'Code Quality', score: 78, benchmark: 85 },
    { metric: 'Test Case Coverage', score: 65, benchmark: 80 },
    { metric: 'Documentation Quality', score: 75, benchmark: 75 }
  ];
  
  const communicationAnalysis = [
    { week: 'Week 1', clientSentiment: 90, teamAlignment: 85, issueResolution: 95 },
    { week: 'Week 2', clientSentiment: 88, teamAlignment: 82, issueResolution: 90 },
    { week: 'Week 3', clientSentiment: 85, teamAlignment: 80, issueResolution: 82 },
    { week: 'Week 4', clientSentiment: 75, teamAlignment: 72, issueResolution: 78 },
    { week: 'Week 5', clientSentiment: 72, teamAlignment: 68, issueResolution: 65 },
    { week: 'Week 6', clientSentiment: 65, teamAlignment: 62, issueResolution: 60 }
  ];

  const getStatusColor = (status) => {
    switch(status) {
      case 'Complete': return '#4CAF50';
      case 'In Review': return '#2196F3';
      case 'In Progress': return '#FF9800';
      case 'Not Started': return '#9E9E9E';
      default: return '#9E9E9E';
    }
  };

  const getRiskColor = (risk) => {
    switch(risk) {
      case 'Low': return '#4CAF50';
      case 'Medium': return '#FF9800';
      case 'High': return '#F44336';
      default: return '#9E9E9E';
    }
  };

  return (
    <div className="w-full h-full bg-white p-4 font-sans">
      <div className="flex justify-between items-center mb-4">
        <h1 className="text-2xl font-bold">AI-Powered Consulting Project Analysis</h1>
        <div className="flex items-center">
          <div className="h-8 w-8 bg-purple-600 rounded-full mr-2"></div>
          <div className="h-8 w-8 bg-blue-600 rounded-full"></div>
        </div>
      </div>
      
      <div className="grid grid-cols-2 gap-4">
        {/* Project Overview */}
        <div className="border-2 border-gray-300 rounded-lg p-3">
          <h2 className="text-lg font-bold mb-2">Enterprise CRM Transformation</h2>
          <div className="text-sm space-y-1 mb-3">
            <p>Global financial services firm implementing new client management platform</p>
            <p>6-month project timeline with 25+ team members across 3 workstreams</p>
            <p>Currently in month 4 (Design/Build phase) with some emerging concerns</p>
            <p>Critical go-live date tied to regulatory compliance requirements</p>
          </div>
          
          <h2 className="text-lg font-bold mb-2">Prizym.ai LENS Project Analysis</h2>
          <div className="grid grid-cols-2 gap-2 mb-3">
            <div className="bg-blue-50 rounded-lg p-2 flex items-center">
              <Calendar size={24} className="text-blue-500 mr-2" />
              <div>
                <p className="font-bold text-sm">Timeline Status</p>
                <p className="text-xs">72% through timeline</p>
                <p className="text-xs">58% completion</p>
              </div>
            </div>
            <div className="bg-purple-50 rounded-lg p-2 flex items-center">
              <Users size={24} className="text-purple-500 mr-2" />
              <div>
                <p className="font-bold text-sm">Resource Variance</p>
                <p className="text-xs">-12% development hours</p>
                <p className="text-xs">+22% management hours</p>
              </div>
            </div>
            <div className="bg-yellow-50 rounded-lg p-2 flex items-center">
              <Activity size={24} className="text-yellow-500 mr-2" />
              <div>
                <p className="font-bold text-sm">Risk Assessment</p>
                <p className="text-xs">Medium-High overall</p>
                <p className="text-xs">3 critical path issues</p>
              </div>
            </div>
            <div className="bg-green-50 rounded-lg p-2 flex items-center">
              <Clock size={24} className="text-green-500 mr-2" />
              <div>
                <p className="font-bold text-sm">Forecast</p>
                <p className="text-xs">80% probability of delay</p>
                <p className="text-xs">2-3 week estimated impact</p>
              </div>
            </div>
          </div>
          
          <div className="h-48 mb-2">
            <p className="text-sm font-bold mb-1 text-center">Project Timeline Analysis</p>
            <ResponsiveContainer width="100%" height="100%">
              <ComposedChart data={projectTimeline} margin={{ top: 5, right: 5, left: 5, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="phase" tick={{ fontSize: 10 }} />
                <YAxis yAxisId="left" orientation="left" tick={{ fontSize: 10 }}>
                  <Label value="Days" angle={-90} position="insideLeft" style={{ textAnchor: 'middle', fontSize: 10 }} />
                </YAxis>
                <YAxis yAxisId="right" orientation="right" domain={[0, 100]} tick={{ fontSize: 10 }}>
                  <Label value="% Complete" angle={90} position="insideRight" style={{ textAnchor: 'middle', fontSize: 10 }} />
                </YAxis>
                <Tooltip />
                <Legend wrapperStyle={{ fontSize: 8 }} />
                <Bar yAxisId="left" dataKey="planned" name="Planned Days" fill="#8884d8" />
                <Bar yAxisId="left" dataKey="actual" name="Actual Days" fill="#82ca9d" />
                <Line yAxisId="right" type="monotone" dataKey="complete" name="% Complete" stroke="#ff7300" />
              </ComposedChart>
            </ResponsiveContainer>
          </div>
        </div>
        
        {/* Resource Analysis */}
        <div className="border-2 border-gray-300 rounded-lg p-3">
          <h2 className="text-lg font-bold mb-2">Resource Utilization & Deliverables</h2>
          <div className="h-40 mb-3">
            <p className="text-sm font-bold mb-1 text-center">Resource Allocation (Hours)</p>
            <ResponsiveContainer width="100%" height="100%">
              <BarChart
                data={resourceAllocation}
                layout="vertical"
                margin={{ top: 5, right: 30, left: 80, bottom: 5 }}
              >
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis type="number" />
                <YAxis dataKey="role" type="category" tick={{ fontSize: 10 }} width={80} />
                <Tooltip />
                <Legend wrapperStyle={{ fontSize: 8 }} />
                <Bar dataKey="planned" name="Planned Hours" fill="#8884d8" />
                <Bar dataKey="actual" name="Actual Hours" fill="#82ca9d" />
              </BarChart>
            </ResponsiveContainer>
          </div>
          
          <div className="mb-3">
            <h3 className="font-bold text-sm mb-1">Deliverable Status</h3>
            <div className="overflow-auto max-h-48">
              <table className="w-full text-xs border-collapse">
                <thead className="bg-gray-100">
                  <tr>
                    <th className="border border-gray-300 p-1 text-left">Deliverable</th>
                    <th className="border border-gray-300 p-1 text-left">Progress</th>
                    <th className="border border-gray-300 p-1 text-left">Status</th>
                    <th className="border border-gray-300 p-1 text-left">Risk</th>
                  </tr>
                </thead>
                <tbody>
                  {deliverableStatus.map((item, index) => (
                    <tr key={index} className="hover:bg-gray-50">
                      <td className="border border-gray-300 p-1">{item.name}</td>
                      <td className="border border-gray-300 p-1">
                        <div className="w-full bg-gray-200 rounded-full h-2.5">
                          <div 
                            className="h-2.5 rounded-full" 
                            style={{ 
                              width: `${item.progress}%`,
                              backgroundColor: getStatusColor(item.status)
                            }}
                          ></div>
                        </div>
                      </td>
                      <td className="border border-gray-300 p-1">
                        <span className="px-1 py-0.5 rounded-full text-xs" style={{ 
                          backgroundColor: getStatusColor(item.status),
                          color: item.status === 'Not Started' ? 'black' : 'white'
                        }}>
                          {item.status}
                        </span>
                      </td>
                      <td className="border border-gray-300 p-1">
                        <span className="px-1 py-0.5 rounded-full text-xs text-white" style={{ 
                          backgroundColor: getRiskColor(item.riskLevel)
                        }}>
                          {item.riskLevel}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
        
        {/* Risk & Issue Analysis */}
        <div className="border-2 border-gray-300 rounded-lg p-3">
          <h2 className="text-lg font-bold mb-2">AI-Detected Risks & Quality Analysis</h2>
          
          <div className="grid grid-cols-2 gap-4 mb-4">
            <div>
              <h3 className="font-bold text-sm mb-1">Quality Metrics</h3>
              <div className="h-40">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart
                    data={qualityMetrics}
                    margin={{ top: 5, right: 5, left: 5, bottom: 5 }}
                    layout="vertical"
                  >
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis type="number" domain={[0, 100]} />
                    <YAxis dataKey="metric" type="category" tick={{ fontSize: 9 }} width={100} />
                    <Tooltip />
                    <Legend wrapperStyle={{ fontSize: 8 }} />
                    <Bar dataKey="score" name="Current Score" fill="#8884d8" />
                    <Bar dataKey="benchmark" name="Benchmark" fill="#82ca9d" />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>
            
            <div>
              <h3 className="font-bold text-sm mb-1">Communication Analysis</h3>
              <div className="h-40">
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart data={communicationAnalysis} margin={{ top: 5, right: 5, left: 5, bottom: 5 }}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="week" tick={{ fontSize: 9 }} />
                    <YAxis domain={[50, 100]} tick={{ fontSize: 9 }} />
                    <Tooltip />
                    <Legend wrapperStyle={{ fontSize: 8 }} />
                    <Line type="monotone" dataKey="clientSentiment" stroke="#8884d8" name="Client Sentiment" />
                    <Line type="monotone" dataKey="teamAlignment" stroke="#82ca9d" name="Team Alignment" />
                    <Line type="monotone" dataKey="issueResolution" stroke="#ffc658" name="Issue Resolution" />
                  </LineChart>
                </ResponsiveContainer>
              </div>
            </div>
          </div>
          
          <div className="mb-3">
            <h3 className="font-bold text-sm mb-1">AI-Detected Risks</h3>
            <div className="space-y-2">
              {riskAnalysis.map((risk) => (
                <div key={risk.id} className="bg-gray-50 rounded-lg p-2 border-l-4" style={{ borderColor: risk.probability === "High" ? "#F44336" : "#FF9800" }}>
                  <div className="flex justify-between items-start">
                    <p className="font-bold text-sm">{risk.category}: {risk.issue}</p>
                    <span className="text-xs px-1 py-0.5 rounded-full text-white" style={{ 
                      backgroundColor: risk.probability === "High" ? "#F44336" : "#FF9800" 
                    }}>
                      {risk.probability}
                    </span>
                  </div>
                  <p className="text-xs"><span className="font-bold">Impact:</span> {risk.impact}</p>
                  <p className="text-xs italic"><span className="font-bold">Mitigation:</span> {risk.mitigation}</p>
                </div>
              ))}
            </div>
          </div>
        </div>
        
        {/* AI Insights & Recommendations */}
        <div className="border-2 border-gray-300 rounded-lg p-3">
          <h2 className="text-lg font-bold mb-2">AI Insights & Recommendations</h2>
          
          <div className="border-l-4 border-purple-500 pl-2 mb-3">
            <div className="flex items-start">
              <AlertTriangle size={16} className="text-purple-600 mr-1 mt-0.5" />
              <div>
                <p className="font-bold text-sm">Resource Misalignment Detected</p>
                <p className="text-xs">Technical resources are 24% below plan while management overhead is 18% above plan. Analysis of project artifacts shows excessive review cycles and documentation rework taking developer time.</p>
                <p className="text-xs italic mt-1"><span className="font-bold">Recommendation:</span> Implement streamlined approval workflow and reassign 2 senior developers from supporting workstream to core development.</p>
              </div>
            </div>
          </div>
          
          <div className="border-l-4 border-blue-500 pl-2 mb-3">
            <div className="flex items-start">
              <AlertTriangle size={16} className="text-blue-600 mr-1 mt-0.5" />
              <div>
                <p className="font-bold text-sm">Communication Pattern Breakdown</p>
                <p className="text-xs">Natural language processing of meeting notes and email threads shows declining client alignment starting in Week 4, coinciding with key architecture decisions. Client feedback sentiment analysis shows concerns about technical approach not adequately addressed.</p>
                <p className="text-xs italic mt-1"><span className="font-bold">Recommendation:</span> Schedule technical review session with client architecture team to address concerns and document agreements.</p>
              </div>
            </div>
          </div>
          
          <div className="border-l-4 border-green-500 pl-2 mb-3">
            <div className="flex items-start">
              <AlertTriangle size={16} className="text-green-600 mr-1 mt-0.5" />
              <div>
                <p className="font-bold text-sm">Critical Path Risk</p>
                <p className="text-xs">API integration deliverable shows only 25% completion despite 72% timeline elapsed. Dependency analysis confirms this is blocking 3 downstream deliverables. Documentation quality metrics show insufficient technical specifications for development team.</p>
                <p className="text-xs italic mt-1"><span className="font-bold">Recommendation:</span> Implement daily stand-up specifically for API workstream and supplement team with integration specialist from available resource pool.</p>
              </div>
            </div>
          </div>
          
          <div className="bg-gray-100 rounded-lg p-2">
            <h3 className="font-bold text-sm mb-1">Timeline Impact Analysis</h3>
            <div className="flex items-start">
              <div className="w-12 h-12 rounded-full bg-yellow-100 border-2 border-yellow-500 flex items-center justify-center text-yellow-800 font-bold text-xl mr-2 flex-shrink-0">
                18d
              </div>
              <div>
                <p className="text-xs">Based on current velocity, critical path analysis, and historical patterns, the AI projects an 18-day delay to final delivery unless corrective actions are taken immediately.</p>
                <div className="flex items-center mt-1">
                  <CheckCircle size={14} className="text-green-500 mr-1" />
                  <p className="text-xs font-bold">Implementing recommendations could reduce delay to 5-7 days</p>
                </div>
              </div>
            </div>
          </div>
          
          <div className="mt-3">
            <h3 className="font-bold text-sm mb-1">Next Steps</h3>
            <div className="text-xs">
              <div className="flex items-start mb-1">
                <div className="w-5 h-5 rounded-full bg-purple-600 text-white flex items-center justify-center font-bold mr-1 flex-shrink-0">1</div>
                <p>Conduct emergency resource planning session (Tomorrow, 10:00 AM)</p>
              </div>
              <div className="flex items-start mb-1">
                <div className="w-5 h-5 rounded-full bg-purple-600 text-white flex items-center justify-center font-bold mr-1 flex-shrink-0">2</div>
                <p>Technical alignment review with client architecture team (Thursday)</p>
              </div>
              <div className="flex items-start">
                <div className="w-5 h-5 rounded-full bg-purple-600 text-white flex items-center justify-center font-bold mr-1 flex-shrink-0">3</div>
                <p>Revise project plan and obtain client sign-off on timeline adjustment</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProjectAnalysis;