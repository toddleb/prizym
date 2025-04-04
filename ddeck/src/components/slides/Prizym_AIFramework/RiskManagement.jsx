import React from 'react';
import { AlertTriangle, Shield, Lock, CheckCircle, Eye, FileText, AlertCircle } from 'lucide-react';

const risks = [
  { title: "Data Privacy Breach", impact: "High", likelihood: "Low", owner: "Joint", mitigation: "Encryption, access control, audits" },
  { title: "Integration Failure", impact: "High", likelihood: "Medium", owner: "KPMG", mitigation: "Pre-assessment, flexible API" },
  { title: "Adoption Resistance", impact: "Medium", likelihood: "High", owner: "KPMG", mitigation: "Change mgmt, staged rollout" },
  { title: "Model Degradation", impact: "Medium", likelihood: "Medium", owner: "Prizym", mitigation: "Monitoring, scheduled retraining" },
  { title: "Resource Constraints", impact: "Medium", likelihood: "Medium", owner: "KPMG", mitigation: "Cross-training, resource planning" },
  { title: "Over-reliance on AI", impact: "High", likelihood: "Medium", owner: "Joint", mitigation: "Human oversight, decision explanations" },
];

const assessmentApproaches = [
  { title: "Regular Assessments", detail: "Quarterly evaluation sessions" },
  { title: "Automated Monitoring", detail: "AI-driven real-time risk alerts" },
  { title: "Predictive Analytics", detail: "Identify emerging risks proactively" },
  { title: "Scenario Planning", detail: "Stress tests and contingency planning" },
];

const getColor = (impact, likelihood) => {
  if (impact === "High") return likelihood === "Low" ? "#FFA726" : "#EF5350";
  if (impact === "Medium") return likelihood === "High" ? "#FFA726" : "#66BB6A";
  return "#66BB6A";
};

const RiskManagement = () => (
  <div className="w-full h-full bg-white p-6 font-sans flex flex-col overflow-hidden">
    <h1 className="text-3xl font-bold text-center mb-4">Risk Management Framework</h1>

    <div className="grid grid-cols-2 gap-4 flex-1 overflow-auto">
      {/* Left: Key Risks */}
      <div className="space-y-3">
        <div className="flex items-center">
          <AlertTriangle className="text-red-600 mr-2" />
          <h2 className="text-xl font-bold">Key Risks & Mitigations</h2>
        </div>
        {risks.map((risk, idx) => (
          <div key={idx} className="border-l-4 shadow p-2" style={{ borderColor: getColor(risk.impact, risk.likelihood) }}>
            <h3 className="font-bold">{risk.title}</h3>
            <p className="text-sm">
              <strong>Impact:</strong> {risk.impact} | <strong>Likelihood:</strong> {risk.likelihood} | <strong>Owner:</strong> {risk.owner}
            </p>
            <p className="text-xs"><strong>Mitigation:</strong> {risk.mitigation}</p>
          </div>
        ))}
      </div>

      {/* Right: Assessments & Governance */}
      <div className="space-y-4">
        {/* Expanded Assessment Approaches */}
        <div>
          <div className="flex items-center">
            <Shield className="text-blue-600 mr-2" />
            <h2 className="text-xl font-bold">Risk Assessment Approaches</h2>
          </div>
          <div className="mt-2 grid grid-cols-2 gap-2 text-sm">
            {assessmentApproaches.map((item, idx) => (
              <div key={idx} className="bg-gray-100 rounded p-2 shadow">
                <p className="font-bold">{item.title}</p>
                <p className="text-xs">{item.detail}</p>
              </div>
            ))}
          </div>
        </div>

        {/* Risk Matrix */}
        <div>
          <h3 className="text-lg font-bold mb-1">Risk Matrix</h3>
          <div className="grid grid-cols-4 gap-1 text-xs text-center">
            <div></div><div>Low</div><div>Medium</div><div>High</div>
            <div>High</div>
            <div className="bg-yellow-200 p-1">Monitor</div>
            <div className="bg-red-200 p-1">Mitigate</div>
            <div className="bg-red-400 p-1 text-white">Avoid</div>
            <div>Medium</div>
            <div className="bg-green-200 p-1">Accept</div>
            <div className="bg-yellow-200 p-1">Monitor</div>
            <div className="bg-red-200 p-1">Mitigate</div>
            <div>Low</div>
            <div className="bg-green-200 p-1">Accept</div>
            <div className="bg-green-200 p-1">Accept</div>
            <div className="bg-yellow-200 p-1">Monitor</div>
          </div>
        </div>

        {/* Governance Controls */}
        <div className="pt-2 border-t border-gray-200">
          <div className="flex items-center">
            <Lock className="text-purple-600 mr-2" />
            <h2 className="text-xl font-bold">Governance & Controls</h2>
          </div>
          <div className="grid grid-cols-2 gap-2 mt-2 text-xs">
            <div className="flex items-center">
              <CheckCircle className="text-green-600 mr-2" /> Regular Reviews
            </div>
            <div className="flex items-center">
              <Eye className="text-blue-600 mr-2" /> Real-Time Monitoring
            </div>
            <div className="flex items-center">
              <FileText className="text-indigo-600 mr-2" /> Risk Documentation
            </div>
            <div className="flex items-center">
              <AlertCircle className="text-orange-600 mr-2" /> Escalation Protocol
            </div>
          </div>
        </div>

        {/* Responsibility Matrix */}
        <div className="text-xs mt-2">
          <h3 className="font-bold">Responsibility Matrix</h3>
          <table className="w-full border text-center mt-1">
            <thead className="bg-gray-100">
              <tr>
                <th>Area</th><th>Prizym</th><th>KPMG</th><th>Client</th>
              </tr>
            </thead>
            <tbody>
              <tr><td>Security</td><td>R/A</td><td>C</td><td>I</td></tr>
              <tr><td>Model</td><td>R/A</td><td>I</td><td>C</td></tr>
              <tr><td>Integration</td><td>C</td><td>R/A</td><td>C</td></tr>
              <tr><td>Change Mgmt</td><td>I</td><td>R/A</td><td>C</td></tr>
            </tbody>
          </table>
          <p className="mt-1"><strong>R:</strong> Responsible | <strong>A:</strong> Accountable | <strong>C:</strong> Consulted | <strong>I:</strong> Informed</p>
        </div>
      </div>
    </div>
  </div>
);

export default RiskManagement;