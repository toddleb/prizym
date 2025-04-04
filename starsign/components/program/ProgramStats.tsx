// components/program/ProgramStats.tsx
import { 
  Box, 
  SimpleGrid, 
  Stat, 
  StatLabel, 
  StatNumber, 
  StatHelpText, 
  StatArrow,
  Flex,
  ButtonGroup,
  Button,
  Icon
} from '@chakra-ui/react';
import { StarIcon, ArrowUpIcon, ArrowDownIcon, CheckIcon } from '@chakra-ui/icons';
import { FaUserGraduate, FaUsers, FaComments, FaChartLine } from 'react-icons/fa';

interface ProgramStatsProps {
  data: {
    matchCount: number;
    highMatchCount: number;
    applicationCount: number;
    acceptedCount: number;
    matchRate: number;
    responseRate: number;
    signatureStrength: number;
  };
  periodFilter: string;
  setPeriodFilter: (period: string) => void;
}

export default function ProgramStats({ 
  data, 
  periodFilter, 
  setPeriodFilter 
}: ProgramStatsProps) {
  // Sample change data - in a real app, this would be calculated
  const changes = {
    matchCount: 8.2,
    highMatchCount: 15.3,
    applicationCount: 5.7,
    acceptedCount: -2.1,
    matchRate: 2.8,
    responseRate: -3.4
  };
  
  return (
    <Box>
      <Flex justify="space-between" align="center" mb={4}>
        <ButtonGroup size="sm" isAttached variant="outline">
          <Button 
            colorScheme={periodFilter === '7d' ? 'purple' : 'gray'}
            onClick={() => setPeriodFilter('7d')}
          >
            7 Days
          </Button>
          <Button 
            colorScheme={periodFilter === '30d' ? 'purple' : 'gray'}
            onClick={() => setPeriodFilter('30d')}
          >
            30 Days
          </Button>
          <Button 
            colorScheme={periodFilter === '90d' ? 'purple' : 'gray'}
            onClick={() => setPeriodFilter('90d')}
          >
            90 Days
          </Button>
        </ButtonGroup>
      </Flex>

      <SimpleGrid columns={{ base: 2, md: 3, lg: 6 }} spacing={4}>
        {/* Total Matches */}
        <Stat p={4} bg="white" borderRadius="lg" boxShadow="sm">
          <Flex align="center">
            <Box 
              mr={3} 
              bg="blue.50" 
              p={2} 
              borderRadius="md" 
              color="blue.500"
            >
              <Icon as={FaUsers} boxSize={5} />
            </Box>
            <Box>
              <StatLabel fontSize="xs">Total Matches</StatLabel>
              <StatNumber fontSize="2xl">{data.matchCount}</StatNumber>
              <StatHelpText mb={0}>
                <StatArrow 
                  type={changes.matchCount >= 0 ? 'increase' : 'decrease'} 
                />
                {Math.abs(changes.matchCount)}%
              </StatHelpText>
            </Box>
          </Flex>
        </Stat>

        {/* High Matches (95%+) */}
        <Stat p={4} bg="white" borderRadius="lg" boxShadow="sm">
          <Flex align="center">
            <Box 
              mr={3} 
              bg="purple.50" 
              p={2} 
              borderRadius="md" 
              color="purple.500"
            >
              <StarIcon boxSize={5} />
            </Box>
            <Box>
              <StatLabel fontSize="xs">95%+ Matches</StatLabel>
              <StatNumber fontSize="2xl">{data.highMatchCount}</StatNumber>
              <StatHelpText mb={0}>
                <StatArrow 
                  type={changes.highMatchCount >= 0 ? 'increase' : 'decrease'} 
                />
                {Math.abs(changes.highMatchCount)}%
              </StatHelpText>
            </Box>
          </Flex>
        </Stat>

        {/* Applications */}
        <Stat p={4} bg="white" borderRadius="lg" boxShadow="sm">
          <Flex align="center">
            <Box 
              mr={3} 
              bg="green.50" 
              p={2} 
              borderRadius="md" 
              color="green.500"
            >
              <Icon as={FaChartLine} boxSize={5} />
            </Box>
            <Box>
              <StatLabel fontSize="xs">Applications</StatLabel>
              <StatNumber fontSize="2xl">{data.applicationCount}</StatNumber>
              <StatHelpText mb={0}>
                <StatArrow 
                  type={changes.applicationCount >= 0 ? 'increase' : 'decrease'} 
                />
                {Math.abs(changes.applicationCount)}%
              </StatHelpText>
            </Box>
          </Flex>
        </Stat>

        {/* Accepted */}
        <Stat p={4} bg="white" borderRadius="lg" boxShadow="sm">
          <Flex align="center">
            <Box 
              mr={3} 
              bg="teal.50" 
              p={2} 
              borderRadius="md" 
              color="teal.500"
            >
              <CheckIcon boxSize={5} />
            </Box>
            <Box>
              <StatLabel fontSize="xs">Accepted</StatLabel>
              <StatNumber fontSize="2xl">{data.acceptedCount}</StatNumber>
              <StatHelpText mb={0}>
                <StatArrow 
                  type={changes.acceptedCount >= 0 ? 'increase' : 'decrease'} 
                />
                {Math.abs(changes.acceptedCount)}%
              </StatHelpText>
            </Box>
          </Flex>
        </Stat>

        {/* Match Rate */}
        <Stat p={4} bg="white" borderRadius="lg" boxShadow="sm">
          <Flex align="center">
            <Box 
              mr={3} 
              bg="orange.50" 
              p={2} 
              borderRadius="md" 
              color="orange.500"
            >
              <Icon as={FaUserGraduate} boxSize={5} />
            </Box>
            <Box>
              <StatLabel fontSize="xs">Match Rate</StatLabel>
              <StatNumber fontSize="2xl">{data.matchRate}%</StatNumber>
              <StatHelpText mb={0}>
                <StatArrow 
                  type={changes.matchRate >= 0 ? 'increase' : 'decrease'} 
                />
                {Math.abs(changes.matchRate)}%
              </StatHelpText>
            </Box>
          </Flex>
        </Stat>

        {/* Response Rate */}
        <Stat p={4} bg="white" borderRadius="lg" boxShadow="sm">
          <Flex align="center">
            <Box 
              mr={3} 
              bg="cyan.50" 
              p={2} 
              borderRadius="md" 
              color="cyan.500"
            >
              <Icon as={FaComments} boxSize={5} />
            </Box>
            <Box>
              <StatLabel fontSize="xs">Response Rate</StatLabel>
              <StatNumber fontSize="2xl">{data.responseRate}%</StatNumber>
              <StatHelpText mb={0}>
                <StatArrow 
                  type={changes.responseRate >= 0 ? 'increase' : 'decrease'} 
                />
                {Math.abs(changes.responseRate)}%
              </StatHelpText>
            </Box>
          </Flex>
        </Stat>
      </SimpleGrid>
    </Box>
  );
}