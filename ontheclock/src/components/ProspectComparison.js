import React, { useState, useContext, useEffect } from 'react';
import { DraftContext } from '../context/DraftContext';

const ProspectComparison = () => {
  const { prospects } = useContext(DraftContext);
  
  const [selectedProspects, setSelectedProspects] = useState([]);
  const [filteredProspects, setFilteredProspects] = useState([]);
  const [positionFilter, setPositionFilter] = useState('All');
  const [searchQuery, setSearchQuery] = useState('');
  const [comparisonData, setComparisonData] = useState(null);
  const [similarPlayers, setSimilarPlayers] = useState({});
  const [activeTab, setActiveTab] = useState('metrics'); // 'metrics', 'similar', 'radar'
  
  // Get unique positions from prospects
  const positions = ['All', ...new Set(prospects.map(p => p.position))].sort();
  
  // Filter prospects based on position and search
  useEffect(() => {
    let filtered = [...prospects];
    
    // Filter by position
    if (positionFilter !== 'All') {
      filtered = filtered.filter(p => p.position === positionFilter);
    }
    
    // Filter by search query
    if (searchQuery.trim()) {
      const query = searchQuery.toLowerCase();
      filtered = filtered.filter(p => 
        p.name.toLowerCase().includes(query) || 
        p.college.toLowerCase().includes(query)
      );
    }
    
    setFilteredProspects(filtered);
  }, [prospects, positionFilter, searchQuery]);
  
  // Generate mock combine data for a prospect
  const generateMockCombineData = (prospect) => {
    // Seed random with name to ensure consistent results
    const nameSeed = prospect.name.split('').reduce((sum, char) => sum + char.charCodeAt(0), 0);
    const random = (min, max) => min + ((nameSeed % 100) / 100) * (max - min);
    
    // Base ranges by position
    const positionRanges = {
      'QB': { forty: [4.5, 5.1], bench: [12, 24], vertical: [28, 36] },
      'RB': { forty: [4.3, 4.7], bench: [15, 30], vertical: [32, 42] },
      'WR': { forty: [4.3, 4.6], bench: [10, 22], vertical: [34, 44] },
      'TE': { forty: [4.5, 4.9], bench: [15, 28], vertical: [30, 40] },
      'OT': { forty: [4.8, 5.5], bench: [20, 35], vertical: [24, 32] },
      'OG': { forty: [4.9, 5.5], bench: [22, 36], vertical: [24, 32] },
      'C': { forty: [4.9, 5.5], bench: [25, 36], vertical: [24, 32] },
      'DT': { forty: [4.8, 5.5], bench: [25, 40], vertical: [26, 34] },
      'EDGE': { forty: [4.5, 4.9], bench: [20, 35], vertical: [30, 40] },
      'DL': { forty: [4.7, 5.3], bench: [22, 38], vertical: [28, 36] },
      'LB': { forty: [4.4, 4.9], bench: [20, 32], vertical: [30, 40] },
      'CB': { forty: [4.3, 4.6], bench: [10, 20], vertical: [34, 44] },
      'S': { forty: [4.4, 4.7], bench: [12, 24], vertical: [32, 40] }
    };
    
    // Default ranges if position not found
    const defaultRange = { forty: [4.5, 5.0], bench: [15, 30], vertical: [30, 40] };
    const range = positionRanges[prospect.position] || defaultRange;
    
    // Generate values based on prospect grade - better grade = better ranges
    const gradeModifier = (prospect.grade - 7.5) / 2; // Scale from -1 to +1 around grade 8.5
    
    return {
      forty_time: (range.forty[0] + (range.forty[1] - range.forty[0]) * (0.5 - gradeModifier * 0.5)).toFixed(2),
      bench_press: Math.round(range.bench[0] + (range.bench[1] - range.bench[0]) * (0.3 + gradeModifier * 0.7)),
      vertical_jump: (range.vertical[0] + (range.vertical[1] - range.vertical[0]) * (0.3 + gradeModifier * 0.7)).toFixed(1),
      broad_jump: (9 + gradeModifier * 1.5).toFixed(1),
      three_cone: (7.2 - gradeModifier * 0.5).toFixed(2),
      shuttle: (4.4 - gradeModifier * 0.3).toFixed(2),
      production_score: Math.round(75 + gradeModifier * 15),
      athleticism_score: Math.round(70 + gradeModifier * 20)
    };
  };
  
  // Generate historical player comparisons
  const generateHistoricalComparisons = (prospect) => {
    // Position-specific historical comparisons
    const positionComparisons = {
      'QB': [
        { name: 'Peyton Manning', similarity: 0.92, draftYear: 1998, draftPos: 1 },
        { name: 'Aaron Rodgers', similarity: 0.88, draftYear: 2005, draftPos: 24 },
        { name: 'Tom Brady', similarity: 0.82, draftYear: 2000, draftPos: 199 }
      ],
      'RB': [
        { name: 'Adrian Peterson', similarity: 0.94, draftYear: 2007, draftPos: 7 },
        { name: 'LaDainian Tomlinson', similarity: 0.89, draftYear: 2001, draftPos: 5 },
        { name: 'Marshawn Lynch', similarity: 0.85, draftYear: 2007, draftPos: 12 }
      ],
      'WR': [
        { name: 'Calvin Johnson', similarity: 0.93, draftYear: 2007, draftPos: 2 },
        { name: 'Julio Jones', similarity: 0.91, draftYear: 2011, draftPos: 6 },
        { name: 'Larry Fitzgerald', similarity: 0.88, draftYear: 2004, draftPos: 3 }
      ],
      'TE': [
        { name: 'Rob Gronkowski', similarity: 0.90, draftYear: 2010, draftPos: 42 },
        { name: 'Tony Gonzalez', similarity: 0.87, draftYear: 1997, draftPos: 13 },
        { name: 'Travis Kelce', similarity: 0.85, draftYear: 2013, draftPos: 63 }
      ],
      'OT': [
        { name: 'Joe Thomas', similarity: 0.94, draftYear: 2007, draftPos: 3 },
        { name: 'Tyron Smith', similarity: 0.90, draftYear: 2011, draftPos: 9 },
        { name: 'Trent Williams', similarity: 0.88, draftYear: 2010, draftPos: 4 }
      ],
      'EDGE': [
        { name: 'Von Miller', similarity: 0.93, draftYear: 2011, draftPos: 2 },
        { name: 'Khalil Mack', similarity: 0.91, draftYear: 2014, draftPos: 5 },
        { name: 'T.J. Watt', similarity: 0.89, draftYear: 2017, draftPos: 30 }
      ],
      'CB': [
        { name: 'Jalen Ramsey', similarity: 0.92, draftYear: 2016, draftPos: 5 },
        { name: 'Patrick Peterson', similarity: 0.90, draftYear: 2011, draftPos: 5 },
        { name: 'Darrelle Revis', similarity: 0.87, draftYear: 2007, draftPos: 14 }
      ]
    };
    
    // Default comparisons for positions not in the list
    const defaultComparisons = [
      { name: 'All-Pro Caliber', similarity: 0.91, draftYear: 2018, draftPos: 12 },
      { name: 'Pro Bowl Player', similarity: 0.85, draftYear: 2015, draftPos: 32 },
      { name: 'Solid Starter', similarity: 0.80, draftYear: 2019, draftPos: 48 }
    ];
    
    // Get position-specific comparisons or default
    let comparisons = positionComparisons[prospect.position] || defaultComparisons;
    
    // Adjust similarity based on prospect grade
    const gradeModifier = (prospect.grade - 7.5) / 2; // Scale around grade 8.5
    comparisons = comparisons.map(comp => ({
      ...comp,
      // Better prospects get higher similarity to elite players
      similarity: Math.min(0.99, Math.max(0.50, comp.similarity + gradeModifier * 0.1)).toFixed(2)
    }));
    
    return comparisons;
  };
  
  // Generate comparison data when selected prospects change
  useEffect(() => {
    if (selectedProspects.length > 0) {
      const data = selectedProspects.map(prospect => {
        const combineData = generateMockCombineData(prospect);
        return {
          id: prospect.id,
          name: prospect.name,
          position: prospect.position,
          college: prospect.college,
          height: prospect.height || '6\'2"',
          weight: prospect.weight || 215,
          grade: prospect.grade,
          ...combineData
        };
      });
      
      setComparisonData(data);
      
      // Generate historical comparisons
      const comparisons = {};
      selectedProspects.forEach(prospect => {
        comparisons[prospect.id] = generateHistoricalComparisons(prospect);
      });
      setSimilarPlayers(comparisons);
    } else {
      setComparisonData(null);
      setSimilarPlayers({});
    }
  }, [selectedProspects]);
  
  // Toggle prospect selection
  const toggleProspectSelection = (prospect) => {
    if (selectedProspects.some(p => p.id === prospect.id)) {
      setSelectedProspects(selectedProspects.filter(p => p.id !== prospect.id));
    } else {
      // Limit to 3 prospects
      if (selectedProspects.length < 3) {
        setSelectedProspects([...selectedProspects, prospect]);
      }
    }
  };
  
  // Render comparison metrics table
  const renderMetricsComparison = () => {
    if (!comparisonData || comparisonData.length === 0) return null;
    
    const metrics = [
      { key: 'position', label: 'Position' },
      { key: 'college', label: 'College' },
      { key: 'height', label: 'Height' },
      { key: 'weight', label: 'Weight' },
      { key: 'grade', label: 'Overall Grade', format: val => val.toFixed(1) },
      { key: 'forty_time', label: '40-Yard Dash', highlight: 'low' },
      { key: 'bench_press', label: 'Bench Press', highlight: 'high' },
      { key: 'vertical_jump', label: 'Vertical Jump', highlight: 'high' },
      { key: 'broad_jump', label: 'Broad Jump', highlight: 'high' },
      { key: 'three_cone', label: '3-Cone Drill', highlight: 'low' },
      { key: 'shuttle', label: 'Shuttle', highlight: 'low' },
      { key: 'production_score', label: 'Production Score', highlight: 'high' },
      { key: 'athleticism_score', label: 'Athleticism Score', highlight: 'high' }
    ];
    
    return (
      <div className="overflow-x-auto">
        <table className="min-w-full text-sm">
          <thead className="bg-gray-100">
            <tr>
              <th className="px-4 py-2 text-left">Metric</th>
              {comparisonData.map(prospect => (
                <th key={prospect.id} className="px-4 py-2 text-center">
                  {prospect.name}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {metrics.map(metric => (
              <tr key={metric.key} className="border-b">
                <td className="px-4 py-2 font-medium">{metric.label}</td>
                {comparisonData.map(prospect => {
                  const value = prospect[metric.key];
                  const formattedValue = metric.format ? metric.format(value) : value;
                  
                  // Calculate if this value is best among the prospects
                  let isBest = false;
                  if (metric.highlight) {
                    const values = comparisonData.map(p => p[metric.key]);
                    isBest = metric.highlight === 'high' 
                      ? value === Math.max(...values)
                      : value === Math.min(...values);
                  }
                  
                  return (
                    <td 
                      key={`${prospect.id}-${metric.key}`} 
                      className={`px-4 py-2 text-center ${isBest ? 'font-bold text-green-600' : ''}`}
                    >
                      {formattedValue}
                    </td>
                  );
                })}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    );
  };
  
  // Render similar players comparison
  const renderSimilarPlayers = () => {
    if (Object.keys(similarPlayers).length === 0) return null;
    
    return (
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {selectedProspects.map(prospect => (
          <div key={prospect.id} className="border rounded p-3">
            <h3 className="font-bold text-lg mb-2">{prospect.name}</h3>
            <p className="text-sm mb-3">Historical Player Comparisons</p>
            
            {similarPlayers[prospect.id]?.map((player, idx) => (
              <div key={idx} className="mb-3 pb-3 border-b last:border-0">
                <div className="flex justify-between">
                  <span className="font-medium">{player.name}</span>
                  <span className={`text-sm ${
                    parseFloat(player.similarity) > 0.9 ? 'text-green-600' : 
                    parseFloat(player.similarity) > 0.8 ? 'text-blue-600' : 
                    'text-gray-600'
                  }`}>
                    {(parseFloat(player.similarity) * 100).toFixed(0)}% match
                  </span>
                </div>
                <div className="text-xs text-gray-600 mt-1">
                  {player.draftYear} Draft: Round {Math.floor(player.draftPos / 32) + 1}, Pick {player.draftPos % 32 || 32}
                </div>
              </div>
            ))}
          </div>
        ))}
      </div>
    );
  };
  
  // Render radar chart visualization
  const renderRadarChart = () => {
    if (!comparisonData || comparisonData.length === 0) return null;
    
    // Create SVG radar chart
    // This is a simplified version - a real implementation would use D3.js or Chart.js
    // We'll create a basic SVG radar chart
    
    const metrics = [
      { key: 'forty_time', label: '40-Time', invert: true },
      { key: 'bench_press', label: 'Bench Press' },
      { key: 'vertical_jump', label: 'Vertical' },
      { key: 'broad_jump', label: 'Broad Jump' },
      { key: 'three_cone', label: '3-Cone', invert: true },
      { key: 'shuttle', label: 'Shuttle', invert: true },
      { key: 'production_score', label: 'Production' },
      { key: 'athleticism_score', label: 'Athleticism' }
    ];
    
    // Normalize values between 0 and 1
    const normalizedData = {};
    
    metrics.forEach(metric => {
      const values = comparisonData.map(p => parseFloat(p[metric.key]));
      const min = Math.min(...values);
      const max = Math.max(...values);
      
      normalizedData[metric.key] = comparisonData.map(prospect => {
        const value = parseFloat(prospect[metric.key]);
        // For metrics where lower is better (like times), invert the normalization
        if (metric.invert) {
          return 1 - ((value - min) / (max - min) || 0);
        } else {
          return (value - min) / (max - min) || 0;
        }
      });
    });
    
    // Radar chart parameters
    const centerX = 200;
    const centerY = 200;
    const radius = 150;
    const numPoints = metrics.length;
    const angleStep = (2 * Math.PI) / numPoints;
    
    // Generate coordinates for each prospect
    const prospectCoordinates = comparisonData.map((prospect, prospectIdx) => {
      const points = metrics.map((metric, i) => {
        const angle = i * angleStep - Math.PI / 2; // Start at the top
        const normalized = normalizedData[metric.key][prospectIdx];
        const distance = normalized * radius;
        
        return {
          x: centerX + distance * Math.cos(angle),
          y: centerY + distance * Math.sin(angle)
        };
      });
      
      // Create the polygon path
      const pathData = `M ${points[0].x} ${points[0].y} ${points.slice(1).map(p => `L ${p.x} ${p.y}`).join(' ')} Z`;
      
      return {
        name: prospect.name,
        pathData,
        points
      };
    });
    
    // Colors for each prospect
    const colors = ['rgba(59, 130, 246, 0.7)', 'rgba(16, 185, 129, 0.7)', 'rgba(245, 158, 11, 0.7)'];
    
    // Calculate axis point coordinates
    const axisPoints = Array.from({ length: numPoints }, (_, i) => {
      const angle = i * angleStep - Math.PI / 2;
      return {
        x: centerX + radius * Math.cos(angle),
        y: centerY + radius * Math.sin(angle),
        label: metrics[i].label,
        labelX: centerX + (radius + 20) * Math.cos(angle),
        labelY: centerY + (radius + 20) * Math.sin(angle)
      };
    });
    
    return (
      <div className="flex justify-center p-4">
        <svg width="450" height="450" viewBox="0 0 400 400">
          {/* Background circles */}
          {[0.25, 0.5, 0.75, 1].map((level, i) => (
            <circle 
              key={i}
              cx={centerX}
              cy={centerY}
              r={radius * level}
              fill="none"
              stroke="#e5e7eb"
              strokeWidth="1"
            />
          ))}
          
          {/* Axis lines */}
          {axisPoints.map((point, i) => (
            <line
              key={i}
              x1={centerX}
              y1={centerY}
              x2={point.x}
              y2={point.y}
              stroke="#e5e7eb"
              strokeWidth="1"
            />
          ))}
          
          {/* Axis labels */}
          {axisPoints.map((point, i) => (
            <text
              key={i}
              x={point.labelX}
              y={point.labelY}
              fontSize="11"
              textAnchor={
                point.labelX < centerX - 5 ? 'end' :
                point.labelX > centerX + 5 ? 'start' : 'middle'
              }
              dominantBaseline={
                point.labelY < centerY - 5 ? 'auto' :
                point.labelY > centerY + 5 ? 'hanging' : 'middle'
              }
              fill="#6b7280"
            >
              {point.label}
            </text>
          ))}
          
          {/* Prospect polygon shapes */}
          {prospectCoordinates.map((prospect, i) => (
            <path
              key={i}
              d={prospect.pathData}
              fill={colors[i % colors.length]}
              stroke={colors[i % colors.length].replace('0.7', '1')}
              strokeWidth="2"
              fillOpacity="0.3"
            />
          ))}
          
          {/* Legend */}
          <g transform="translate(20, 20)">
            {comparisonData.map((prospect, i) => (
              <g key={i} transform={`translate(0, ${i * 20})`}>
                <rect
                  width="15"
                  height="15"
                  fill={colors[i % colors.length]}
                  fillOpacity="0.7"
                />
                <text
                  x="20"
                  y="12"
                  fontSize="12"
                  fill="#374151"
                >
                  {prospect.name}
                </text>
              </g>
            ))}
          </g>
        </svg>
      </div>
    );
  };
  
  return (
    <div className="bg-white rounded-lg shadow-md h-full flex flex-col">
      <div className="p-4 border-b">
        <h2 className="text-xl font-bold">Prospect Comparison</h2>
        <p className="text-sm text-gray-600">Compare measurables and metrics between prospects</p>
      </div>
      
      <div className="p-4 border-b">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="col-span-1">
            <label className="block text-sm font-medium text-gray-700 mb-1">Position</label>
            <select
              className="w-full p-2 border rounded"
              value={positionFilter}
              onChange={(e) => setPositionFilter(e.target.value)}
            >
              {positions.map(pos => (
                <option key={pos} value={pos}>{pos}</option>
              ))}
            </select>
          </div>
          
          <div className="col-span-2">
            <label className="block text-sm font-medium text-gray-700 mb-1">Search</label>
            <input
              type="text"
              placeholder="Search by name or college"
              className="w-full p-2 border rounded"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
            />
          </div>
        </div>
      </div>
      
      <div className="flex-1 flex flex-col md:flex-row overflow-hidden">
        {/* Prospects list */}
        <div className="w-full md:w-64 border-r overflow-y-auto p-2">
          <h3 className="font-medium mb-2 px-2">Select Prospects (max 3)</h3>
          {filteredProspects.map(prospect => (
            <div 
              key={prospect.id}
              className={`p-2 rounded mb-1 cursor-pointer ${
                selectedProspects.some(p => p.id === prospect.id)
                  ? 'bg-blue-100 border border-blue-300'
                  : 'hover:bg-gray-100'
              }`}
              onClick={() => toggleProspectSelection(prospect)}
            >
              <div className="font-medium">{prospect.name}</div>
              <div className="text-xs text-gray-600 flex justify-between">
                <span>{prospect.position}, {prospect.college}</span>
                <span className={`font-medium ${
                  prospect.grade >= 8.5 ? 'text-green-600' :
                  prospect.grade >= 8.0 ? 'text-blue-600' :
                  prospect.grade >= 7.5 ? 'text-yellow-600' : 'text-gray-600'
                }`}>
                  {prospect.grade.toFixed(1)}
                </span>
              </div>
            </div>
          ))}
          
          {filteredProspects.length === 0 && (
            <div className="text-center py-4 text-gray-500">
              No prospects match your filters
            </div>
          )}
        </div>
        
        {/* Comparison area */}
        <div className="flex-1 flex flex-col overflow-hidden">
          {/* Tabs */}
          <div className="border-b">
            <nav className="flex">
              <button
                className={`px-4 py-2 text-sm font-medium ${
                  activeTab === 'metrics' ? 'border-b-2 border-blue-500 text-blue-600' : 'text-gray-500 hover:text-gray-700'
                }`}
                onClick={() => setActiveTab('metrics')}
              >
                Metrics
              </button>
              <button
                className={`px-4 py-2 text-sm font-medium ${
                  activeTab === 'radar' ? 'border-b-2 border-blue-500 text-blue-600' : 'text-gray-500 hover:text-gray-700'
                }`}
                onClick={() => setActiveTab('radar')}
              >
                Radar Chart
              </button>
              <button
                className={`px-4 py-2 text-sm font-medium ${
                  activeTab === 'similar' ? 'border-b-2 border-blue-500 text-blue-600' : 'text-gray-500 hover:text-gray-700'
                }`}
                onClick={() => setActiveTab('similar')}
              >
                Similar Players
              </button>
            </nav>
          </div>
          
          {/* Content area */}
          <div className="flex-1 overflow-y-auto p-4">
            {selectedProspects.length === 0 ? (
              <div className="text-center py-8 text-gray-500">
                Select prospects to compare
              </div>
            ) : (
              <>
                {activeTab === 'metrics' && renderMetricsComparison()}
                {activeTab === 'radar' && renderRadarChart()}
                {activeTab === 'similar' && renderSimilarPlayers()}
              </>
            )}
          </div>
        </div>
      </div>
      
      <div className="p-3 border-t bg-gray-50 text-xs text-gray-500">
        Note: Combine data is generated based on prospect profiles for demonstration purposes.
      </div>
    </div>
  );
};

export default ProspectComparison;