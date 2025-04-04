import React from 'react';
import { Calendar, ArrowRight, Star, TrendingUp, Compass, Zap, Gift, Target, Users } from 'lucide-react';

const TechRoadmap = () => {
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
    },
    timeline: {
      q1: "#F8BBD0",
      q2: "#C8E6C9",
      q3: "#BBDEFB",
      q4: "#D1C4E9"
    }
  };

  const roadmapItems = [
    {
      quarter: "Q2 2025",
      category: "Framework Enhancement",
      title: "Enhanced Consensus Engine",
      description: "Improved multi-model aggregation with confidence scoring",
      owner: "Prizym",
      color: colors.prizm.primary,
      icon: <Zap size={16} />
    },
    {
      quarter: "Q2 2025",
      category: "Domain Expansion",
      title: "SPM 2.0 Release",
      description: "Advanced forecasting and scenario planning capabilities",
      owner: "Joint",
      color: colors.joint.primary,
      icon: <TrendingUp size={16} />
    },
    {
      quarter: "Q3 2025",
      category: "Infrastructure",
      title: "Multi-Region Deployment",
      description: "EU and APAC region support with data sovereignty",
      owner: "KPMG",
      color: colors.kpmg.primary,
      icon: <Compass size={16} />
    },
    {
      quarter: "Q3 2025",
      category: "Framework Enhancement",
      title: "Custom LLM for Financial Services",
      description: "Specialized model trained on financial industry data",
      owner: "Prizym",
      color: colors.prizm.primary,
      icon: <Zap size={16} />
    },
    {
      quarter: "Q4 2025",
      category: "Domain Expansion",
      title: "Healthcare Analytics Module",
      description: "New domain application for healthcare providers",
      owner: "Joint",
      color: colors.joint.primary, 
      icon: <Gift size={16} />
    },
    {
      quarter: "Q4 2025",
      category: "Operations",
      title: "Self-Service Implementation",
      description: "Simplified deployment for mid-market clients",
      owner: "KPMG",
      color: colors.kpmg.primary,
      icon: <Users size={16} />
    },
    {
      quarter: "Q1 2026",
      category: "Framework Enhancement",
      title: "Unified Agent Framework",
      description: "Autonomous agents for complex workflows",
      owner: "Prizym",
      color: colors.prizm.primary,
      icon: <Zap size={16} />
    },
    {
      quarter: "Q1 2026",
      category: "Domain Expansion",
      title: "Supply Chain Optimization",
      description: "End-to-end supply chain intelligence",
      owner: "Joint",
      color: colors.joint.primary,
      icon: <Gift size={16} />
    }
  ];

  const researchInitiatives = [
    {
      title: "Explainable AI",
      description: "Mechanisms to provide transparency into AI decision-making processes",
      owner: "Prizym",
      timeline: "Ongoing",
      impact: "High"
    },
    {
      title: "Domain-Specific Data Synthesis",
      description: "Techniques to generate synthetic but realistic training data for specialized domains",
      owner: "Prizym",
      timeline: "Q3 2025-Q1 2026",
      impact: "Medium"
    },
    {
      title: "Federated Learning Infrastructure",
      description: "Train models across multiple clients without sharing sensitive data",
      owner: "Joint",
      timeline: "Q4 2025-Q2 2026",
      impact: "High"
    },
    {
      title: "Continuous Learning Systems",
      description: "Models that adapt to new data and feedback without full retraining",
      owner: "Prizym",
      timeline: "Q1-Q3 2026",
      impact: "Medium"
    }
  ];

  const getQuarterColor = (quarter) => {
    if (quarter.includes("Q1")) return colors.timeline.q1;
    if (quarter.includes("Q2")) return colors.timeline.q2;
    if (quarter.includes("Q3")) return colors.timeline.q3;
    if (quarter.includes("Q4")) return colors.timeline.q4;
    return "#E0E0E0";
  };

  const getOwnerColor = (owner) => {
    if (owner === "Prizym") return colors.prizm.primary;
    if (owner === "KPMG") return colors.kpmg.primary;
    if (owner === "Joint") return colors.joint.primary;
    return "#888888";
  };

  const renderRoadmapItem = (item, index) => (
    <div key={index} className="flex flex-row mb-2">
      <div className="w-20 flex-shrink-0 flex flex-col items-center">
        <div className="rounded-lg py-1 px-2 text-xs font-bold text-center w-full" 
             style={{backgroundColor: getQuarterColor(item.quarter)}}>
          {item.quarter}
        </div>
        <div className="h-full border-l border-gray-300 mt-1"></div>
      </div>
      
      <div className="flex-grow border-2 rounded-lg ml-2 p-2" style={{ borderColor: item.color, borderLeft: `4px solid ${item.color}` }}>
        <div className="flex justify-between items-start">
          <div>
            <span className="text-xs font-medium px-2 py-1 rounded-full bg-gray-100">{item.category}</span>
            <h3 className="font-bold mt-1">{item.title}</h3>
            <p className="text-sm">{item.description}</p>
          </div>
          <div className="w-6 h-6 rounded-full flex items-center justify-center" style={{ backgroundColor: item.color }}>
            {React.cloneElement(item.icon, { color: "white", size: 14 })}
          </div>
        </div>
        <div className="flex items-center mt-2">
          <div className="text-xs py-1 px-2 rounded-full" style={{ backgroundColor: getOwnerColor(item.owner), color: "white" }}>
            {item.owner}
          </div>
        </div>
      </div>
    </div>
  );

  return (
    <div className="w-full h-full bg-white p-4 font-sans">
      <h1 className="text-2xl font-bold mb-4 text-center">Roadmap and Future Capabilities</h1>
      
      <div className="grid grid-cols-2 gap-4">
        {/* Left Column: Development Roadmap */}
        <div>
          <div className="flex items-center mb-4">
            <Calendar size={20} className="mr-2" />
            <h2 className="text-xl font-bold">24-Month Development Roadmap</h2>
          </div>
          
          <div className="space-y-2">
            {roadmapItems.map(renderRoadmapItem)}
          </div>
        </div>
        
        {/* Right Column: Research & Strategic Initiatives */}
        <div>
          <div>
            <div className="flex items-center mb-4">
              <Star size={20} className="mr-2" />
              <h2 className="text-xl font-bold">Research & Innovation Pipeline</h2>
            </div>
            
            <div className="space-y-3 mb-6">
              {researchInitiatives.map((initiative, index) => (
                <div key={index} className="border-2 border-gray-300 rounded-lg p-3">
                  <h3 className="font-bold">{initiative.title}</h3>
                  <p className="text-sm mb-2">{initiative.description}</p>
                  <div className="flex justify-between text-sm">
                    <div>
                      <span className="font-bold">Owner:</span> 
                      <span className="ml-1 py-1 px-2 rounded-full text-xs" 
                            style={{ backgroundColor: getOwnerColor(initiative.owner), color: "white" }}>
                        {initiative.owner}
                      </span>
                    </div>
                    <div><span className="font-bold">Timeline:</span> {initiative.timeline}</div>
                    <div>
                      <span className="font-bold">Impact:</span> 
                      <span className={`ml-1 py-1 px-2 rounded-full text-xs text-white ${
                        initiative.impact === "High" ? "bg-green-600" : "bg-blue-600"
                      }`}>
                        {initiative.impact}
                      </span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
          
          <div>
            <div className="flex items-center mb-4">
              <Target size={20} className="mr-2" />
              <h2 className="text-xl font-bold">Strategic Direction</h2>
            </div>
            
            <div className="border-2 border-gray-300 rounded-lg p-4">
              <div className="grid grid-cols-2 gap-4">
                <div className="border-l-4 pl-2" style={{ borderColor: colors.prizm.primary }}>
                  <h3 className="font-bold">Vertical Integration</h3>
                  <p className="text-sm">Deeper domain expertise in key industries with specialized LLMs and workflows</p>
                </div>
                <div className="border-l-4 pl-2" style={{ borderColor: colors.kpmg.primary }}>
                  <h3 className="font-bold">Enterprise Scale</h3>
                  <p className="text-sm">Infrastructure to support global deployments with enhanced security and compliance</p>
                </div>
                <div className="border-l-4 pl-2" style={{ borderColor: colors.joint.primary }}>
                  <h3 className="font-bold">Integrated Ecosystem</h3>
                  <p className="text-sm">Seamless connections with client systems, third-party data, and analytics tools</p>
                </div>
                <div className="border-l-4 pl-2" style={{ borderColor: colors.joint.primary }}>
                  <h3 className="font-bold">Time-to-Value</h3>
                  <p className="text-sm">Accelerated implementation and faster ROI realization for clients</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default TechRoadmap;

