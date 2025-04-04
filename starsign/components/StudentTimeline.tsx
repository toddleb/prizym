// components/StudentTimeline.tsx
import {
  Text,
  HStack,
  VStack,
  Circle,
} from '@chakra-ui/react';
import DashboardCard from './common/DashboardCard';

const stages = ['Freshman', 'Sophomore', 'Junior', 'Senior'];

export default function StudentTimeline() {
  return (
    <DashboardCard title="Star Sign Evolution">
      <HStack justify="space-between">
        {stages.map((stage, idx) => (
          <VStack key={idx} spacing={1} fontSize="xs">
            <Circle size="10px" bg="purple.400" />
            <Text color="gray.300">{stage}</Text>
          </VStack>
        ))}
      </HStack>
    </DashboardCard>
  );
}