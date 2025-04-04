import React from 'react';
import { ArrowDown, RefreshCcw } from 'lucide-react';

const LensFramework = () => {
  const layerColors = {
    aiLayer: { bg: "#EEDDFF" },
    operationalLayer: { bg: "#DCE8F7" },
    domainLayer: { bg: "#F0F0F0" },
    flow: { bg: "#F5E1D0" },
    prizm: { bg: "#7B3FC4", text: "#FFFFFF" },
    kpmg: { bg: "#0073C6", text: "#FFFFFF" },
  };

  const renderModuleBox = (title, color, textColor = "#000", width = "w-40", height = "h-20") => (
    <div
      className={`${width} ${height} rounded-lg border-2 flex items-center justify-center text-center p-2 m-1 font-medium`}
      style={{ backgroundColor: color, borderColor: "#000", color: textColor }}
    >
      {title}
    </div>
  );

  const renderProcessStep = (number, title, description) => (
    <div className="flex items-start mb-3">
      <div
        className="w-8 h-8 rounded-full text-white flex items-center justify-center font-bold mr-2 flex-shrink-0"
        style={{ backgroundColor: "#F57C00" }}
      >
        {number}
      </div>
      <div>
        <h4 className="font-bold">{title}</h4>
        <p className="text-sm">{description}</p>
      </div>
    </div>
  );

  return (
    <div className="flex w-full h-full bg-white p-2 font-sans overflow-hidden">
      {/* Left Side (Layers 1-3) */}
      <div className="w-3/4 flex flex-col pr-2 space-y-2 overflow-auto">
        <h1 className="text-lg font-bold">AI Framework Architecture</h1>

        {/* Domain Use Cases */}
        <div className="rounded border p-2 flex-1" style={{ backgroundColor: layerColors.domainLayer.bg }}>
          <h2 className="text-sm font-bold mb-1">Layer 3: Domain Use Cases</h2>
          <div className="flex flex-wrap justify-center">
            {["SPM", "PE & VC Analysis", "Career Planning", "Lead Generation", "Workforce Optimization", "Financial Planning"]
              .map(item => renderModuleBox(item, item === "SPM" ? layerColors.prizm.bg : "#FFF", item === "SPM" ? "#FFF" : "#000", "w-28"))}
          </div>
        </div>

        {/* KPMG Operational Layer */}
        <div className="rounded border p-2 flex-1" style={{ backgroundColor: layerColors.operationalLayer.bg }}>
          <h2 className="text-sm font-bold mb-1">Layer 2: KPMG Operational Layer</h2>
          <div className="flex h-full">
            <div className="w-1/2 pr-1 border-r">
              <h3 className="text-xs font-semibold text-center">Consulting</h3>
              <div className="flex flex-wrap justify-center">
                {["Inception", "Requirements", "Design", "Build", "Test", "Deploy"]
                  .map(item => renderModuleBox(item, layerColors.kpmg.bg, "#FFF", "w-24"))}
              </div>
            </div>
            <div className="w-1/2 pl-1">
              <h3 className="text-xs font-semibold text-center">Client</h3>
              <div className="flex flex-wrap justify-center">
                {["Process 1", "Process 2", "Process 3", "Process 4", "Process 5", "Process 6"]
                  .map(item => renderModuleBox(item, layerColors.kpmg.bg, "#FFF", "w-24"))}
              </div>
            </div>
          </div>
        </div>

        {/* Prizym.ai LENS Layer */}
        <div className="rounded border p-2 flex-1" style={{ backgroundColor: layerColors.aiLayer.bg }}>
          <h2 className="text-sm font-bold mb-1">Layer 1: Prizym.ai LENS</h2>
          <div className="flex flex-wrap justify-center">
            {["Use Case Input", "Master Controller", "Consensus Engine", "Arbitration Engine", "Evaluation Engine", "Optimization Engine"]
              .map(item => renderModuleBox(item, layerColors.prizm.bg, "#FFF", "w-32"))}
          </div>
          <div className="flex justify-center">
            {["Public LLMs", "Custom LLMs"].map(item =>
              renderModuleBox(item, layerColors.prizm.bg, "#FFF", "w-48")
            )}
          </div>
        </div>
      </div>

      {/* Right Side (Aligned Interaction Flow) */}
      <div className="w-1/4 flex flex-col pl-2 border-l overflow-hidden">
        <div className="rounded border p-2 flex flex-col h-full" style={{ backgroundColor: layerColors.flow.bg }}>
          <h2 className="text-sm font-bold mb-2">Interaction Flow</h2>
          <div className="flex flex-col flex-1 overflow-auto justify-between">
            <div>
              {renderProcessStep(1, "Use Case Ingestion", "Problem enters via Prizym.ai")}
              <ArrowDown size={16} className="text-orange-500 my-1" />
              {renderProcessStep(2, "AI Processing", "Engines evaluate solutions")}
              <ArrowDown size={16} className="text-orange-500 my-1" />
              {renderProcessStep(3, "Operational Execution", "KPMG implements solutions")}
              <ArrowDown size={16} className="text-orange-500 my-1" />
              {renderProcessStep(4, "Domain Application", "Applied to specific business")}
              <ArrowDown size={16} className="text-orange-500 my-1" />
              {renderProcessStep(5, "Feedback Loop", "Continuous improvement")}
            </div>
            <RefreshCcw size={20} className="text-orange-500 my-2 self-center" />

            {/* Expanded Summary */}
            <div className="border-t border-orange-400 pt-2 text-xs leading-tight">
              <h3 className="font-bold">Summary</h3>
              <p>
                The Prizym AI Framework integrates advanced AI processing from Prizym.ai (Layer 1) with KPMG’s extensive consulting and operational expertise (Layer 2). Solutions flow seamlessly to domain-specific applications (Layer 3), ensuring continuous refinement through an iterative feedback loop. This integrated architecture ensures optimal results and continuous improvement, aligning AI insights directly with real-world operational excellence.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LensFramework;
