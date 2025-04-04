// components/StarSignature.tsx
import { Text, VStack, Heading, Divider } from '@chakra-ui/react';
import DashboardCard from './common/DashboardCard';

export default function StarSignature() {
  return (
    <DashboardCard title="Star Signature">
      <Text fontSize="xs" color="gray.300" mb={2}>
        Your unique cosmic pattern of strengths and growth areas.
      </Text>
      <VStack align="start" spacing={1} fontSize="xs">
        <Text fontWeight="semibold">Strengths:</Text>
        <Text color="gray.300">• Data Analysis</Text>
        <Text color="gray.300">• Problem Solving</Text>
        <Text color="gray.300">• Creativity</Text>
        <Divider my={1} />
        <Text fontWeight="semibold">Growth Areas:</Text>
        <Text color="gray.300">• Team Leadership</Text>
        <Text color="gray.300">• Public Speaking</Text>
      </VStack>
    </DashboardCard>
  );
}
