import { Flex, Box } from '@chakra-ui/react';
import Sidebar from './Sidebar';
import Navbar from './Navbar';

export default function Layout({
  children,
  role,
}: {
  children: React.ReactNode;
  role: string;
}) {
  return (
    <Flex height="100vh" overflow="hidden">
      <Sidebar role={role} />
      <Flex direction="column" flex="1" height="100vh" overflow="hidden">
        <Navbar />
        <Box
          flex="1"
          overflowY="auto"
          px={6}
          py={4}
          position="relative"
          zIndex="1"
        >
          {children}
        </Box>
      </Flex>
    </Flex>
  );
}