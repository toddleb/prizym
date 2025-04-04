import React from 'react';
import StarSignature from '../components/starsignature/StarSignature';

const TestStarPage = () => {
  return (
    <div style={{ background: '#111', minHeight: '100vh', padding: '2rem' }}>
      <StarSignature
        skills={[
          { name: 'Technical', score: 88 },
          { name: 'Creative', score: 70 },
          { name: 'Analytical', score: 95 },
          { name: 'Social', score: 60 },
          { name: 'Implementation', score: 55 },
          { name: 'Strategic', score: 82 },
        ]}
        comparisonSkills={[
          { name: 'Technical', score: 72 },
          { name: 'Creative', score: 80 },
          { name: 'Analytical', score: 75 },
          { name: 'Social', score: 70 },
          { name: 'Implementation', score: 65 },
          { name: 'Strategic', score: 90 },
        ]}
        primaryConstellation="The Analyst"
        risingSigns={['Scholar Rising', 'Pragmatist Rising']}
        showTooltips
        animate
      />
    </div>
  );
};

export default TestStarPage;
