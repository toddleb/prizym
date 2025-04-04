// components/program/ProgramIntelligence.tsx
import { 
  Box, 
  Flex, 
  Heading, 
  Text,
  Badge,
  SimpleGrid,
  Button,
  HStack,
  VStack,
  Tag,
  Select,
  Grid,
  GridItem,
  IconButton,
  Menu,
  MenuButton,
  MenuList,
  MenuItem,
  Divider,
  useColorModeValue,
  Image
} from '@chakra-ui/react';
import { 
  ChevronDownIcon, 
  InfoIcon, 
  StarIcon,
  ExternalLinkIcon, 
  ArrowUpIcon,
  ArrowDownIcon
} from '@chakra-ui/icons';
import { 
  FaGraduationCap, 
  FaBuilding, 
  FaChartLine, 
  FaUsers, 
  FaMapMarkerAlt,
  FaFilter
} from 'react-icons/fa';

interface ProgramIntelligenceProps {
  columns?: number;
  gridColumn?: any;
}

export default function ProgramIntelligence({ 
  columns = 1, 
  gridColumn 
}: ProgramIntelligenceProps) {
  const borderColor = useColorModeValue('gray.200', 'gray.700');
  const bgHover = useColorModeValue('gray.50', 'gray.700');
  
  // Sample university data - in a real app, this would come from your API
  const universities = [
    {
      id: 'uni1',
      name: 'Nova State University',
      location: 'West Coast',
      programs: [
        { 
          id: 'p1', 
          name: 'Data Science & AI', 
          students: 245, 
          trend: 'up', 
          trendPercent: 12,
          highlights: ['ML Research', 'NLP Projects', 'Robotics'],
          match: 92,
          signalStrength: 'high'
        },
        { 
          id: 'p2', 
          name: 'Software Engineering', 
          students: 312, 
          trend: 'stable', 
          trendPercent: 3,
          highlights: ['Full-Stack', 'Cloud Computing', 'Mobile'],
          match: 78,
          signalStrength: 'medium'
        }
      ]
    },
    {
      id: 'uni2',
      name: 'Stellar Tech Institute',
      location: 'East Coast',
      programs: [
        { 
          id: 'p3', 
          name: 'Computer Science', 
          students: 421, 
          trend: 'up', 
          trendPercent: 8,
          highlights: ['Algorithms', 'Systems', 'Graphics'],
          match: 82,
          signalStrength: 'high'
        },
        { 
          id: 'p4', 
          name: 'Information Systems', 
          students: 198, 
          trend: 'down', 
          trendPercent: 5,
          highlights: ['Business Analysis', 'Database Design', 'IT Strategy'],
          match: 65,
          signalStrength: 'low'
        }
      ]
    },
    {
      id: 'uni3',
      name: 'Quantum College',
      location: 'Midwest',
      programs: [
        { 
          id: 'p5', 
          name: 'AI & Machine Learning', 
          students: 178, 
          trend: 'up', 
          trendPercent: 18,
          highlights: ['Deep Learning', 'Computer Vision', 'NLP'],
          match: 95,
          signalStrength: 'very-high'
        }
      ]
    }
  ];
  
  // Function to render trend indicator
  const renderTrend = (trend: string, percent: number) => {
    if (trend === 'up') {
      return (
        <HStack spacing={1} color="green.500">
          <ArrowUpIcon boxSize={3} />
          <Text fontSize="xs" fontWeight="medium">{percent}%</Text>
        </HStack>
      );
    } else if (trend === 'down') {
      return (
        <HStack spacing={1} color="red.500">
          <ArrowDownIcon boxSize={3} />
          <Text fontSize="xs" fontWeight="medium">{percent}%</Text>
        </HStack>
      );
    } else {
      return (
        <Text fontSize="xs" color="gray.500">Stable</Text>
      );
    }
  };
  
  // Function to render signal strength indicator
  const getSignalColor = (strength: string) => {
    switch(strength) {
      case 'very-high': return 'purple.500';
      case 'high': return 'green.500';
      case 'medium': return 'blue.500';
      case 'low': return 'gray.500';
      default: return 'gray.400';
    }
  };
  
  const renderSignalStrength = (strength: string) => {
    const color = getSignalColor(strength);
    const dots = strength === 'very-high' ? 4 : 
                 strength === 'high' ? 3 : 
                 strength === 'medium' ? 2 : 1;
                 
    return (
      <HStack spacing={1}>
        {[...Array(4)].map((_, i) => (
          <Box 
            key={i}
            w="5px" 
            h="5px" 
            borderRadius="full" 
            bg={i < dots ? color : 'gray.200'} 
          />
        ))}
      </HStack>
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
        <Heading size="md">Program Intelligence Hub</Heading>
        
        <HStack>
          <IconButton
            aria-label="Filter programs"
            icon={<FaFilter />}
            size="sm"
            variant="ghost"
          />
          
          <Menu>
            <MenuButton as={Button} rightIcon={<ChevronDownIcon />} size="sm" variant="outline">
              Filter By
            </MenuButton>
            <MenuList>
              <MenuItem>All Programs</MenuItem>
              <MenuItem>High Match Score (85%+)</MenuItem>
              <MenuItem>Growing Programs</MenuItem>
              <MenuItem>Recent Activity</MenuItem>
            </MenuList>
          </Menu>
        </HStack>
      </Flex>
      
      <Flex justify="space-between" align="center" mb={4}>
        <HStack spacing={2}>
          <Select size="sm" width="auto" defaultValue="all">
            <option value="all">All Regions</option>
            <option value="west">West Coast</option>
            <option value="east">East Coast</option>
            <option value="midwest">Midwest</option>
            <option value="south">South</option>
          </Select>
          
          <Select size="sm" width="auto" defaultValue="cs">
            <option value="all">All Fields</option>
            <option value="cs">Computer Science</option>
            <option value="ds">Data Science</option>
            <option value="eng">Engineering</option>
          </Select>
        </HStack>
        
        <Button size="sm" variant="ghost" rightIcon={<ExternalLinkIcon />}>
          Map View
        </Button>
      </Flex>
      
      <SimpleGrid columns={columns} spacing={4}>
        {universities.map(university => (
          <Box 
            key={university.id} 
            borderWidth="1px" 
            borderRadius="md"
            borderColor={borderColor}
            overflow="hidden"
          >
            {/* University header */}
            <Flex 
              bg="gray.50" 
              p={3} 
              borderBottomWidth="1px" 
              borderColor={borderColor}
              justify="space-between"
              align="center"
            >
              <Box>
                <Text fontWeight="bold">{university.name}</Text>
                <Flex align="center">
                  <FaMapMarkerAlt size="12px" color="gray" />
                  <Text fontSize="xs" ml={1} color="gray.600">{university.location}</Text>
                </Flex>
              </Box>
              
              <IconButton
                aria-label="University details"
                icon={<ExternalLinkIcon />}
                size="xs"
                variant="ghost"
              />
            </Flex>
            
            {/* Programs */}
            <VStack spacing={0} align="stretch" divider={<Divider />}>
              {university.programs.map(program => (
                <Box 
                  key={program.id} 
                  p={3}
                  _hover={{ bg: bgHover }}
                  transition="background 0.2s"
                >
                  <Flex justify="space-between" align="flex-start">
                    <Box>
                      <Flex align="center">
                        <FaGraduationCap size="14px" color="purple" />
                        <Text fontWeight="medium" ml={2}>{program.name}</Text>
                        <Badge ml={2} colorScheme="purple">{program.match}%</Badge>
                      </Flex>
                      
                      <HStack spacing={4} mt={1}>
                        <Flex align="center">
                          <FaUsers size="10px" color="gray" />
                          <Text fontSize="xs" ml={1}>{program.students} students</Text>
                        </Flex>
                        
                        <Flex align="center">
                          <FaChartLine size="10px" color="gray" />
                          {renderTrend(program.trend, program.trendPercent)}
                        </Flex>
                        
                        <Box>
                          {renderSignalStrength(program.signalStrength)}
                        </Box>
                      </HStack>
                    </Box>
                    
                    <Menu>
                      <MenuButton 
                        as={IconButton}
                        aria-label="Program options"
                        icon={<ChevronDownIcon />}
                        variant="ghost"
                        size="xs"
                      />
                      <MenuList>
                        <MenuItem>View Program Details</MenuItem>
                        <MenuItem>View Candidates</MenuItem>
                        <MenuItem>Track Program</MenuItem>
                        <MenuItem>Connect with Faculty</MenuItem>
                      </MenuList>
                    </Menu>
                  </Flex>
                  
                  <Flex mt={2} flexWrap="wrap" gap={1}>
                    {program.highlights.map((highlight, i) => (
                      <Tag key={i} size="sm" variant="subtle" colorScheme="purple">
                        {highlight}
                      </Tag>
                    ))}
                  </Flex>
                </Box>
              ))}
            </VStack>
          </Box>
        ))}
      </SimpleGrid>
      
      <Button width="full" mt={4} size="sm" variant="outline">
        View All Programs
      </Button>
    </Box>
  );
}