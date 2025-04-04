// components/program/TopCandidates.tsx
import { 
  Box, 
  Flex, 
  Text, 
  Badge, 
  Avatar, 
  VStack,
  HStack,
  Button,
  IconButton,
  Divider,
  useColorModeValue 
} from '@chakra-ui/react';
import { StarIcon, ViewIcon, LockIcon, EmailIcon } from '@chakra-ui/icons';
import { FaUserGraduate } from 'react-icons/fa';

// Sample candidate data - in a real app, this would come from your API
const topCandidates = [
  {
    id: 'c145',
    blindId: 'Candidate #145',
    isRevealed: false,
    name: null,
    matchScore: 95,
    program: 'Data Science & AI',
    university: 'Nova State',
    skills: ['Python', 'ML', 'Statistics'],
    intent: 'high',
    signalStrength: 4
  },
  {
    id: 'c092',
    blindId: 'Candidate #092',
    isRevealed: true,
    name: 'Taylor Kim',
    matchScore: 92,
    program: 'Computer Science',
    university: 'Stellar Tech',
    skills: ['Python', 'ML/AI', 'Data Viz'],
    intent: 'very-high',
    signalStrength: 5
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
    intent: 'medium',
    signalStrength: 3
  }
];

interface TopCandidatesProps {
  highMatchCount: number;
}

export default function TopCandidates({ highMatchCount }: TopCandidatesProps) {
  const borderColor = useColorModeValue('gray.200', 'gray.700');
  
  // Render stars based on match score
  const renderStars = (score: number) => {
    const stars = [];
    const fullStars = Math.floor(score / 20);
    
    for (let i = 0; i < 5; i++) {
      stars.push(
        <StarIcon 
          key={i}
          color={i < fullStars ? 'yellow.400' : 'gray.300'} 
          boxSize={3}
        />
      );
    }
    
    return stars;
  };
  
  // Function to get color based on intent level
  const getIntentColor = (intent: string) => {
    switch (intent) {
      case 'very-high': return 'purple';
      case 'high': return 'green';
      case 'medium': return 'blue';
      case 'low': return 'gray';
      default: return 'gray';
    }
  };
  
  return (
    <Box>
      <VStack spacing={3} align="stretch">
        {topCandidates.map((candidate) => (
          <Box 
            key={candidate.id} 
            borderWidth="1px" 
            borderRadius="md" 
            borderColor={borderColor}
            p={3}
            _hover={{ borderColor: 'purple.300', boxShadow: 'sm' }}
            transition="all 0.2s"
          >
            <Flex justify="space-between" mb={2}>
              {/* Left: Basic info */}
              <Box>
                {candidate.isRevealed ? (
                  <HStack>
                    <Avatar size="xs" name={candidate.name} />
                    <Text fontWeight="medium" fontSize="sm">{candidate.name}</Text>
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
                
                <HStack mt={1} spacing={1}>
                  {renderStars(candidate.matchScore)}
                </HStack>
              </Box>
              
              {/* Right: Match score */}
              <Badge colorScheme="purple" fontSize="sm">
                {candidate.matchScore}%
              </Badge>
            </Flex>
            
            {/* Program and university */}
            <Flex align="center" fontSize="xs" color="gray.600" mb={2}>
              <FaUserGraduate size="10px" style={{ marginRight: '4px' }} />
              <Text>{candidate.program}</Text>
              <Text mx={1}>•</Text>
              <Text>{candidate.university}</Text>
            </Flex>
            
            {/* Skills */}
            <Flex flexWrap="wrap" gap={1} mb={3}>
              {candidate.skills.map((skill, i) => (
                <Badge 
                  key={i} 
                  colorScheme="blue" 
                  variant="subtle" 
                  fontSize="xs"
                >
                  {skill}
                </Badge>
              ))}
            </Flex>
            
            {/* Intent indicator */}
            <Flex justify="space-between" align="center">
              <Badge 
                colorScheme={getIntentColor(candidate.intent)} 
                variant="subtle"
                fontSize="xs"
              >
                {candidate.intent.replace('-', ' ').replace(/^\w/, c => c.toUpperCase())} Intent
              </Badge>
              
              <HStack>
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
                  isDisabled={!candidate.isRevealed}
                />
              </HStack>
            </Flex>
          </Box>
        ))}
      </VStack>
      
      <Flex justify="center" mt={3}>
        <Button size="xs" colorScheme="purple" variant="link">
          View all {highMatchCount} high-quality matches
        </Button>
      </Flex>
    </Box>
  );
}