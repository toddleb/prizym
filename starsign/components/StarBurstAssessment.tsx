// components/StarBurstAssessment.tsx
import {
  Text,
  Radio,
  RadioGroup,
  Stack,
  Button,
  Progress,
} from '@chakra-ui/react';
import { useState } from 'react';
import DashboardCard from './common/DashboardCard';

const questions = [
  'When solving a problem, I prefer to...',
  'In group settings, I usually...',
  'My learning style is best described as...',
  'I enjoy working on...',
  'My ideal day involves...'
];

export default function StarBurstAssessment() {
  const [step, setStep] = useState(0);
  const [value, setValue] = useState('');

  return (
    <DashboardCard title="Star Burst Assessment">
      <Progress
        value={((step + 1) / questions.length) * 100}
        mb={2}
        size="sm"
        colorScheme="purple"
      />
      <Text fontSize="xs" fontWeight="semibold" mb={2} color="gray.300">
        {step + 1}. {questions[step]}
      </Text>
      <RadioGroup onChange={setValue} value={value}>
        <Stack spacing={1} fontSize="xs" color="gray.300">
          <Radio value="1">Break it into steps</Radio>
          <Radio value="2">Explore creative ideas</Radio>
          <Radio value="3">Research others' solutions</Radio>
          <Radio value="4">Discuss with peers</Radio>
        </Stack>
      </RadioGroup>
      <Stack direction="row" spacing={3} mt={3} justify="flex-end">
        <Button size="xs" onClick={() => setStep((s) => Math.max(0, s - 1))}>Back</Button>
        <Button
          size="xs"
          colorScheme="purple"
          onClick={() => setStep((s) => Math.min(questions.length - 1, s + 1))}
        >
          Next
        </Button>
      </Stack>
    </DashboardCard>
  );
}
