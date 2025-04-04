// components/program/dashboard/FilterBar.tsx
import React from 'react';
import {
  Flex,
  Select,
  Input,
  Button,
  useColorModeValue
} from '@chakra-ui/react';

interface FilterBarProps {
  onFilterApply?: () => void;
  onFilterClear?: () => void;
}

const FilterBar: React.FC<FilterBarProps> = ({
  onFilterApply = () => {},
  onFilterClear = () => {}
}) => {
  const borderColor = useColorModeValue('gray.200', 'gray.600');

  return (
    <Flex 
      p={4} 
      bg="white" 
      borderBottomWidth="1px" 
      borderColor={borderColor}
      align="center"
      gap={4}
    >
      <Select placeholder="All Programs" width="auto" size="sm">
        <option value="cs">Computer Science</option>
        <option value="is">Information Systems</option>
        <option value="ds">Data Science</option>
      </Select>
      
      <Select placeholder="All Statuses" width="auto" size="sm">
        <option value="high">High Intent</option>
        <option value="medium">Medium Intent</option>
        <option value="low">Low Intent</option>
      </Select>
      
      <Input placeholder="Search candidates..." size="sm" maxWidth="300px" />
      
      <Button size="sm" variant="outline" colorScheme="gray" onClick={onFilterClear}>Clear</Button>
      <Button size="sm" colorScheme="blue" onClick={onFilterApply}>Apply Filters</Button>
    </Flex>
  );
};

export default FilterBar;