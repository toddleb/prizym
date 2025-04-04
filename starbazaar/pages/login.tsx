import { Box, Button, Heading, Select, VStack } from '@chakra-ui/react';
import { useState } from 'react';
import { useRouter } from 'next/router';

export default function Login() {
  const [role, setRole] = useState('student');
  const router = useRouter();

  const handleLogin = () => {
    localStorage.setItem('userRole', role);
    router.push(`/${role}/dashboard`);
  };

  return (
    <Box minH="100vh" bg="brand.galaxy" color="white" display="flex" justifyContent="center" alignItems="center">
      <VStack spacing={6}>
        <Heading size="xl">Star Navigator</Heading>
        <Select value={role} onChange={(e) => setRole(e.target.value)} maxW="sm" bg="white" color="black">
          <option value="student">Student</option>
          <option value="program">Program</option>
          <option value="agency">Agency</option>
          <option value="military">Military</option>
        </Select>
        <Button onClick={handleLogin} colorScheme="purple" px={6}>
          Enter Dashboard
        </Button>
      </VStack>
    </Box>
  );
}