import React from 'react';
import { motion } from 'framer-motion';
import { Database, Server, Cpu, Code, Layers, MessageCircle, Network, GitBranch, Wifi } from 'lucide-react';

const layerColors = {
  prizm: { bg: "#FFFFFF", border: "#B37DFF", text: "#7B3FC4" },
  kpmg: { bg: "#FFFFFF", border: "#4FA8FF", text: "#0073C6" },
  domain: { bg: "#FFFFFF", border: "#AAAAAA", text: "#333333" }
};

const techComponents = {
  domain: [
    { title: "Domain APIs", desc: "Custom industry APIs", icon: <Code /> },
    { title: "Visualization", desc: "D3.js, Tableau", icon: <Layers /> },
    { title: "Workflow Engine", desc: "Automation", icon: <GitBranch /> },
    { title: "Industry Models", desc: "Pre-trained models", icon: <Network /> },
  ],
  kpmg: [
    { title: "Project Mgmt", desc: "JIRA, Monday.com", icon: <GitBranch /> },
    { title: "ETL Pipeline", desc: "Data processing", icon: <Database /> },
    { title: "AskChat", desc: "NLP interactions", icon: <MessageCircle /> },
    { title: "Business Rules", desc: "Industry rulesets", icon: <Code /> },
  ],
  prizm: [
    { title: "LLM Orchestration", desc: "Prompt optimization", icon: <Cpu /> },
    { title: "Inference Pipeline", desc: "Fast inference", icon: <Server /> },
    { title: "Model Training", desc: "Fine-tuning", icon: <Network /> },
    { title: "LLM API Gateway", desc: "Unified API access", icon: <Wifi /> },
  ],
};

const renderTechComponent = ({ title, desc, icon }, layer) => (
  <motion.div
    initial={{ opacity: 0, y: 20 }}
    animate={{ opacity: 1, y: 0 }}
    transition={{ duration: 0.4 }}
    className="rounded-xl flex flex-row items-center shadow-md p-4 m-2 cursor-pointer hover:shadow-xl"
    style={{
      backgroundColor: layerColors[layer].bg,
      border: `2px solid ${layerColors[layer].border}`,
      width: '260px',
      height: '100px'
    }}
  >
    <div className="mr-4">
      {React.cloneElement(icon, { size: 30, color: layerColors[layer].text })}
    </div>
    <div className="flex flex-col">
      <h3 className="font-bold text-lg" style={{ color: layerColors[layer].text }}>{title}</h3>
      <p className="text-sm text-gray-600">{desc}</p>
    </div>
  </motion.div>
);

const TechStack = () => (
  <div 
    className="w-full h-screen overflow-auto font-sans"
    style={{ 
      backgroundImage: "linear-gradient(to bottom right, #0f2027, #203a43, #2c5364)", 
      backgroundSize: 'cover'
    }}
  >
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.5 }}
      className="flex flex-col justify-start items-center pt-4 pb-4 min-h-screen"
    >
      <h1 className="text-4xl font-bold text-white drop-shadow-lg mb-6">
        Technology Stack Breakdown
      </h1>

      <div className="grid grid-cols-3 gap-6 px-8">
        {Object.entries(techComponents).map(([layer, components], idx) => (
          <div key={layer} className="flex flex-col items-center">
            <h2 className="text-2xl font-semibold mb-3 text-gray-100">
              Layer {3 - idx}: {layer === 'prizm' ? 'Prizym.ai' : layer === 'kpmg' ? 'KPMG Operational' : 'Domain Use Cases'}
            </h2>
            {components.map((comp, index) => (
             <React.Fragment key={`${layer}-${index}`}>
               {renderTechComponent(comp, layer)}
             </React.Fragment>
            ))}
          </div>
        ))}
      </div>

      <div className="mt-6 text-lg text-gray-200 flex items-center gap-2">
        Inputs ➡️ AI Processing ➡️ Execution ➡️ Domain App ➡️ Results
      </div>
    </motion.div>
  </div>
);

export default TechStack;
