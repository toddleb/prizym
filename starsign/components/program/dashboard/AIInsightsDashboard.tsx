// components/program/dashboard/AIInsightsDashboard.tsx
import { useState, useEffect } from 'react';
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

// Import utilities and types
import {
  InsightData,
  getImpactColor,
  getDifficultyColor,
  getMatchQualityColorScheme,
  getSampleInsightsData,
  getTimeRangeLabel,
  formatDate,
  formatTime
} from '../AIInsightsDashboardUtils';

export default function AIInsightsDashboard() {
  const [activeTab, setActiveTab] = useState('overview');
  const [timeRange, setTimeRange] = useState('90d');
  const [insights, setInsights] = useState<InsightData>(getSampleInsightsData());
  const [lastUpdated, setLastUpdated] = useState(new Date());
  
  const bgColor = useColorModeValue('white', 'gray.700');
  const borderColor = useColorModeValue('gray.200', 'gray.600');
  
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
                {getTimeRangeLabel(timeRange)}
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
                          colorScheme={getMatchQualityColorScheme(program.matchQuality)}
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
          
          {/* Other tabs content would be here */}
          {/* For brevity, I've removed the other tab contents, but you would include them in the full implementation */}
          <TabPanel px={6} py={4}>
            <Heading size="md">Trends</Heading>
            <Text>Trends content would go here</Text>
          </TabPanel>
          
          <TabPanel px={6} py={4}>
            <Heading size="md">Recommendations</Heading>
            <Text>Recommendations content would go here</Text>
          </TabPanel>
          
          <TabPanel px={6} py={4}>
            <Heading size="md">Predictions</Heading>
            <Text>Predictions content would go here</Text>
          </TabPanel>
        </TabPanels>
      </Tabs>
      
      <Flex justify="space-between" p={4} borderTopWidth="1px" borderColor={borderColor} bg="gray.50">
        <Text fontSize="sm" color="gray.500">Data last updated: {formatDate(lastUpdated)} at {formatTime(lastUpdated)}</Text>
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
}