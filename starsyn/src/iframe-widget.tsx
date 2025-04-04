import React from 'react';
import StarsynCard, { MatchData } from './components/StarsynCard';

const demoData: MatchData = {
  studentName: 'Alex Johnson',
  programName: 'Data Science Bootcamp',
  overallMatch: 87,
  categories: [
    {
      id: 'tech',
      name: 'Technical Skills',
      color: '#3B82F6',
      factors: [
        { id: 't1', name: 'Python', score: 90 },
        { id: 't2', name: 'Data Analysis', score: 85 },
        { id: 't3', name: 'ML', score: 75 },
        { id: 't4', name: 'Databases', score: 80 },
        { id: 't5', name: 'Stats', score: 70 },
      ],
    },
    {
      id: 'soft',
      name: 'Soft Skills',
      color: '#EC4899',
      factors: [
        { id: 's1', name: 'Communication', score: 88 },
        { id: 's2', name: 'Teamwork', score: 82 },
        { id: 's3', name: 'Adaptability', score: 79 },
        { id: 's4', name: 'Time Management', score: 85 },
        { id: 's5', name: 'Leadership', score: 76 },
      ],
    },
  ],
};

const RadialSpokeIframe = () => {
  return (
    <div
      style={{
        width: '100%',
        height: '100vh',
        padding: '1rem',
        boxSizing: 'border-box',
        backgroundColor: '#f9fafb',
      }}
    >
      <StarsynCard data={demoData} />
    </div>
  );
};

export default RadialSpokeIframe;
