import React from 'react';
import { ArrowRight, CheckCircle, UserCircle, BarChart, FileText, Database, Briefcase, ThumbsUp } from 'lucide-react';

const DomainDeepDive = () => {
  const colors = {
    prizm: "#7B3FC4",
    kpmg: "#0073C6",
    joint: "#6A3DB8",
    lightPurple: "#EEDDFF",
    lightBlue: "#DCE8F7",
    gray: "#F0F0F0"
  };

  const renderFlowStep = (number, title, description, icon, color = colors.prizm, borderColor = "#000000") => (
    <div className="flex flex-row items-start mb-3">
      <div className="flex-shrink-0 mr-2">
        <div className="w-7 h-7 rounded-full flex items-center justify-center font-bold text-white"
             style={{ backgroundColor: color }}>
          {number}
        </div>
      </div>
      <div className="flex-grow border-2 rounded-lg p-2" style={{ borderColor: borderColor }}>
        <div className="flex items-center">
          {React.cloneElement(icon, { size: 16, className: "mr-2" })}
          <h4 className="font-bold">{title}</h4>
        </div>
        <p className="text-xs mt-1">{description}</p>
      </div>
    </div>
  );

  const renderArrow = () => (
    <div className="flex justify-center my-1">
      <ArrowRight size={16} />
    </div>
  );

  return (
    <div className="w-full h-full bg-white p-4 font-sans">
      <h1 className="text-2xl font-bold mb-4 text-center">Domain Use Case Deep Dives</h1>
      
      <div className="grid grid-cols-2 gap-6">
        {/* SPM (Sales Performance Management) */}
        <div className="rounded-lg border-2 p-3" 
             style={{ background: `linear-gradient(135deg, ${colors.lightPurple} 49%, ${colors.lightBlue} 51%)`, borderColor: "#000000" }}>
          <h2 className="text-xl font-bold mb-2 text-center">SPM (Sales Performance Management)</h2>
          <div className="bg-white rounded-lg p-3">
            <p className="text-sm mb-3 font-bold text-center">Joint KPMG/Prizym Solution</p>
            
            {renderFlowStep(1, "Data Ingestion", "Import sales data from CRM, ERP, and other systems", 
              <Database />, colors.prizm)}
            {renderArrow()}
            
            {renderFlowStep(2, "Pattern Recognition", "AI identifies sales performance patterns and anomalies", 
              <BarChart />, colors.prizm)}
            {renderArrow()}
            
            {renderFlowStep(3, "Strategy Formulation", "KPMG consultants develop sales improvement strategies", 
              <Briefcase />, colors.kpmg)}
            {renderArrow()}
            
            {renderFlowStep(4, "Implementation Plan", "Custom implementation roadmap with specific actions", 
              <FileText />, colors.kpmg)}
            {renderArrow()}
            
            {renderFlowStep(5, "Continuous Monitoring", "Ongoing AI-powered performance tracking", 
              <BarChart />, colors.joint)}
            
            <div className="mt-3 p-2 bg-gray-100 rounded-lg">
              <p className="text-xs font-bold">Key Outcomes:</p>
              <ul className="text-xs list-disc pl-5">
                <li>15-25% increase in sales performance</li>
                <li>Data-driven sales strategy</li>
                <li>Personalized coaching recommendations</li>
              </ul>
            </div>
          </div>
        </div>
        
        {/* Career Planning */}
        <div className="rounded-lg border-2 p-3" 
             style={{ backgroundColor: colors.lightPurple, borderColor: "#000000" }}>
          <h2 className="text-xl font-bold mb-2 text-center">Career Planning</h2>
          <div className="bg-white rounded-lg p-3">
            <p className="text-sm mb-3 font-bold text-center">Prizym Solution</p>
            
            {renderFlowStep(1, "Candidate Profile", "Analyze resume, skills, and career aspirations", 
              <UserCircle />, colors.prizm)}
            {renderArrow()}
            
            {renderFlowStep(2, "Market Analysis", "AI assessment of job market and industry trends", 
              <Database />, colors.prizm)}
            {renderArrow()}
            
            {renderFlowStep(3, "Path Generation", "Generate personalized career path options", 
              <BarChart />, colors.prizm)}
            {renderArrow()}
            
            {renderFlowStep(4, "Skills Gap Analysis", "Identify training needs for desired careers", 
              <FileText />, colors.prizm)}
            {renderArrow()}
            
            {renderFlowStep(5, "Action Planning", "Concrete steps and timeline for career progression", 
              <CheckCircle />, colors.prizm)}
            
            <div className="mt-3 p-2 bg-gray-100 rounded-lg">
              <p className="text-xs font-bold">Key Outcomes:</p>
              <ul className="text-xs list-disc pl-5">
                <li>Personalized career roadmaps</li>
                <li>Skills development prioritization</li>
                <li>Industry-specific guidance</li>
              </ul>
            </div>
          </div>
        </div>
        
        {/* Lead Generation */}
        <div className="rounded-lg border-2 p-3" 
             style={{ backgroundColor: colors.lightPurple, borderColor: "#000000" }}>
          <h2 className="text-xl font-bold mb-2 text-center">Lead Generation</h2>
          <div className="bg-white rounded-lg p-3">
            <p className="text-sm mb-3 font-bold text-center">Prizym Solution</p>
            
            {renderFlowStep(1, "Market Segmentation", "AI-driven identification of target segments", 
              <Database />, colors.prizm)}
            {renderArrow()}
            
            {renderFlowStep(2, "Content Optimization", "Custom content generation for each segment", 
              <FileText />, colors.prizm)}
            {renderArrow()}
            
            {renderFlowStep(3, "Channel Selection", "Determine optimal marketing channels", 
              <BarChart />, colors.prizm)}
            {renderArrow()}
            
            {renderFlowStep(4, "Engagement Analysis", "Monitor response and engagement metrics", 
              <UserCircle />, colors.prizm)}
            {renderArrow()}
            
            {renderFlowStep(5, "Lead Qualification", "AI-powered lead scoring and prioritization", 
              <ThumbsUp />, colors.prizm)}
            
            <div className="mt-3 p-2 bg-gray-100 rounded-lg">
              <p className="text-xs font-bold">Key Outcomes:</p>
              <ul className="text-xs list-disc pl-5">
                <li>30% increase in qualified leads</li>
                <li>Reduced cost per acquisition</li>
                <li>Higher conversion rates</li>
              </ul>
            </div>
          </div>
        </div>
        
        {/* Workforce Optimization */}
        <div className="rounded-lg border-2 p-3" 
             style={{ backgroundColor: colors.gray, borderColor: "#000000" }}>
          <h2 className="text-xl font-bold mb-2 text-center">Workforce Optimization</h2>
          <div className="bg-white rounded-lg p-3">
            <p className="text-sm mb-3 font-bold text-center">Partner-Led Solution</p>
            
            {renderFlowStep(1, "Workforce Assessment", "Current state analysis and skill mapping", 
              <UserCircle />, colors.joint)}
            {renderArrow()}
            
            {renderFlowStep(2, "Demand Forecasting", "AI prediction of future workforce needs", 
              <BarChart />, colors.prizm)}
            {renderArrow()}
            
            {renderFlowStep(3, "Gap Analysis", "Identify shortfalls in talent and capabilities", 
              <Database />, colors.kpmg)}
            {renderArrow()}
            
            {renderFlowStep(4, "Development Planning", "Create targeted upskilling programs", 
              <FileText />, colors.kpmg)}
            {renderArrow()}
            
            {renderFlowStep(5, "Implementation", "Execute and monitor optimization strategy", 
              <Briefcase />, colors.kpmg)}
            
            <div className="mt-3 p-2 bg-gray-100 rounded-lg">
              <p className="text-xs font-bold">Key Outcomes:</p>
              <ul className="text-xs list-disc pl-5">
                <li>Optimized workforce allocation</li>
                <li>Reduced skill gaps</li>
                <li>Improved employee retention</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DomainDeepDive;
