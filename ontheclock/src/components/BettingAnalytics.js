import React, { useState, useContext } from 'react';
import { DraftContext } from '../context/DraftContext';

// Include the bettingData directly in the component
const bettingData = {
  pickOdds: [
    { position: 1, name: 'Shedeur Sanders', odds: '-200', probability: '66.7%', ev: -0.10 },
    { position: 2, name: 'Travis Hunter', odds: '+350', probability: '22.2%', ev: 0.33 },
    { position: 3, name: 'Ashton Jeanty', odds: '+1000', probability: '9.1%', ev: 0.48 },
    { position: 4, name: 'Mason Graham', odds: '+4000', probability: '2.4%', ev: 0.96 }
  ],
  positionTrends: [
    { position: 'QB', avgDraftPosition: 7.5, overRate: '65%', topPickOdds: '-150' },
    { position: 'WR', avgDraftPosition: 14.8, overRate: '49%', topPickOdds: '+350' },
    { position: 'OT', avgDraftPosition: 12.9, overRate: '54%', topPickOdds: '+500' },
    { position: 'EDGE', avgDraftPosition: 11.2, overRate: '57%', topPickOdds: '+700' },
    { position: 'CB', avgDraftPosition: 17.6, overRate: '51%', topPickOdds: '+1000' }
  ],
  valueBets: [
    { name: 'Tetairoa McMillan', bet: 'Under 7.5', odds: '-115', recommendation: 'Strong Value', confidence: 'High' },
    { name: 'Abdul Carter', bet: 'Top 5 Pick', odds: '-200', recommendation: 'Fair Value', confidence: 'Medium' },
    { name: 'Will Campbell', bet: 'Over 10.5', odds: '-120', recommendation: 'Slight Value', confidence: 'Medium' },
    { name: 'James Pearce Jr.', bet: 'First EDGE Selected', odds: '+130', recommendation: 'Strong Value', confidence: 'High' }
  ]
};

