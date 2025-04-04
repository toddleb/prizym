// components/program/AIInsightsDashboard.tsx
import { useState } from 'react';
import {
  Box,
  Flex,
  Heading,
  Text,
  Button,
  VStack,
  HStack,
  SimpleGrid,
  Badge,
  IconButton,
  Menu,
  MenuButton,
  MenuList,
  MenuItem,
  Stat,
  StatLabel,
  StatNumber,
  StatHelpText,
  StatArrow,
  Progress,
  Divider,
  Tabs,
  TabList,
  Tab,
  TabPanels,
  TabPanel,
  Tag,
  TagLabel,
  Tooltip,
  useColorModeValue
} from '@chakra-ui/react';
import { 
  InfoIcon, 
  DownloadIcon, 
  ChevronDownIcon, 
  QuestionIcon,
  SettingsIcon,
  RepeatIcon, 
  StarIcon 
} from '@chakra-ui/icons';
import { 
  FaBrain, 
  FaChartBar, 
  FaUniversity, 
  FaUserGraduate, 
  FaCode, 
  FaGithub, 
  FaLinkedin,
  FaUsers,
  FaRegCalendarAlt,
  FaLightbulb
} from 'react-icons/fa';

export default function AIInsightsDashboard() {
  const [activeTab, setActiveTab] = useState('overview');
  const [timeRange, setTimeRange] = useState('90d');
  
  const bgColor = useColorModeValue('white', 'gray.700');
  const borderColor = useColorModeValue('gray.200', 'gray.600');
  
  // Sample AI insights data
  const insights = {
    overview: {
      candidateCount: 142,
      highQualityCount: 28,
      averageMatchScore: 78.4,
      matchScoreTrend: 3.2,
      responseRateTrend: 5.5,
      conversionRateTrend: -1.2,
      topPrograms: [
        { name: 'B.S. Computer Science', candidateCount: 45, matchQuality: 82 },
        { name: 'B.S. Data Science', candidateCount: 38, matchQuality: 89 },
        { name: 'M.S. Computer Science', candidateCount: 22, matchQuality: 76 },
        { name: 'B.S. Information Systems', candidateCount: 16, matchQuality: 70 },
        { name: 'M.S. Business Analytics', candidateCount: 12, matchQuality: 80 }
      ],
    },
    trends: {
      candidateGrowth: 14.5,
      engagementGrowth: 8.2,
      skillTrends: [
        { name: 'Machine Learning', growth: 18.5, prevalence: 68 },
        { name: 'Python', growth: 12.3, prevalence: 82 },
        { name: 'Data Visualization', growth: 15.7, prevalence: 60 },
        { name: 'Cloud Computing', growth: 24.8, prevalence: 42 },
        { name: 'Deep Learning', growth: 32.1, prevalence: 35 }
      ],
      institutionTrends: [
        { name: 'Northern Arizona University', growth: 15.2, matchQuality: 88 },
        { name: 'Arizona State University', growth: 8.5, matchQuality: 75 },
        { name: 'University of Arizona', growth: 5.2, matchQuality: 72 }
      ]
    },
    recommendations: {
      programSuggestions: [
        { 
          action: 'Create specialized AI track', 
          impact: 'high', 
          reasoning: 'Growing demand in candidate skill profiles shows 32% increase in AI-related interests',
          difficulty: 'medium'
        },
        { 
          action: 'Develop cloud computing partnerships', 
          impact: 'medium', 
          reasoning: 'Cloud skills growing 24.8% with limited program coverage',
          difficulty: 'high'
        },
        { 
          action: 'Add data visualization workshop', 
          impact: 'medium', 
          reasoning: '60% of high-matching candidates show interest in visualization skills',
          difficulty: 'low'
        }
      ],
      outreachSuggestions: [
        { 
          action: 'Target Computer Science juniors at NAU', 
          impact: 'high', 
          reasoning: '88% match quality with 15.2% growth in qualified candidates',
          difficulty: 'low'
        },
        { 
          action: 'Host virtual ML competition', 
          impact: 'medium', 
          reasoning: 'High engagement rates among ML-interested candidates',
          difficulty: 'medium'
        },
        { 
          action: 'Develop early connection with sophomore students', 
          impact: 'high', 
          reasoning: 'Data shows 45% higher conversion when relationships start early',
          difficulty: 'medium'
        }
      ]
    },
    predictions: {
      candidateVolume: {
        nextQuarter: 165,
        nextYear: 210,
        growthRate: 12.5
      },
      skillGaps: [
        { skill: 'Neural Networks', currentCoverage: 35, futureImportance: 70 },
        { skill: 'MLOps', currentCoverage: 25, futureImportance: 65 },
        { skill: 'Data Ethics', currentCoverage: 40, futureImportance: 75 }
      ],
      upcomingTrends: [
        { trend: 'Specialized AI certifications', confidence: 85 },
        { trend: 'Cloud-native development focus', confidence: 80 },
        { trend: 'Cross-disciplinary data science', confidence: 75 }
      ]
    }
  };
  
  // Helper functions
  const getImpactColor = (impact) => {
    switch (impact) {
      case 'high': return 'green';
      case 'medium': return 'blue';
      case 'low': return 'yellow';
      default: return 'gray';
    }
  };
  
  const getDifficultyColor = (difficulty) => {
    switch (difficulty) {
      case 'high': return 'red';
      case 'medium': return 'yellow';
      case 'low': return 'green';
      default: return 'gray';
    }
  };
  
  return (
    <Box bg={bgColor} borderRadius="lg" boxShadow="md" overflow="hidden">
      <Box bg="blue.600" p={4} color="white">
        <Flex justify="space-between" align="center">
          <HStack>
            <FaBrain size="20px" />
            <Heading size="md">AI Talent Intelligence Hub</Heading>
          </HStack>
          
          <HStack>
            <Menu>
              <MenuButton as={Button} rightIcon={<ChevronDownIcon />} size="sm" colorScheme="whiteAlpha">
                {timeRange === '30d' ? 'Last 30 Days' : 
                 timeRange === '90d' ? 'Last 90 Days' : 
                 timeRange === '1y' ? 'Last Year' : 'All Time'}
              </MenuButton>
              <MenuList>
                <MenuItem onClick={() => setTimeRange('30d')}>Last 30 Days</MenuItem>
                <MenuItem onClick={() => setTimeRange('90d')}>Last 90 Days</MenuItem>
                <MenuItem onClick={() => setTimeRange('1y')}>Last Year</MenuItem>
                <MenuItem onClick={() => setTimeRange('all')}>All Time</MenuItem>
              </MenuList>
            </Menu>
            
            <IconButton
              aria-label="Refresh insights"
              icon={<RepeatIcon />}
              size="sm"
              variant="ghost"
              colorScheme="whiteAlpha"
            />
            
            <IconButton
              aria-label="Settings"
              icon={<SettingsIcon />}
              size="sm"
              variant="ghost"
              colorScheme="whiteAlpha"
            />
          </HStack>
        </Flex>
      </Box>
      
      <Tabs colorScheme="blue" onChange={(index) => {
        const tabs = ['overview', 'trends', 'recommendations', 'predictions'];
        setActiveTab(tabs[index]);
      }}>
        <TabList px={4} pt={4}>
          <Tab>Overview</Tab>
          <Tab>Trends</Tab>
          <Tab>Recommendations</Tab>
          <Tab>Predictions</Tab>
        </TabList>
        
        <TabPanels>
          {/* Overview Tab */}
          <TabPanel px={6} py={4}>
            <SimpleGrid columns={{ base: 1, md: 4 }} spacing={6} mb={6}>
              <Stat bg="blue.50" p={4} borderRadius="lg">
                <Flex align="center" mb={2}>
                  <FaUsers color="#3182CE" style={{ marginRight: '8px' }} />
                  <StatLabel>Total Candidates</StatLabel>
                </Flex>
                <StatNumber>{insights.overview.candidateCount}</StatNumber>
                <StatHelpText mb={0}>
                  <StatArrow type="increase" />
                  14.5% from previous period
                </StatHelpText>
              </Stat>
              
              <Stat bg="green.50" p={4} borderRadius="lg">
                <Flex align="center" mb={2}>
                  <StarIcon color="green.500" mr={2} />
                  <StatLabel>High-Quality Matches</StatLabel>
                </Flex>
                <StatNumber>{insights.overview.highQualityCount}</StatNumber>
                <StatHelpText mb={0}>
                  <StatArrow type="increase" />
                  8.2% from previous period
                </StatHelpText>
              </Stat>
              
              <Stat bg="purple.50" p={4} borderRadius="lg">
                <Flex align="center" mb={2}>
                  <FaChartBar color="#805AD5" style={{ marginRight: '8px' }} />
                  <StatLabel>Avg Match Score</StatLabel>
                </Flex>
                <StatNumber>{insights.overview.averageMatchScore}%</StatNumber>
                <StatHelpText mb={0}>
                  <StatArrow type={insights.overview.matchScoreTrend > 0 ? "increase" : "decrease"} />
                  {Math.abs(insights.overview.matchScoreTrend)}% from previous period
                </StatHelpText>
              </Stat>
              
              <Stat bg="orange.50" p={4} borderRadius="lg">
                <Flex align="center" mb={2}>
                  <FaRegCalendarAlt color="#DD6B20" style={{ marginRight: '8px' }} />
                  <StatLabel>Response Rate</StatLabel>
                </Flex>
                <StatNumber>64.5%</StatNumber>
                <StatHelpText mb={0}>
                  <StatArrow type={insights.overview.responseRateTrend > 0 ? "increase" : "decrease"} />
                  {Math.abs(insights.overview.responseRateTrend)}% from previous period
                </StatHelpText>
              </Stat>
            </SimpleGrid>
            
            <SimpleGrid columns={{ base: 1, md: 2 }} spacing={6}>
              <Box>
                <Heading size="sm" mb={4}>Top Program Matches</Heading>
                <VStack align="stretch" spacing={3}>
                  {insights.overview.topPrograms.map((program, index) => (
                    <Flex 
                      key={index}
                      p={3}
                      borderWidth="1px"
                      borderRadius="md"
                      borderColor={borderColor}
                      justify="space-between"
                      align="center"
                    >
                      <VStack align="start" spacing={0}>
                        <Text fontWeight="medium">{program.name}</Text>
                        <Text fontSize="xs" color="gray.500">{program.candidateCount} candidates</Text>
                      </VStack>
                      
                      <HStack>
                        <Progress 
                          value={program.matchQuality} 
                          size="sm" 
                          width="120px" 
                          colorScheme={program.matchQuality >= 85 ? "green" : 
                                       program.matchQuality >= 75 ? "blue" : "yellow"}
                          borderRadius="full"
                        />
                        <Text fontWeight="bold" fontSize="sm">{program.matchQuality}%</Text>
                      </HStack>
                    </Flex>
                  ))}
                </VStack>
              </Box>
              
              <Box>
                <Heading size="sm" mb={4}>AI-Generated Insights</Heading>
                <Box
                  p={4}
                  borderWidth="1px"
                  borderRadius="md"
                  borderColor={borderColor}
                  bg="blue.50"
                >
                  <VStack align="stretch" spacing={4}>
                    <HStack align="start" spacing={3}>
                      <Box color="blue.500" mt={1}>
                        <FaBrain />
                      </Box>
                      <Box>
                        <Text fontWeight="medium" color="blue.700">Candidate Quality Trend</Text>
                        <Text fontSize="sm" color="blue.600">
                          The quality of matching candidates has increased by {insights.overview.matchScoreTrend}% over the past period, 
                          with particularly strong growth in AI and machine learning skills.
                        </Text>
                      </Box>
                    </HStack>
                    
                    <HStack align="start" spacing={3}>
                      <Box color="green.500" mt={1}>
                        <FaChartBar />
                      </Box>
                      <Box>
                        <Text fontWeight="medium" color="green.700">Engagement Opportunity</Text>
                        <Text fontSize="sm" color="green.600">
                          Response rates are up {insights.overview.responseRateTrend}%, suggesting improved engagement strategies. 
                          Continue focusing on personalized outreach for high-match candidates.
                        </Text>
                      </Box>
                    </HStack>
                    
                    <HStack align="start" spacing={3}>
                      <Box color="orange.500" mt={1}>
                        <FaCode />
                      </Box>
                      <Box>
                        <Text fontWeight="medium" color="orange.700">Skill Gap Alert</Text>
                        <Text fontSize="sm" color="orange.600">
                          There's a growing demand-supply gap in cloud computing skills (24.8% growth) 
                          that could be addressed through targeted program enhancements.
                        </Text>
                      </Box>
                    </HStack>
                  </VStack>
                  
                  <Button 
                    mt={4} 
                    size="sm" 
                    leftIcon={<FaBrain />}
                    colorScheme="blue"
                    width="full"
                  >
                    Generate More Insights
                  </Button>
                </Box>
              </Box>
            </SimpleGrid>
          </TabPanel>
          
          {/* Trends Tab */}
          <TabPanel px={6} py={4}>
            <SimpleGrid columns={{ base: 1, md: 2 }} spacing={6} mb={6}>
              <Box>
                <Heading size="sm" mb={4}>Candidate Growth Trends</Heading>
                <Box
                  p={4}
                  borderWidth="1px"
                  borderRadius="md"
                  borderColor={borderColor}
                  height="200px"
                  bg="gray.50"
                  display="flex"
                  alignItems="center"
                  justifyContent="center"
                >
                  <Text color="gray.500">Candidate Growth Chart Placeholder</Text>
                </Box>
                <Flex justify="space-between" mt={2}>
                  <Text fontSize="sm" color="gray.600">Overall growth:</Text>
                  <Badge colorScheme="green">{insights.trends.candidateGrowth}%</Badge>
                </Flex>
              </Box>
              
              <Box>
                <Heading size="sm" mb={4}>Engagement Metrics</Heading>
                <Box
                  p={4}
                  borderWidth="1px"
                  borderRadius="md"
                  borderColor={borderColor}
                  height="200px"
                  bg="gray.50"
                  display="flex"
                  alignItems="center"
                  justifyContent="center"
                >
                  <Text color="gray.500">Engagement Metrics Chart Placeholder</Text>
                </Box>
                <Flex justify="space-between" mt={2}>
                  <Text fontSize="sm" color="gray.600">Engagement growth:</Text>
                  <Badge colorScheme="blue">{insights.trends.engagementGrowth}%</Badge>
                </Flex>
              </Box>
            </SimpleGrid>
            
            <SimpleGrid columns={{ base: 1, md: 2 }} spacing={6} mb={6}>
              <Box>
                <Heading size="sm" mb={4}>Emerging Skill Trends</Heading>
                <VStack align="stretch" spacing={3}>
                  {insights.trends.skillTrends.map((skill, index) => (
                    <Box 
                      key={index}
                      p={3}
                      borderWidth="1px"
                      borderRadius="md"
                      borderColor={borderColor}
                    >
                      <Flex justify="space-between" mb={2}>
                        <HStack>
                          <FaLightbulb color="#3182CE" />
                          <Text fontWeight="medium" color="blue.700">{trend.trend}</Text>
                        </HStack>
                        <Badge colorScheme="blue">{trend.confidence}% Confidence</Badge>
                      </Flex>
                      
                      <Text fontSize="sm" color="blue.600">
                        Our AI models predict this trend will significantly impact 
                        candidate skills and interests in the next 12-24 months.
                      </Text>
                      
                      <HStack mt={3}>
                        <Button size="xs" colorScheme="blue">Plan for this</Button>
                        <Button size="xs" variant="ghost">Learn more</Button>
                      </HStack>
                    </Box>
                  ))}
                </VStack>
                
                <Box mt={4} p={4} borderWidth="1px" borderColor={borderColor} borderRadius="md">
                  <Heading size="xs" mb={2}>Long-Term Outlook</Heading>
                  <Text fontSize="sm" color="gray.600">
                    AI and data science skills will remain in high demand, with specialization becoming increasingly important. 
                    Cross-disciplinary programs that combine technical skills with domain expertise will see 
                    growing interest from both students and employers.
                  </Text>
                </Box>
              </Box>
            </SimpleGrid>
            
            <Box>
              <Heading size="sm" mb={4}>Recruitment Timeline Forecast</Heading>
              <Box
                p={4}
                borderWidth="1px"
                borderRadius="md"
                borderColor={borderColor}
                height="200px"
                bg="gray.50"
                display="flex"
                alignItems="center"
                justifyContent="center"
              >
                <Text color="gray.500">Timeline Forecast Chart Placeholder</Text>
              </Box>
              
              <SimpleGrid columns={3} spacing={4} mt={3}>
                <Box p={3} bg="green.50" borderRadius="md">
                  <Text fontWeight="medium" mb={1}>Peak Recruitment Periods</Text>
                  <Text fontSize="sm">October-November and February-March show highest quality candidate engagement.</Text>
                </Box>
                
                <Box p={3} bg="yellow.50" borderRadius="md">
                  <Text fontWeight="medium" mb={1}>Competition Intensity</Text>
                  <Text fontSize="sm">Highest in Spring for traditional programs, Fall for specialized tracks.</Text>
                </Box>
                
                <Box p={3} bg="blue.50" borderRadius="md">
                  <Text fontWeight="medium" mb={1}>Optimal Outreach Windows</Text>
                  <Text fontSize="sm">2-3 months before peak periods yields 25% higher conversion rates.</Text>
                </Box>
              </SimpleGrid>
            </Box>
          </TabPanel>
        </TabPanels>
      </Tabs>
      
      <Flex justify="space-between" p={4} borderTopWidth="1px" borderColor={borderColor} bg="gray.50">
        <Text fontSize="sm" color="gray.500">Data last updated: Today at 9:32 AM</Text>
        <HStack>
          <Button size="sm" leftIcon={<DownloadIcon />} colorScheme="blue" variant="outline">
            Export Insights
          </Button>
          <Button size="sm" leftIcon={<FaBrain />} colorScheme="purple">
            Get Custom Analysis
          </Button>
        </HStack>
      </Flex>
    </Box>
  );
}-between" mb={2}>
                        <Text fontWeight="medium">{skill.name}</Text>
                        <Badge colorScheme="green">+{skill.growth}%</Badge>
                      </Flex>
                      
                      <Text fontSize="xs" color="gray.500" mb={1}>Current prevalence in candidate profiles:</Text>
                      <Progress 
                        value={skill.prevalence} 
                        size="sm" 
                        colorScheme="blue" 
                        borderRadius="full" 
                      />
                      <Text fontSize="xs" textAlign="right" mt={1}>{skill.prevalence}%</Text>
                    </Box>
                  ))}
                </VStack>
              </Box>
              
              <Box>
                <Heading size="sm" mb={4}>Institution Performance</Heading>
                <VStack align="stretch" spacing={3}>
                  {insights.trends.institutionTrends.map((institution, index) => (
                    <Box 
                      key={index}
                      p={3}
                      borderWidth="1px"
                      borderRadius="md"
                      borderColor={borderColor}
                    >
                      <Flex justify="space-between" mb={2}>
                        <HStack>
                          <FaUniversity />
                          <Text fontWeight="medium">{institution.name}</Text>
                        </HStack>
                        <Badge colorScheme="green">+{institution.growth}%</Badge>
                      </Flex>
                      
                      <Text fontSize="xs" color="gray.500" mb={1}>Average match quality:</Text>
                      <Progress 
                        value={institution.matchQuality} 
                        size="sm" 
                        colorScheme="purple" 
                        borderRadius="full" 
                      />
                      <Text fontSize="xs" textAlign="right" mt={1}>{institution.matchQuality}%</Text>
                    </Box>
                  ))}
                </VStack>
              </Box>
            </SimpleGrid>
            
            <Box>
              <Heading size="sm" mb={4}>Seasonal Patterns</Heading>
              <Box
                p={4}
                borderWidth="1px"
                borderRadius="md"
                borderColor={borderColor}
                height="200px"
                bg="gray.50"
                display="flex"
                alignItems="center"
                justifyContent="center"
              >
                <Text color="gray.500">Seasonal Patterns Chart Placeholder</Text>
              </Box>
              <SimpleGrid columns={4} spacing={4} mt={2}>
                <Box textAlign="center">
                  <Text fontWeight="bold">Winter</Text>
                  <Text fontSize="sm" color="gray.600">+5% activity</Text>
                </Box>
                <Box textAlign="center">
                  <Text fontWeight="bold">Spring</Text>
                  <Text fontSize="sm" color="gray.600">+15% activity</Text>
                </Box>
                <Box textAlign="center">
                  <Text fontWeight="bold">Summer</Text>
                  <Text fontSize="sm" color="gray.600">-10% activity</Text>
                </Box>
                <Box textAlign="center">
                  <Text fontWeight="bold">Fall</Text>
                  <Text fontSize="sm" color="gray.600">+22% activity</Text>
                </Box>
              </SimpleGrid>
            </Box>
          </TabPanel>
          
          {/* Recommendations Tab */}
          <TabPanel px={6} py={4}>
            <SimpleGrid columns={{ base: 1, md: 2 }} spacing={6}>
              <Box>
                <Heading size="sm" mb={4}>Program Enhancement Recommendations</Heading>
                <VStack align="stretch" spacing={4}>
                  {insights.recommendations.programSuggestions.map((suggestion, index) => (
                    <Box 
                      key={index}
                      p={4}
                      borderWidth="1px"
                      borderRadius="md"
                      borderColor={borderColor}
                      bg="white"
                    >
                      <Flex mb={2}>
                        <Badge 
                          colorScheme={getImpactColor(suggestion.impact)} 
                          mr={2}
                        >
                          {suggestion.impact.toUpperCase()} IMPACT
                        </Badge>
                        <Badge 
                          colorScheme={getDifficultyColor(suggestion.difficulty)}
                        >
                          {suggestion.difficulty.toUpperCase()} EFFORT
                        </Badge>
                      </Flex>
                      
                      <Text fontWeight="medium" fontSize="md" mb={2}>
                        {suggestion.action}
                      </Text>
                      
                      <Text fontSize="sm" color="gray.600">
                        {suggestion.reasoning}
                      </Text>
                      
                      <HStack mt={3}>
                        <Button size="xs" colorScheme="blue">Implement</Button>
                        <Button size="xs" variant="ghost">Dismiss</Button>
                      </HStack>
                    </Box>
                  ))}
                </VStack>
              </Box>
              
              <Box>
                <Heading size="sm" mb={4}>Outreach Strategy Recommendations</Heading>
                <VStack align="stretch" spacing={4}>
                  {insights.recommendations.outreachSuggestions.map((suggestion, index) => (
                    <Box 
                      key={index}
                      p={4}
                      borderWidth="1px"
                      borderRadius="md"
                      borderColor={borderColor}
                      bg="white"
                    >
                      <Flex mb={2}>
                        <Badge 
                          colorScheme={getImpactColor(suggestion.impact)} 
                          mr={2}
                        >
                          {suggestion.impact.toUpperCase()} IMPACT
                        </Badge>
                        <Badge 
                          colorScheme={getDifficultyColor(suggestion.difficulty)}
                        >
                          {suggestion.difficulty.toUpperCase()} EFFORT
                        </Badge>
                      </Flex>
                      
                      <Text fontWeight="medium" fontSize="md" mb={2}>
                        {suggestion.action}
                      </Text>
                      
                      <Text fontSize="sm" color="gray.600">
                        {suggestion.reasoning}
                      </Text>
                      
                      <HStack mt={3}>
                        <Button size="xs" colorScheme="blue">Implement</Button>
                        <Button size="xs" variant="ghost">Dismiss</Button>
                      </HStack>
                    </Box>
                  ))}
                </VStack>
              </Box>
            </SimpleGrid>
            
            <Box mt={6} p={4} bg="blue.50" borderRadius="md">
              <Flex align="center" mb={3}>
                <FaBrain color="#3182CE" style={{ marginRight: '8px' }} />
                <Heading size="sm" color="blue.700">AI-Generated Action Plan</Heading>
              </Flex>
              
              <Text fontSize="sm" color="blue.700" mb={4}>
                Based on candidate trends and program objectives, here's a recommended 90-day action plan to maximize recruitment outcomes:
              </Text>
              
              <SimpleGrid columns={{ base: 1, md: 3 }} spacing={4}>
                <Box bg="white" p={3} borderRadius="md" boxShadow="sm">
                  <Text fontWeight="bold" mb={2} color="blue.700">Days 1-30:</Text>
                  <VStack align="start" spacing={2}>
                    <Text fontSize="sm">• Create specialized AI track</Text>
                    <Text fontSize="sm">• Target CS juniors at NAU</Text>
                    <Text fontSize="sm">• Develop early sophomore connections</Text>
                  </VStack>
                </Box>
                
                <Box bg="white" p={3} borderRadius="md" boxShadow="sm">
                  <Text fontWeight="bold" mb={2} color="blue.700">Days 31-60:</Text>
                  <VStack align="start" spacing={2}>
                    <Text fontSize="sm">• Launch data visualization workshop</Text>
                    <Text fontSize="sm">• Plan virtual ML competition</Text>
                    <Text fontSize="sm">• Begin cloud computing partnerships</Text>
                  </VStack>
                </Box>
                
                <Box bg="white" p={3} borderRadius="md" boxShadow="sm">
                  <Text fontWeight="bold" mb={2} color="blue.700">Days 61-90:</Text>
                  <VStack align="start" spacing={2}>
                    <Text fontSize="sm">• Host ML competition</Text>
                    <Text fontSize="sm">• Measure initiative outcomes</Text>
                    <Text fontSize="sm">• Refine strategies based on data</Text>
                  </VStack>
                </Box>
              </SimpleGrid>
              
              <Button 
                mt={4} 
                size="sm" 
                colorScheme="blue" 
                width="full"
                leftIcon={<DownloadIcon />}
              >
                Export Action Plan
              </Button>
            </Box>
          </TabPanel>
          
          {/* Predictions Tab */}
          <TabPanel px={6} py={4}>
            <SimpleGrid columns={{ base: 1, md: 3 }} spacing={6} mb={6}>
              <Stat bg="blue.50" p={4} borderRadius="lg">
                <StatLabel>Predicted Candidates</StatLabel>
                <Flex align="center">
                  <StatNumber>{insights.predictions.candidateVolume.nextQuarter}</StatNumber>
                  <Text fontSize="sm" color="gray.500" ml={2}>Next Quarter</Text>
                </Flex>
                <StatHelpText mb={0}>
                  <StatArrow type="increase" />
                  {insights.predictions.candidateVolume.growthRate}% growth
                </StatHelpText>
              </Stat>
              
              <Stat bg="purple.50" p={4} borderRadius="lg">
                <StatLabel>12-Month Forecast</StatLabel>
                <Flex align="center">
                  <StatNumber>{insights.predictions.candidateVolume.nextYear}</StatNumber>
                  <Text fontSize="sm" color="gray.500" ml={2}>Candidates</Text>
                </Flex>
                <StatHelpText mb={0}>
                  <StatArrow type="increase" />
                  {Math.round(insights.predictions.candidateVolume.growthRate * 1.2)}% annual growth
                </StatHelpText>
              </Stat>
              
              <Stat bg="green.50" p={4} borderRadius="lg">
                <StatLabel>Confidence Level</StatLabel>
                <StatNumber>85%</StatNumber>
                <StatHelpText mb={0}>
                  Based on historical accuracy
                </StatHelpText>
              </Stat>
            </SimpleGrid>
            
            <SimpleGrid columns={{ base: 1, md: 2 }} spacing={6} mb={6}>
              <Box>
                <Heading size="sm" mb={4}>Future Skill Gap Analysis</Heading>
                <VStack align="stretch" spacing={4}>
                  {insights.predictions.skillGaps.map((gap, index) => (
                    <Box 
                      key={index}
                      p={4}
                      borderWidth="1px"
                      borderRadius="md"
                      borderColor={borderColor}
                    >
                      <Flex justify="space-between" mb={2}>
                        <Text fontWeight="medium">{gap.skill}</Text>
                        <Badge colorScheme="red">
                          {gap.futureImportance - gap.currentCoverage}% Gap
                        </Badge>
                      </Flex>
                      
                      <SimpleGrid columns={2} spacing={4}>
                        <Box>
                          <Text fontSize="xs" color="gray.500">Current Coverage:</Text>
                          <Progress 
                            value={gap.currentCoverage} 
                            size="sm" 
                            colorScheme="blue" 
                            borderRadius="full"
                            mb={1}
                          />
                          <Text fontSize="xs" textAlign="right">{gap.currentCoverage}%</Text>
                        </Box>
                        
                        <Box>
                          <Text fontSize="xs" color="gray.500">Future Importance:</Text>
                          <Progress 
                            value={gap.futureImportance} 
                            size="sm" 
                            colorScheme="purple" 
                            borderRadius="full"
                            mb={1}
                          />
                          <Text fontSize="xs" textAlign="right">{gap.futureImportance}%</Text>
                        </Box>
                      </SimpleGrid>
                      
                      <Text fontSize="sm" mt={3} color="gray.600">
                        {gap.skill} is predicted to become {gap.futureImportance > 70 ? 'critical' : 'important'} 
                        in candidate profiles, but current program coverage is 
                        {gap.currentCoverage < 30 ? ' minimal' : ' moderate'}.
                      </Text>
                    </Box>
                  ))}
                </VStack>
              </Box>
              
              <Box>
                <Heading size="sm" mb={4}>Emerging Trends</Heading>
                <VStack align="stretch" spacing={4}>
                  {insights.predictions.upcomingTrends.map((trend, index) => (
                    <Box 
                      key={index}
                      p={4}
                      borderWidth="1px"
                      borderRadius="md"
                      borderColor={borderColor}
                      bg="blue.50"
                    >
                      <Flex justify="space