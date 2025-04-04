// components/DailyStarBurst.tsx
import { Button, Text, VStack } from '@chakra-ui/react';
import DashboardCard from './common/DashboardCard';

export default function DailyStarBurst({ onStart }) {
  return (
    <DashboardCard title="Daily Star Burst">
      <VStack align="start" spacing={2}>
        <Text fontSize="sm" color="gray.300">
          Answer 5 quick questions and earn 10 cosmic credits.
        </Text>
        <Button size="sm" colorScheme="purple" onClick={onStart}>
          Take Star Burst
        </Button>
      </VStack>
    </DashboardCard>
  );
}