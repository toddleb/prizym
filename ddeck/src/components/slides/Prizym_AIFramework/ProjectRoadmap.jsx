import React from 'react';
import { Gantt, Willow } from "wx-react-gantt";
import "wx-react-gantt/dist/gantt.css";

const ProjectRoadmap = () => {
  const tasks = [
    // Phase 0: Pre-Implementation
    { id: 1, text: "Phase 0: Discovery & Design", type: "summary", open: true },
    { id: 2, text: "RFP & Client Engagement", start: "2025-03-01", duration: 7, parent: 1 },
    { id: 3, text: "Requirements Gathering (AI)", start: "2025-03-08", duration: 14, parent: 1 },
    { id: 4, text: "Territory & Quota Planning (AI)", start: "2025-03-15", duration: 10, parent: 1 },
    { id: 5, text: "ICM Framework Setup (AI)", start: "2025-03-15", duration: 10, parent: 1 },
    { id: 6, text: "Sales Reporting Strategy (AI)", start: "2025-03-25", duration: 10, parent: 1 },
    { id: 7, text: "Fit-Gap Analysis & Workshop", start: "2025-04-05", duration: 7, parent: 1 },
    { id: 8, text: "High-Level Architecture (AI)", start: "2025-04-12", duration: 7, parent: 1 },

    // Phase 1: Implementation & Deployment
    { id: 10, text: "Phase 1: Implementation", type: "summary", open: true },
    { id: 11, text: "Project Planning & PMO Setup", start: "2025-04-20", duration: 7, parent: 10 },
    { id: 12, text: "Detailed Business Analysis (AI)", start: "2025-04-27", duration: 10, parent: 10 },
    { id: 13, text: "Sprint 1: Design & Build (AI)", start: "2025-05-07", duration: 14, parent: 10 },
    { id: 14, text: "Sprint 2: Build & Test (AI)", start: "2025-05-21", duration: 14, parent: 10 },
    { id: 15, text: "Integrated System Testing (AI)", start: "2025-06-04", duration: 7, parent: 10 },
    { id: 16, text: "UAT & Final Deployment", start: "2025-06-12", duration: 7, parent: 10 },
    { id: 17, text: "Hypercare Support (AI)", start: "2025-06-20", duration: 14, parent: 10 },
    { id: 18, text: "Continuous Improvement (AI)", start: "2025-07-05", duration: 21, parent: 10 },
    { id: 19, text: "Optimization & COE Launch (AI)", start: "2025-07-26", duration: 21, parent: 10 },

    // Regional Rollouts
    { id: 20, text: "Phase 2: EMEA Expansion", type: "summary", open: false },
    { id: 21, text: "EMEA Implementation Cycle (AI)", start: "2025-08-20", duration: 30, parent: 20 },

    { id: 30, text: "Phase 3: APAC Expansion", type: "summary", open: false },
    { id: 31, text: "APAC Implementation Cycle (AI)", start: "2025-09-25", duration: 30, parent: 30 },
  ];

  const links = [
    { id: 1, source: 2, target: 3, type: "finish_to_start" },
    { id: 2, source: 3, target: 4, type: "finish_to_start" },
    { id: 3, source: 4, target: 6, type: "finish_to_start" },
    { id: 4, source: 5, target: 6, type: "finish_to_start" },
    { id: 5, source: 6, target: 7, type: "finish_to_start" },
    { id: 6, source: 7, target: 8, type: "finish_to_start" },
    { id: 7, source: 8, target: 11, type: "finish_to_start" },
    { id: 8, source: 11, target: 12, type: "finish_to_start" },
    { id: 9, source: 12, target: 13, type: "finish_to_start" },
    { id: 10, source: 13, target: 14, type: "finish_to_start" },
    { id: 11, source: 14, target: 15, type: "finish_to_start" },
    { id: 12, source: 15, target: 16, type: "finish_to_start" },
    { id: 13, source: 16, target: 17, type: "finish_to_start" },
    { id: 14, source: 17, target: 18, type: "finish_to_start" },
    { id: 15, source: 18, target: 19, type: "finish_to_start" },
    { id: 16, source: 19, target: 21, type: "finish_to_start" },
    { id: 17, source: 21, target: 31, type: "finish_to_start" },
  ];

  const scales = [
    { unit: "month", step: 1, format: "MMMM yyyy" },
    { unit: "day", step: 1, format: "d" },
  ];

  return (
    <Willow>
      <Gantt tasks={tasks} links={links} scales={scales} />
    </Willow>
  );
};

export default ProjectRoadmap;
