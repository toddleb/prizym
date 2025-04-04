import React from 'react';
import { Users, Award, Calendar, ArrowUp, FileText, Briefcase } from 'lucide-react';

const ProjectGovernance = () => {
  const colors = {
    prizm: {
      bg: "#EEDDFF",
      primary: "#7B3FC4",
      border: "#5A2CA0"
    },
    kpmg: {
      bg: "#DCE8F7",
      primary: "#0073C6", 
      border: "#0B5EA8"
    },
    joint: {
      bg: "#F0F0F0",
      primary: "#6A3DB8",
      border: "#000000"
    }
  };

  const committees = [
    {
      name: "Executive Steering Committee",
      composition: "2 KPMG Executives, 2 Prizym Executives",
      responsibilities: [
        "Strategic direction and vision",
        "Investment decisions",
        "Performance oversight",
        "Dispute resolution"
      ],
      cadence: "Quarterly",
      level: "Strategic",
      color: colors.joint.border
    },
    {
      name: "Joint Solution Board",
      composition: "2 KPMG Solution Leaders, 2 Prizym Product Leads",
      responsibilities: [
        "Solution roadmap management",
        "Feature prioritization",
        "Domain expansion decisions",
        "Go-to-market alignment"
      ],
      cadence: "Monthly",
      level: "Tactical",
      color: colors.joint.primary
    },
    {
      name: "Delivery Management Team",
      composition: "KPMG Project Leads, Prizym Technical Leads",
      responsibilities: [
        "Implementation oversight",
        "Cross-functional coordination",
        "Resource allocation",
        "Client experience management"
      ],
      cadence: "Bi-weekly",
      level: "Operational",
      color: "#888888"
    }
  ];

  const escalationPaths = [
    {
      level: "Level 1",
      issue: "Technical Implementation Issues",
      owner: "Delivery Teams",
      timeframe: "24-48 hours",
      color: colors.prizm.primary
    },
    {
      level: "Level 2",
      issue: "Project Timeline/Budget Issues",
      owner: "Delivery Management Team",
      timeframe: "1 week",
      color: "#888888"
    },
    {
      level: "Level 3",
      issue: "Solution Design Conflicts",
      owner: "Joint Solution Board",
      timeframe: "2 weeks",
      color: colors.joint.primary
    },
    {
      level: "Level 4",
      issue: "Strategic/Commercial Conflicts",
      owner: "Executive Steering Committee",
      timeframe: "30 days",
      color: colors.joint.border
    }
  ];

  const ipOwnership = [
    {
      component: "Layer 1: AI Framework",
      owner: "Prizym",
      rights: "KPMG receives perpetual license for client implementations",
      color: colors.prizm.primary
    },
    {
      component: "Layer 2: Operational Layer",
      owner: "KPMG",
      rights: "Prizym receives implementation rights for joint clients",
      color: colors.kpmg.primary
    },
    {
      component: "Layer 3: Domain Applications",
      owner: "Joint IP",
      rights: "50/50 ownership with mutual commercialization rights",
      color: colors.joint.primary
    },
    {
      component: "Client-Specific Customizations",
      owner: "Client",
      rights: "Partners retain right to reuse patterns with other clients",
      color: "#888888"
    }
  ];

  const renderCommittee = (committee, index) => (
    <div key={index} className="border-2 rounded-lg p-3 mb-3" style={{ borderColor: committee.color }}>
      <div className="flex items-center mb-2">
        <Users size={20} className="mr-2" />
        <h3 className="font-bold text-lg">{committee.name}</h3>
      </div>
      <div className="grid grid-cols-3 gap-2 text-sm">
        <div>
          <p className="font-bold">Composition:</p>
          <p>{committee.composition}</p>
        </div>
        <div className="col-span-2">
          <p className="font-bold">Responsibilities:</p>
          <ul className="list-disc pl-5">
            {committee.responsibilities.map((resp, i) => (
              <li key={i}>{resp}</li>
            ))}
          </ul>
        </div>
      </div>
      <div className="flex justify-between mt-2 text-sm">
        <div>
          <Calendar size={16} className="inline mr-1" />
          <span className="font-bold">Cadence:</span> {committee.cadence}
        </div>
        <div>
          <ArrowUp size={16} className="inline mr-1" />
          <span className="font-bold">Level:</span> {committee.level}
        </div>
      </div>
    </div>
  );

  return (
    <div className="w-full h-full bg-white p-4 font-sans">
      <h1 className="text-2xl font-bold mb-4 text-center">Partnership Governance Model</h1>
      
      <div className="grid grid-cols-2 gap-4">
        {/* Governance Structure */}
        <div>
          <h2 className="text-xl font-bold mb-3">Governance Structure</h2>
          {committees.map(renderCommittee)}
        </div>
        
        {/* Right Column */}
        <div className="space-y-4">
          {/* Escalation Paths */}
          <div>
            <h2 className="text-xl font-bold mb-3">Escalation Framework</h2>
            <div className="border-2 border-gray-300 rounded-lg p-3">
              {escalationPaths.map((path, index) => (
                <div key={index} className="flex mb-2 last:mb-0">
                  <div className="w-1/4 font-bold" style={{ color: path.color }}>{path.level}</div>
                  <div className="w-3/4">
                    <p><span className="font-bold">Issue:</span> {path.issue}</p>
                    <p><span className="font-bold">Owner:</span> {path.owner}</p>
                    <p><span className="font-bold">Timeframe:</span> {path.timeframe}</p>
                    {index < escalationPaths.length - 1 && <div className="border-b border-gray-300 my-2"></div>}
                  </div>
                </div>
              ))}
            </div>
          </div>
          
          {/* IP Ownership */}
          <div>
            <h2 className="text-xl font-bold mb-3">IP & Licensing Model</h2>
            <div className="border-2 border-gray-300 rounded-lg p-3">
              <div className="grid grid-cols-3 gap-2 font-bold mb-2 text-sm">
                <div>Component</div>
                <div>Ownership</div>
                <div>Rights</div>
              </div>
              
              {ipOwnership.map((ip, index) => (
                <div key={index} className="grid grid-cols-3 gap-2 text-sm mb-2 last:mb-0">
                  <div className="font-bold" style={{ color: ip.color }}>{ip.component}</div>
                  <div>{ip.owner}</div>
                  <div>{ip.rights}</div>
                </div>
              ))}
            </div>
          </div>
          
          {/* Team Structure */}
          <div>
            <h2 className="text-xl font-bold mb-3">Partnership Team Structure</h2>
            <div className="border-2 border-gray-300 rounded-lg p-3">
              <div className="flex justify-around items-center">
                <div className="text-center p-2 rounded-lg" style={{ backgroundColor: colors.prizm.bg }}>
                  <h3 className="font-bold">Prizym Team</h3>
                  <ul className="list-disc text-sm text-left pl-5">
                    <li>AI Product Leads</li>
                    <li>ML Engineers</li>
                    <li>LLM Specialists</li>
                    <li>Technical Architects</li>
                  </ul>
                </div>
                
                <div className="text-center border-2 p-2 rounded-lg" style={{ borderColor: colors.joint.border }}>
                  <h3 className="font-bold">Joint Resources</h3>
                  <ul className="list-disc text-sm text-left pl-5">
                    <li>Solution Architects</li>
                    <li>Domain SMEs</li>
                    <li>Client Success Mgrs</li>
                  </ul>
                </div>
                
                <div className="text-center p-2 rounded-lg" style={{ backgroundColor: colors.kpmg.bg }}>
                  <h3 className="font-bold">KPMG Team</h3>
                  <ul className="list-disc text-sm text-left pl-5">
                    <li>Engagement Managers</li>
                    <li>Business Consultants</li>
                    <li>Industry Specialists</li>
                    <li>Change Management</li>
                  </ul>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProjectGovernance;
