// RadialSpokeSignatureTest.tsx
// Local dev harness for the RadialSpokeSignature component

import React from 'react';
import RadialSpokeSignature, { MatchData } from '../components/RadialSpokeSignature';

const sampleData: MatchData = {
  studentName: "Alex Johnson",
  programName: "Data Science Bootcamp",
  overallMatch: 87,
  categories: [
    {
      id: 'technical',
      name: 'Technical Skills',
      color: '#3B82F6',
      factors: [
        { id: 't1', name: 'Python Proficiency', score: 95 },
        { id: 't2', name: 'Data Analysis', score: 90 },
        { id: 't3', name: 'Statistics', score: 85 },
        { id: 't4', name: 'Machine Learning', score: 78 },
        { id: 't5', name: 'Database Management', score: 88 }
      ]
    },
    {
      id: 'learning',
      name: 'Learning Style',
      color: '#10B981',
      factors: [
        { id: 'l1', name: 'Self-Directed', score: 92 },
        { id: 'l2', name: 'Project-Based', score: 96 },
        { id: 'l3', name: 'Collaborative', score: 75 },
        { id: 'l4', name: 'Visual Learning', score: 82 },
        { id: 'l5', name: 'Learning Pace', score: 89 }
      ]
    }
  ]
};

const RadialSpokeSignatureTest = () => {
  return (
    <div style={{ height: '100vh', background: '#f0f4f8', padding: '2rem' }}>
      <h1 style={{ fontSize: '1.5rem', marginBottom: '1rem' }}>Radial Spoke Signature Demo</h1>
      <div style={{ height: '80vh', background: '#fff', borderRadius: '12px', boxShadow: '0 2px 10px rgba(0,0,0,0.1)' }}>
        <RadialSpokeSignature data={sampleData} />
      </div>
    </div>
  );
};

export default RadialSpokeSignatureTest;
