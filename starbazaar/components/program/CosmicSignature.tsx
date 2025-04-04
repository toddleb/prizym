// components/program/CosmicSignature.tsx
import { Box, Flex, Text, Progress, SimpleGrid, Badge, Icon } from '@chakra-ui/react';
import { StarIcon } from '@chakra-ui/icons';
import { FaCode, FaUserGraduate, FaUsers, FaBrain } from 'react-icons/fa';

interface CosmicSignatureProps {
  signatureStrength: number;
}

export default function CosmicSignature({ signatureStrength }: CosmicSignatureProps) {
  // Sample signature data - in a real app, this would come from your API
  const signatureCategories = [
    { 
      id: 'technical', 
      name: 'Technical Skills', 
      score: 95, 
      color: 'blue.500',
      icon: FaCode,
      factors: [
        { name: 'Python', value: 90 },
        { name: 'Data Science', value: 95 },
        { name: 'Statistics', value: 85 }
      ]
    },
    { 
      id: 'learning', 
      name: 'Learning Style', 
      score: 88, 
      color: 'green.500',
      icon: FaBrain,
      factors: [
        { name: 'Project-based', value: 92 },
        { name: 'Self-directed', value: 88 },
        { name: 'Hands-on', value: 85 }
      ]
    },
    { 
      id: 'experience', 
      name: 'Prior Experience', 
      score: 75, 
      color: 'orange.500',
      icon: FaUserGraduate,
      factors: [
        { name: 'Coding Projects', value: 80 },
        { name: 'Industry Work', value: 70 },
        { name: 'Academic Research', value: 75 }
      ]
    },
    { 
      id: 'soft', 
      name: 'Soft Skills', 
      score: 90, 
      color: 'purple.500',
      icon: FaUsers,
      factors: [
        { name: 'Problem Solving', value: 95 },
        { name: 'Communication', value: 85 },
        { name: 'Teamwork', value: 90 }
      ]
    }
  ];

  return (
    <Box>
      <Flex justify="space-between" align="center" mb={4}>
        <Box>
          <Badge colorScheme="purple" fontSize="sm">
            <StarIcon mr={1} />
            {signatureStrength}% Clarity
          </Badge>
          <Text fontSize="xs" color="gray.500" mt={1}>
            Your cosmic signature defines how we match students to your program
          </Text>
        </Box>
      </Flex>

      {/* Simplified star signature visualization */}
      <Box 
        position="relative" 
        h="180px" 
        bg="purple.50" 
        borderRadius="md" 
        mb={4}
        overflow="hidden"
      >
        {/* This would be replaced by an actual visualization component */}
        <Flex 
          position="absolute" 
          top="0" 
          left="0" 
          width="100%" 
          height="100%" 
          align="center" 
          justify="center"
          direction="column"
        >
          <Box position="relative" width="100px" height="100px">
            {/* Star shape visualization */}
            <Box 
              position="absolute" 
              top="50%" 
              left="50%" 
              transform="translate(-50%, -50%)" 
              borderRadius="full"
              bg="purple.100"
              width="80px"
              height="80px"
              zIndex={1}
            />
            
            {/* Spokes for each category */}
            {signatureCategories.map((category, index) => {
              const angle = (index * Math.PI / 2);
              const length = (category.score / 100) * 40;
              
              return (
                <Box
                  key={category.id}
                  position="absolute"
                  top="50%"
                  left="50%"
                  height="2px"
                  width={`${length}px`}
                  bg={category.color}
                  transform={`translate(-1px, -50%) rotate(${angle}rad)`}
                  transformOrigin="left center"
                  zIndex={2}
                >
                  <Box 
                    position="absolute" 
                    right="-4px" 
                    top="-4px"
                    width="8px" 
                    height="8px" 
                    borderRadius="full" 
                    bg={category.color} 
                  />
                </Box>
              );
            })}
            
            {/* Center star */}
            <StarIcon 
              position="absolute" 
              top="50%" 
              left="50%" 
              transform="translate(-50%, -50%)" 
              boxSize={6}
              color="yellow.400"
              zIndex={3}
            />
          </Box>
          <Text fontWeight="bold" mt={4} color="purple.600">
            Program Star Signature
          </Text>
        </Flex>
      </Box>

      {/* Categories */}
      <SimpleGrid columns={2} spacing={4}>
        {signatureCategories.map(category => (
          <Box key={category.id}>
            <Flex align="center" mb={1}>
              <Icon as={category.icon} color={category.color} mr={1} />
              <Text fontSize="sm" fontWeight="medium">{category.name}</Text>
              <Text fontSize="xs" ml="auto" fontWeight="bold">
                {category.score}%
              </Text>
            </Flex>
            <Progress 
              value={category.score} 
              size="sm" 
              colorScheme={category.color.split('.')[0]}
              borderRadius="full"
              mb={2}
            />
            <Flex flexWrap="wrap" gap={1}>
              {category.factors.map(factor => (
                <Badge 
                  key={factor.name} 
                  variant="subtle" 
                  colorScheme={category.color.split('.')[0]}
                  fontSize="10px"
                >
                  {factor.name}: {factor.value}%
                </Badge>
              ))}
            </Flex>
          </Box>
        ))}
      </SimpleGrid>
    </Box>
  );
}