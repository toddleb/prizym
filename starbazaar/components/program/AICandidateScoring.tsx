// components/program/AICandidateScoring.tsx
import { useState, useEffect } from 'react';
import {
  Box,
  Flex,
  Heading,
  Text,
  Button,
  VStack,
  HStack,
  Badge,
  Progress,
  SimpleGrid,
  Stat,
  StatLabel,
  StatNumber,
  StatHelpText,
  StatArrow,
  Tag,
  TagLabel,
  Avatar,
  Grid,
  GridItem,
  IconButton,
  Select,
  Divider,
  Tooltip,
  useColorModeValue
} from '@chakra-ui/react';
import { 
  StarIcon, 
  InfoIcon, 
  ChevronDownIcon, 
  ChevronRightIcon, 
  QuestionIcon, 
  DownloadIcon,
  ViewIcon
} from '@chakra-ui/icons';
import { 
  FaCode, 
  FaBrain, 
  FaUserGraduate, 
  FaUsers, 
  FaLightbulb, 
  FaChartLine, 
  FaGithub, 
  FaLinkedin,
  FaRegCalendarAlt
} from 'react-icons/fa';

interface CandidateScore {
  id: string;
  name: string | null;
  blindId: string;
  isRevealed: boolean;
  matchScore: number;
  skillsMatch: number;
  learningMatch: number;
  experienceMatch: number;
  softSkillsMatch: number;
  intentScore: number;
  signalStrength: number;
  program: string;
  department: string;
  institution: string;
  predictedSuccess: number;
  skills: string[];
  lastActivity: string;
  signals: {
    type: string;
    description: string;
    date: string;
    strength: number;
  }[];
  strengthFactors: string[];
  growthAreas: string[];
}