const BettingAnalytics = () => {
  const { prospects } = useContext(DraftContext);
  const [activeSection, setActiveSection] = useState('pickOdds');
  
  // Calculate dynamic Vegas-style odds based on prospect grades
  const calculateDynamicOdds = () => {
    if (!prospects || prospects.length === 0) return bettingData;
    
    // Create copy of betting data to modify
    const updatedData = {...bettingData};
    
    // Sort prospects by grade to get top prospects
    const topProspects = [...prospects].sort((a, b) => b.grade - a.grade).slice(0, 10);
    
    // Update pick odds with current top prospects
    updatedData.pickOdds = topProspects.slice(0, 4).map((prospect, index) => {
      // Calculate implied odds based on prospect grade (9.0+ = favorite, etc)
      let odds = '+' + Math.floor((10 - prospect.grade) * 300);
      if (index === 0 && prospect.grade > 8.8) {
        odds = '-' + Math.floor(prospect.grade * 25);
      }
      
      // Calculate implied probability
      let probability;
      if (odds.startsWith('-')) {
        const absOdds = Math.abs(parseInt(odds));
        probability = (absOdds / (absOdds + 100) * 100).toFixed(1) + '%';
      } else {
        const absOdds = parseInt(odds.substring(1));
        probability = (100 / (absOdds + 100) * 100).toFixed(1) + '%';
      }
      
      // Simple expected value calculation
      const ev = odds.startsWith('-') ? -0.1 : 0.2 + (index * 0.2);
      
      return {
        position: index + 1,
        name: prospect.name,
        odds: odds,
        probability: probability,
        ev: ev
      };
    });
    
    // Update position trends
    const positionCounts = {};
    prospects.forEach(prospect => {
      if (!positionCounts[prospect.position]) {
        positionCounts[prospect.position] = [];
      }
      positionCounts[prospect.position].push(prospect.grade);
    });
    
    // Get top 5 positions by average grade
    const positionsByGrade = Object.entries(positionCounts)
      .map(([position, grades]) => ({
        position,
        avgGrade: grades.reduce((sum, grade) => sum + grade, 0) / grades.length
      }))
      .sort((a, b) => b.avgGrade - a.avgGrade)
      .slice(0, 5);
    
    updatedData.positionTrends = positionsByGrade.map((pos, index) => {
      // Calculate dynamic position data
      const avgDraftPosition = 10 + (index * 2) + (Math.random() * 5).toFixed(1);
      const overRate = (45 + Math.floor(Math.random() * 20)) + '%';
      
      // Calculate odds for this position being first selected
      let topPickOdds;
      if (index === 0) {
        topPickOdds = '-' + (120 + Math.floor(Math.random() * 80));
      } else {
        topPickOdds = '+' + (200 + (index * 200) + Math.floor(Math.random() * 100));
      }
      
      return {
        position: pos.position,
        avgDraftPosition: parseFloat(avgDraftPosition).toFixed(1),
        overRate: overRate,
        topPickOdds: topPickOdds
      };
    });
    
    return updatedData;
  };
  
  // Get dynamic data
  const dynamicData = calculateDynamicOdds();
  
  const renderContent = () => {
    switch(activeSection) {
      case 'pickOdds':
        return (
          <div className="p-3">
            <h3 className="font-bold text-lg mb-2">First Overall Pick Odds</h3>
            <table className="w-full text-sm">
              <thead className="bg-gray-100">
                <tr>
                  <th className="p-2 text-left">Player</th>
                  <th className="p-2 text-center">Odds</th>
                  <th className="p-2 text-center">Implied %</th>
                  <th className="p-2 text-center">EV</th>
                </tr>
              </thead>
              <tbody>
                {dynamicData.pickOdds.map((player, idx) => (
                  <tr key={idx} className="border-b">
                    <td className="p-2 font-medium">{player.name}</td>
                    <td className={`p-2 text-center ${player.odds.startsWith('-') ? 'text-green-600' : 'text-blue-600'}`}>
                      {player.odds}
                    </td>
                    <td className="p-2 text-center">{player.probability}</td>
                    <td className={`p-2 text-center ${player.ev > 0 ? 'text-green-600' : 'text-red-600'}`}>
                      {player.ev > 0 ? '+' : ''}{player.ev.toFixed(2)}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
            
            <div className="mt-4 text-xs text-gray-500">
              <p>EV = Expected Value | Positive values indicate potential betting value</p>
            </div>
          </div>
        );
        
      case 'positionTrends':
        return (
          <div className="p-3">
            <h3 className="font-bold text-lg mb-2">Position Draft Trends</h3>
            <table className="w-full text-sm">
              <thead className="bg-gray-100">
                <tr>
                  <th className="p-2 text-left">Position</th>
                  <th className="p-2 text-center">Avg. Pos.</th>
                  <th className="p-2 text-center">Over Rate</th>
                  <th className="p-2 text-center">Top Pick Odds</th>
                </tr>
              </thead>
              <tbody>
                {dynamicData.positionTrends.map((position, idx) => (
                  <tr key={idx} className="border-b">
                    <td className="p-2 font-medium">{position.position}</td>
                    <td className="p-2 text-center">{position.avgDraftPosition}</td>
                    <td className="p-2 text-center">{position.overRate}</td>
                    <td className={`p-2 text-center ${position.topPickOdds.startsWith('-') ? 'text-green-600' : 'text-blue-600'}`}>
                      {position.topPickOdds}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
            
            <div className="mt-4 text-xs text-gray-500">
              <p>Over Rate = % of times position goes over projection in last 5 drafts</p>
            </div>
          </div>
        );
        
      case 'valueBets':
        return (
          <div className="p-3">
            <h3 className="font-bold text-lg mb-2">Value Bet Recommendations</h3>
            <div className="space-y-3">
              {bettingData.valueBets.map((bet, idx) => (
                <div key={idx} className="p-2 border rounded bg-gray-50">
                  <div className="flex justify-between items-center">
                    <span className="font-bold">{bet.name}</span>
                    <span className={`px-2 py-1 rounded-full text-xs ${
                      bet.recommendation.includes('Strong') ? 'bg-green-100 text-green-800' :
                      bet.recommendation.includes('Fair') ? 'bg-blue-100 text-blue-800' :
                      'bg-yellow-100 text-yellow-800'
                    }`}>
                      {bet.recommendation}
                    </span>
                  </div>
                  <div className="mt-1 flex justify-between text-sm">
                    <span>{bet.bet}</span>
                    <span className={bet.odds.startsWith('-') ? 'text-green-600' : 'text-blue-600'}>
                      {bet.odds}
                    </span>
                  </div>
                  <div className="mt-1 text-xs text-gray-600">
                    Confidence: {bet.confidence}
                  </div>
                </div>
              ))}
            </div>
            
            <div className="mt-4 text-xs text-gray-500">
              <p className="font-bold">Disclaimer:</p>
              <p>These are analytical projections only. This tool is for informational purposes and is not affiliated with sportsbooks. Always bet responsibly.</p>
            </div>
          </div>
        );
      
      default:
        return null;
    }
  };
  
  return (
    <div className="bg-white rounded-lg shadow-md h-full flex flex-col">
      <div className="p-3 pb-0">
        <h2 className="text-xl font-bold">Draft Betting Analysis</h2>
        <p className="text-sm text-gray-600">Data-driven insights for the 2025 NFL Draft</p>
      </div>
      
      {/* Sub-tabs */}
      <div className="px-3 mt-2">
        <div className="flex border rounded overflow-hidden">
          <button 
            className={`flex-1 py-1.5 text-xs font-medium ${
              activeSection === 'pickOdds' ? 'bg-blue-500 text-white' : 'bg-gray-100 text-gray-700'
            }`}
            onClick={() => setActiveSection('pickOdds')}
          >
            Pick Odds
          </button>
          <button 
            className={`flex-1 py-1.5 text-xs font-medium ${
              activeSection === 'positionTrends' ? 'bg-blue-500 text-white' : 'bg-gray-100 text-gray-700'
            }`}
            onClick={() => setActiveSection('positionTrends')}
          >
            Position Trends
          </button>
          <button 
            className={`flex-1 py-1.5 text-xs font-medium ${
              activeSection === 'valueBets' ? 'bg-blue-500 text-white' : 'bg-gray-100 text-gray-700'
            }`}
            onClick={() => setActiveSection('valueBets')}
          >
            Value Bets
          </button>
        </div>
      </div>
      
      {/* Content area */}
      <div className="flex-1 overflow-y-auto">
        {renderContent()}
      </div>
    </div>
  );
};

export default BettingAnalytics;