// components/StarsynCard.tsx
import React, { useState } from 'react';
import { Star, ChevronRight, Info } from 'lucide-react';

// Define TypeScript interfaces for the data structure
export interface Skill {
  id: string;
  name: string;
  score: number;
}

export interface SkillCategory {
  id: string;
  name: string;
  color: string;
  description: string;
  score: number;
  skills: Skill[];
}

export interface SecondaryInfluence {
  name: string;
  level: number;
  color: string;
  description: string;
}

export interface AssessmentDetails {
  date: string;
  version: string;
  completionRate: number;
  reliability: string;
  questionCount: number;
}

export interface PrimaryType {
  name: string;
  description: string;
  color: string;
  strengths: string;
  learningStyle: string;
  careerPaths: string;
}

export interface StudentProfileData {
  candidateId: string;
  studentName?: string; // Optional, for when in connected mode
  assessmentDetails: AssessmentDetails;
  primaryType: PrimaryType;
  secondaryInfluences: SecondaryInfluence[];
  skillCategories: SkillCategory[];
}

// Internal type for skill visualization
interface EnhancedSkill extends Skill {
  categoryId?: string;
  categoryColor?: string;
  categoryName?: string;
  angle?: number;
  x?: number;
  y?: number;
}

// Props for the component
interface StarsynCardProps {
  studentData: StudentProfileData;
  initialBlindMode?: boolean; // Optional, defaults to true
  onConnect?: (candidateId: string) => void; // Optional callback when connection happens
  userType?: string; // Added for user type-specific customizations
}