export default function AICandidateScoring() {
  const [selectedCandidate, setSelectedCandidate] = useState<CandidateScore | null>(null);
  const [scoreView, setScoreView] = useState<'simple' | 'detailed'>('simple');
  const [compareMode, setCompareMode] = useState(false);
  const [comparedCandidates, setComparedCandidates] = useState<CandidateScore[]>([]);
  
  const bgColor = useColorModeValue('white', 'gray.700');
  const borderColor = useColorModeValue('gray.200', 'gray.600');
  
  // Sample matched candidates data
  const candidates: CandidateScore[] = [
    {
      id: 'c001',
      name: null,
      blindId: 'Candidate #145',
      isRevealed: false,
      matchScore: 95,
      skillsMatch: 98,
      learningMatch: 92,
      experienceMatch: 88,
      softSkillsMatch: 94,
      intentScore: 87,
      signalStrength: 4,
      program: 'B.S. Data Science',
      department: 'Computer Science',
      institution: 'Northern Arizona University',
      predictedSuccess: 94,
      skills: ['Python', 'Machine Learning', 'Data Analysis', 'Statistics', 'SQL'],
      lastActivity: '3 hours ago',
      signals: [
        {
          type: 'github',
          description: 'Contributed to ML project',
          date: '3 hours ago',
          strength: 5
        },
        {
          type: 'event',
          description: 'RSVP\'d to AI Career Fair',
          date: '2 days ago',
          strength: 4
        }
      ],
      strengthFactors: [
        'Advanced Python skills',
        'Multiple ML projects',
        'Statistical analysis experience',
        'High engagement with AI content'
      ],
      growthAreas: [
        'Limited industry experience',
        'No team project indication'
      ]
    },
    {
      id: 'c002',
      name: 'Taylor Kim',
      blindId: 'Candidate #092',
      isRevealed: true,
      matchScore: 92,
      skillsMatch: 94,
      learningMatch: 95,
      experienceMatch: 82,
      softSkillsMatch: 90,
      intentScore: 92,
      signalStrength: 5,
      program: 'B.S. Computer Science',
      department: 'Computer Science',
      institution: 'Northern Arizona University',
      predictedSuccess: 91,
      skills: ['Python', 'AI/ML', 'Data Visualization', 'Cloud Computing', 'JavaScript'],
      lastActivity: '1 day ago',
      signals: [
        {
          type: 'linkedin',
          description: 'Added AI certification',
          date: '1 day ago',
          strength: 4
        },
        {
          type: 'event',
          description: 'Attended ML workshop',
          date: '1 week ago',
          strength: 5
        }
      ],
      strengthFactors: [
        'Strong programming fundamentals',
        'Self-learning initiative',
        'Project portfolio',
        'Communication skills'
      ],
      growthAreas: [
        'Limited statistical background',
        'No research experience'
      ]
    },
    {
      id: 'c003',
      name: null,
      blindId: 'Candidate #217',
      isRevealed: false,
      matchScore: 87,
      skillsMatch: 84,
      learningMatch: 92,
      experienceMatch: 78,
      softSkillsMatch: 89,
      intentScore: 76,
      signalStrength: 3,
      program: 'M.S. Business Analytics',
      department: 'Information Systems',
      institution: 'Northern Arizona University',
      predictedSuccess: 85,
      skills: ['Python', 'Data Analysis', 'SQL', 'Business Intelligence', 'Tableau'],
      lastActivity: 'Today',
      signals: [
        {
          type: 'linkedin',
          description: 'Updated skills profile',
          date: 'Today',
          strength: 3
        }
      ],
      strengthFactors: [
        'Strong data analysis skills',
        'Business domain knowledge',
        'SQL proficiency',
        'Visualization experience'
      ],
      growthAreas: [
        'Limited ML experience',
        'Less programming background',
        'Fewer projects'
      ]
    }
  ];
  
  // Set first candidate as selected by default
  useEffect(() => {
    if (candidates.length > 0 && !selectedCandidate) {
      setSelectedCandidate(candidates[0]);
    }
  }, [candidates]);

  // Function to toggle candidate in comparison
  const toggleCandidateComparison = (candidate: CandidateScore) => {
    if (comparedCandidates.some(c => c.id === candidate.id)) {
      setComparedCandidates(comparedCandidates.filter(c => c.id !== candidate.id));
    } else if (comparedCandidates.length < 3) {
      setComparedCandidates([...comparedCandidates, candidate]);
    }
  };
  
  // Helper function to get a color based on score
  const getScoreColor = (score: number) => {
    if (score >= 90) return 'green';
    if (score >= 80) return 'blue';
    if (score >= 70) return 'yellow';
    return 'red';
  };
  
  // Helper function to get category name and icon
  const getCategoryInfo = (category: string) => {
    switch (category) {
      case 'skillsMatch':
        return { name: 'Technical Skills', icon: <FaCode />, color: 'blue.500' };
      case 'learningMatch':
        return { name: 'Learning Style', icon: <FaBrain />, color: 'green.500' };
      case 'experienceMatch':
        return { name: 'Prior Experience', icon: <FaUserGraduate />, color: 'orange.500' };
      case 'softSkillsMatch':
        return { name: 'Soft Skills', icon: <FaUsers />, color: 'purple.500' };
      default:
        return { name: category, icon: <StarIcon />, color: 'gray.500' };
    }
  };
  
  // Helper function for signal icon
  const getSignalIcon = (type: string) => {
    switch (type) {
      case 'github':
        return <FaGithub />;
      case 'linkedin':
        return <FaLinkedin />;
      case 'event':
        return <FaRegCalendarAlt />;
      default:
        return <FaLightbulb />;
    }
  };
  
  return (
    <Box>
      <Box mb={6} bg={bgColor} borderRadius="lg" boxShadow="md" overflow="hidden">
        <Flex 
          justify="space-between" 
          align="center" 
          bg="blue.600" 
          p={4} 
          color="white"
        >
          <Heading size="md">AI-Powered Candidate Analysis</Heading>
          <HStack>
            <Button 
              size="sm" 
              variant="outline" 
              colorScheme="whiteAlpha"
              leftIcon={<FaChartLine />}
              onClick={() => setScoreView(scoreView === 'simple' ? 'detailed' : 'simple')}
            >
              {scoreView === 'simple' ? 'Detailed Analysis' : 'Simple View'}
            </Button>
            <Button 
              size="sm" 
              variant={compareMode ? "solid" : "outline"} 
              colorScheme={compareMode ? "green" : "whiteAlpha"}
              onClick={() => {
                setCompareMode(!compareMode);
                if (!compareMode && selectedCandidate) {
                  setComparedCandidates([selectedCandidate]);
                }
              }}
            >
              {compareMode ? 'Exit Compare' : 'Compare Candidates'}
            </Button>
          </HStack>
        </Flex>
        
        {!compareMode ? (
          // Single candidate analysis
          <Box p={6}>
            {selectedCandidate ? (
              <>
                <Flex justify="space-between" align="start" mb={6}>
                  <HStack align="start" spacing={4}>
                    {selectedCandidate.isRevealed ? (
                      <Avatar 
                        size="lg" 
                        name={selectedCandidate.name} 
                        bg="blue.500"
                      />
                    ) : (
                      <Flex 
                        width="64px"
                        height="64px"
                        bg="blue.100"
                        borderRadius="full"
                        align="center"
                        justify="center"
                      >
                        <ViewIcon color="blue.500" boxSize={6} />
                      </Flex>
                    )}
                    
                    <Box>
                      <HStack mb={1}>
                        <Heading size="md">
                          {selectedCandidate.isRevealed ? selectedCandidate.name : selectedCandidate.blindId}
                        </Heading>
                        {!selectedCandidate.isRevealed && (
                          <Badge colorScheme="gray">Blind Mode</Badge>
                        )}
                      </HStack>
                      
                      <Text color="gray.600" fontSize="sm">
                        {selectedCandidate.program} • {selectedCandidate.department}
                      </Text>
                      
                      <HStack mt={2} spacing={2}>
                        <Badge colorScheme="blue" fontSize="md" p={1} borderRadius="md">
                          {selectedCandidate.matchScore}% Match
                        </Badge>
                        <Badge colorScheme="green" fontSize="md" p={1} borderRadius="md">
                          {selectedCandidate.predictedSuccess}% Success
                        </Badge>
                      </HStack>
                    </Box>
                  </HStack>
                  
                  <Box>
                    <Select 
                      placeholder="Select candidate" 
                      size="sm" 
                      width="200px"
                      value={selectedCandidate.id}
                      onChange={(e) => {
                        const selected = candidates.find(c => c.id === e.target.value);
                        if (selected) setSelectedCandidate(selected);
                      }}
                    >
                      {candidates.map(candidate => (
                        <option key={candidate.id} value={candidate.id}>
                          {candidate.isRevealed ? candidate.name : candidate.blindId} ({candidate.matchScore}%)
                        </option>
                      ))}
                    </Select>
                  </Box>
                </Flex>
                
                {scoreView === 'simple' ? (
                  // Simple score view
                  <SimpleGrid columns={2} spacing={6}>
                    <Box>
                      <Heading size="sm" mb={3}>Match Breakdown</Heading>
                      
                      <VStack align="stretch" spacing={3}>
                        {['skillsMatch', 'learningMatch', 'experienceMatch', 'softSkillsMatch'].map(category => {
                          const { name, icon, color } = getCategoryInfo(category);
                          const score = selectedCandidate[category];
                          
                          return (
                            <Box key={category}>
                              <Flex justify="space-between" align="center" mb={1}>
                                <HStack>
                                  <Box color={color}>{icon}</Box>
                                  <Text fontSize="sm">{name}</Text>
                                </HStack>
                                <Text fontWeight="bold" fontSize="sm">{score}%</Text>
                              </Flex>
                              <Progress 
                                value={score} 
                                size="sm" 
                                colorScheme={getScoreColor(score)}
                                borderRadius="full"
                              />
                            </Box>
                          );
                        })}
                      </VStack>
                      
                      <Box mt={6}>
                        <Heading size="sm" mb={3}>Intent Signals</Heading>
                        
                        <Flex justify="space-between" align="center" mb={1}>
                          <Text fontSize="sm">Signal Strength</Text>
                          <HStack spacing={1}>
                            {[1, 2, 3, 4, 5].map(i => (
                              <Box 
                                key={i} 
                                w="12px" 
                                h="12px" 
                                borderRadius="full" 
                                bg={i <= selectedCandidate.signalStrength ? 'blue.500' : 'gray.200'} 
                              />
                            ))}
                          </HStack>
                        </Flex>
                        
                        <Box mt={3}>
                          <Text fontSize="sm" fontWeight="medium" mb={2}>Recent Activity:</Text>
                          {selectedCandidate.signals.map((signal, index) => (
                            <HStack key={index} mb={2} bg="gray.50" p={2} borderRadius="md">
                              <Box color="blue.500">
                                {getSignalIcon(signal.type)}
                              </Box>
                              <Box flex="1">
                                <Text fontSize="sm">{signal.description}</Text>
                                <Text fontSize="xs" color="gray.500">{signal.date}</Text>
                              </Box>
                              <Badge colorScheme={signal.strength > 3 ? 'green' : 'blue'}>
                                {signal.strength}/5
                              </Badge>
                            </HStack>
                          ))}
                        </Box>
                      </Box>
                    </Box>
                    
                    <Box>
                      <Heading size="sm" mb={3}>AI Insights</Heading>
                      
                      <Box p={4} bg="blue.50" borderRadius="md" mb={4}>
                        <Flex align="center" mb={2}>
                          <FaBrain color="#3182CE" style={{ marginRight: '8px' }} />
                          <Heading size="xs" color="blue.700">Success Prediction</Heading>
                        </Flex>
                        <Text fontSize="sm" color="blue.700">
                          This candidate has a <b>{selectedCandidate.predictedSuccess}%</b> predicted success 
                          rate in your program based on skill alignment and engagement patterns.
                        </Text>
                      </Box>
                      
                      <Box mb={4}>
                        <Heading size="xs" mb={2}>Key Strengths</Heading>
                        <VStack align="stretch" spacing={1}>
                          {selectedCandidate.strengthFactors.map((factor, index) => (
                            <HStack key={index} bg="green.50" p={2} borderRadius="md">
                              <Box color="green.500" fontSize="sm">✓</Box>
                              <Text fontSize="sm">{factor}</Text>
                            </HStack>
                          ))}
                        </VStack>
                      </Box>
                      
                      <Box>
                        <Heading size="xs" mb={2}>Growth Areas</Heading>
                        <VStack align="stretch" spacing={1}>
                          {selectedCandidate.growthAreas.map((area, index) => (
                            <HStack key={index} bg="yellow.50" p={2} borderRadius="md">
                              <Box color="yellow.500" fontSize="sm">→</Box>
                              <Text fontSize="sm">{area}</Text>
                            </HStack>
                          ))}
                        </VStack>
                      </Box>
                      
                      <Divider my={4} />
                      
                      <Box>
                        <Heading size="xs" mb={2}>Skills</Heading>
                        <Flex wrap="wrap" gap={2}>
                          {selectedCandidate.skills.map((skill, index) => (
                            <Tag key={index} colorScheme="blue" size="sm">
                              <TagLabel>{skill}</TagLabel>
                            </Tag>
                          ))}
                        </Flex>
                      </Box>
                    </Box>
                  </SimpleGrid>
                ) : (
                  // Detailed analysis view
                  <Box>
                    <Heading size="sm" mb={4}>Comprehensive Analysis</Heading>
                    
                    <SimpleGrid columns={3} spacing={4} mb={6}>
                      <Stat bg="blue.50" p={3} borderRadius="md">
                        <StatLabel>Technical Match</StatLabel>
                        <StatNumber>{selectedCandidate.skillsMatch}%</StatNumber>
                        <StatHelpText>
                          <StatArrow type={selectedCandidate.skillsMatch > 85 ? 'increase' : 'decrease'} />
                          vs. program average
                        </StatHelpText>
                      </Stat>
                      
                      <Stat bg="green.50" p={3} borderRadius="md">
                        <StatLabel>Learning Fit</StatLabel>
                        <StatNumber>{selectedCandidate.learningMatch}%</StatNumber>
                        <StatHelpText>
                          <StatArrow type={selectedCandidate.learningMatch > 85 ? 'increase' : 'decrease'} />
                          vs. program average
                        </StatHelpText>
                      </Stat>
                      
                      <Stat bg="purple.50" p={3} borderRadius="md">
                        <StatLabel>Intent Score</StatLabel>
                        <StatNumber>{selectedCandidate.intentScore}%</StatNumber>
                        <StatHelpText>
                          <StatArrow type={selectedCandidate.intentScore > 80 ? 'increase' : 'decrease'} />
                          vs. program average
                        </StatHelpText>
                      </Stat>
                    </SimpleGrid>
                    
                    <Grid templateColumns="1fr 1fr" gap={6}>
                      <GridItem>
                        <Box p={4} borderWidth="1px" borderRadius="md" borderColor={borderColor} height="100%">
                          <Heading size="sm" mb={3}>Signal Analysis</Heading>
                          
                          <Box mb={4}>
                            <Text fontSize="sm" fontWeight="medium">Signal Strength Assessment:</Text>
                            <Text fontSize="sm" mt={1}>
                              This candidate shows {selectedCandidate.signalStrength >= 4 ? 'strong' : 
                                                    selectedCandidate.signalStrength >= 3 ? 'moderate' : 'limited'} indicators of 
                              interest in your program. {selectedCandidate.signalStrength >= 4 ? 
                                'Early outreach is highly recommended.' : 
                                'Consider nurturing this candidate with more information.'}
                            </Text>
                          </Box>
                          
                          <Box mb={4}>
                            <Text fontSize="sm" fontWeight="medium">Recent Activity Pattern:</Text>
                            <Text fontSize="sm" mt={1}>
                              Activity frequency and quality suggests {selectedCandidate.intentScore >= 85 ? 
                                'high intent' : 'moderate intent'} to pursue opportunities in this field.
                              {selectedCandidate.signals.length > 1 ? 
                                ' Multiple touchpoints indicate sustained interest.' : 
                                ' Limited touchpoints suggest potential for more engagement.'}
                            </Text>
                          </Box>
                          
                          <Box>
                            <Text fontSize="sm" fontWeight="medium">Engagement Recommendation:</Text>
                            <Text fontSize="sm" mt={1} bg="blue.50" p={2} borderRadius="md">
                              {selectedCandidate.intentScore >= 90 ? 
                                'Direct outreach with personalized invitation to apply.' :
                                selectedCandidate.intentScore >= 80 ?
                                'Invite to program-specific info session or webinar.' :
                                'Share relevant content and learning opportunities.'}
                            </Text>
                          </Box>
                        </Box>
                      </GridItem>
                      
                      <GridItem>
                        <Box p={4} borderWidth="1px" borderRadius="md" borderColor={borderColor} height="100%">
                          <Heading size="sm" mb={3}>Success Prediction Model</Heading>
                          
                          <HStack spacing={4} mb={4}>
                            <Box textAlign="center" p={3} borderRadius="md" bg="green.50" flex="1">
                              <Heading size="md" color="green.500">{selectedCandidate.predictedSuccess}%</Heading>
                              <Text fontSize="xs">Success Probability</Text>
                            </Box>
                            
                            <Box textAlign="center" p={3} borderRadius="md" bg="blue.50" flex="1">
                              <Heading size="md" color="blue.500">{selectedCandidate.matchScore}%</Heading>
                              <Text fontSize="xs">Profile Match</Text>
                            </Box>
                          </HStack>
                          
                          <Box mb={4}>
                            <Text fontSize="sm" fontWeight="medium">Success Factors:</Text>
                            <Text fontSize="sm" mt={1}>
                              AI analysis indicates this candidate has a {selectedCandidate.predictedSuccess >= 90 ? 
                                'very strong' : selectedCandidate.predictedSuccess >= 80 ? 'strong' : 'moderate'} likelihood of 
                              success based on skill alignment, learning style, and engagement patterns.
                            </Text>
                          </Box>
                          
                          <Box>
                            <Text fontSize="sm" fontWeight="medium">Comparable Outcomes:</Text>
                            <Text fontSize="sm" mt={1} bg="gray.50" p={2} borderRadius="md">
                              Based on historical data, candidates with similar profiles have a 
                              {selectedCandidate.predictedSuccess >= 90 ? 
                                ' 92% program completion rate and 88% job placement rate.' :
                                selectedCandidate.predictedSuccess >= 80 ?
                                ' 85% program completion rate and 75% job placement rate.' :
                                ' 70% program completion rate and 65% job placement rate.'}
                            </Text>
                          </Box>
                        </Box>
                      </GridItem>
                    </Grid>
                  </Box>
                )}
                
                <Flex justify="center" mt={6}>
                  <Button 
                    colorScheme="blue" 
                    leftIcon={<DownloadIcon />}
                    mr={4}
                  >
                    Export Analysis
                  </Button>
                  
                  {!compareMode && (
                    <Button 
                      colorScheme="green" 
                      onClick={() => {
                        setCompareMode(true);
                        setComparedCandidates([selectedCandidate]);
                      }}
                    >
                      Compare With Others
                    </Button>
                  )}
                </Flex>
              </>
            ) : (
              <Box textAlign="center" p={10} color="gray.500">
                <Text>No candidate selected</Text>
              </Box>
            )}
          </Box>
        ) : (
          // Comparison view
          <Box p={6}>
            <Flex justify="space-between" align="center" mb={6}>
              <Heading size="sm">Candidate Comparison ({comparedCandidates.length}/3)</Heading>
              <HStack>
                <Select 
                  placeholder="Add candidate to compare" 
                  size="sm" 
                  width="200px"
                  onChange={(e) => {
                    const candidateToAdd = candidates.find(c => c.id === e.target.value);
                    if (candidateToAdd && !comparedCandidates.some(c => c.id === candidateToAdd.id)) {
                      if (comparedCandidates.length < 3) {
                        setComparedCandidates([...comparedCandidates, candidateToAdd]);
                      }
                    }
                  }}
                >
                  {candidates
                    .filter(c => !comparedCandidates.some(cc => cc.id === c.id))
                    .map(candidate => (
                      <option key={candidate.id} value={candidate.id}>
                        {candidate.isRevealed ? candidate.name : candidate.blindId} ({candidate.matchScore}%)
                      </option>
                    ))}
                </Select>
              </HStack>
            </Flex>
            
            <Grid templateColumns={`repeat(${comparedCandidates.length}, 1fr)`} gap={4} mb={6}>
              {comparedCandidates.map(candidate => (
                <GridItem key={candidate.id}>
                  <Box 
                    p={4} 
                    borderWidth="1px" 
                    borderRadius="md" 
                    borderColor={borderColor}
                    bg={candidate.id === selectedCandidate?.id ? 'blue.50' : 'white'}
                    onClick={() => setSelectedCandidate(candidate)}
                    cursor="pointer"
                    _hover={{ borderColor: 'blue.300' }}
                  >
                    <Flex justify="space-between" align="center" mb={3}>
                      <HStack>
                        {candidate.isRevealed ? (
                          <Avatar size="sm" name={candidate.name} />
                        ) : (
                          <Flex 
                            width="32px"
                            height="32px"
                            bg="blue.100"
                            borderRadius="full"
                            align="center"
                            justify="center"
                          >
                            <ViewIcon color="blue.500" boxSize={4} />
                          </Flex>
                        )}
                        <Text fontWeight="medium">
                          {candidate.isRevealed ? candidate.name : candidate.blindId}
                        </Text>
                      </HStack>
                      
                      <IconButton
                        aria-label="Remove from comparison"
                        icon={<ChevronDownIcon />}
                        size="xs"
                        variant="ghost"
                        onClick={(e) => {
                          e.stopPropagation();
                          setComparedCandidates(comparedCandidates.filter(c => c.id !== candidate.id));
                        }}
                      />
                    </Flex>
                    
                    <Box textAlign="center" mb={4}>
                      <Badge colorScheme="blue" fontSize="lg" p={2} borderRadius="md">
                        {candidate.matchScore}% Match
                      </Badge>
                    </Box>
                    
                    <Text fontSize="sm" color="gray.600" mb={2}>
                      {candidate.program}
                    </Text>
                    
                    <Text fontSize="xs" color="gray.500">
                      Last activity: {candidate.lastActivity}
                    </Text>
                  </Box>
                </GridItem>
              ))}
            </Grid>
            
            <Box mb={6}>
              <Heading size="sm" mb={4}>Match Categories Comparison</Heading>
              
              <VStack align="stretch" spacing={4}>
                {['skillsMatch', 'learningMatch', 'experienceMatch', 'softSkillsMatch', 'intentScore', 'predictedSuccess'].map(category => {
                  const { name, icon, color } = getCategoryInfo(category);
                  const displayName = category === 'intentScore' ? 'Intent Level' : 
                                      category === 'predictedSuccess' ? 'Success Prediction' : name;
                  
                  return (
                    <Box key={category}>
                      <Flex align="center" mb={2}>
                        <Box color={color} mr={2}>{icon}</Box>
                        <Text fontWeight="medium">{displayName}</Text>
                      </Flex>
                      
                      <Grid templateColumns={`repeat(${comparedCandidates.length}, 1fr)`} gap={2}>
                        {comparedCandidates.map(candidate => (
                          <GridItem key={`${candidate.id}-${category}`}>
                            <Box>
                              <Progress 
                                value={candidate[category]} 
                                size="lg" 
                                colorScheme={getScoreColor(candidate[category])}
                                borderRadius="full"
                              />
                              <Flex justify="space-between" mt={1}>
                                <Text fontSize="xs" color="gray.500">
                                  {candidate.isRevealed ? candidate.name : candidate.blindId}
                                </Text>
                                <Text fontSize="xs" fontWeight="bold">
                                  {candidate[category]}%
                                </Text>
                              </Flex>
                            </Box>
                          </GridItem>
                        ))}
                      </Grid>
                    </Box>
                  );
                })}
              </VStack>
            </Box>
            
            <Box>
              <Heading size="sm" mb={4}>Skills Comparison</Heading>
              
              <Box borderWidth="1px" borderRadius="md" borderColor={borderColor} p={4}>
                <Grid templateColumns={`auto ${comparedCandidates.map(() => '1fr').join(' ')}`} gap={4}>
                  <GridItem>
                    <Text fontWeight="bold" mb={3}>Skills</Text>
                    {Array.from(new Set(comparedCandidates.flatMap(c => c.skills))).map(skill => (
                      <Text key={skill} fontSize="sm" py={1}>{skill}</Text>
                    ))}
                  </GridItem>
                  
                  {comparedCandidates.map(candidate => (
                    <GridItem key={candidate.id}>
                      <Text fontWeight="bold" mb={3} textAlign="center">
                        {candidate.isRevealed ? candidate.name : candidate.blindId}
                      </Text>
                      
                      {Array.from(new Set(comparedCandidates.flatMap(c => c.skills))).map(skill => (
                        <Flex key={skill} justify="center" py={1}>
                          {candidate.skills.includes(skill) ? (
                            <Badge colorScheme="green">✓</Badge>
                          ) : (
                            <Badge colorScheme="gray">-</Badge>
                          )}
                        </Flex>
                      ))}
                    </GridItem>
                  ))}
                </Grid>
              </Box>
            </Box>
            
            <Flex justify="center" mt={6}>
              <Button 
                colorScheme="blue" 
                leftIcon={<DownloadIcon />}
                mr={4}
              >
                Export Comparison
              </Button>
              
              <Button 
                colorScheme="gray" 
                onClick={() => {
                  setCompareMode(false);
                }}
              >
                Exit Comparison
              </Button>
            </Flex>
          </Box>
        )}
      </Box>
    </Box>
  );
}