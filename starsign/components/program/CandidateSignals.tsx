// components/program/CandidateSignals.tsx
import { 
  Box, 
  Flex, 
  Heading, 
  Text,
  Badge,
  Button,
  HStack,
  VStack,
  Tag,
  IconButton,
  Menu,
  MenuButton,
  MenuList,
  MenuItem,
  Avatar,
  Divider,
  useColorModeValue,
  Progress,
  Tabs,
  TabList,
  Tab,
  TabPanels,
  TabPanel
} from '@chakra-ui/react';
import { 
  ChevronDownIcon, 
  StarIcon,
  EmailIcon,
  ExternalLinkIcon,
  ViewIcon,
  TimeIcon,
  LockIcon,
  CheckIcon
} from '@chakra-ui/icons';
import { 
  FaGithub, 
  FaLinkedin, 
  FaCalendarAlt, 
  FaUserGraduate,
  FaCode,
  FaLightbulb,
  FaTrophy,
  FaRocket,
  FaFilter
} from 'react-icons/fa';

interface CandidateSignalsProps {
  columns?: number;
  gridColumn?: any;
}

export default function CandidateSignals({ 
  columns = 1, 
  gridColumn 
}: CandidateSignalsProps) {
  const borderColor = useColorModeValue('gray.200', 'gray.700');
  
  // Sample signal data - in a real app, this would come from your API
  const signals = [
    {
      id: 's1',
      type: 'github',
      candidateId: 'c145',
      candidateName: null,
      blindId: 'Candidate #145',
      isRevealed: false,
      matchScore: 95,
      time: '28 minutes ago',
      action: 'Committed to open-source ML project',
      details: 'Added PyTorch implementation of a new algorithm',
      signalStrength: 4,
      program: 'Data Science & AI',
      university: 'Nova State University'
    },
    {
      id: 's2',
      type: 'event',
      candidateId: 'c092',
      candidateName: 'Taylor Kim',
      blindId: 'Candidate #092',
      isRevealed: true,
      matchScore: 92,
      time: '2 hours ago',
      action: 'RSVP\'d to AI Careers Info Session',
      details: 'Attending virtual session on March 15',
      signalStrength: 3,
      program: 'Computer Science',
      university: 'Stellar Tech Institute'
    },
    {
      id: 's3',
      type: 'linkedin',
      candidateId: 'c217',
      candidateName: null,
      blindId: 'Candidate #217',
      isRevealed: false,
      matchScore: 87,
      time: '4 hours ago',
      action: 'Updated skills profile',
      details: 'Added Data Science, Python, and ML certifications',
      signalStrength: 4,
      program: 'AI & Machine Learning',
      university: 'Quantum College'
    },
    {
      id: 's4',
      type: 'club',
      candidateId: 'c078',
      candidateName: 'Jordan Lee',
      blindId: 'Candidate #078',
      isRevealed: true,
      matchScore: 85,
      time: 'Yesterday',
      action: 'Joined AI Research Club',
      details: 'Working on computer vision project',
      signalStrength: 3,
      program: 'Computer Science',
      university: 'Stellar Tech Institute'
    },
    {
      id: 's5',
      type: 'capstone',
      candidateId: 'c122',
      candidateName: null,
      blindId: 'Candidate #122',
      isRevealed: false,
      matchScore: 81,
      time: '2 days ago',
      action: 'Started capstone project',
      details: 'Building a predictive analytics platform',
      signalStrength: 5,
      program: 'Data Science & AI',
      university: 'Nova State University'
    }
  ];

  // Function to get icon based on signal type
  const getSignalIcon = (type: string) => {
    switch (type) {
      case 'github':
        return <FaGithub />;
      case 'linkedin':
        return <FaLinkedin />;
      case 'event':
        return <FaCalendarAlt />;
      case 'club':
        return <FaUserGraduate />;
      case 'capstone':
        return <FaRocket />;
      default:
        return <FaLightbulb />;
    }
  };
  
  // Function to get color based on signal type
  const getSignalColor = (type: string) => {
    switch (type) {
      case 'github':
        return 'gray';
      case 'linkedin':
        return 'blue';
      case 'event':
        return 'green';
      case 'club':
        return 'purple';
      case 'capstone':
        return 'orange';
      default:
        return 'teal';
    }
  };
  
  // Function to render signal strength
  const renderSignalStrength = (strength: number) => {
    const color = 
      strength >= 5 ? 'purple.500' :
      strength === 4 ? 'green.500' :
      strength === 3 ? 'blue.500' :
      strength === 2 ? 'yellow.500' : 'gray.500';
      
    const label = 
      strength >= 5 ? 'Very Strong' :
      strength === 4 ? 'Strong' :
      strength === 3 ? 'Moderate' :
      strength === 2 ? 'Light' : 'Weak';
      
    return (
      <Flex align="center">
        <Progress 
          value={strength * 20} 
          size="xs" 
          colorScheme={color.split('.')[0]} 
          width="60px" 
          mr={2}
        />
        <Text fontSize="xs" color="gray.600">{label}</Text>
      </Flex>
    );
  };
  
  return (
    <Box 
      p={5} 
      bg="white" 
      borderRadius="lg" 
      boxShadow="sm"
      gridColumn={gridColumn}
    >
      <Flex justify="space-between" align="center" mb={4}>
        <Heading size="md">Candidate Signal Feed</Heading>
        
        <HStack>
          <Button 
            size="sm" 
            leftIcon={<FaLinkedin />} 
            colorScheme="linkedin" 
            variant="outline"
          >
            Connect
          </Button>
          <Button 
            size="sm" 
            leftIcon={<FaGithub />} 
            colorScheme="gray" 
            variant="outline"
          >
            Connect
          </Button>
          <IconButton
            aria-label="Filter signals"
            icon={<FaFilter />}
            size="sm"
            variant="ghost"
          />
        </HStack>
      </Flex>
      
      <Tabs variant="soft-rounded" colorScheme="purple" size="sm" mb={4}>
        <TabList>
          <Tab>All Signals</Tab>
          <Tab>High Intent</Tab>
          <Tab>GitHub</Tab>
          <Tab>LinkedIn</Tab>
          <Tab>Events</Tab>
        </TabList>
      </Tabs>
      
      <VStack spacing={4} align="stretch">
        {signals.map(signal => (
          <Box 
            key={signal.id}
            borderWidth="1px"
            borderRadius="md"
            borderColor={borderColor}
            p={4}
            _hover={{ borderColor: 'purple.300', boxShadow: 'sm' }}
            transition="all 0.2s"
          >
            <Flex justify="space-between" mb={3}>
              {/* Left: Signal type and time */}
              <HStack>
                <Box 
                  p={2} 
                  borderRadius="md" 
                  bg={`${getSignalColor(signal.type)}.100`}
                  color={`${getSignalColor(signal.type)}.700`}
                >
                  {getSignalIcon(signal.type)}
                </Box>
                <Box>
                  <Text fontWeight="bold" fontSize="sm">
                    {signal.action}
                  </Text>
                  <Flex align="center" mt={1}>
                    <TimeIcon boxSize={3} color="gray.500" mr={1} />
                    <Text fontSize="xs" color="gray.500">{signal.time}</Text>
                  </Flex>
                </Box>
              </HStack>
              
              {/* Right: Match score */}
              <VStack spacing={1} align="flex-end">
                <Badge colorScheme="purple" variant="solid">
                  {signal.matchScore}% Match
                </Badge>
                {renderSignalStrength(signal.signalStrength)}
              </VStack>
            </Flex>
            
            {/* Candidate info */}
            <Flex align="center" mb={3}>
              {signal.isRevealed ? (
                <HStack>
                  <Avatar size="sm" name={signal.candidateName} />
                  <Text fontWeight="medium">{signal.candidateName}</Text>
                </HStack>
              ) : (
                <HStack>
                  <Box 
                    bg="purple.100" 
                    p={2} 
                    borderRadius="full" 
                    display="flex" 
                    alignItems="center" 
                    justifyContent="center"
                  >
                    <LockIcon color="purple.500" boxSize={3} />
                  </Box>
                  <Text>{signal.blindId}</Text>
                  <Badge colorScheme="gray" variant="outline" size="sm">
                    Blind Mode
                  </Badge>
                </HStack>
              )}
              <Box ml="auto">
                <HStack spacing={1}>
                  <IconButton
                    aria-label="View profile"
                    icon={<ViewIcon />}
                    size="xs"
                    variant="ghost"
                  />
                  <IconButton
                    aria-label="Contact"
                    icon={<EmailIcon />}
                    size="xs"
                    variant="ghost"
                    isDisabled={!signal.isRevealed}
                  />
                </HStack>
              </Box>
            </Flex>
            
            {/* Signal details */}
            <Box px={8} mb={3}>
              <Text fontSize="sm" color="gray.600">{signal.details}</Text>
            </Box>
            
            {/* Footer: program and actions */}
            <Flex justify="space-between" align="center" pt={2} borderTopWidth="1px" borderColor="gray.100">
              <HStack spacing={1}>
                <FaUserGraduate size="12px" color="gray" />
                <Text fontSize="xs" color="gray.600">{signal.program}</Text>
                <Text fontSize="xs" color="gray.400">•</Text>
                <Text fontSize="xs" color="gray.600">{signal.university}</Text>
              </HStack>
              
              <HStack>
                {!signal.isRevealed && (
                  <Button size="xs" leftIcon={<LockIcon />} colorScheme="purple" variant="outline">
                    Reveal Identity
                  </Button>
                )}
                <Button size="xs" rightIcon={<CheckIcon />} colorScheme="green" variant="ghost">
                  Track
                </Button>
              </HStack>
            </Flex>
          </Box>
        ))}
      </VStack>
      
      <Button width="full" mt={4} size="sm" variant="outline">
        View All Signals
      </Button>
    </Box>
  );
}