const StarsynCard: React.FC<StarsynCardProps> = ({ 
  studentData, 
  initialBlindMode = true,
  onConnect,
  userType = 'STUDENT'
}) => {
  // State declarations
  const [isConnected, setIsConnected] = useState(!initialBlindMode);
  const [expandedCategory, setExpandedCategory] = useState<string | null>('technical');
  const [selectedSkill, setSelectedSkill] = useState<EnhancedSkill | null>(null);
  const [showDetailsPanel, setShowDetailsPanel] = useState(false);
  
  // Section visibility toggles
  const [showTopGrid, setShowTopGrid] = useState(true);
  const [showTopSkills, setShowTopSkills] = useState(true);
  const [showCategories, setShowCategories] = useState(true);
  
  // Flatten all skills for the mini-visualization
  const allSkills: EnhancedSkill[] = studentData.skillCategories.flatMap(category => 
    category.skills.map(skill => ({
      ...skill,
      categoryId: category.id,
      categoryColor: category.color,
      categoryName: category.name
    }))
  );
  
  // Calculate top 5 skills for quick view
  const topSkills = [...allSkills].sort((a, b) => b.score - a.score).slice(0, 5);
  
  // Calculate positions for radial lines based on all individual skills
  const calculateRadialPoints = () => {
    const totalSkills = allSkills.length;
    const angleStep = (2 * Math.PI) / totalSkills;
    
    return allSkills.map((skill, index) => {
      const angle = index * angleStep;
      // Scale the score to determine line length
      const length = (skill.score / 100) * 45;
      
      // Calculate end point of the line
      const x = 50 + length * Math.cos(angle);
      const y = 50 + length * Math.sin(angle);
      
      return {
        ...skill,
        angle,
        x,
        y
      };
    });
  };
  
  const radialSkills = calculateRadialPoints();
  
  // Generate circular guides
  const generateGuides = (count = 3) => {
    return Array.from({ length: count }).map((_, i) => {
      const percentage = ((i + 1) * 33); // 33%, 66%, 100%
      const radius = (percentage / 100) * 45; // Map to 0-45% of container radius
      return { percentage, radius };
    });
  };
  
  const guides = generateGuides();
  
  // Handle skill selection
  const handleSkillSelect = (skill: EnhancedSkill) => {
    setSelectedSkill(selectedSkill?.id === skill.id ? null : skill);
    setShowDetailsPanel(selectedSkill?.id !== skill.id);
  };
  
  const toggleCategory = (categoryId: string) => {
    setExpandedCategory(expandedCategory === categoryId ? null : categoryId);
  };

  const toggleConnection = () => {
    const newConnectedState = !isConnected;
    setIsConnected(newConnectedState);
    if (newConnectedState && onConnect) {
      onConnect(studentData.candidateId);
    }
  };

  // Get title based on user type
  const getTitleByUserType = () => {
    switch (userType) {
      case 'STUDENT':
        return 'Cosmic Profile';
      case 'PROGRAM':
        return 'Program Profile';
      case 'AGENCY':
        return 'Agency Profile';
      case 'MILITARY':
        return 'Service Profile';
      default:
        return 'Starsyn Profile';
    }
  };
  
  return (
    <div className="bg-white rounded-lg shadow-md border border-gray-200 overflow-hidden max-w-4xl mx-auto">
      {/* Header with primary type */}
      <div 
        className="p-3 text-white"
        style={{ 
          background: `linear-gradient(to right, ${studentData.primaryType.color} 100%, ${studentData.primaryType.color}55 33%)` 
        }}
      >
        <div className="flex items-center justify-between">
          <div className="flex items-center">
            <div className="bg-white bg-opacity-20 p-1 rounded-full mr-2">
              <Star className="w-5 h-5 text-yellow-300" />
            </div>
            <div>
              <h1 className="text-lg font-bold">{studentData.primaryType.name.replace('The ', '')} {studentData.candidateId}</h1>
              <p className="text-xs opacity-90">{studentData.primaryType.description}</p>
            </div>
          </div>
          <div className="text-right">
            <div className="text-xs uppercase tracking-wider opacity-80">{getTitleByUserType()}</div>
            <div className="font-bold cursor-pointer" onClick={toggleConnection}>
              {isConnected && studentData.studentName ? studentData.studentName : "Blind Mode"}
            </div>
          </div>
        </div>
      </div>
      
      {/* Secondary Influences - Mini version */}
      <div 
        className="px-3 py-2 flex items-center space-x-2 text-xs"
        style={{ backgroundColor: `${studentData.primaryType.color}10` }}
      >
        <div 
          className="font-medium" 
          style={{ color: studentData.primaryType.color }}
        >
          Influences:
        </div>
        {studentData.secondaryInfluences.map((influence, index) => (
          <div key={index} className="flex items-center">
            <div 
              className="w-2 h-2 rounded-full mr-1" 
              style={{ backgroundColor: influence.color }}
            ></div>
            <span>{influence.name} {influence.level}%</span>
          </div>
        ))}
      </div>
      
      {/* Section header for the top grid */}
      <div className="px-4 pt-4 flex justify-between items-center">
        <h2 className="text-sm font-semibold text-gray-700">Current Assessment</h2>
        <button 
          className="text-xs text-blue-500 hover:text-blue-700 transition"
          onClick={() => setShowTopGrid(!showTopGrid)}
        >
          {showTopGrid ? 'Hide' : 'Show'}
        </button>
      </div>
      
      {/* Main content - 2x2 Grid Layout */}
      {showTopGrid && (
        <div className="p-4 grid grid-cols-2 gap-4">
          {/* Main Type Details - Top Left */}
          <div className="border rounded-lg p-3 shadow-sm">
            <div className="flex items-center mb-2">
              <div 
                className="w-3 h-3 rounded-full mr-1" 
                style={{ backgroundColor: studentData.primaryType.color }}
              ></div>
              <h2 className="text-sm font-semibold" style={{ color: studentData.primaryType.color }}>
                {studentData.primaryType.name.replace('The ', '')}
              </h2>
            </div>
            
            <div className="text-xs space-y-2">
              <div>
                <div className="text-gray-500 mb-1">Key Strengths:</div>
                <div className="font-medium">{studentData.primaryType.strengths}</div>
              </div>
              <div>
                <div className="text-gray-500 mb-1">Learning Style:</div>
                <div className="font-medium">{studentData.primaryType.learningStyle}</div>
              </div>
              <div>
                <div className="text-gray-500 mb-1">Potential Career Paths:</div>
                <div className="font-medium">{studentData.primaryType.careerPaths}</div>
              </div>
            </div>
          </div>
          
          {/* Assessment Details Card - Top Right */}
          <div className="border rounded-lg p-3 shadow-sm">
            <div className="flex items-center mb-2">
              <Info className="w-4 h-4 mr-1 text-indigo-600" />
              <h2 className="text-sm font-semibold text-gray-700">Assessment Details</h2>
            </div>
            
            <div className="text-xs space-y-2">
              <div className="flex justify-between">
                <span className="text-gray-500">Date Completed:</span>
                <span className="font-medium">{studentData.assessmentDetails.date}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-500">Assessment Version:</span>
                <span className="font-medium">{studentData.assessmentDetails.version}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-500">Completion Rate:</span>
                <span className="font-medium">{studentData.assessmentDetails.completionRate}%</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-500">Reliability Score:</span>
                <span className="font-medium">{studentData.assessmentDetails.reliability}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-500">Questions Answered:</span>
                <span className="font-medium">{studentData.assessmentDetails.questionCount}</span>
              </div>
            </div>
          </div>
          
          {/* Secondary Influences - Bottom Left */}
          <div className="border rounded-lg p-3 shadow-sm">
            <h2 className="text-sm font-semibold mb-3 text-gray-700">Secondary Influences</h2>
            <div className="space-y-3">
              {studentData.secondaryInfluences.map((influence, index) => (
                <div key={index} className="p-2 border rounded">
                  <div className="flex justify-between items-center mb-1">
                    <div className="flex items-center">
                      <div 
                        className="w-3 h-3 rounded-full mr-2" 
                        style={{ backgroundColor: influence.color }}
                      ></div>
                      <h3 className="text-sm font-medium">{influence.name}</h3>
                    </div>
                    <div 
                      className="px-2 py-0.5 rounded-full text-xs font-semibold"
                      style={{ 
                        backgroundColor: `${influence.color}20`,
                        color: influence.color
                      }}
                    >
                      {influence.level}%
                    </div>
                  </div>
                  <div className="text-xs mt-1">{influence.description}</div>
                  <div className="mt-1.5">
                    <div className="h-1.5 bg-gray-200 rounded-full overflow-hidden">
                      <div 
                        className="h-full rounded-full" 
                        style={{ width: `${influence.level}%`, backgroundColor: influence.color }}
                      ></div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
          
          {/* Starsyn Fingerprint - Bottom Right */}
          <div className="border rounded-lg p-3 shadow-sm">
            <h2 className="text-sm font-semibold mb-2 text-gray-700">Starsyn for Candidate {studentData.candidateId}</h2>
            
            <div className="flex justify-center items-center" style={{ height: "220px" }}>
              <div className="relative w-full h-full">
                <svg viewBox="0 0 100 100" className="w-full h-full">
                  {/* Circular guides */}
                  {guides.map((guide, i) => (
                    <g key={`guide-${i}`}>
                      <circle 
                        cx="50" 
                        cy="50" 
                        r={guide.radius} 
                        fill="none" 
                        stroke="#e5e7eb" 
                        strokeWidth="0.2" 
                        strokeDasharray="1,1"
                      />
                    </g>
                  ))}
                  
                  {/* Radial lines (spokes) grouped by category */}
                  {studentData.skillCategories.map((category) => {
                    // Filter skills in this category
                    const categorySkills = radialSkills.filter(skill => skill.categoryId === category.id);
                    
                    // Is this category highlighted in the accordion?
                    const isHighlighted = expandedCategory === category.id;
                    
                    return (
                      <g 
                        key={`category-${category.id}`}
                        className="transition-all duration-300"
                      >
                        {/* Category area highlight */}
                        {isHighlighted && (
                          <path
                            d={`M50,50 ${categorySkills.map(skill => `L${skill.x},${skill.y}`).join(' ')} Z`}
                            fill={`${category.color}10`}
                            stroke={category.color}
                            strokeWidth="0.2"
                            strokeDasharray="1,1"
                          />
                        )}
                        
                        {categorySkills.map((skill) => (
                          <g 
                            key={`spoke-${skill.id}`}
                            className="cursor-pointer"
                            onClick={() => handleSkillSelect(skill)}
                          >
                            <line 
                              x1="50" 
                              y1="50" 
                              x2={skill.x} 
                              y2={skill.y} 
                              stroke={category.color} 
                              strokeWidth={selectedSkill?.id === skill.id ? "1.2" : "0.5"} 
                              strokeLinecap="round"
                            />
                            
                            {/* Skill point */}
                            <circle 
                              cx={skill.x} 
                              cy={skill.y} 
                              r={selectedSkill?.id === skill.id ? "1.8" : "1.2"} 
                              fill={category.color}
                            />
                            
                            {/* Glow effect for selected skill */}
                            {selectedSkill?.id === skill.id && (
                              <circle 
                                cx={skill.x} 
                                cy={skill.y} 
                                r="2.5" 
                                fill="none"
                                stroke={category.color}
                                strokeWidth="0.3"
                                opacity="0.6"
                              />
                            )}
                            
                            {/* Selected skill tooltip (without percentage) */}
                            {selectedSkill?.id === skill.id && (
                              <g>
                                <rect
                                  x={skill.x - 10}
                                  y={skill.y - 8}
                                  width="20"
                                  height="6"
                                  rx="1"
                                  fill="white"
                                  stroke={category.color}
                                  strokeWidth="0.2"
                                />
                                <text
                                  x={skill.x}
                                  y={skill.y - 4.5}
                                  fontSize="2.5"
                                  fill={category.color}
                                  textAnchor="middle"
                                  fontWeight="bold"
                                >
                                  {skill.name.split(' ')[0]}
                                </text>
                              </g>
                            )}
                          </g>
                        ))}
                      </g>
                    );
                  })}
                  
                  {/* Center Circle with pulse animation */}
                  <circle 
                    cx="50" 
                    cy="50" 
                    r="8" 
                    fill={`url(#centerGradient)`}
                  >
                    <animate 
                      attributeName="r" 
                      values="7.5;8.5;7.5" 
                      dur="3s" 
                      repeatCount="indefinite" 
                    />
                  </circle>
                  
                  {/* Outer glow */}
                  <circle 
                    cx="50" 
                    cy="50" 
                    r="10" 
                    fill="none"
                    stroke={studentData.primaryType.color}
                    strokeWidth="0.5"
                    opacity="0.4"
                  >
                    <animate 
                      attributeName="opacity" 
                      values="0.4;0.1;0.4" 
                      dur="2s" 
                      repeatCount="indefinite" 
                    />
                  </circle>
                  
                  <text 
                    x="50" 
                    y="52" 
                    fontSize="4"
                    fontWeight="bold"
                    fill="white"
                    textAnchor="middle"
                    dominantBaseline="middle"
                    className="text-center"
                  >
                    {studentData.primaryType.name.split(' ')[1]?.[0] || 'A'}
                  </text>
                  
                  <defs>
                    <radialGradient id="centerGradient" cx="50%" cy="50%" r="50%" fx="40%" fy="40%">
                      <stop offset="0%" stopColor="#FFFFFF" stopOpacity="0.3" />
                      <stop offset="70%" stopColor={studentData.primaryType.color} stopOpacity="1" />
                    </radialGradient>
                  </defs>
                </svg>
              </div>
            </div>
          </div>
        </div>
      )}
      
      {/* Top Skills Section below the grid */}
      <div className="px-4 pb-4">
        <div className="flex justify-between items-center mb-2 mt-1">
          <h2 className="text-sm font-semibold text-gray-700">Top Skills</h2>
          <button 
            className="text-xs text-blue-500 hover:text-blue-700 transition"
            onClick={() => setShowTopSkills(!showTopSkills)}
          >
            {showTopSkills ? 'Hide' : 'Show'}
          </button>
        </div>
        
        {showTopSkills && (
          <div className="grid grid-cols-5 gap-2">
            {topSkills.map((skill, index) => (
              <div 
                key={skill.id} 
                className={`flex flex-col p-2 rounded border ${
                  selectedSkill?.id === skill.id ? 'bg-gray-50 border-gray-300 shadow-sm' : 'hover:bg-gray-50 border-gray-200'
                } cursor-pointer transition-all`}
                onClick={() => handleSkillSelect(skill)}
              >
                <div className="flex items-center justify-between mb-1">
                  <div 
                    className="w-2 h-2 rounded-full"
                    style={{ backgroundColor: skill.categoryColor }}
                  ></div>
                  <div className="text-xs font-bold">#{index + 1}</div>
                </div>
                <div 
                  className="w-full h-1 rounded-full mb-1"
                  style={{ backgroundColor: skill.categoryColor }}
                ></div>
                <div className="text-xs text-center font-medium truncate w-full">{skill.name}</div>
                <div 
                  className="text-xs text-center px-1 py-0.5 mt-1 rounded-full mx-auto"
                  style={{ 
                    backgroundColor: `${skill.categoryColor}15`,
                    color: skill.categoryColor 
                  }}
                >
                  {skill.score}%
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
      
      {/* Skill Details Panel - when a skill is selected */}
      {selectedSkill && showDetailsPanel && (
        <div className="mx-4 mb-4 p-3 bg-white rounded-md border border-gray-200 shadow-sm text-xs animate-fadeIn">
          <div className="flex justify-between items-center mb-2">
            <div className="flex items-center">
              <div 
                className="w-3 h-3 rounded-full mr-2" 
                style={{ backgroundColor: selectedSkill.categoryColor }}
              ></div>
              <span className="font-semibold">{selectedSkill.name}</span>
            </div>
            <div 
              className="px-2 py-0.5 rounded-full font-medium"
              style={{ 
                backgroundColor: `${selectedSkill.categoryColor}20`,
                color: selectedSkill.categoryColor 
              }}
            >
              {selectedSkill.score}%
            </div>
          </div>
          
          <div className="mb-2">
            <div className="flex justify-between mb-1">
              <span className="text-gray-500">Proficiency</span>
              <span className="font-medium">
                {selectedSkill.score >= 90 ? 'Expert' : 
                 selectedSkill.score >= 80 ? 'Advanced' : 
                 selectedSkill.score >= 70 ? 'Proficient' : 
                 selectedSkill.score >= 60 ? 'Intermediate' : 'Beginner'}
              </span>
            </div>
            <div className="h-1.5 bg-gray-200 rounded-full overflow-hidden">
              <div 
                className="h-full rounded-full" 
                style={{ width: `${selectedSkill.score}%`, backgroundColor: selectedSkill.categoryColor }}
              ></div>
            </div>
          </div>
          
          <div className="text-gray-600">
            <p>Part of {selectedSkill.categoryName} skill group, ranking {topSkills.findIndex(s => s.id === selectedSkill.id) > -1 ? 'among your top skills' : 'as a solid skill'}.</p>
          </div>
        </div>
      )}
      
      {/* Skill Categories Section - Accordion style */}
      <div className="px-4 pb-4">
        <div className="flex justify-between items-center mb-2">
          <h2 className="text-sm font-semibold text-gray-700">Skill Categories</h2>
          <button 
            className="text-xs text-blue-500 hover:text-blue-700 transition"
            onClick={() => setShowCategories(!showCategories)}
          >
            {showCategories ? 'Hide' : 'Show'}
          </button>
        </div>
        
        {showCategories && (
          <div className="space-y-2">
            {studentData.skillCategories.map(category => (
              <div key={category.id} className="border rounded-md overflow-hidden">
                <div 
                  className="flex justify-between items-center p-2 cursor-pointer hover:bg-gray-50"
                  onClick={() => toggleCategory(category.id)}
                >
                  <div className="flex items-center">
                    <div 
                      className="w-3 h-3 rounded-full mr-2" 
                      style={{ backgroundColor: category.color }}
                    ></div>
                    <span className="text-sm font-medium">{category.name}</span>
                  </div>
                  <div className="flex items-center">
                    <span 
                      className="text-xs font-medium px-2 py-0.5 rounded-full mr-2"
                      style={{ 
                        backgroundColor: `${category.color}20`,
                        color: category.color 
                      }}
                    >
                      {category.score}%
                    </span>
                    <ChevronRight 
                      className={`w-4 h-4 text-gray-400 transition-transform ${
                        expandedCategory === category.id ? 'transform rotate-90' : ''
                      }`} 
                    />
                  </div>
                </div>
                
                {/* Skills within category - collapsible */}
                {expandedCategory === category.id && (
                  <div className="p-2 pt-0 bg-gray-50 border-t">
                    <div className="text-xs text-gray-500 italic p-1 mb-1">{category.description}</div>
                    <div className="grid grid-cols-3 gap-2">
                      {category.skills.map(skill => (
                        <div 
                          key={skill.id}
                          className={`p-2 text-xs bg-white rounded border cursor-pointer hover:shadow-sm ${
                            selectedSkill?.id === skill.id ? 'border-gray-300 shadow-sm' : ''
                          }`}
                          onClick={() => handleSkillSelect({
                            ...skill,
                            categoryColor: category.color,
                            categoryName: category.name
                          })}
                        >
                          <div className="flex justify-between mb-1">
                            <span className="truncate">{skill.name}</span>
                            <span 
                              className="font-medium px-1 rounded"
                              style={{ 
                                backgroundColor: `${category.color}20`,
                                color: category.color 
                              }}
                            >
                              {skill.score}%
                            </span>
                          </div>
                          <div className="h-1.5 bg-gray-200 rounded-full overflow-hidden">
                            <div 
                              className="h-full rounded-full" 
                              style={{ width: `${skill.score}%`, backgroundColor: category.color }}
                            ></div>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </div>
      
      {/* Footer */}
      <div 
        className="px-4 py-2 border-t border-gray-200 flex justify-between items-center text-xs"
        style={{ backgroundColor: `${studentData.primaryType.color}05`, color: studentData.primaryType.color }}
      >
        <div>Starsyn.ai</div>
        <div>{studentData.assessmentDetails.date}</div>
      </div>
    </div>
  );
};

export default StarsynCard;
