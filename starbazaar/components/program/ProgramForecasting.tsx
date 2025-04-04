// components/program/ProgramForecasting.tsx
import { 
  Box, 
  Flex, 
  Heading, 
  Text,
  SimpleGrid,
  HStack,
  VStack,
  Badge,
  Button,
  IconButton,
  Stat,
  StatLabel,
  StatNumber,
  StatHelpText,
  StatArrow,
  Progress,
  Table,
  Thead,
  Tbody,
  Tr,
  Th,
  Td,
  useColorModeValue,
  Image,
  Avatar
} from '@chakra-ui/react';
import { 
  ChevronDownIcon, 
  StarIcon, 
  InfoIcon, 
  ExternalLinkIcon, 
  RepeatIcon,
  ArrowUpIcon,
  ArrowDownIcon
} from '@chakra-ui/icons';
import { 
  FaChartLine, 
  FaUniversity, 
  FaCalendarAlt, 
  FaDollarSign,
  FaGraduationCap,
  FaLightbulb,
  FaUserGraduate,
  FaStar
} from 'react-icons/fa';

export default function ProgramForecasting() {
  const borderColor = useColorModeValue('gray.200', 'gray.700');
  
  // Sample ROI data - in a real app, this would come from your API
  const roiMetrics = [
    { 
      id: 'conversion', 
      name: 'Conversion Rate', 
      value: 17.4, 
      change: 2.8, 
      note: 'Identified → Offer Accepted',
      isGood: true 
    },
    { 
      id: 'cost', 
      name: 'Cost per Hire', 
      value: 2450, 
      unit: '$',
      change: -8.5, 
      note: '12-month average',
      isGood: true 
    },
    { 
      id: 'time', 
      name: 'Time to Hire', 
      value: 38, 
      unit: 'days',
      change: -5.2, 
      note: 'From first contact',
      isGood: true 
    },
    { 
      id: 'retention', 
      name: 'Retention Rate', 
      value: 82.6, 
      change: -1.4, 
      note: 'After 12 months',
      isGood: false 
    }
  ];
  
  // Program performance data
  const programPerformance = [
    { 
      id: 'p1',
      name: 'Data Science & AI', 
      university: 'Nova State University',
      totalCandidates: 84,
      highMatchCandidates: 12,
      conversionRate: 18.5,
      costPerHire: 2250,
      trend: 'up',
      growthRate: 14.2
    },
    { 
      id: 'p2',
      name: 'Computer Science', 
      university: 'Stellar Tech Institute',
      totalCandidates: 62,
      highMatchCandidates: 8,
      conversionRate: 15.7,
      costPerHire: 2680,
      trend: 'stable',
      growthRate: 3.1
    },
    { 
      id: 'p3',
      name: 'AI & Machine Learning', 
      university: 'Quantum College',
      totalCandidates: 38,
      highMatchCandidates: 6,
      conversionRate: 21.3,
      costPerHire: 2100,
      trend: 'up',
      growthRate: 18.7
    }
  ];
  
  // Talent hotspots forecast
  const talentHotspots = [
    {
      skill: 'Deep Learning',
      current: 85,
      forecast: 95,
      growth: 11.8,
      programs: ['AI & Machine Learning @ Quantum', 'Data Science @ Nova State'],
      recommendation: 'Increase early engagement with AI/ML courses'
    },
    {
      skill: 'Cloud Computing',
      current: 62,
      forecast: 82,
      growth: 32.3,
      programs: ['Software Engineering @ Nova State', 'Computer Science @ Stellar'],
      recommendation: 'Create specialized cloud tech career track'
    },
    {
      skill: 'Data Engineering',
      current: 58,
      forecast: 75,
      growth: 29.3,
      programs: ['Data Science & AI @ Nova State', 'Information Systems @ Stellar'],
      recommendation: 'Partner with database/data processing companies'
    }
  ];
  
  // Rising star candidates
  const risingStars = [
    {
      id: 'rs1',
      blindId: 'Candidate #212',
      isRevealed: false,
      name: null,
      program: 'AI & Machine Learning',
      university: 'Quantum College',
      graduation: 'June 2025',
      whyRising: 'Open-source AI contributions, research with Prof. Johnson',
      matchScore: 94
    },
    {
      id: 'rs2',
      blindId: 'Candidate #178',
      isRevealed: false,
      name: null,
      program: 'Data Science & AI',
      university: 'Nova State',
      graduation: 'Dec 2025',
      whyRising: 'ML competition winner, advanced statistics focus',
      matchScore: 91
    },
    {
      id: 'rs3',
      blindId: 'Candidate #256',
      isRevealed: false,
      name: null,
      program: 'Computer Science',
      university: 'Stellar Tech',
      graduation: 'May 2026',
      whyRising: 'Impressive GitHub contributions, AI club leader',
      matchScore: 89
    }
  ];
  
  // Function to render trend indicator
  const renderTrend = (trend, growthRate) => {
    if (trend === 'up') {
      return (
        <HStack spacing={1} color="green.500">
          <ArrowUpIcon boxSize={3} />
          <Text fontSize="xs" fontWeight="medium">{growthRate}%</Text>
        </HStack>
      );
    } else if (trend === 'down') {
      return (
        <HStack spacing={1} color="red.500">
          <ArrowDownIcon boxSize={3} />
          <Text fontSize="xs" fontWeight="medium">{growthRate}%</Text>
        </HStack>
      );
    } else {
      return (
        <Text fontSize="xs" color="gray.500">Stable</Text>
      );
    }
  };
  
  return (
    <Box>
      <SimpleGrid columns={{ base: 1, lg: 2 }} spacing={6}>
        {/* Left column */}
        <Box>
          {/* ROI metrics */}
          <Box p={5} bg="white" borderRadius="lg" boxShadow="sm" mb={6}>
            <Flex justify="space-between" align="center" mb={4}>
              <Heading size="md">
                <FaChartLine style={{ display: 'inline', marginRight: '8px' }} />
                Recruiting ROI Metrics
              </Heading>
              <Button size="xs" leftIcon={<RepeatIcon />} colorScheme="purple" variant="outline">
                Refresh
              </Button>
            </Flex>
            
            <SimpleGrid columns={2} spacing={6}>
              {roiMetrics.map(metric => (
                <Stat key={metric.id} bg="gray.50" p={3} borderRadius="md">
                  <StatLabel fontSize="sm">{metric.name}</StatLabel>
                  <StatNumber fontSize="2xl">
                    {metric.unit && metric.unit}{metric.value}
                    {!metric.unit && metric.name.includes('Rate') && '%'}
                    {metric.unit === 'days' && ' ' + metric.unit}
                  </StatNumber>
                  <Flex justify="space-between" align="center">
                    <StatHelpText mb={0}>
                      <StatArrow 
                        type={metric.isGood ? 
                          (metric.change >= 0 ? 'increase' : 'decrease') : 
                          (metric.change >= 0 ? 'decrease' : 'increase')} 
                      />
                      {Math.abs(metric.change)}%
                    </StatHelpText>
                    <Text fontSize="xs" color="gray.500">{metric.note}</Text>
                  </Flex>
                </Stat>
              ))}
            </SimpleGrid>
          </Box>
          
          {/* Program performance */}
          <Box p={5} bg="white" borderRadius="lg" boxShadow="sm">
            <Flex justify="space-between" align="center" mb={4}>
              <Heading size="md">
                <FaUniversity style={{ display: 'inline', marginRight: '8px' }} />
                Program Performance
              </Heading>
              <HStack>
                <Badge colorScheme="purple">Last 90 Days</Badge>
                <Button size="xs" variant="ghost">View All</Button>
              </HStack>
            </Flex>
            
            <Box overflowX="auto">
              <Table size="sm" variant="simple">
                <Thead>
                  <Tr>
                    <Th>Program</Th>
                    <Th isNumeric>Candidates</Th>
                    <Th isNumeric>Conversion</Th>
                    <Th isNumeric>Cost/Hire</Th>
                    <Th isNumeric>Growth</Th>
                  </Tr>
                </Thead>
                <Tbody>
                  {programPerformance.map(program => (
                    <Tr key={program.id}>
                      <Td>
                        <VStack align="start" spacing={0}>
                          <Text fontWeight="medium">{program.name}</Text>
                          <Text fontSize="xs" color="gray.500">{program.university}</Text>
                        </VStack>
                      </Td>
                      <Td isNumeric>
                        <Text fontWeight="medium">{program.totalCandidates}</Text>
                        <Text fontSize="xs" color="gray.500">{program.highMatchCandidates} high-match</Text>
                      </Td>
                      <Td isNumeric>
                        <Text>{program.conversionRate}%</Text>
                      </Td>
                      <Td isNumeric>
                        <Text>${program.costPerHire}</Text>
                      </Td>
                      <Td>
                        {renderTrend(program.trend, program.growthRate)}
                      </Td>
                    </Tr>
                  ))}
                </Tbody>
              </Table>
            </Box>
          </Box>
        </Box>
        
        {/* Right column */}
        <Box>
          {/* Talent Hotspots Forecast */}
          <Box p={5} bg="white" borderRadius="lg" boxShadow="sm" mb={6}>
            <Flex justify="space-between" align="center" mb={4}>
              <Heading size="md">
                <FaLightbulb style={{ display: 'inline', marginRight: '8px' }} />
                Talent Hotspots Forecast
              </Heading>
              <Badge colorScheme="green">12-Month Prediction</Badge>
            </Flex>
            
            <VStack spacing={4} align="stretch">
              {talentHotspots.map((hotspot, index) => (
                <Box 
                  key={index} 
                  borderWidth="1px" 
                  borderRadius="md" 
                  borderColor={borderColor}
                  p={3}
                >
                  <Flex justify="space-between" align="center" mb={2}>
                    <Text fontWeight="bold">{hotspot.skill}</Text>
                    <HStack>
                      <ArrowUpIcon color="green.500" />
                      <Text color="green.500" fontWeight="medium">{hotspot.growth}%</Text>
                    </HStack>
                  </Flex>
                  
                  <Flex align="center" mb={2}>
                    <Text fontSize="sm" color="gray.500" width="60px">Current:</Text>
                    <Box flex="1">
                      <Progress 
                        value={hotspot.current} 
                        size="sm" 
                        colorScheme="blue" 
                        borderRadius="full" 
                      />
                    </Box>
                    <Text fontSize="sm" fontWeight="medium" ml={2}>{hotspot.current}%</Text>
                  </Flex>
                  
                  <Flex align="center" mb={3}>
                    <Text fontSize="sm" color="gray.500" width="60px">Forecast:</Text>
                    <Box flex="1">
                      <Progress 
                        value={hotspot.forecast} 
                        size="sm" 
                        colorScheme="green" 
                        borderRadius="full" 
                      />
                    </Box>
                    <Text fontSize="sm" fontWeight="medium" ml={2}>{hotspot.forecast}%</Text>
                  </Flex>
                  
                  <Text fontSize="xs" color="gray.600" mb={2}>Key Programs:</Text>
                  <Flex flexWrap="wrap" gap={1} mb={2}>
                    {hotspot.programs.map((program, i) => (
                      <Badge key={i} colorScheme="purple" variant="subtle" fontSize="xs">
                        {program}
                      </Badge>
                    ))}
                  </Flex>
                  
                  <Flex align="center" mt={2} bg="purple.50" p={2} borderRadius="md">
                    <InfoIcon color="purple.500" mr={2} />
                    <Text fontSize="xs" color="purple.700">{hotspot.recommendation}</Text>
                  </Flex>
                </Box>
              ))}
            </VStack>
          </Box>
          
          {/* Rising Stars */}
          <Box p={5} bg="white" borderRadius="lg" boxShadow="sm">
            <Flex justify="space-between" align="center" mb={4}>
              <Heading size="md">
                <FaStar style={{ display: 'inline', marginRight: '8px', color: '#F6AD55' }} />
                Rising Stars (Next 6-12 Months)
              </Heading>
              <Button size="xs" variant="ghost">
                View All
              </Button>
            </Flex>
            
            <VStack spacing={3} align="stretch">
              {risingStars.map((star) => (
                <Box 
                  key={star.id}
                  borderWidth="1px"
                  borderRadius="md"
                  borderColor={borderColor}
                  p={4}
                  _hover={{ borderColor: 'yellow.400', boxShadow: 'sm' }}
                  transition="all 0.2s"
                >
                  <Flex justify="space-between" align="center" mb={3}>
                    <HStack>
                      <Box 
                        bg="yellow.100" 
                        p={2} 
                        borderRadius="full" 
                        display="flex" 
                        alignItems="center" 
                        justifyContent="center"
                      >
                        <FaUserGraduate color="#D69E2E" />
                      </Box>
                      <Text>{star.blindId}</Text>
                      <Badge colorScheme="yellow" variant="subtle">
                        Blind Mode
                      </Badge>
                    </HStack>
                    <Badge colorScheme="purple" fontSize="sm">{star.matchScore}% Match</Badge>
                  </Flex>
                  
                  <HStack spacing={4} mb={3}>
                    <VStack align="start" spacing={0}>
                      <Text fontSize="sm" color="gray.500">Program</Text>
                      <Text fontSize="sm" fontWeight="medium">{star.program}</Text>
                    </VStack>
                    
                    <VStack align="start" spacing={0}>
                      <Text fontSize="sm" color="gray.500">University</Text>
                      <Text fontSize="sm" fontWeight="medium">{star.university}</Text>
                    </VStack>
                    
                    <VStack align="start" spacing={0}>
                      <Text fontSize="sm" color="gray.500">Graduation</Text>
                      <Text fontSize="sm" fontWeight="medium">{star.graduation}</Text>
                    </VStack>
                  </HStack>
                  
                  <Box bg="yellow.50" p={3} borderRadius="md">
                    <Text fontSize="sm" fontWeight="medium" color="yellow.800" mb={1}>
                      Why they're on our radar:
                    </Text>
                    <Text fontSize="sm" color="gray.700">
                      {star.whyRising}
                    </Text>
                  </Box>
                  
                  <Flex mt={3} justify="space-between">
                    <Button size="xs" colorScheme="yellow" variant="outline">
                      Reveal Identity
                    </Button>
                    <Button size="xs" colorScheme="purple">
                      Track Candidate
                    </Button>
                  </Flex>
                </Box>
              ))}
            </VStack>
          </Box>
        </Box>
      </SimpleGrid>
    </Box>
  );
}