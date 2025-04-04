// components/program/RelationshipPipeline.tsx
import { 
  Box, 
  Flex, 
  Heading, 
  Text,
  SimpleGrid,
  HStack,
  Badge,
  Button,
  IconButton,
  Tag,
  Avatar,
  Grid,
  GridItem,
  Menu,
  MenuButton,
  MenuList,
  MenuItem,
  Tooltip,
  useColorModeValue,
  Divider
} from '@chakra-ui/react';
import { 
  ChevronDownIcon, 
  StarIcon, 
  AddIcon,
  ArrowForwardIcon,
  EmailIcon, 
  LockIcon,
  ViewIcon,
  CheckIcon,
  CalendarIcon
} from '@chakra-ui/icons';
import { 
  FaUserGraduate, 
  FaFilter, 
  FaUserPlus, 
  FaUserClock, 
  FaUserCheck,
  FaHandshake,
  FaUsers
} from 'react-icons/fa';

interface RelationshipPipelineProps {
  matched: number;
  contacted: number;
  responded: number;
  applied: number;
  accepted: number;
}

export default function RelationshipPipeline({
  matched,
  contacted,
  responded,
  applied,
  accepted
}: RelationshipPipelineProps) {
  const columnBg = useColorModeValue('gray.50', 'gray.700');
  const borderColor = useColorModeValue('gray.200', 'gray.600');
  
  // Sample candidates - in a real app, this would come from your API
  const pipelineData = [
    {
      stage: 'identified',
      title: 'Identified',
      icon: FaUsers,
      color: 'blue',
      count: matched,
      candidates: [
        {
          id: 'c145',
          blindId: 'Candidate #145',
          isRevealed: false,
          name: null,
          matchScore: 95,
          program: 'Data Science & AI',
          university: 'Nova State',
          skills: ['Python', 'ML', 'Statistics'],
          tags: ['High Potential', 'ML Focus']
        },
        {
          id: 'c217',
          blindId: 'Candidate #217',
          isRevealed: false,
          name: null,
          matchScore: 87,
          program: 'AI & Machine Learning',
          university: 'Quantum College',
          skills: ['Python', 'Data Analysis', 'SQL'],
          tags: ['Data Science']
        }
      ]
    },
    {
      stage: 'engaged',
      title: 'Engaged',
      icon: FaUserClock,
      color: 'purple',
      count: contacted,
      candidates: [
        {
          id: 'c092',
          blindId: 'Candidate #092',
          isRevealed: true,
          name: 'Taylor Kim',
          matchScore: 92,
          program: 'Computer Science',
          university: 'Stellar Tech',
          skills: ['Python', 'ML/AI', 'Data Viz'],
          tags: ['AI Research'],
          lastContact: '2 days ago'
        },
        {
          id: 'c078',
          blindId: 'Candidate #078',
          isRevealed: true,
          name: 'Jordan Lee',
          matchScore: 85,
          program: 'Computer Science',
          university: 'Stellar Tech',
          skills: ['Python', 'Algorithms', 'Web'],
          tags: ['Full-Stack'],
          lastContact: '5 days ago'
        }
      ]
    },
    {
      stage: 'applied',
      title: 'Applied',
      icon: FaUserPlus,
      color: 'green',
      count: applied,
      candidates: [
        {
          id: 'c056',
          blindId: 'Candidate #056',
          isRevealed: true,
          name: 'Alex Chen',
          matchScore: 89,
          program: 'Data Science & AI',
          university: 'Nova State',
          skills: ['Python', 'Deep Learning', 'NLP'],
          tags: ['Interview Scheduled'],
          applicationDate: '3 days ago'
        }
      ]
    },
    {
      stage: 'accepted',
      title: 'Accepted',
      icon: FaUserCheck,
      color: 'teal',
      count: accepted,
      candidates: [
        {
          id: 'c028',
          blindId: 'Candidate #028',
          isRevealed: true,
          name: 'Riley Johnson',
          matchScore: 93,
          program: 'Computer Science',
          university: 'Stellar Tech',
          skills: ['Python', 'ML/AI', 'Computer Vision'],
          tags: ['Starting June'],
          acceptanceDate: '2 weeks ago'
        }
      ]
    }
  ];
  
  return (
    <Box>
      <Flex justify="space-between" align="center" mb={4}>
        <Box>
          <Heading size="md">Relationship Pipeline</Heading>
          <Text color="gray.600" fontSize="sm" mt={1}>
            Track candidates from discovery to offer acceptance
          </Text>
        </Box>
        
        <HStack spacing={2}>
          <IconButton
            aria-label="Filter pipeline"
            icon={<FaFilter />}
            size="sm"
            variant="ghost"
          />
          <Button size="sm" leftIcon={<AddIcon />}>Add Candidate</Button>
        </HStack>
      </Flex>
      
      {/* Pipeline stats */}
      <SimpleGrid columns={5} spacing={4} mb={6} p={4} bg="white" borderRadius="lg" boxShadow="sm">
        {pipelineData.map((stage) => (
          <Box key={stage.stage} textAlign="center">
            <Flex 
              justify="center" 
              align="center" 
              mb={2}
              w="12"
              h="12"
              bg={`${stage.color}.100`}
              color={`${stage.color}.700`}
              borderRadius="lg"
              mx="auto"
            >
              <Box as={stage.icon} size="24px" />
            </Flex>
            <Text fontWeight="bold">{stage.title}</Text>
            <Text fontSize="2xl" fontWeight="bold" color={`${stage.color}.600`}>
              {stage.count}
            </Text>
          </Box>
        ))}
      </SimpleGrid>
      
      {/* Kanban board */}
      <Grid templateColumns="repeat(4, 1fr)" gap={4}>
        {pipelineData.map((stage) => (
          <GridItem key={stage.stage}>
            <Box 
              bg={columnBg} 
              borderRadius="md" 
              borderWidth="1px"
              borderColor={borderColor}
              h="full"
            >
              {/* Column header */}
              <Flex
                justify="space-between"
                align="center"
                bg={`${stage.color}.100`}
                color={`${stage.color}.800`}
                p={3}
                borderTopLeftRadius="md"
                borderTopRightRadius="md"
                borderBottomWidth="1px"
                borderBottomColor={borderColor}
              >
                <HStack>
                  <Box as={stage.icon} size="14px" />
                  <Text fontWeight="bold">{stage.title}</Text>
                </HStack>
                <Badge bg={`${stage.color}.200`} color={`${stage.color}.800`} fontSize="sm">
                  {stage.count}
                </Badge>
              </Flex>
              
              {/* Candidates in this stage */}
              <Box p={2} maxH="480px" overflowY="auto">
                {stage.candidates.map((candidate) => (
                  <Box
                    key={candidate.id}
                    bg="white"
                    borderRadius="md"
                    boxShadow="sm"
                    p={3}
                    mb={2}
                    borderLeftWidth="3px"
                    borderLeftColor={`${stage.color}.500`}
                    _hover={{ 
                      boxShadow: 'md', 
                      borderLeftColor: `${stage.color}.600` 
                    }}
                    transition="all 0.2s"
                  >
                    {/* Candidate header with match score */}
                    <Flex justify="space-between" align="center" mb={2}>
                      {candidate.isRevealed ? (
                        <HStack>
                          <Avatar size="xs" name={candidate.name} />
                          <Text fontWeight="medium" fontSize="sm">
                            {candidate.name}
                          </Text>
                        </HStack>
                      ) : (
                        <HStack>
                          <Box 
                            bg="purple.100" 
                            p={1} 
                            borderRadius="full" 
                            display="flex" 
                            alignItems="center" 
                            justifyContent="center"
                          >
                            <LockIcon color="purple.500" boxSize={2.5} />
                          </Box>
                          <Text fontSize="sm">{candidate.blindId}</Text>
                        </HStack>
                      )}
                      <Badge colorScheme="purple" fontSize="xs">
                        {candidate.matchScore}%
                      </Badge>
                    </Flex>
                    
                    {/* Program and university */}
                    <HStack spacing={1} fontSize="xs" color="gray.600" mb={2}>
                      <FaUserGraduate size="10px" />
                      <Text>{candidate.program}</Text>
                      <Text>•</Text>
                      <Text>{candidate.university}</Text>
                    </HStack>
                    
                    {/* Skills */}
                    <Flex flexWrap="wrap" gap={1} mb={2}>
                      {candidate.skills.map((skill, i) => (
                        <Tag 
                          key={i} 
                          size="sm" 
                          variant="subtle" 
                          colorScheme="blue"
                          fontSize="10px"
                        >
                          {skill}
                        </Tag>
                      ))}
                    </Flex>
                    
                    {/* Candidate tags */}
                    <Flex flexWrap="wrap" gap={1} mb={2}>
                      {candidate.tags.map((tag, i) => (
                        <Tag 
                          key={i} 
                          size="sm" 
                          variant="subtle" 
                          colorScheme="purple"
                          fontSize="10px"
                        >
                          {tag}
                        </Tag>
                      ))}
                    </Flex>
                    
                    {/* Stage-specific info */}
                    {stage.stage === 'engaged' && candidate.lastContact && (
                      <Text fontSize="xs" color="gray.500" mb={2}>
                        Last contact: {candidate.lastContact}
                      </Text>
                    )}
                    
                    {stage.stage === 'applied' && candidate.applicationDate && (
                      <Text fontSize="xs" color="gray.500" mb={2}>
                        Applied: {candidate.applicationDate}
                      </Text>
                    )}
                    
                    {stage.stage === 'accepted' && candidate.acceptanceDate && (
                      <Text fontSize="xs" color="gray.500" mb={2}>
                        Accepted: {candidate.acceptanceDate}
                      </Text>
                    )}
                    
                    {/* Actions */}
                    <Flex justify="space-between" pt={2} borderTopWidth="1px" borderColor="gray.100">
                      {/* Left side actions */}
                      <HStack spacing={1}>
                        <Tooltip label="View Profile">
                          <IconButton
                            aria-label="View profile"
                            icon={<ViewIcon />}
                            size="xs"
                            variant="ghost"
                          />
                        </Tooltip>
                        
                        <Tooltip label={candidate.isRevealed ? "Send Message" : "Reveal First"}>
                          <IconButton
                            aria-label="Contact"
                            icon={<EmailIcon />}
                            size="xs"
                            variant="ghost"
                            isDisabled={!candidate.isRevealed}
                          />
                        </Tooltip>
                        
                        <Tooltip label="Schedule">
                          <IconButton
                            aria-label="Schedule"
                            icon={<CalendarIcon />}
                            size="xs"
                            variant="ghost"
                          />
                        </Tooltip>
                      </HStack>
                      
                      {/* Move to next stage button */}
                      {stage.stage !== 'accepted' && (
                        <Tooltip label={`Move to ${stage.stage === 'identified' ? 'Engaged' : stage.stage === 'engaged' ? 'Applied' : 'Accepted'}`}>
                          <IconButton
                            aria-label="Move to next stage"
                            icon={<ArrowForwardIcon />}
                            size="xs"
                            colorScheme={stage.color.split('.')[0]}
                            variant="ghost"
                          />
                        </Tooltip>
                      )}
                    </Flex>
                  </Box>
                ))}
                
                {/* Add candidate to stage button */}
                <Button 
                  size="sm" 
                  leftIcon={<AddIcon />} 
                  variant="outline" 
                  width="full" 
                  mt={2}
                >
                  Add to {stage.title}
                </Button>
              </Box>
            </Box>
          </GridItem>
        ))}
      </Grid>
    </Box>
  );
}