// components/program/CosmicProfileSetup.tsx
import { useState, useEffect } from 'react';
import {
  Box,
  Flex,
  Heading,
  Text,
  Button,
  VStack,
  HStack,
  Slider,
  SliderTrack,
  SliderFilledTrack,
  SliderThumb,
  Tabs,
  TabList,
  Tab,
  TabPanels,
  TabPanel,
  Badge,
  FormControl,
  FormLabel,
  Input,
  Select,
  Checkbox,
  Divider,
  Grid,
  GridItem,
  useColorModeValue,
  Tag,
  TagLabel,
  TagCloseButton,
  useToast
} from '@chakra-ui/react';
import { StarIcon, AddIcon, ChevronRightIcon } from '@chakra-ui/icons';
import { FaBrain, FaCode, FaUserGraduate, FaUsers } from 'react-icons/fa';

// Define types for our profile categories and skills
interface Skill {
  id: string;
  name: string;
  weight: number;
  required: boolean;
}

interface Category {
  id: string;
  name: string;
  icon: React.ReactElement;
  color: string;
  weight: number;
  skills: Skill[];
}

export default function CosmicProfileSetup() {
  const toast = useToast();
  const borderColor = useColorModeValue('gray.200', 'gray.600');
  const bgColor = useColorModeValue('white', 'gray.700');
  
  // Initial categories with their weights and skills
  const [categories, setCategories] = useState<Category[]>([
    {
      id: 'technical',
      name: 'Technical Skills',
      icon: <FaCode />,
      color: 'blue.500',
      weight: 40,
      skills: [
        { id: 't1', name: 'Python', weight: 90, required: true },
        { id: 't2', name: 'Data Science', weight: 85, required: true },
        { id: 't3', name: 'Machine Learning', weight: 80, required: false },
        { id: 't4', name: 'SQL', weight: 70, required: false },
        { id: 't5', name: 'Statistics', weight: 75, required: true }
      ]
    },
    {
      id: 'learning',
      name: 'Learning Style',
      icon: <FaBrain />,
      color: 'green.500',
      weight: 25,
      skills: [
        { id: 'l1', name: 'Self-directed', weight: 85, required: false },
        { id: 'l2', name: 'Project-based', weight: 90, required: true },
        { id: 'l3', name: 'Collaborative', weight: 70, required: false },
        { id: 'l4', name: 'Fast-paced', weight: 65, required: false }
      ]
    },
    {
      id: 'experience',
      name: 'Prior Experience',
      icon: <FaUserGraduate />,
      color: 'orange.500',
      weight: 20,
      skills: [
        { id: 'e1', name: 'Projects', weight: 80, required: true },
        { id: 'e2', name: 'Internships', weight: 70, required: false },
        { id: 'e3', name: 'Research', weight: 65, required: false },
        { id: 'e4', name: 'Open Source', weight: 75, required: false }
      ]
    },
    {
      id: 'soft',
      name: 'Soft Skills',
      icon: <FaUsers />,
      color: 'purple.500',
      weight: 15,
      skills: [
        { id: 's1', name: 'Communication', weight: 75, required: false },
        { id: 's2', name: 'Problem Solving', weight: 90, required: true },
        { id: 's3', name: 'Teamwork', weight: 70, required: false },
        { id: 's4', name: 'Time Management', weight: 65, required: false }
      ]
    }
  ]);
  
  // State for new skill form
  const [newSkillName, setNewSkillName] = useState('');
  const [newSkillWeight, setNewSkillWeight] = useState(75);
  const [newSkillRequired, setNewSkillRequired] = useState(false);
  const [selectedCategoryId, setSelectedCategoryId] = useState('technical');
  
  // AI-generated suggestions for skills
  const [aiSuggestions, setAiSuggestions] = useState([
    { id: 'ai1', name: 'Neural Networks', category: 'technical', confidence: 92 },
    { id: 'ai2', name: 'Data Visualization', category: 'technical', confidence: 88 },
    { id: 'ai3', name: 'Critical Thinking', category: 'soft', confidence: 85 },
    { id: 'ai4', name: 'Research Methodology', category: 'experience', confidence: 79 },
  ]);
  
  // Function to update category weights
  const updateCategoryWeight = (categoryId: string, newWeight: number) => {
    const updatedCategories = categories.map(category => 
      category.id === categoryId ? { ...category, weight: newWeight } : category
    );
    
    // Normalize weights to ensure they sum to 100
    const totalWeight = updatedCategories.reduce((sum, cat) => sum + cat.weight, 0);
    
    if (totalWeight !== 100) {
      const normalizationFactor = 100 / totalWeight;
      
      // Normalize all weights except the one being updated
      const normalizedCategories = updatedCategories.map(cat => {
        if (cat.id === categoryId) {
          return cat;
        }
        
        const remainingWeight = 100 - newWeight;
        const originalTotalMinusCurrent = totalWeight - updatedCategories.find(c => c.id === categoryId)!.weight;
        const normalizedWeight = (cat.weight / originalTotalMinusCurrent) * remainingWeight;
        
        return {
          ...cat,
          weight: Math.round(normalizedWeight)
        };
      });
      
      setCategories(normalizedCategories);
    } else {
      setCategories(updatedCategories);
    }
  };
  
  // Function to update skill weight
  const updateSkillWeight = (categoryId: string, skillId: string, newWeight: number) => {
    setCategories(categories.map(cat => {
      if (cat.id === categoryId) {
        return {
          ...cat,
          skills: cat.skills.map(skill => 
            skill.id === skillId ? { ...skill, weight: newWeight } : skill
          )
        };
      }
      return cat;
    }));
  };
  
  // Function to toggle skill required status
  const toggleSkillRequired = (categoryId: string, skillId: string) => {
    setCategories(categories.map(cat => {
      if (cat.id === categoryId) {
        return {
          ...cat,
          skills: cat.skills.map(skill => 
            skill.id === skillId ? { ...skill, required: !skill.required } : skill
          )
        };
      }
      return cat;
    }));
  };
  
  // Function to add a new skill
  const addNewSkill = () => {
    if (!newSkillName.trim()) {
      toast({
        title: "Skill name required",
        status: "error",
        duration: 3000,
        isClosable: true,
      });
      return;
    }
    
    const categoryToUpdate = categories.find(cat => cat.id === selectedCategoryId);
    
    if (!categoryToUpdate) return;
    
    const newSkill = {
      id: `new-${Date.now()}`,
      name: newSkillName,
      weight: newSkillWeight,
      required: newSkillRequired
    };
    
    setCategories(categories.map(cat => {
      if (cat.id === selectedCategoryId) {
        return {
          ...cat,
          skills: [...cat.skills, newSkill]
        };
      }
      return cat;
    }));
    
    // Reset form
    setNewSkillName('');
    setNewSkillWeight(75);
    setNewSkillRequired(false);
    
    toast({
      title: "Skill added",
      description: `${newSkillName} added to ${categoryToUpdate.name}`,
      status: "success",
      duration: 3000,
      isClosable: true,
    });
  };
  
  // Function to remove a skill
  const removeSkill = (categoryId: string, skillId: string) => {
    setCategories(categories.map(cat => {
      if (cat.id === categoryId) {
        return {
          ...cat,
          skills: cat.skills.filter(skill => skill.id !== skillId)
        };
      }
      return cat;
    }));
  };
  
  // Function to add an AI suggestion
  const addSuggestion = (suggestion) => {
    const categoryToUpdate = categories.find(cat => cat.id === suggestion.category);
    
    if (!categoryToUpdate) return;
    
    const newSkill = {
      id: `ai-${Date.now()}`,
      name: suggestion.name,
      weight: suggestion.confidence,
      required: false
    };
    
    setCategories(categories.map(cat => {
      if (cat.id === suggestion.category) {
        return {
          ...cat,
          skills: [...cat.skills, newSkill]
        };
      }
      return cat;
    }));
    
    // Remove suggestion from list
    setAiSuggestions(aiSuggestions.filter(s => s.id !== suggestion.id));
    
    toast({
      title: "AI suggestion added",
      description: `${suggestion.name} added to ${categoryToUpdate.name}`,
      status: "success",
      duration: 3000,
      isClosable: true,
    });
  };
  
  // Calculate match profile completeness
  const calculateCompleteness = () => {
    const totalExpectedSkills = 15; // Example: baseline expectation for a complete profile
    const totalSkills = categories.reduce((sum, cat) => sum + cat.skills.length, 0);
    const requiredSkills = categories.reduce((sum, cat) => 
      sum + cat.skills.filter(skill => skill.required).length, 0);
    
    const skillsScore = Math.min(100, (totalSkills / totalExpectedSkills) * 100);
    const requiredScore = requiredSkills > 0 ? 100 : 0;
    const categoryScore = categories.reduce((sum, cat) => sum + (cat.skills.length > 0 ? 25 : 0), 0);
    
    return Math.floor((skillsScore * 0.5) + (requiredScore * 0.3) + (categoryScore * 0.2));
  };
  
  const completeness = calculateCompleteness();
  
  return (
    <Box bg={bgColor} borderRadius="lg" boxShadow="md" overflow="hidden">
      <Box bg="blue.600" p={4} color="white">
        <Flex justify="space-between" align="center">
          <Heading size="md">Cosmic Profile Setup</Heading>
          <HStack>
            <Text fontSize="sm">Profile Completeness:</Text>
            <Badge 
              colorScheme={completeness > 80 ? "green" : completeness > 50 ? "yellow" : "red"}
              fontSize="sm"
              variant="solid"
            >
              {completeness}%
            </Badge>
          </HStack>
        </Flex>
      </Box>
      
      <Tabs colorScheme="blue" p={4}>
        <TabList>
          <Tab>Category Weights</Tab>
          <Tab>Skill Details</Tab>
          <Tab>AI Suggestions</Tab>
        </TabList>
        
        <TabPanels>
          {/* Category Weights Panel */}
          <TabPanel>
            <Text mb={4} fontSize="sm" color="gray.600">
              Adjust the relative importance of each category to fine-tune your matching algorithm.
            </Text>
            
            <VStack spacing={6} align="stretch">
              {categories.map(category => (
                <Box key={category.id} p={4} borderWidth="1px" borderRadius="md" borderColor={borderColor}>
                  <Flex justify="space-between" align="center" mb={3}>
                    <HStack>
                      <Box color={category.color}>{category.icon}</Box>
                      <Text fontWeight="medium">{category.name}</Text>
                    </HStack>
                    <Badge colorScheme="blue">{category.weight}%</Badge>
                  </Flex>
                  
                  <Slider 
                    aria-label={`${category.name} weight slider`}
                    defaultValue={category.weight}
                    min={5}
                    max={70}
                    onChange={(val) => updateCategoryWeight(category.id, val)}
                    colorScheme={category.color.split('.')[0]}
                  >
                    <SliderTrack>
                      <SliderFilledTrack />
                    </SliderTrack>
                    <SliderThumb boxSize={6}>
                      <Box color={category.color} as={StarIcon} />
                    </SliderThumb>
                  </Slider>
                  
                  <Text mt={1} fontSize="xs" color="gray.500">
                    {category.skills.length} skills defined
                  </Text>
                </Box>
              ))}
            </VStack>
            
            <HStack justify="center" mt={6}>
              <Button colorScheme="blue">Save Category Weights</Button>
            </HStack>
          </TabPanel>
          
          {/* Skill Details Panel */}
          <TabPanel>
            <Flex justify="space-between" align="start" mb={6}>
              <Box>
                <Heading size="sm" mb={2}>Define Required Skills</Heading>
                <Text fontSize="sm" color="gray.600">
                  Adjust weights and mark required skills to fine-tune candidate matching.
                </Text>
              </Box>
              
              <Box p={4} bg="blue.50" borderRadius="md" maxW="200px">
                <Text fontSize="xs" color="blue.700">
                  <StarIcon mr={1} color="blue.500" />
                  Higher weights will prioritize candidates with those skills in matching
                </Text>
              </Box>
            </Flex>
            
            <Grid templateColumns="250px 1fr" gap={6}>
              {/* Category selection */}
              <GridItem>
                <VStack align="stretch" spacing={2}>
                  {categories.map(category => (
                    <Button
                      key={category.id}
                      leftIcon={<Box as="span" color={category.color}>{category.icon}</Box>}
                      variant={selectedCategoryId === category.id ? "solid" : "outline"}
                      colorScheme={selectedCategoryId === category.id ? category.color.split('.')[0] : "gray"}
                      justifyContent="flex-start"
                      onClick={() => setSelectedCategoryId(category.id)}
                      size="sm"
                    >
                      {category.name}
                    </Button>
                  ))}
                </VStack>
                
                <Divider my={4} />
                
                <Box p={4} borderWidth="1px" borderRadius="md" borderColor={borderColor}>
                  <Heading size="xs" mb={3}>Add New Skill</Heading>
                  
                  <FormControl mb={3}>
                    <FormLabel fontSize="xs">Skill Name</FormLabel>
                    <Input 
                      placeholder="Enter skill name" 
                      size="sm"
                      value={newSkillName}
                      onChange={(e) => setNewSkillName(e.target.value)}
                    />
                  </FormControl>
                  
                  <FormControl mb={3}>
                    <FormLabel fontSize="xs">
                      Importance ({newSkillWeight}%)
                    </FormLabel>
                    <Slider
                      min={1}
                      max={100}
                      value={newSkillWeight}
                      onChange={(val) => setNewSkillWeight(val)}
                      colorScheme="blue"
                    >
                      <SliderTrack>
                        <SliderFilledTrack />
                      </SliderTrack>
                      <SliderThumb />
                    </Slider>
                  </FormControl>
                  
                  <Checkbox 
                    colorScheme="blue" 
                    mb={3}
                    isChecked={newSkillRequired}
                    onChange={(e) => setNewSkillRequired(e.target.checked)}
                  >
                    Required Skill
                  </Checkbox>
                  
                  <Button 
                    leftIcon={<AddIcon />} 
                    colorScheme="blue" 
                    size="sm" 
                    width="full"
                    onClick={addNewSkill}
                  >
                    Add Skill
                  </Button>
                </Box>
              </GridItem>
              
              {/* Skills for selected category */}
              <GridItem>
                {selectedCategoryId && (
                  <Box>
                    <Heading size="sm" mb={4}>
                      {categories.find(c => c.id === selectedCategoryId)?.name} Skills
                    </Heading>
                    
                    <VStack spacing={4} align="stretch">
                      {categories
                        .find(c => c.id === selectedCategoryId)
                        ?.skills.map(skill => (
                          <Flex 
                            key={skill.id} 
                            p={3} 
                            borderWidth="1px" 
                            borderRadius="md" 
                            borderColor={borderColor}
                            justify="space-between"
                            align="center"
                          >
                            <VStack align="start" spacing={0}>
                              <HStack>
                                <Text fontWeight="medium">{skill.name}</Text>
                                {skill.required && (
                                  <Badge colorScheme="red">Required</Badge>
                                )}
                              </HStack>
                              
                              <Text fontSize="xs" color="gray.500">
                                Importance: {skill.weight}%
                              </Text>
                            </VStack>
                            
                            <HStack spacing={4}>
                              <Slider
                                aria-label={`${skill.name} weight slider`}
                                value={skill.weight}
                                min={1}
                                max={100}
                                onChange={(val) => updateSkillWeight(selectedCategoryId, skill.id, val)}
                                colorScheme="blue"
                                width="150px"
                              >
                                <SliderTrack>
                                  <SliderFilledTrack />
                                </SliderTrack>
                                <SliderThumb />
                              </Slider>
                              
                              <Checkbox
                                isChecked={skill.required}
                                onChange={() => toggleSkillRequired(selectedCategoryId, skill.id)}
                                colorScheme="blue"
                                size="sm"
                              >
                                Required
                              </Checkbox>
                              
                              <Button
                                size="xs"
                                colorScheme="red"
                                variant="ghost"
                                onClick={() => removeSkill(selectedCategoryId, skill.id)}
                              >
                                Remove
                              </Button>
                            </HStack>
                          </Flex>
                        ))
                      }
                      
                      {categories.find(c => c.id === selectedCategoryId)?.skills.length === 0 && (
                        <Box p={6} textAlign="center" color="gray.500">
                          <Text>No skills defined for this category yet.</Text>
                          <Text fontSize="sm" mt={2}>Add skills to improve your matching algorithm.</Text>
                        </Box>
                      )}
                    </VStack>
                  </Box>
                )}
              </GridItem>
            </Grid>
            
            <HStack justify="center" mt={6}>
              <Button colorScheme="blue">Save Skill Configuration</Button>
            </HStack>
          </TabPanel>
          
          {/* AI Suggestions Panel */}
          <TabPanel>
            <Flex justify="space-between" align="center" mb={6}>
              <Box>
                <Heading size="sm" mb={2}>AI-Generated Skill Suggestions</Heading>
                <Text fontSize="sm" color="gray.600">
                  Based on your profile and industry trends, our AI suggests these additional skills.
                </Text>
              </Box>
              
              <Button 
                colorScheme="purple" 
                size="sm"
                leftIcon={<FaBrain />}
              >
                Generate New Suggestions
              </Button>
            </Flex>
            
            <Grid templateColumns="repeat(2, 1fr)" gap={4}>
              {aiSuggestions.map(suggestion => (
                <Box 
                  key={suggestion.id}
                  p={4}
                  borderWidth="1px"
                  borderRadius="md"
                  borderColor={borderColor}
                  bg="gray.50"
                >
                  <Flex justify="space-between" align="start">
                    <VStack align="start" spacing={1}>
                      <Text fontWeight="medium">{suggestion.name}</Text>
                      <HStack>
                        <Badge 
                          colorScheme={
                            suggestion.category === 'technical' ? 'blue' :
                            suggestion.category === 'learning' ? 'green' :
                            suggestion.category === 'experience' ? 'orange' : 'purple'
                          }
                        >
                          {suggestion.category}
                        </Badge>
                        <Text fontSize="xs" color="gray.500">
                          {suggestion.confidence}% confidence
                        </Text>
                      </HStack>
                    </VStack>
                    
                    <Button 
                      size="sm" 
                      colorScheme="blue"
                      onClick={() => addSuggestion(suggestion)}
                    >
                      Add
                    </Button>
                  </Flex>
                  
                  <Text fontSize="xs" color="gray.600" mt={2}>
                    This skill is trending in {suggestion.category === 'technical' ? 'tech job descriptions' : 'candidate profiles'} related to your program.
                  </Text>
                </Box>
              ))}
            </Grid>
            
            {aiSuggestions.length === 0 && (
              <Box p={8} textAlign="center" color="gray.500">
                <FaBrain size="24px" style={{ margin: '0 auto 16px' }} />
                <Text>You've added all our AI suggestions!</Text>
                <Button 
                  colorScheme="purple" 
                  size="sm" 
                  mt={4}
                  leftIcon={<FaBrain />}
                >
                  Generate New Suggestions
                </Button>
              </Box>
            )}
          </TabPanel>
        </TabPanels>
      </Tabs>
      
      <Flex justify="space-between" p={4} borderTopWidth="1px" borderColor={borderColor} bg="gray.50">
        <Button variant="outline">Cancel</Button>
        <HStack>
          <Button variant="outline" colorScheme="blue">Preview Matching</Button>
          <Button colorScheme="blue">Save Profile</Button>
        </HStack>
      </Flex>
    </Box>
  );
}