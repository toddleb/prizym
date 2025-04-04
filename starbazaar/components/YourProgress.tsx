// components/YourProgress.tsx
import { Text, Progress, HStack, VStack } from '@chakra-ui/react';
import DashboardCard from './common/DashboardCard';

export default function YourProgress() {
  return (
    <DashboardCard title="Your Progress">
      <HStack spacing={4} mb={2} fontSize="sm" color="gray.300">
        <Text>Day Streak: 7</Text>
        <Text>Achievements: 12</Text>
        <Text>Level: 3</Text>
      </HStack>
      <VStack align="start" spacing={1}>
        <Progress value={45} colorScheme="green" w="full" borderRadius="lg" />
        <Text fontSize="xs" color="gray.400">Level up to unlock bonus credits</Text>
      </VStack>
    </DashboardCard>
  );
}