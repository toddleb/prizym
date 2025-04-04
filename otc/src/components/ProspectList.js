import React, { useContext, useState } from 'react';
import { DraftContext } from '../context/DraftContext';

const SimplifiedProspectList = ({ setSelectedProspect }) => {
  const { prospects } = useContext(DraftContext);
  
  const [search, setSearch] = useState('');
  const [positionFilter, setPositionFilter] = useState('All');

  const positions = ['All', 'QB', 'RB', 'WR', 'TE', 'OT', 'OG', 'EDGE', 'DT', 'LB', 'CB', 'S'];
  
  const filteredProspects = Array.isArray(prospects) ? prospects.filter(prospect => {
    const matchesSearch = prospect.name.toLowerCase().includes(search.toLowerCase()) || 
                         prospect.college.toLowerCase().includes(search.toLowerCase());
    
    const matchesPosition = positionFilter === 'All' || 
                         prospect.position === positionFilter ||
                         (positionFilter === 'OL' && ['OT', 'OG', 'C'].includes(prospect.position)) ||
                         (positionFilter === 'DL' && ['DT', 'DE'].includes(prospect.position));
    
    return matchesSearch && matchesPosition;
  }) : [];

  return (
    <div className="bg-white h-full p-4 overflow-hidden flex flex-col">
      <h2 className="text-xl font-bold mb-4">Draft Prospects</h2>
      
      <div className="mb-4 flex space-x-2">
        <input
          type="text"
          placeholder="Search prospects..."
          className="flex-1 px-4 py-2 border rounded"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
        
        <select 
          className="px-4 py-2 border rounded bg-white"
          value={positionFilter}
          onChange={(e) => setPositionFilter(e.target.value)}
        >
          {positions.map(pos => (
            <option key={pos} value={pos}>{pos}</option>
          ))}
        </select>
      </div>
      
      <div className="overflow-y-auto flex-grow">
        <table className="min-w-full">
          <thead className="bg-gray-100 sticky top-0">
            <tr>
              <th className="px-4 py-2 text-left">Name</th>
              <th className="px-4 py-2 text-center">Pos</th>
              <th className="px-4 py-2 text-left">College</th>
              <th className="px-4 py-2 text-center">Grade</th>
            </tr>
          </thead>
          <tbody>
            {filteredProspects.map(prospect => (
              <tr 
                key={prospect.id} 
                className="border-b hover:bg-gray-50 cursor-pointer"
                onClick={() => setSelectedProspect(prospect)}
              >
                <td className="px-4 py-2 font-medium">{prospect.name}</td>
                <td className="px-4 py-2 text-center">
                  <span className="px-2 py-1 rounded-full text-xs bg-gray-100">
                    {prospect.position}
                  </span>
                </td>
                <td className="px-4 py-2">{prospect.college}</td>
                <td className="px-4 py-2 text-center">
                  {prospect.grade.toFixed(1)}
                </td>
              </tr>
            ))}
            
            {filteredProspects.length === 0 && (
              <tr>
                <td colSpan="4" className="px-4 py-2 text-center text-gray-500">
                  No prospects match your filters
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default SimplifiedProspectList;