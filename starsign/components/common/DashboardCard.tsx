// components/common/DashboardCard.tsx
import { Box, Heading } from '@chakra-ui/react';
import { ReactNode } from 'react';

export default function DashboardCard({
  title,
  children,
  maxH = '260px',
}: {
  title: string;
  children: ReactNode;
  maxH?: string;
}) {
  return (
    <Box
      p={3}
      borderWidth={1}
      borderRadius="xl"
      boxShadow="sm"
      maxH={maxH}
      overflowY="auto"
      bg="gray.700"
    >
      <Heading size="sm" mb={2}>{title}</Heading>
      {children}
    </Box>
  );
}