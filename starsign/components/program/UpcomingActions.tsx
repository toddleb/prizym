// components/program/UpcomingActions.tsx
import { 
  Box, 
  Flex, 
  Text, 
  VStack,
  HStack,
  IconButton,
  Badge,
  Checkbox,
  useColorModeValue,
  Button
} from '@chakra-ui/react';
import { 
  CalendarIcon, 
  CheckIcon, 
  EmailIcon, 
  StarIcon, 
  TimeIcon,
  ViewIcon
} from '@chakra-ui/icons';
import { 
  FaUserGraduate, 
  FaUsers, 
  FaBell, 
  FaFileAlt
} from 'react-icons/fa';

export default function UpcomingActions() {
  const borderColor = useColorModeValue('gray.200', 'gray.700');
  
  // Sample actions - in a real app, this would come from your API
  const actions = [
    {
      id: 'a1',
      type: 'follow-up',
      title: 'Follow up with interested candidates',
      description: '7 candidates awaiting response',
      icon: EmailIcon,
      color: 'blue',
      dueDate: 'Due in 2 days',
      priority: 'high'
    },
    {
      id: 'a2',
      type: 'event',
      title: 'Virtual Info Session',
      description: 'Sep 18, 7pm ET - 15 RSVPs',
      icon: CalendarIcon,
      color: 'purple',
      dueDate: 'In 5 days',
      priority: 'medium'
    },
    {
      id: 'a3',
      type: 'application',
      title: 'Review applications',
      description: '6 new applications pending review',
      icon: FaFileAlt,
      color: 'green',
      dueDate: 'Due by Sep 20',
      priority: 'high'
    },
    {
      id: 'a4',
      type: 'faculty',
      title: 'Connect with Prof. Johnson',
      description: 'Re: AI program collaboration',
      icon: FaUserGraduate,
      color: 'orange',
      dueDate: 'Suggested task',
      priority: 'low'
    }
  ];
  
  // Function to get priority badge color
  const getPriorityColor = (priority) => {
    switch (priority) {
      case 'high': return 'red';
      case 'medium': return 'orange';
      case 'low': return 'green';
      default: return 'gray';
    }
  };
  
  return (
    <VStack spacing={3} align="stretch">
      {actions.map((action) => (
        <Box 
          key={action.id}
          borderWidth="1px"
          borderRadius="md"
          borderColor={borderColor}
          p={3}
          _hover={{ borderColor: `${action.color}.300`, boxShadow: 'sm' }}
          transition="all 0.2s"
        >
          <Flex justify="space-between" align="flex-start">
            <HStack align="flex-start" spacing={3}>
              {/* Icon */}
              <Box 
                p={2} 
                borderRadius="md" 
                bg={`${action.color}.100`}
                color={`${action.color}.700`}
              >
                <Box as={action.icon} size="16px" />
              </Box>
              
              {/* Content */}
              <Box>
                <Text fontWeight="medium">{action.title}</Text>
                <Text fontSize="sm" color="gray.600" mt={1}>
                  {action.description}
                </Text>
                
                <Flex align="center" mt={2}>
                  <TimeIcon boxSize={3} color="gray.500" mr={1} />
                  <Text fontSize="xs" color="gray.500">{action.dueDate}</Text>
                </Flex>
              </Box>
            </HStack>
            
            {/* Priority */}
            <Badge colorScheme={getPriorityColor(action.priority)} size="sm">
              {action.priority}
            </Badge>
          </Flex>
          
          <Flex justify="space-between" align="center" mt={3} pt={2} borderTopWidth="1px" borderColor="gray.100">
            <Checkbox size="sm" colorScheme={action.color.split('.')[0]}>
              <Text fontSize="xs">Mark complete</Text>
            </Checkbox>
            
            <IconButton
              aria-label="View details"
              icon={<ViewIcon />}
              size="xs"
              variant="ghost"
            />
          </Flex>
        </Box>
      ))}
      
      <Button size="sm" colorScheme="purple" variant="outline" leftIcon={<FaBell />} width="full">
        Set up smart reminders
      </Button>
    </VStack>
  );
}