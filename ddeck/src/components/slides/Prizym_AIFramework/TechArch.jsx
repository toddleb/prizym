import React from 'react';
import ReactFlow, { Controls, Background, MiniMap } from 'reactflow';
import 'reactflow/dist/style.css';
import dagre from 'dagre';

const nodeStyle = {
  padding: '10px',
  borderRadius: '8px',
  fontSize: '11px',
  textAlign: 'center',
  background: '#fff',
  border: '2px solid #4A90E2',
};

const nodes = [
  { id: 'data-sources', data: { label: '📂 Data Sources\nCRM, ERP, Unstructured' }, position: { x: 0, y: 0 }, style: nodeStyle },
  { id: 'connectors', data: { label: '🔗 Data Connectors\nETL & Integration' }, position: { x: 0, y: 0 }, style: nodeStyle },
  { id: 'security', data: { label: '🔐 Security Layer\nEncryption & Access Control' }, position: { x: 0, y: 0 }, style: nodeStyle },
  { id: 'ai-processing', data: { label: '🤖 AI Processing\nConsensus, Arbitration,\nEvaluation, Optimization' }, position: { x: 0, y: 0 }, style: nodeStyle },
  { id: 'kpmg-layer', data: { label: '🏛️ KPMG Operational\nRequirements, Design,\nImplementation' }, position: { x: 0, y: 0 }, style: nodeStyle },
  { id: 'apps', data: { label: '🚀 Applications\nSPM, Career Planning,\nLead Gen, Workforce Opt.' }, position: { x: 0, y: 0 }, style: nodeStyle },
  { id: 'deployment', data: { label: '☁️ Deployment\nCloud, Hybrid, On-Prem' }, position: { x: 0, y: 0 }, style: nodeStyle },
];

const edges = [
  { id: 'e1', source: 'data-sources', target: 'connectors', animated: true, label: 'Extract Data' },
  { id: 'e2', source: 'connectors', target: 'security', animated: true, label: 'Secure Data Flow' },
  { id: 'e3', source: 'security', target: 'ai-processing', animated: true, label: 'Protected Data' },
  { id: 'e4', source: 'ai-processing', target: 'kpmg-layer', animated: true, label: 'AI Insights' },
  { id: 'e5', source: 'kpmg-layer', target: 'apps', animated: true, label: 'Tailored Solutions' },
  { id: 'e6', source: 'apps', target: 'deployment', animated: true, label: 'Flexible Deployment' },
];

const getHorizontalLayout = (nodes, edges) => {
  const dagreGraph = new dagre.graphlib.Graph();
  dagreGraph.setDefaultEdgeLabel(() => ({}));
  dagreGraph.setGraph({ rankdir: 'LR' }); // Horizontal layout (Left to Right)

  nodes.forEach((node) => dagreGraph.setNode(node.id, { width: 220, height: 80 }));
  edges.forEach((edge) => dagreGraph.setEdge(edge.source, edge.target));

  dagre.layout(dagreGraph);

  return {
    nodes: nodes.map((node) => {
      const pos = dagreGraph.node(node.id);
      return { ...node, position: { x: pos.x - 110, y: pos.y - 40 } };
    }),
    edges,
  };
};

const TechArch = () => {
  const { nodes: layoutedNodes, edges: layoutedEdges } = getHorizontalLayout(nodes, edges);

  return (
    <div style={{ width: '100%', height: '100%' }}>
      <ReactFlow nodes={layoutedNodes} edges={layoutedEdges} fitView>
        <Background color="#f0f0f0" gap={12} />
        <Controls />
        <MiniMap nodeColor="#4A90E2" nodeStrokeWidth={3} />
      </ReactFlow>
    </div>
  );
};

export default TechArch;
