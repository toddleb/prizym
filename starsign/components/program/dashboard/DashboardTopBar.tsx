// components/program/dashboard/DashboardTopBar.tsx
import React from 'react';
import {
  Flex,
  HStack,
  Image,
  Heading,
  InputGroup,
  Input,
  InputRightElement,
  IconButton,
  Button,
  Menu,
  MenuButton,
  MenuList,
  MenuItem,
  useColorModeValue
} from '@chakra-ui/react';
import { 
  SettingsIcon, 
  SearchIcon,
  ChatIcon,
  ChevronDownIcon,
  AddIcon,
  EditIcon,
  StarIcon
} from '@chakra-ui/icons';
import { FaBrain } from 'react-icons/fa';

// Define prop interface
interface DashboardTopBarProps {
  programData: {
    name: string;
    logo: string;
  };
  isAiChatVisible: boolean;
  setIsAiChatVisible: (visible: boolean) => void;
}

const DashboardTopBar: React.FC<DashboardTopBarProps> = ({
  programData,
  isAiChatVisible,
  setIsAiChatVisible
}) => {
  const borderColor = useColorModeValue('gray.200', 'gray.600');

  return (
    <Flex 
      as="header" 
      align="center" 
      justify="space-between" 
      py={4} 
      px={6} 
      bg="white" 
      borderBottomWidth="1px" 
      borderColor={borderColor}
      boxShadow="sm"
    >
      <HStack spacing={4}>
        <Image 
          src={programData.logo} 
          alt={programData.name} 
          height="40px" 
          fallbackSrc="https://via.placeholder.com/80x40?text=Logo"
        />
        <Heading size="md">{programData.name}</Heading>
      </HStack>
      
      <HStack spacing={4}>
        <InputGroup size="sm" width="300px" display={{ base: 'none', md: 'inline-flex' }}>
          <Input placeholder="Search candidates, programs, or schools..." />
          <InputRightElement>
            <SearchIcon color="gray.500" />
          </InputRightElement>
        </InputGroup>
        
        <IconButton
          aria-label="AI Chat Assistant"
          icon={<ChatIcon />}
          variant="outline"
          colorScheme="blue"
          size="sm"
          onClick={() => setIsAiChatVisible(!isAiChatVisible)}
        />
        
        <IconButton
          aria-label="AI Insights"
          icon={<FaBrain />}
          variant="outline"
          colorScheme="purple"
          size="sm"
          onClick={() => {
            // Find and click the AI tab
            const aiTab = document.querySelector('.chakra-tabs__tablist button:nth-child(2)');
            if (aiTab) (aiTab as HTMLElement).click();
          }}
        />
        
        <Menu>
          <MenuButton 
            as={Button} 
            rightIcon={<ChevronDownIcon />} 
            size="sm"
            colorScheme="blue"
          >
            Actions
          </MenuButton>
          <MenuList>
            <MenuItem icon={<AddIcon />}>Add New Program</MenuItem>
            <MenuItem icon={<EditIcon />}>Edit Institution</MenuItem>
            <MenuItem icon={<StarIcon />}>Edit Cosmic Signature</MenuItem>
          </MenuList>
        </Menu>
        
        <IconButton 
          aria-label="Settings" 
          icon={<SettingsIcon />} 
          variant="ghost" 
          size="sm" 
        />
      </HStack>
    </Flex>
  );
};

export default DashboardTopBar;