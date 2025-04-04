// components/program/dashboard/InsightsSidebar.tsx
import React from 'react';
import {
  Box,
  VStack,
  Heading,
  Text,
  Badge,
  Divider,
  HStack,
  Flex,
  IconButton,
  InputGroup,
  Input,
  InputRightElement,
  Button,
  useColorModeValue
} from '@chakra-ui/react';
import { 
  EditIcon, 
  ChatIcon,
  ChevronDownIcon
} from '@chakra-ui/icons';
import { FaBrain } from 'react-icons/fa';

// Import components
import CosmicSignature from '@/components/program/CosmicSignature';
import UpcomingActions from '@/components/program/UpcomingActions';

// Define prop interface
interface InsightsSidebarProps {
  programData: {
    signatureStrength: number;
  };
  insightsData: {
    title: string;
    value: string;
    change: string;
    trend: string;
  }[];
  isAiChatVisible: boolean;
  setIsAiChatVisible: (visible: boolean) => void;
}

const InsightsSidebar: React.FC<InsightsSidebarProps> = ({
  programData,
  insightsData,
  isAiChatVisible,
  setIsAiChatVisible
}) => {
  const borderColor = useColorModeValue('gray.200', 'gray.600');

  return (
    <Box 
      width="280px" 
      bg="white" 
      p={4}
      overflowY="auto"
      borderLeftWidth="1px"
      borderColor={borderColor}
      boxShadow="md"
    >
      <VStack align="stretch" spacing={6}>
        {/* Cosmic Signature */}
        <Box>
          <Flex justify="space-between" align="center" mb={4}>
            <Heading size="sm">Cosmic Signature</Heading>
            <IconButton
              aria-label="Edit signature"
              icon={<EditIcon />}
              size="xs"
              variant="ghost"
            />
          </Flex>
          <CosmicSignature signatureStrength={programData.signatureStrength} />
        </Box>
        
        <Divider />
        
        {/* Performance Insights */}
        <Box>
          <Heading size="sm" mb={4}>Performance Insights</Heading>
          
          <VStack align="stretch" spacing={3}>
            {insightsData.map((insight, index) => (
              <Flex key={index} justify="space-between" align="center" pb={2} borderBottomWidth="1px" borderColor="gray.100">
                <Text fontSize="sm">{insight.title}</Text>
                <HStack>
                  <Text fontWeight="bold">{insight.value}</Text>
                  <Badge 
                    colorScheme={insight.trend === 'up' ? 'green' : 'red'} 
                    variant="subtle"
                  >
                    {insight.change}
                  </Badge>
                </HStack>
              </Flex>
            ))}
          </VStack>
        </Box>
        
        <Divider />
        
        {/* Upcoming Actions */}
        <Box>
          <Heading size="sm" mb={4}>Upcoming Actions</Heading>
          <UpcomingActions />
        </Box>
        
        <Divider />
        
        {/* AI Link */}
        <Box>
          <Heading size="sm" mb={4}>
            <Flex align="center">
              <FaBrain style={{ marginRight: '8px' }} />
              AI Insights
            </Flex>
          </Heading>
          <Button 
            colorScheme="purple" 
            size="sm" 
            width="full"
            leftIcon={<FaBrain />}
            onClick={() => {
              // Find and click the AI tab
              const aiTab = document.querySelector('.chakra-tabs__tablist button:nth-child(2)');
              if (aiTab) (aiTab as HTMLElement).click();
            }}
          >
            View AI Talent Intelligence
          </Button>
        </Box>
        
        <Divider />
        
        {/* AI Assistant */}
        {isAiChatVisible && (
          <Box>
            <Flex justify="space-between" align="center" mb={3}>
              <Heading size="sm">AI Assistant</Heading>
              <IconButton
                aria-label="Close assistant"
                icon={<ChevronDownIcon />}
                size="xs"
                variant="ghost"
                onClick={() => setIsAiChatVisible(false)}
              />
            </Flex>
            
            <VStack align="stretch" spacing={3} maxH="300px" overflowY="auto" p={2} borderWidth="1px" borderRadius="md">
              <Box bg="blue.50" p={3} borderRadius="lg" borderTopLeftRadius="sm">
                <Text fontSize="sm">
                  What insights can I help you discover about your candidates?
                </Text>
              </Box>
              
              <Box bg="gray.100" p={3} borderRadius="lg" borderTopRightRadius="sm" alignSelf="flex-end">
                <Text fontSize="sm">
                  Show top Data Science candidates
                </Text>
              </Box>
              
              <Box bg="blue.50" p={3} borderRadius="lg" borderTopLeftRadius="sm">
                <Text fontSize="sm">
                  I've identified 3 high-matching Data Science candidates. The top match (95%) has strong Python and ML skills with high intent signals from GitHub activity.
                </Text>
              </Box>
            </VStack>
            
            <InputGroup size="sm" mt={3}>
              <Input placeholder="Ask about candidates or programs..." />
              <InputRightElement>
                <IconButton
                  aria-label="Send message"
                  icon={<ChatIcon />}
                  size="xs"
                  variant="ghost"
                />
              </InputRightElement>
            </InputGroup>
          </Box>
        )}
        
        {!isAiChatVisible && (
          <Button 
            leftIcon={<ChatIcon />} 
            onClick={() => setIsAiChatVisible(true)}
            colorScheme="blue"
            size="sm"
            width="full"
            variant="outline"
          >
            Ask AI Assistant
          </Button>
        )}
      </VStack>
    </Box>
  );
};

export default InsightsSidebar;
  
  