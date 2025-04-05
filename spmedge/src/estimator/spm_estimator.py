"""
SPM Project Estimator

This module analyzes SPM components from a communication plan and estimates
the required story points and hours based on complexity levels.
"""

import pandas as pd
import os
import re
from typing import Dict, List, Tuple, Optional, Union


class SPMEstimator:
    """
    Estimates story points and hours for SPM components based on complexity.
    """
    
    # Constants for complexity levels
    COMPLEXITY_LOW = "L"
    COMPLEXITY_MID = "M"
    COMPLEXITY_HIGH = "H"
    
    # Default complexity mapping based on analysis of SPM_ESTIMATOR.xlsx
    DEFAULT_COMPLEXITY_HOURS = {
        COMPLEXITY_LOW: 40,   # 40 hours per component for Low complexity
        COMPLEXITY_MID: 120,  # 120 hours per component for Medium complexity
        COMPLEXITY_HIGH: 240  # 240 hours per component for High complexity
    }
    
    # Story point conversion factor (from SPM_ESTIMATOR.xlsx)
    DEFAULT_HOURS_PER_SP = 15
    
    def __init__(
        self, 
        meta_framework_path: Optional[str] = None,
        db_connection = None,
        complexity_hours: Optional[Dict[str, int]] = None,
        hours_per_sp: Optional[int] = None
    ):
        """
        Initialize the SPM estimator.
        
        Args:
            meta_framework_path: Path to the SPM META FRAMEWORK Excel file
            db_connection: Database connection to load framework from
            complexity_hours: Custom complexity to hours mapping
            hours_per_sp: Custom hours per story point conversion
        """
        self.meta_framework = None
        
        # Load from database if connection provided
        if db_connection:
            self.load_meta_framework_from_db(db_connection)
        # Otherwise try to load from file
        elif meta_framework_path and os.path.exists(meta_framework_path):
            self.load_meta_framework(meta_framework_path)
        
        # Use custom complexity hours mapping or default
        self.complexity_hours = complexity_hours or self.DEFAULT_COMPLEXITY_HOURS
        
        # Use custom hours per SP or default
        self.hours_per_sp = hours_per_sp or self.DEFAULT_HOURS_PER_SP
        
        # Initialize component tracking
        self.component_counts = {
            'Configuration': {},
            'Data Integration': {},
            'Reporting': {},
            'Workflow': {},
            'Change Management': {},
            'Release Management': {},
            'Vendor Support': {}
        }
        
        # Initialize complexity assignments
        self.component_complexity = {}
        
        # Initialize known complexity mappings from META_FRAMEWORK
        self.known_complexities = {}
        
    def load_meta_framework(self, file_path: str) -> None:
        """
        Load the SPM META FRAMEWORK from Excel file.
        
        Args:
            file_path: Path to the META FRAMEWORK Excel file
        """
        try:
            self.meta_framework = pd.read_excel(file_path, sheet_name='Sheet1')
            print(f"Loaded {len(self.meta_framework)} components from META FRAMEWORK Excel")
            
            # Build a dictionary of components for quick lookup
            self.component_lookup = {}
            for _, row in self.meta_framework.iterrows():
                component = row.get('SPM_COMPONENT', '')
                if component and isinstance(component, str):
                    # Clean up component name
                    clean_component = component.strip()
                    self.component_lookup[clean_component] = row.to_dict()
            
            # Try to infer complexity from META_FRAMEWORK by looking for keywords
            self._infer_component_complexity()
            
        except Exception as e:
            print(f"Error loading META FRAMEWORK from Excel: {e}")
            self.meta_framework = None
    
    def load_meta_framework_from_db(self, db_connection) -> None:
        """
        Load the SPM META FRAMEWORK from the database.
        
        Args:
            db_connection: Database connection
        """
        try:
            cursor = db_connection.cursor()
            
            # Query the spm_framework table with correct column names
            cursor.execute(
                """
                SELECT 
                    version, 
                    spm_process, 
                    spm_category, 
                    spm_component, 
                    spm_keyword, 
                    spm_definition,
                    spm_user_type,
                    spm_prompt,
                    spm_complexity_level,
                    spm_analysis_00,
                    spm_analysis_01,
                    spm_analysis_02,
                    spm_analysis_03,
                    spm_contextual_example,
                    spm_traceability_code
                FROM 
                    spm_framework
                ORDER BY
                    version
                """
            )
            
            results = cursor.fetchall()
            cursor.close()
            
            # Convert to a format similar to what we'd get from Excel
            data = []
            for row in results:
                data.append({
                    'SPM_ID': row[0],  # Maps 'version' to 'SPM_ID' for backward compatibility
                    'SPM_PROCESS': row[1],
                    'SPM_CATEGORY': row[2],
                    'SPM_COMPONENT': row[3],
                    'SPM_KEYWORD': row[4],
                    'SPM_DEFINTION': row[5],  # Keep the misspelling to match Excel
                    'SPM_USER_TYPE': row[6],
                    'SPM_PROMPT': row[7],
                    'SPM_COMPLEXITY_LEVEL': row[8],
                    'SPM_ANALYSIS_00': row[9],
                    'SPM_ANALYSIS_01': row[10],
                    'SPM_ANALYSIS_02': row[11],
                    'SPM_ANALYSIS_03': row[12],
                    'SPM_CONTEXTUAL_EXAMPLE': row[13],
                    'SPM_TRACEABILITY_CODE': row[14]
                })
            
            # Create a pandas DataFrame
            self.meta_framework = pd.DataFrame(data)
            print(f"Loaded {len(self.meta_framework)} components from database")
            
            # Build a dictionary of components for quick lookup
            self.component_lookup = {}
            for _, row in self.meta_framework.iterrows():
                component = row.get('SPM_COMPONENT', '')
                if component and isinstance(component, str):
                    # Clean up component name
                    clean_component = component.strip()
                    self.component_lookup[clean_component] = row.to_dict()
            
            # Try to infer complexity from META_FRAMEWORK by looking for keywords
            self._infer_component_complexity()
            
        except Exception as e:
            print(f"Error loading META FRAMEWORK from database: {e}")
            self.meta_framework = None
    
    def _infer_component_complexity(self) -> None:
        """
        Infer component complexity from META_FRAMEWORK by analyzing definition text.
        """
        if self.meta_framework is None:
            return
        
        # Keywords that might indicate complexity
        high_complexity_keywords = ['complex', 'challenging', 'difficult', 'sophisticated', 'advanced']
        low_complexity_keywords = ['simple', 'easy', 'basic', 'straightforward']
        
        for _, row in self.meta_framework.iterrows():
            component = row.get('SPM_COMPONENT', '')
            definition = row.get('SPM_DEFINTION', '')
            keyword = row.get('SPM_KEYWORD', '')
            
            if not component or not isinstance(component, str):
                continue
                
            component = component.strip()
            complexity = None
            
            # Check for explicit complexity indicators
            if isinstance(keyword, str) and 'complex' in keyword.lower():
                complexity = self.COMPLEXITY_HIGH
            elif isinstance(definition, str):
                # Check for high complexity indicators
                if any(kw in definition.lower() for kw in high_complexity_keywords):
                    complexity = self.COMPLEXITY_HIGH
                # Check for low complexity indicators
                elif any(kw in definition.lower() for kw in low_complexity_keywords):
                    complexity = self.COMPLEXITY_LOW
            
            if complexity:
                self.known_complexities[component] = complexity
    
    def analyze_comm_plan(self, components_data: Dict[str, List[str]]) -> None:
        """
        Analyze components from communication plan and categorize them.
        
        Args:
            components_data: Dictionary of components by category from comm plan
        """
        # Reset component counts
        for category in self.component_counts:
            self.component_counts[category] = {}
        
        # Process each component by category
        for category, components in components_data.items():
            # Map the comm plan category to estimator category
            estimator_category = self._map_category_to_estimator(category)
            
            if estimator_category:
                for component in components:
                    # Clean component name
                    clean_component = component.strip()
                    
                    # Increment count for this component
                    if clean_component in self.component_counts[estimator_category]:
                        self.component_counts[estimator_category][clean_component] += 1
                    else:
                        self.component_counts[estimator_category][clean_component] = 1
                        
                    # If we haven't assigned complexity yet, set to None
                    if clean_component not in self.component_complexity:
                        # Try to use known complexity from META_FRAMEWORK
                        if clean_component in self.known_complexities:
                            self.component_complexity[clean_component] = self.known_complexities[clean_component]
                        else:
                            self.component_complexity[clean_component] = None
    
    def _map_category_to_estimator(self, comm_plan_category: str) -> Optional[str]:
        """
        Map communication plan category to estimator category.
        
        Args:
            comm_plan_category: Category from communication plan
            
        Returns:
            Mapped estimator category or None if no match
        """
        category_mapping = {
            # Configuration mappings
            'Sales Planning': 'Configuration',
            'Sales Hierarchies': 'Configuration',
            'Sales Role': 'Configuration',
            'Sales Plan': 'Configuration',
            'Territory': 'Configuration',
            'Quota': 'Configuration',
            'Data Classification': 'Configuration',
            
            # Incentive Compensation mappings
            'Incentive Compensation': 'Configuration',
            'Sales Crediting': 'Configuration',
            'Performance Measurements': 'Configuration',
            'Measurement Attainments': 'Configuration',
            'Incentives': 'Configuration',
            'Compensation': 'Configuration',
            'Earnings': 'Configuration',
            'Payments': 'Configuration',
            
            # Data Integration mappings
            'Data Integration': 'Data Integration',
            'Import': 'Data Integration',
            'Export': 'Data Integration',
            'ETL': 'Data Integration',
            'API': 'Data Integration',
            'File': 'Data Integration',
            
            # Reporting mappings
            'Reports': 'Reporting',
            'Reporting': 'Reporting',
            'Analytics': 'Reporting',
            'Dashboard': 'Reporting',
            'Visualizations': 'Reporting',
            'Sales Intelligence': 'Reporting',
            'Sales Insights': 'Reporting',
            
            # Workflow mappings
            'Workflow': 'Workflow',
            'Process': 'Workflow',
            'Approval': 'Workflow',
            'State Transition': 'Workflow',
            
            # Change Management mappings
            'Change Management': 'Change Management',
            'Training': 'Change Management',
            'Communication': 'Change Management',
            'Adoption': 'Change Management',
            
            # Release Management mappings
            'Release': 'Release Management',
            'Deployment': 'Release Management',
            'Migration': 'Release Management',
            
            # Vendor Support mappings
            'Vendor': 'Vendor Support',
            'Support': 'Vendor Support',
            'SSO': 'Vendor Support',
            'Performance': 'Vendor Support',
            'Testing': 'Vendor Support'
        }
        
        # Look for exact match first
        for key, value in category_mapping.items():
            if key.lower() == comm_plan_category.lower():
                return value
        
        # If no exact match, try partial match
        for key, value in category_mapping.items():
            if key.lower() in comm_plan_category.lower() or comm_plan_category.lower() in key.lower():
                return value
        
        # Default to Configuration if no match is found
        return 'Configuration'
    
    def estimate_component_complexity(self, component: str, category: str) -> str:
        """
        Estimate complexity for a component if not already assigned.
        
        Args:
            component: The component name
            category: The component's category
            
        Returns:
            Complexity level (L, M, or H)
        """
        # If complexity is already assigned, return it
        if component in self.component_complexity and self.component_complexity[component]:
            return self.component_complexity[component]
        
        # Look up in META_FRAMEWORK if available
        if self.meta_framework is not None and component in self.component_lookup:
            meta_data = self.component_lookup[component]
            
            # Check for complexity indicators in the definition
            definition = meta_data.get('SPM_DEFINTION', '')
            
            # Define complexity indicator keywords
            high_keywords = ['complex', 'advanced', 'sophisticated', 'comprehensive', 'multiple']
            medium_keywords = ['moderate', 'standard', 'normal', 'typical']
            low_keywords = ['simple', 'basic', 'straightforward', 'single', 'minimal']
            
            # Count keyword occurrences
            high_count = sum(1 for kw in high_keywords if kw in str(definition).lower())
            medium_count = sum(1 for kw in medium_keywords if kw in str(definition).lower())
            low_count = sum(1 for kw in low_keywords if kw in str(definition).lower())
            
            # Determine complexity based on keyword counts
            if high_count > low_count and high_count > medium_count:
                return self.COMPLEXITY_HIGH
            elif low_count > high_count and low_count > medium_count:
                return self.COMPLEXITY_LOW
            elif medium_count > 0:
                return self.COMPLEXITY_MID
        
        # Default complexity mapping based on category
        category_complexity = {
            'Configuration': self.COMPLEXITY_MID,
            'Data Integration': self.COMPLEXITY_MID,
            'Reporting': self.COMPLEXITY_HIGH,
            'Workflow': self.COMPLEXITY_HIGH,
            'Change Management': self.COMPLEXITY_MID,
            'Release Management': self.COMPLEXITY_HIGH,
            'Vendor Support': self.COMPLEXITY_MID
        }
        
        # Special case handling based on component name
        if any(term in component.lower() for term in ['complex', 'advanced', 'multiple']):
            return self.COMPLEXITY_HIGH
        elif any(term in component.lower() for term in ['simple', 'basic']):
            return self.COMPLEXITY_LOW
        
        # Use category-based default
        return category_complexity.get(category, self.COMPLEXITY_MID)
    
    def calculate_story_points(self, component: str, count: int, complexity: str) -> float:
        """
        Calculate story points for a component based on count and complexity.
        
        Args:
            component: The component name
            count: The number of instances of this component
            complexity: The complexity level (L, M, or H)
            
        Returns:
            Story points value
        """
        # Get hours based on complexity
        hours_per_component = self.complexity_hours.get(complexity, 
                                                     self.complexity_hours[self.COMPLEXITY_MID])
        
        # Calculate total hours
        total_hours = count * hours_per_component
        
        # Convert to story points
        story_points = total_hours / self.hours_per_sp
        
        return story_points
    
    def set_component_complexity(self, component: str, complexity: str) -> None:
        """
        Set complexity for a specific component.
        
        Args:
            component: The component name
            complexity: The complexity level (L, M, or H)
        """
        if complexity not in [self.COMPLEXITY_LOW, self.COMPLEXITY_MID, self.COMPLEXITY_HIGH]:
            raise ValueError(f"Invalid complexity level: {complexity}")
        
        self.component_complexity[component] = complexity
    
    def get_component_details(self) -> List[Dict]:
        """
        Get detailed information about all components.
        
        Returns:
            List of component details including category, count, complexity, etc.
        """
        details = []
        
        for category, components in self.component_counts.items():
            for component, count in components.items():
                # Get or estimate complexity
                complexity = (self.component_complexity.get(component) or 
                             self.estimate_component_complexity(component, category))
                
                # Update component complexity for future use
                if not self.component_complexity.get(component):
                    self.component_complexity[component] = complexity
                
                # Calculate story points
                story_points = self.calculate_story_points(component, count, complexity)
                
                # Calculate hours
                hours = story_points * self.hours_per_sp
                
                details.append({
                    'category': category,
                    'component': component,
                    'count': count,
                    'complexity': complexity,
                    'story_points': story_points,
                    'hours': hours
                })
        
        return details
    
    def get_total_estimates(self) -> Dict[str, Dict[str, float]]:
        """
        Get total estimates by category.
        
        Returns:
            Dictionary with totals by category for story points and hours
        """
        totals = {
            'total': {'story_points': 0, 'hours': 0},
        }
        
        # Initialize category totals
        for category in self.component_counts.keys():
            totals[category] = {'story_points': 0, 'hours': 0}
        
        # Get component details
        component_details = self.get_component_details()
        
        # Sum up totals by category
        for detail in component_details:
            category = detail['category']
            story_points = detail['story_points']
            hours = detail['hours']
            
            totals[category]['story_points'] += story_points
            totals[category]['hours'] += hours
            
            totals['total']['story_points'] += story_points
            totals['total']['hours'] += hours
        
        return totals
    
    def generate_estimator_excel(self, output_path: str) -> bool:
        """
        Generate an Excel file similar to the SPM_ESTIMATOR.xlsx format.
        
        Args:
            output_path: Path to save the Excel file
        
        Returns:
            True if successful, False otherwise
        """
        try:
            # Create a Pandas Excel writer
            writer = pd.ExcelWriter(output_path, engine='xlsxwriter')
            
            # Create Delivery Estimates sheet
            self._create_delivery_estimates_sheet(writer)
            
            # Create component category sheets
            component_details = self.get_component_details()
            category_groups = {}
            
            # Group components by category
            for detail in component_details:
                category = detail['category']
                if category not in category_groups:
                    category_groups[category] = []
                category_groups[category].append(detail)
            
            # Create each category sheet
            for category, details in category_groups.items():
                self._create_category_sheet(writer, category, details)
            
            # Create Modifiers sheet
            self._create_modifiers_sheet(writer)
            
            # Save the Excel file
            writer.close()
            
            print(f"Estimator Excel file created at: {output_path}")
            return True
        except Exception as e:
            print(f"Error generating Excel file: {e}")
            return False
    
    def _create_delivery_estimates_sheet(self, writer: pd.ExcelWriter) -> None:
        """
        Create the Delivery Estimates sheet in the Excel workbook.
        
        Args:
            writer: Pandas ExcelWriter object
        """
        # Get total estimates
        totals = self.get_total_estimates()
        
        # Create data for Delivery Estimates sheet
        data = [
            ['', 'Account:'],
            ['', 'Account ID:'],
            ['', 'Opportunity ID:'],
            ['', 'Partner Sponsor:'],
            ['', 'Delivery Lead:'],
            [''],
            ['', 'ICM Implementation Project', '', 'Story Points', 'Hours', 'G&O', 'Contingency', 'Total', '% of Total'],
            ['', '', '', '', '', 0.1, 0.2],
        ]
        
        # Add category rows
        categories = [cat for cat in totals.keys() if cat != 'total']
        for category in categories:
            category_totals = totals[category]
            sp = category_totals['story_points']
            hrs = category_totals['hours']
            
            # Calculate G&O and Contingency
            go = sp * 0.1
            contingency = sp * 0.2
            total = sp + go + contingency
            
            data.append(['', category, '', sp, hrs, go, contingency, total])
        
        # Add total row
        total_sp = totals['total']['story_points']
        total_hrs = totals['total']['hours']
        total_go = total_sp * 0.1
        total_contingency = total_sp * 0.2
        grand_total = total_sp + total_go + total_contingency
        
        data.append(['', 'Total:', '', total_sp, total_hrs, total_go, total_contingency, grand_total])
        
        # Create DataFrame
        df = pd.DataFrame(data)
        
        # Write to Excel
        df.to_excel(writer, sheet_name='Delivery Estimates', index=False, header=False)
        
        # Format the sheet
        workbook = writer.book
        worksheet = writer.sheets['Delivery Estimates']
        
        # Add formats
        header_format = workbook.add_format({'bold': True, 'bg_color': '#D9D9D9', 'border': 1})
        number_format = workbook.add_format({'num_format': '#,##0.0'})
        
        # Apply formats
        worksheet.set_column('A:A', 5)
        worksheet.set_column('B:C', 20)
        worksheet.set_column('D:H', 12, number_format)
    
    def _create_category_sheet(self, writer: pd.ExcelWriter, category: str, details: List[Dict]) -> None:
        """
        Create a sheet for a specific category.
        
        Args:
            writer: Pandas ExcelWriter object
            category: Category name
            details: List of component details for this category
        """
        # Create header row
        if category == 'Configuration':
            headers = ['#', 'Description', 'New v Mod', 'Component Count', 'H/M/L', 'SP', 'Hrs']
        else:
            headers = ['#', 'Description', 'New v Mod', 'Count', 'H/M/L', 'SP', 'Hrs']
        
        # Create data rows
        data = [headers]
        
        for i, detail in enumerate(details, 1):
            row = [
                i,
                detail['component'],
                'N',  # Assuming all are new
                detail['count'],
                detail['complexity'],
                detail['story_points'],
                detail['hours']
            ]
            data.append(row)
        
        # Add totals row
        total_count = sum(detail['count'] for detail in details)
        total_sp = sum(detail['story_points'] for detail in details)
        total_hours = sum(detail['hours'] for detail in details)
        
        # Add empty rows to match the totals row index
        while len(data) < 16:
            data.append([None] * len(headers))
        
        # Add totals row
        if category == 'Configuration':
            data.append(['', '', '', total_count, '', total_sp, total_hours])
        else:
            data.append(['', '', '', total_count, '', total_sp, total_hours])
        
        # Create DataFrame
        df = pd.DataFrame(data)
        
        # Write to Excel
        df.to_excel(writer, sheet_name=category, index=False, header=False)
        
        # Format the sheet
        workbook = writer.book
        worksheet = writer.sheets[category]
        
        # Add formats
        header_format = workbook.add_format({'bold': True, 'bg_color': '#D9D9D9', 'border': 1})
        number_format = workbook.add_format({'num_format': '#,##0.0'})
        
        # Apply formats
        worksheet.set_column('A:A', 5)
        worksheet.set_column('B:B', 30)
        worksheet.set_column('C:C', 10)
        worksheet.set_column('D:G', 12, number_format)
    
    def _create_modifiers_sheet(self, writer: pd.ExcelWriter) -> None:
        """
        Create the Modifiers sheet in the Excel workbook.
        
        Args:
            writer: Pandas ExcelWriter object
        """
        # Create data for Modifiers sheet
        data = [
            [''],
            [''],
            [''],
            [''],
            [''],
            [''],
            ['Delivery Framework %', '', '', '', 'Story Point Hours'],
            ['Implementation', 'Phase', '%', 'Hr/task', self.hours_per_sp],
            ['', 'Plan', 0.05, 0.5],
            ['', 'Analysis', 0.1, 2],
            ['', 'Build', 0.45, 8],
            ['', 'Test', 0.35, 4],
            ['', 'Deploy', 0.05, 0.5],
            ['', '', 1],
            [''],
            ['', 'Configuration Modifiers'],
            ['', 'Plan', 'Analyze', 'Build', 'Test', 'Deploy', 'Hours', 'Analyze', 'Build', 'Test', 'Deploy'],
            ['Low', 2, 4, 18, 14, 2, self.complexity_hours[self.COMPLEXITY_LOW], 8, 144, 56, 1],
            ['Mid', 6, 12, 54, 42, 6, self.complexity_hours[self.COMPLEXITY_MID], 3],
            ['High', 12, 24, 108, 84, 12, self.complexity_hours[self.COMPLEXITY_HIGH]]
        ]
        
        # Create DataFrame
        df = pd.DataFrame(data)
        
        # Write to Excel
        df.to_excel(writer, sheet_name='Modifiers', index=False, header=False)
        
        # Format the sheet
        workbook = writer.book
        worksheet = writer.sheets['Modifiers']
        
        # Add formats
        header_format = workbook.add_format({'bold': True, 'bg_color': '#D9D9D9', 'border': 1})
        
        # Apply formats
        worksheet.set_column('A:A', 15)
        worksheet.set_column('B:G', 10)