import React from 'react';
import { Target, Users, TrendingUp, Award, BookOpen, Monitor, MessageSquare, Briefcase } from 'lucide-react';

const G2M = () => {
  const colors = {
    prizm: {
      primary: "#7B3FC4",
      light: "#EEDDFF",
      border: "#5A2CA0"
    },
    kpmg: {
      primary: "#0073C6",
      light: "#DCE8F7",
      border: "#0B5EA8"
    },
    joint: {
      primary: "#6A3DB8",
      light: "#E5E0EE",
      border: "#000000"
    }
  };

  const targetSegments = [
    {
      name: "Enterprise Financial Services",
      fit: "High",
      description: "Large banks & insurance firms seeking competitive advantage through AI",
      painPoints: "Regulatory pressure, legacy systems, data silos",
      fitReason: "Complex workflows & high-value decisions benefit most from AI framework",
      entryPoint: "SPM, Workforce Optimization"
    },
    {
      name: "Mid-Market Healthcare",
      fit: "Medium",
      description: "Regional healthcare providers & payers looking to optimize operations",
      painPoints: "Staff shortages, patient experience, operational inefficiency",
      fitReason: "Strong need but longer sales cycle due to compliance concerns",
      entryPoint: "Career Planning, Lead Generation"
    },
    {
      name: "Tech-Forward Manufacturing",
      fit: "High",
      description: "Manufacturers investing in digital transformation initiatives",
      painPoints: "Supply chain disruption, workforce challenges, cost pressure",
      fitReason: "Clear ROI path with measurable operational improvements",
      entryPoint: "SPM, Workforce Optimization"
    },
    {
      name: "Professional Services",
      fit: "Medium",
      description: "Consulting, legal and accounting firms seeking efficiency",
      painPoints: "Talent retention, knowledge management, client acquisition",
      fitReason: "Direct alignment with Career Planning and Lead Generation solutions",
      entryPoint: "Career Planning, Lead Generation"
    }
  ];

  const salesEnablement = [
    {
      title: "Value Proposition Deck",
      description: "Comprehensive slides with clear value messaging by industry",
      owner: "Joint",
      status: "Complete"
    },
    {
      title: "Technical Deep Dive",
      description: "Framework architecture and capabilities for technical stakeholders",
      owner: "Prizym",
      status: "Complete"
    },
    {
      title: "ROI Calculator",
      description: "Interactive tool to estimate client-specific returns",
      owner: "KPMG",
      status: "In Progress"
    },
    {
      title: "Demo Environment",
      description: "Sandbox with pre-populated data for common use cases",
      owner: "Prizym",
      status: "In Progress"
    },
    {
      title: "Case Studies",
      description: "Detailed success stories from early implementations",
      owner: "Joint",
      status: "Planned"
    }
  ];

  const marketingActivities = [
    {
      quarter: "Q2 2025",
      activity: "Thought Leadership Series",
      description: "5-part whitepaper series on AI decision frameworks",
      owner: "Joint",
      channels: "Website, LinkedIn, Direct Mail"
    },
    {
      quarter: "Q2 2025",
      activity: "Industry Conference",
      description: "Speaking engagement at Financial Innovation Summit",
      owner: "KPMG",
      channels: "In-person, Livestream"
    },
    {
      quarter: "Q3 2025",
      activity: "Executive Roundtables",
      description: "Intimate discussions with C-suite prospects in target industries",
      owner: "KPMG",
      channels: "In-person, Virtual"
    },
    {
      quarter: "Q3 2025",
      activity: "Technical Webinar Series",
      description: "Deep dives into AI capabilities and integration approaches",
      owner: "Prizym",
      channels: "Webinar, YouTube"
    },
    {
      quarter: "Q4 2025",
      activity: "Client Showcase Event",
      description: "Early adopters sharing success stories and results",
      owner: "Joint",
      channels: "In-person, Livestream"
    }
  ];

  const renderTargetSegment = (segment, index) => (
    <div key={index} className="border-2 rounded-lg p-3 mb-3" style={{ borderColor: segment.fit === "High" ? colors.joint.primary : "#888888" }}>
      <div className="flex justify-between items-start">
        <h3 className="font-bold">{segment.name}</h3>
        <div className="px-2 py-1 rounded-full text-xs text-white" style={{ 
          backgroundColor: segment.fit === "High" ? "#4CAF50" : "#FF9800" 
        }}>
          {segment.fit} Fit
        </div>
      </div>
      
      <p className="text-sm mb-2">{segment.description}</p>
      
      <div className="grid grid-cols-2 gap-2 text-sm">
        <div>
          <p className="font-bold">Pain Points:</p>
          <p className="text-xs">{segment.painPoints}</p>
        </div>
        <div>
          <p className="font-bold">Fit Rationale:</p>
          <p className="text-xs">{segment.fitReason}</p>
        </div>
      </div>
      
      <div className="mt-2 text-sm">
        <span className="font-bold">Entry Point Solutions:</span> {segment.entryPoint}
      </div>
    </div>
  );

  const renderSalesEnablement = () => (
    <div className="border-2 border-gray-300 rounded-lg p-3">
      <h3 className="font-bold mb-2">Sales Enablement Materials</h3>
      <div className="space-y-2">
        {salesEnablement.map((item, index) => (
          <div key={index} className="flex justify-between items-center border-b border-gray-200 pb-2 last:border-0 last:pb-0">
            <div>
              <p className="font-bold">{item.title}</p>
              <p className="text-xs">{item.description}</p>
            </div>
            <div className="flex items-center space-x-2">
              <div className="text-xs px-2 py-1 rounded-full" style={{ 
                backgroundColor: 
                  item.owner === "Prizym" ? colors.prizm.light : 
                  item.owner === "KPMG" ? colors.kpmg.light : 
                  colors.joint.light,
                color: 
                  item.owner === "Prizym" ? colors.prizm.primary : 
                  item.owner === "KPMG" ? colors.kpmg.primary : 
                  colors.joint.primary
              }}>
                {item.owner}
              </div>
              <div className="text-xs px-2 py-1 rounded-full" style={{
                backgroundColor: 
                  item.status === "Complete" ? "#E8F5E9" : 
                  item.status === "In Progress" ? "#FFF3E0" : 
                  "#ECEFF1",
                color: 
                  item.status === "Complete" ? "#2E7D32" : 
                  item.status === "In Progress" ? "#E65100" : 
                  "#546E7A"
              }}>
                {item.status}
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );

  const renderMarketingPlan = () => (
    <div className="border-2 border-gray-300 rounded-lg p-3">
      <h3 className="font-bold mb-2">Marketing & Thought Leadership</h3>
      <div className="space-y-3">
        {marketingActivities.map((activity, index) => (
          <div key={index} className="flex items-start">
            <div className="w-16 flex-shrink-0 text-center">
              <div className="text-xs font-bold p-1 rounded" style={{ backgroundColor: "#E0E0E0" }}>
                {activity.quarter}
              </div>
            </div>
            <div className="flex-grow ml-2 pb-3 border-b border-gray-200 last:border-0 last:pb-0">
              <div className="flex justify-between">
                <h4 className="font-bold">{activity.activity}</h4>
                <div className="text-xs px-2 py-1 rounded-full" style={{ 
                  backgroundColor: 
                    activity.owner === "Prizym" ? colors.prizm.light : 
                    activity.owner === "KPMG" ? colors.kpmg.light : 
                    colors.joint.light,
                  color: 
                    activity.owner === "Prizym" ? colors.prizm.primary : 
                    activity.owner === "KPMG" ? colors.kpmg.primary : 
                    colors.joint.primary
                }}>
                  {activity.owner}
                </div>
              </div>
              <p className="text-sm">{activity.description}</p>
              <p className="text-xs mt-1"><span className="font-bold">Channels:</span> {activity.channels}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );

  const renderPartnerEnablement = () => (
    <div className="border-2 border-gray-300 rounded-lg p-3">
      <h3 className="font-bold mb-2">Partnership Enablement Program</h3>
      <div className="grid grid-cols-2 gap-3">
        <div className="border-l-4 p-2" style={{ borderColor: colors.kpmg.primary }}>
          <h4 className="font-bold">KPMG Team Training</h4>
          <ul className="text-xs list-disc pl-4">
            <li>Technical certification program</li>
            <li>Value proposition workshops</li>
            <li>Implementation methodology training</li>
            <li>Demos & roleplay sessions</li>
          </ul>
        </div>
        
        <div className="border-l-4 p-2" style={{ borderColor: colors.prizm.primary }}>
          <h4 className="font-bold">Prizym Team Training</h4>
          <ul className="text-xs list-disc pl-4">
            <li>Consulting methodology overview</li>
            <li>Enterprise sales process training</li>
            <li>Client success management</li>
            <li>Industry-specific modules</li>
          </ul>
        </div>
        
        <div className="border-l-4 p-2" style={{ borderColor: colors.joint.primary }}>
          <h4 className="font-bold">Joint Activities</h4>
          <ul className="text-xs list-disc pl-4">
            <li>Quarterly planning sessions</li>
            <li>Pipeline review meetings</li>
            <li>Success story documentation</li>
            <li>Cross-team shadowing</li>
          </ul>
        </div>
        
        <div className="border-l-4 p-2" style={{ borderColor: "#888888" }}>
          <h4 className="font-bold">Metrics & KPIs</h4>
          <ul className="text-xs list-disc pl-4">
            <li>Certification completion rates</li>
            <li>Joint pipeline growth</li>
            <li>Win rates by team composition</li>
            <li>Implementation efficiency</li>
          </ul>
        </div>
      </div>
    </div>
  );

  return (
    <div className="w-full h-full bg-white p-4 font-sans">
      <h1 className="text-2xl font-bold mb-4 text-center">Go-to-Market Strategy</h1>
      
      <div className="grid grid-cols-2 gap-4">
        {/* Left Column */}
        <div>
          <div className="flex items-center mb-3">
            <Target size={20} className="mr-2" />
            <h2 className="text-xl font-bold">Target Market Segments</h2>
          </div>
          
          <div className="space-y-1">
            {targetSegments.map(renderTargetSegment)}
          </div>
          
          <div className="mt-4">
            <div className="flex items-center mb-3">
              <Users size={20} className="mr-2" />
              <h2 className="text-xl font-bold">Ideal Client Profile</h2>
            </div>
            
            <div className="border-2 border-gray-300 rounded-lg p-3">
              <div className="grid grid-cols-2 gap-3">
                <div className="flex items-start">
                  <TrendingUp size={18} className="mr-2 text-green-600 flex-shrink-0" />
                  <div>
                    <h4 className="font-bold">Growth Oriented</h4>
                    <p className="text-xs">Actively investing in digital transformation initiatives</p>
                  </div>
                </div>
                
                <div className="flex items-start">
                  <Award size={18} className="mr-2 text-purple-600 flex-shrink-0" />
                  <div>
                    <h4 className="font-bold">Innovation Culture</h4>
                    <p className="text-xs">Willing to adopt new approaches and technologies</p>
                  </div>
                </div>
                
                <div className="flex items-start">
                  <BookOpen size={18} className="mr-2 text-blue-600 flex-shrink-0" />
                  <div>
                    <h4 className="font-bold">Data Maturity</h4>
                    <p className="text-xs">Has quality data assets and basic analytics capabilities</p>
                  </div>
                </div>
                
                <div className="flex items-start">
                  <Monitor size={18} className="mr-2 text-orange-600 flex-shrink-0" />
                  <div>
                    <h4 className="font-bold">Technical Readiness</h4>
                    <p className="text-xs">Flexible IT infrastructure with API capabilities</p>
                  </div>
                </div>
              </div>
              
              <div className="mt-3 border-t border-gray-200 pt-3">
                <h4 className="font-bold">Revenue & Organization</h4>
                <p className="text-sm">Primary: $500M+ enterprise accounts with complex decision processes</p>
                <p className="text-sm">Secondary: $100M-500M mid-market with tech-forward leadership</p>
              </div>
            </div>
          </div>
        </div>
        
        {/* Right Column */}
        <div>
          <div className="mb-4">
            <div className="flex items-center mb-3">
              <Briefcase size={20} className="mr-2" />
              <h2 className="text-xl font-bold">Sales Strategy</h2>
            </div>
            
            {renderSalesEnablement()}
          </div>
          
          <div className="mb-4">
            <div className="flex items-center mb-3">
              <MessageSquare size={20} className="mr-2" />
              <h2 className="text-xl font-bold">Marketing Plan</h2>
            </div>
            
            {renderMarketingPlan()}
          </div>
          
          <div>
            <div className="flex items-center mb-3">
              <Users size={20} className="mr-2" />
              <h2 className="text-xl font-bold">Partner Enablement</h2>
            </div>
            
            {renderPartnerEnablement()}
          </div>
        </div>
      </div>
    </div>
  );
};

export default G2M;
