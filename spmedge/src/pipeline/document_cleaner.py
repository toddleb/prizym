#!/usr/bin/env python3
"""
Enhanced Document Cleaner - Third stage of the SPM Edge processing pipeline.
- Intelligently identifies document sections and structures
- Applies context-aware cleaning based on section type 
- Preserves critical content like compensation tables and formulas
- Maintains document coherence while removing noise
- Supports dynamic rule management with database-driven patterns
- Maps document content to SPM Framework components
- Identifies and extracts structured compensation information
"""

import os
import sys
import json
import logging
import argparse
import re
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Optional, Tuple, Union

# Fix import path for absolute imports
sys.path.insert(0, '/Users/toddlebaron/prizym/spmedge')

# Import pipeline components
from config.config import config
from src.pipeline.db_integration import DBManager
from src.pipeline.pipeline_processor import PipelineProcessor, PipelineStage

# Ensure logs directory exists
LOG_DIR = config.LOG_DIR
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "document_cleaner.log")

# Configure module logger
logger = logging.getLogger("document_cleaner")
logger.propagate = False  # Prevent propagation to parent loggers

if not logger.handlers:
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler
    file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

# Initialize pipeline components
processor = PipelineProcessor(PipelineStage.CLEAN)
db_manager = DBManager()

# Add this near the top
def debug_documents():
    try:
        docs = processor.get_documents_for_stage(current_stage="load", status="completed")
        print(f"DEBUG: Found {len(docs)} documents for cleaning")
        for doc in docs:
            print(f"DEBUG: Document ID: {doc['id']}")
    except Exception as e:
        print(f"DEBUG: Error in debug: {e}")

# Call it
debug_documents()

def fetch_document_schema(document_type: str) -> Dict[str, Any]:
    """Fetch the schema definition for a document type.
    
    Args:
        document_type: Document type (e.g., 'comp_plan')
        
    Returns:
        Dictionary representing the schema
    """
    try:
        db_manager.cursor.execute("""
            SELECT schema_definition
            FROM document_schema
            WHERE document_type = %s;
        """, (document_type,))
        
        result = db_manager.cursor.fetchone()
        if result and result[0]:
            # Check if the result is already a dictionary
            if isinstance(result[0], dict):
                return result[0]
            # If it's a string, parse it as JSON
            elif isinstance(result[0], str):
                return json.loads(result[0])
            else:
                logger.warning(f"⚠️ Unexpected schema type for document type: {document_type}")
                return {}
        else:
            logger.warning(f"⚠️ No schema found for document type: {document_type}")
            return {}
            
    except Exception as e:
        logger.error(f"❌ Error fetching document schema: {e}")
        return {}


def fetch_ai_prompt(document_type: str) -> str:
    """Fetch the AI analysis prompt for a document type.
    
    Args:
        document_type: Document type (e.g., 'comp_plan')
        
    Returns:
        String containing the AI prompt for analysis
    """
    try:
        db_manager.cursor.execute("""
            SELECT ai_prompt
            FROM document_types
            WHERE name = %s;
        """, (document_type,))
        
        result = db_manager.cursor.fetchone()
        if result and result[0]:
            return result[0]
        else:
            logger.warning(f"⚠️ No AI prompt found for document type: {document_type}")
            return ""
            
    except Exception as e:
        logger.error(f"❌ Error fetching AI prompt: {e}")
        return ""


def fetch_cleaning_patterns(document_type: str = None) -> List[Dict[str, Any]]:
    """Fetch active cleaning patterns from the database.
    
    Args:
        document_type: Optional document type to filter rules
        
    Returns:
        List of cleaning rule dictionaries
    """
    try:
        # Get all active cleaning patterns
        # Note: We're not using document type filtering for now since the join table doesn't exist
        db_manager.cursor.execute("""
            SELECT pattern, replacement, pattern_type, description, 
                   sort_order as priority, 'all' as context
            FROM cleaning_patterns 
            WHERE active = true 
            ORDER BY sort_order ASC;
        """)
        
        patterns = db_manager.cursor.fetchall()
        
        # Check if we got any patterns
        if patterns:
            return [
                {
                    "pattern": row[0],
                    "replacement": row[1] or '',
                    "pattern_type": row[2],
                    "description": row[3],
                    "priority": row[4] or 5,
                    "context": row[5] or 'all'
                } 
                for row in patterns
            ]
        else:
            logger.warning(f"⚠️ No cleaning patterns found in database")
    
    except Exception as e:
        logger.error(f"❌ Error fetching cleaning patterns: {e}")
    
    # Return a minimal set of default cleaning patterns if DB fetch fails
    return [
        {
            "pattern": r"\s{2,}",
            "replacement": " ",
            "pattern_type": "regex",
            "description": "Normalize whitespace",
            "priority": 10,
            "context": "all"
        },
        {
            "pattern": r"(Confidential|MDT Confidential|Medtronic Confidential)",
            "replacement": "",
            "pattern_type": "regex",
            "description": "Remove confidentiality markers",
            "priority": 1,
            "context": "all"
        },
        {
            "pattern": r"^\s*\d+\s*$",
            "replacement": "",
            "pattern_type": "regex",
            "description": "Remove standalone page numbers",
            "priority": 2,
            "context": "all"
        },
        {
            "pattern": r"(Page\s*\d+\s*of\s*\d+)",
            "replacement": "",
            "pattern_type": "regex",
            "description": "Remove page numbers",
            "priority": 2,
            "context": "all"
        }
    ]


def identify_document_sections(content: str) -> List[Dict[str, Any]]:
    """Identify document structural elements and return as sections.
    
    Args:
        content: Document content string
        
    Returns:
        List of section dictionaries with text, type, and position information
    """
    sections = []
    
    # Identify headers (level 1-3)
    header_patterns = [
        r'^(#{1,3})\s+(.+)$',  # Markdown-style
        r'^([A-Z][^a-z\n]{3,})$',  # All caps line (min 5 chars)
        r'^(\d+\.)\s+(.+)$',  # Numbered headers
        r'^(Plan\s+Overview|Plan\s+Measures|Plan\s+Summary|Payouts|Terms\s+&?\s+Conditions)',  # Known section names
        r'^([IVX]{1,5}\.)\s+(.+)$',  # Roman numeral headers
        r'^([A-Z]\.)\s+(.+)$',  # Letter headers
    ]
    
    # Table detection patterns
    table_patterns = [
        r'[|+][-+]+[|+]',  # ASCII table borders
        r'^\s*\|.+\|\s*$',  # Markdown table row
        r'^[^|]+\|[^|]+\|[^|]+',  # Simple pipe-delimited data
        r'^\s*[-]+[-\s]+[-]+\s*$',  # Table separator line
    ]
    
    # Formula and compensation patterns 
    formula_patterns = [
        r'[%$][\d,.]+\s+(?:per|for)',  # Dollar or percent amounts with "per" or "for"
        r'[\d,.]+[%$]\s+(?:of|per)',   # Dollar or percent with "of" or "per"
        r'Attainment.*?[%$]',           # Attainment with percentage or dollar
        r'Quota.*?Attainment',          # Quota attainment lines
        r'Target.*?Incentive',          # Target incentive lines
    ]
    
    # SPM specific section detection
    spm_section_patterns = {
        "plan_info": [
            r'(Plan\s+Information|Plan\s+Details|Program\s+Information)',
            r'(Role|Position):\s*([A-Za-z\s]+)',
            r'(Region|Territory):\s*([A-Za-z\s]+)',
            r'(Plan\s+Year|Fiscal\s+Year):\s*(\d{4})'
        ],
        "plan_summary": [
            r'(Plan\s+Summary|Executive\s+Summary|Overview)',
            r'(Purpose|Objective)(\s+of\s+the\s+Plan)?:',
        ],
        "effective_dates": [
            r'(Effective\s+Date|Plan\s+Period|Performance\s+Period)',
            r'(Start\s+Date|Begin\s+Date):\s*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|\w+\s+\d{1,2},?\s+\d{4})',
            r'(End\s+Date|Termination\s+Date):\s*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|\w+\s+\d{1,2},?\s+\d{4})'
        ],
        "payout_schedule": [
            r'(Payout\s+Schedule|Payment\s+Schedule|Payout\s+Timing)',
            r'(Monthly|Quarterly|Annual)\s+Payments',
            r'(Payout|Payment)\s+(Calculation|Formula)'
        ],
        "special_provisions": [
            r'(Special\s+Provisions|Exceptions|Adjustments)',
            r'(Clawback|Windfall|Adjustment)',
            r'(Termination|Proration|Leave\s+of\s+Absence)'
        ],
        "terms_and_conditions": [
            r'(Terms\s+and\s+Conditions|General\s+Provisions|Plan\s+Rules)',
            r'(Eligibility|Participation\s+Requirements)',
            r'(Amendment|Modification)\s+of\s+Plan',
            r'(Disclaimer|General\s+Terms)'
        ],
        "compensation_components": [
            r'(Compensation\s+Components|Incentive\s+Components|Plan\s+Components)',
            r'(Bonus|Incentive|Commission)\s+Structure',
            r'(Quota|Target|Goal)\s+Achievement',
            r'(Revenue|Sales)\s+Attainment'
        ]
    }
    
    lines = content.split('\n')
    current_section = {"type": "body", "text": "", "level": 0, "start": 0, "spm_category": None}
    
    for i, line in enumerate(lines):
        # Skip empty lines
        if not line.strip():
            current_section["text"] += line + "\n"
            continue
            
        # Check for header patterns
        is_header = False
        header_level = 0
        
        for pattern in header_patterns:
            match = re.search(pattern, line.strip(), re.MULTILINE)
            if match:
                is_header = True
                # Determine header level
                if len(match.groups()) > 1:
                    # Use first group to determine level if pattern supports it
                    level_indicator = match.group(1)
                    if '#' in level_indicator:
                        header_level = len(level_indicator)  # Markdown heading level
                    elif re.match(r'\d+\.', level_indicator):
                        header_level = 2  # Numbered heading (level 2)
                    elif re.match(r'[IVX]+\.', level_indicator):
                        header_level = 2  # Roman numeral (level 2)
                    elif re.match(r'[A-Z]\.', level_indicator):
                        header_level = 3  # Letter heading (level 3)
                    else:
                        header_level = 1  # All caps or known section
                else:
                    header_level = 1  # Default to top level
                break
        
        if is_header:
            # Save the previous section if it has content
            if current_section["text"].strip():
                sections.append(current_section)
            
            # Determine if this header identifies an SPM-specific section
            spm_category = None
            for category, patterns in spm_section_patterns.items():
                if any(re.search(pattern, line, re.IGNORECASE) for pattern in patterns):
                    spm_category = category
                    break
            
            # Start a new section
            current_section = {
                "type": "header",
                "text": line + "\n",
                "level": header_level,
                "start": i,
                "spm_category": spm_category,
                "children": []
            }
            continue
        
        # Check for table structures
        is_table = False
        for pattern in table_patterns:
            if re.search(pattern, line):
                is_table = True
                break
                
        if is_table:
            if current_section["type"] != "table":
                # Save previous section
                if current_section["text"].strip():
                    sections.append(current_section)
                # Start table section
                current_section = {
                    "type": "table",
                    "text": line + "\n",
                    "level": 0,
                    "start": i,
                    "spm_category": current_section.get("spm_category")  # Inherit from parent section
                }
            else:
                current_section["text"] += line + "\n"
            continue
        
        # Check for payout formulas or compensation-specific content
        is_formula = False
        for pattern in formula_patterns:
            if re.search(pattern, line):
                is_formula = True
                break
                
        if is_formula:
            if current_section["type"] != "formula":
                # Save previous section
                if current_section["text"].strip():
                    sections.append(current_section)
                # Start formula section
                current_section = {
                    "type": "formula",
                    "text": line + "\n",
                    "level": 0,
                    "start": i,
                    "spm_category": "compensation_components"  # Formulas are usually compensation components
                }
            else:
                current_section["text"] += line + "\n"
            continue
            
        # Check for footer content (page numbers, confidentiality notices)
        if (re.search(r'^\s*\d+\s*$', line) or  # Just a page number
            re.search(r'(Confidential|for Internal Use Only)', line)):
            if current_section["type"] != "footer":
                # Save previous section
                if current_section["text"].strip():
                    sections.append(current_section)
                # Start footer section
                current_section = {
                    "type": "footer",
                    "text": line + "\n",
                    "level": 0,
                    "start": i,
                    "spm_category": None
                }
            else:
                current_section["text"] += line + "\n"
            continue
        
        # Check if line matches any SPM category patterns
        for category, patterns in spm_section_patterns.items():
            if any(re.search(pattern, line, re.IGNORECASE) for pattern in patterns):
                if current_section.get("spm_category") != category:
                    # Save previous section
                    if current_section["text"].strip():
                        sections.append(current_section)
                    # Start a new SPM category section
                    current_section = {
                        "type": "body",
                        "text": line + "\n",
                        "level": 0,
                        "start": i,
                        "spm_category": category
                    }
                    break
        else:
            # Regular content - append to current section
            current_section["text"] += line + "\n"
                
    # Add the last section
    if current_section["text"].strip():
        sections.append(current_section)
    
    # Organize sections hierarchically
    structured_sections = organize_sections_hierarchically(sections)
    
    return structured_sections


def organize_sections_hierarchically(sections: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Organize sections into a hierarchical structure based on header levels.
    
    Args:
        sections: Flat list of document sections
        
    Returns:
        Hierarchically organized list of sections
    """
    # Clone sections to avoid modifying originals
    top_level_sections = []
    current_path = []  # Stack to track current section hierarchy
    
    for section in sections:
        # Header sections determine the structure
        if section["type"] == "header":
            level = section["level"]
            
            # Pop higher or equal level sections from path
            while current_path and current_path[-1]["level"] >= level:
                current_path.pop()
            
            # Add this section to its parent's children or to top level
            if current_path:
                parent = current_path[-1]
                parent["children"].append(section)
            else:
                top_level_sections.append(section)
            
            # Add to current path
            current_path.append(section)
        else:
            # Non-header sections are added to the most recent parent's children or top level
            if current_path:
                parent = current_path[-1]
                parent["children"].append(section)
            else:
                top_level_sections.append(section)
    
    return top_level_sections


def apply_section_specific_cleaning(section: Dict[str, Any], cleaning_rules: List[Dict[str, Any]]) -> str:
    """Apply appropriate cleaning rules based on section type.
    
    Args:
        section: Document section with text and type
        cleaning_rules: List of cleaning rule dictionaries
        
    Returns:
        Cleaned section text
    """
    section_type = section["type"]
    section_text = section["text"]
    spm_category = section.get("spm_category")
    
    # Filter rules applicable to this section type and SPM category
    applicable_rules = [
        rule for rule in cleaning_rules 
        if rule.get("context") in ["all", section_type]
    ]
    
    # Sort by priority (lower number = higher priority)
    applicable_rules.sort(key=lambda x: x.get("priority", 5))
    
    # Apply rules in priority order
    for rule in applicable_rules:
        pattern = rule["pattern"]
        replacement = rule["replacement"]
        pattern_type = rule["pattern_type"]
        
        if pattern_type == "regex":
            section_text = re.sub(pattern, replacement, section_text, flags=re.MULTILINE)
        elif pattern_type == "exact":
            section_text = section_text.replace(pattern, replacement)
    
    # Special handling for certain section types
    if section_type == "table":
        # Preserve table structure - don't collapse whitespace
        section_text = section_text.rstrip()
    elif section_type == "formula":
        # Preserve formula structure - just trim excessively repeated whitespace
        section_text = re.sub(r'\s{3,}', '  ', section_text).rstrip()
    elif section_type == "footer":
        # Minimal footer content
        if len(section_text.strip()) < 30:  # Short footers can be removed
            section_text = ''
        else:
            section_text = section_text.strip()
    else:
        # Normalize whitespace for text sections
        section_text = re.sub(r'\s+', ' ', section_text).strip()
    
    # Process SPM-specific sections
    if spm_category:
        # Preserve structure in SPM-specific sections
        pass
    
    return section_text


def extract_compensation_component(section: Dict[str, Any]) -> Dict[str, Any]:
    """Extract compensation component information from a section.
    
    Args:
        section: Document section
        
    Returns:
        Dictionary with compensation component information
    """
    component = {
        "name": None,
        "type": None,
        "metrics": [],
        "category": None,
        "keywords": [],
        "frequency": None,
        "structure": None,
        "spm_mapping": {
            "spm_process": None,
            "spm_category": None,
            "spm_component": None,
            "matched_keyword": None
        },
        "target_amount": None
    }
    
    text = extract_text_content(section)
    
    # Extract component name
    name_match = re.search(r'^([A-Z][^.]+?)(?::|\.|\n)', text, re.MULTILINE)
    if name_match:
        component["name"] = name_match.group(1).strip()
    
    # Determine component type
    component_type_patterns = [
        (r'bonus', 'Bonus'),
        (r'commission', 'Commission'),
        (r'incentive', 'Incentive'),
        (r'quota.*bonus', 'Quota-Based Bonus'),
        (r'revenue.*commission', 'Revenue-Based Commission'),
        (r'multiplier', 'Multiplier'),
        (r'accelerator', 'Accelerator'),
        (r'spif', 'SPIF'),
        (r'mbo', 'MBO'),
        (r'kpi', 'KPI-Based')
    ]
    
    for pattern, comp_type in component_type_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            component["type"] = comp_type
            component["keywords"].append(pattern)
            break
    
    # Extract metrics
    metric_patterns = [
        r'quota', r'revenue', r'attainment', r'profit', r'margin', r'units', r'sales',
        r'growth', r'market share', r'customer', r'retention', r'churn', r'performance',
        r'objective', r'goal', r'target'
    ]
    
    for pattern in metric_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            component["metrics"].append(pattern)
            component["keywords"].append(pattern)
    
    # Extract frequency
    frequency_patterns = [
        (r'monthly', 'Monthly'),
        (r'quarterly', 'Quarterly'),
        (r'annual', 'Annual'),
        (r'semi-annual', 'Semi-Annual'),
        (r'one-time', 'One-Time')
    ]
    
    for pattern, freq in frequency_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            component["frequency"] = freq
            break
    
    # Extract target amount
    target_match = re.search(r'(?:target|amount):\s*\$?([\d,.]+)(?:\s*%)?', text, re.IGNORECASE)
    if target_match:
        component["target_amount"] = target_match.group(1).strip()
    
    # Determine category
    category_patterns = [
        (r'base.*salary', 'Base Salary'),
        (r'variable.*pay', 'Variable Pay'),
        (r'commission', 'Commission'),
        (r'bonus', 'Bonus'),
        (r'incentive', 'Incentive'),
        (r'long.*term', 'Long-Term Incentive'),
        (r'recognition', 'Recognition Award')
    ]
    
    for pattern, category in category_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            component["category"] = category
            break
    
    # Determine structure
    if "table" in section["type"]:
        component["structure"] = "Table-Based"
    elif "formula" in section["type"]:
        component["structure"] = "Formula-Based"
    else:
        # Try to determine structure from text
        if re.search(r'tier|level|step|threshold', text, re.IGNORECASE):
            component["structure"] = "Tiered"
        elif re.search(r'formula|calculation|compute', text, re.IGNORECASE):
            component["structure"] = "Formula-Based"
        elif re.search(r'flat|fixed', text, re.IGNORECASE):
            component["structure"] = "Flat Rate"
    
    # Map to SPM framework
    if component["type"] and component["metrics"]:
        # Default mapping
        component["spm_mapping"] = {
            "spm_process": "Incentive Compensation Management",
            "spm_category": "Incentives",
            "spm_component": None,
            "matched_keyword": component["keywords"][0] if component["keywords"] else None
        }
        
        # Map specific types to components
        type_mapping = {
            "Bonus": "Bonus Calculation",
            "Commission": "Commission Calculation",
            "Quota-Based Bonus": "Quota Achievement Bonus",
            "Revenue-Based Commission": "Revenue Attainment Commission",
            "Multiplier": "Performance Multipliers",
            "Accelerator": "Accelerator Rules",
            "SPIF": "Special Incentive Programs",
            "MBO": "Management by Objectives",
            "KPI-Based": "KPI-Based Incentives"
        }
        
        if component["type"] in type_mapping:
            component["spm_mapping"]["spm_component"] = type_mapping[component["type"]]
    
    return component

def extract_spm_components(sections: List[Dict[str, Any]], document_schema: Dict[str, Any]) -> Dict[str, Any]:
    """Extract SPM components from document sections based on schema.
    
    Args:
        sections: List of document sections
        document_schema: Schema definition for the document type
        
    Returns:
        Dictionary with extracted SPM components
    """
    spm_components = {}
    
    # Initialize structure based on schema
    for key in document_schema.keys():
        if isinstance(document_schema[key], dict):
            spm_components[key] = {}
        elif isinstance(document_schema[key], list):
            spm_components[key] = []
        else:
            spm_components[key] = None
    
    # Process sections to extract SPM components
    for section in sections:
        spm_category = section.get("spm_category")
        
        if not spm_category:
            # Process children recursively
            if "children" in section and section["children"]:
                child_components = extract_spm_components(section["children"], document_schema)
                # Merge with existing components
                for key, value in child_components.items():
                    if key in spm_components:
                        if isinstance(value, dict) and isinstance(spm_components[key], dict):
                            spm_components[key].update(value)
                        elif isinstance(value, list) and isinstance(spm_components[key], list):
                            spm_components[key].extend(value)
                        elif spm_components[key] is None:
                            spm_components[key] = value
            continue
        
        # Process section based on its SPM category
        if spm_category == "plan_info":
            plan_info = extract_plan_info(section)
            spm_components["plan_info"] = plan_info
            
        elif spm_category == "plan_summary":
            summary = extract_text_content(section)
            spm_components["plan_summary"] = summary
            
        elif spm_category == "effective_dates":
            dates = extract_effective_dates(section)
            spm_components["effective_dates"] = dates
            
        elif spm_category == "payout_schedule":
            payout = extract_payout_schedule(section)
            if payout:
                spm_components["payout_schedule"].append(payout)
            
        elif spm_category == "special_provisions":
            provision = extract_special_provision(section)
            if provision:
                spm_components["special_provisions"].append(provision)
            
        elif spm_category == "terms_and_conditions":
            term = extract_term_condition(section)
            if term:
                spm_components["terms_and_conditions"].append(term)
            
        elif spm_category == "compensation_components":
            component = extract_compensation_component(section)
            if component:
                spm_components["compensation_components"].append(component)
        
        # Recursively process children
        if "children" in section and section["children"]:
            child_components = extract_spm_components(section["children"], document_schema)
            # Merge with existing components
            for key, value in child_components.items():
                if key in spm_components:
                    if isinstance(value, dict) and isinstance(spm_components[key], dict):
                        spm_components[key].update(value)
                    elif isinstance(value, list) and isinstance(spm_components[key], list):
                        spm_components[key].extend(value)
                    elif spm_components[key] is None:
                        spm_components[key] = value
    
    return spm_components


def extract_plan_info(section: Dict[str, Any]) -> Dict[str, str]:
    """Extract plan information from a section.
    
    Args:
        section: Document section
        
    Returns:
        Dictionary with plan information
    """
    info = {
        "role": None,
        "region": None,
        "plan_id": None,
        "plan_year": None,
        "plan_title": None,
        "process_flow": None,
        "business_unit": None
    }
    
    text = extract_text_content(section)
    
    # Extract role
    role_match = re.search(r'(?:role|position):\s*([^,\n]+)', text, re.IGNORECASE)
    if role_match:
        info["role"] = role_match.group(1).strip()
    
    # Extract region
    region_match = re.search(r'(?:region|territory):\s*([^,\n]+)', text, re.IGNORECASE)
    if region_match:
        info["region"] = region_match.group(1).strip()
    
    # Extract plan ID
    plan_id_match = re.search(r'(?:plan\s+id|plan\s+number):\s*([^,\n]+)', text, re.IGNORECASE)
    if plan_id_match:
        info["plan_id"] = plan_id_match.group(1).strip()
    
    # Extract plan year
    plan_year_match = re.search(r'(?:plan\s+year|fiscal\s+year):\s*(\d{4})', text, re.IGNORECASE)
    if plan_year_match:
        info["plan_year"] = plan_year_match.group(1).strip()
    
    # Extract plan title
    plan_title_match = re.search(r'(?:plan\s+title|plan\s+name):\s*([^,\n]+)', text, re.IGNORECASE)
    if plan_title_match:
        info["plan_title"] = plan_title_match.group(1).strip()
    else:
        # Try to find a title in the text
        title_candidates = re.findall(r'^([A-Z][A-Z\s]+(?:PLAN|PROGRAM|INCENTIVE))', text, re.MULTILINE)
        if title_candidates:
            info["plan_title"] = title_candidates[0].strip()
    
    # Extract business unit
    bu_match = re.search(r'(?:business\s+unit|division|department):\s*([^,\n]+)', text, re.IGNORECASE)
    if bu_match:
        info["business_unit"] = bu_match.group(1).strip()
    
    return info


def extract_text_content(section: Dict[str, Any]) -> str:
    """Extract all text content from a section and its children.
    
    Args:
        section: Document section
        
    Returns:
        Combined text content
    """
    text = section["text"]
    
    # Add text from children
    if "children" in section and section["children"]:
        for child in section["children"]:
            child_text = extract_text_content(child)
            text += "\n" + child_text
    
    return text


def extract_effective_dates(section: Dict[str, Any]) -> Dict[str, str]:
    """Extract effective dates from a section.
    
    Args:
        section: Document section
        
    Returns:
        Dictionary with start and end dates
    """
    dates = {
        "start_date": None,
        "end_date": None
    }
    
    text = extract_text_content(section)
    
    # Extract start date
    start_date_match = re.search(r'(?:start\s+date|begin\s+date|effective\s+date):\s*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|\w+\s+\d{1,2},?\s+\d{4})', 
                                 text, re.IGNORECASE)
    if start_date_match:
        dates["start_date"] = start_date_match.group(1).strip()
    
    # Extract end date
    end_date_match = re.search(r'(?:end\s+date|termination\s+date|expiration\s+date):\s*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|\w+\s+\d{1,2},?\s+\d{4})', 
                                text, re.IGNORECASE)
    if end_date_match:
        dates["end_date"] = end_date_match.group(1).strip()
    
    # Look for date range pattern
    date_range_match = re.search(r'(?:period|effective)(?:\s+from|\s+of)?\s+(\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|\w+\s+\d{1,2},?\s+\d{4})\s+(?:to|through|until)\s+(\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|\w+\s+\d{1,2},?\s+\d{4})', 
                                 text, re.IGNORECASE)
    if date_range_match:
        if not dates["start_date"]:
            dates["start_date"] = date_range_match.group(1).strip()
        if not dates["end_date"]:
            dates["end_date"] = date_range_match.group(2).strip()
    
    return dates


def extract_payout_schedule(section: Dict[str, Any]) -> Dict[str, str]:
    """Extract payout schedule information from a section.
    
    Args:
        section: Document section
        
    Returns:
        Dictionary with payout schedule information
    """
    payout = {
        "type": None,
        "formula": None,
        "conditions": None
    }
    
    text = extract_text_content(section)
    
    # Extract payout type
    type_patterns = [
        (r'monthly', 'Monthly'),
        (r'quarterly', 'Quarterly'),
        (r'annual', 'Annual'),
        (r'bi-weekly', 'Bi-Weekly'),
        (r'semi-annual', 'Semi-Annual')
    ]
    
    for pattern, payout_type in type_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            payout["type"] = payout_type
            break
    
    # Extract formula if present
    formula_match = re.search(r'(?:formula|calculation):\s*([^.]+)', text, re.IGNORECASE)
    if formula_match:
        payout["formula"] = formula_match.group(1).strip()
    
    # Extract conditions
    conditions_match = re.search(r'(?:conditions|requirements|criteria):\s*([^.]+)', text, re.IGNORECASE)
    if conditions_match:
        payout["conditions"] = conditions_match.group(1).strip()
    else:
        # Use the whole text as conditions if specific match not found
        payout["conditions"] = text.strip()
    
    return payout


def extract_special_provision(section: Dict[str, Any]) -> Dict[str, Any]:
    """Extract special provision information from a section.
    
    Args:
        section: Document section
        
    Returns:
        Dictionary with special provision information
    """
    provision = {
        "name": None,
        "keywords": [],
        "conditions": None,
        "description": None,
        "spm_mapping": {
            "spm_process": None,
            "spm_category": None,
            "spm_component": None,
            "matched_keyword": None
        }
    }
    
    text = extract_text_content(section)
    
    # Extract provision name
    name_match = re.search(r'^([A-Z][^.]+?)(?::|\.|\n)', text, re.MULTILINE)
    if name_match:
        provision["name"] = name_match.group(1).strip()
    
    # Extract keywords
    # Look for common special provision keywords
    keyword_patterns = [
        r'clawback', r'windfall', r'leave of absence', r'termination', r'proration',
        r'adjustment', r'exception', r'credit split', r'dispute', r'draw', r'guarantee',
        r'advance', r'eligibility', r'threshold', r'minimum', r'maximum', r'cap'
    ]
    
    for pattern in keyword_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            provision["keywords"].append(pattern)
    
    # Extract conditions and description
    provision["description"] = text.strip()
    conditions_match = re.search(r'(?:conditions|criteria|requirements):\s*([^.]+)', text, re.IGNORECASE)
    if conditions_match:
        provision["conditions"] = conditions_match.group(1).strip()
    
    # Basic SPM mapping based on keywords
    if provision["keywords"]:
        # Default mapping
        provision["spm_mapping"] = {
            "spm_process": "Incentive Compensation Management",
            "spm_category": "Special Provisions",
            "spm_component": None,
            "matched_keyword": provision["keywords"][0]
        }
        
        # Map specific keywords to components
        keyword_mapping = {
            "clawback": "Recovery Provisions",
            "windfall": "Adjustments",
            "leave of absence": "Eligibility Rules",
            "termination": "Employment Changes",
            "proration": "Calculation Adjustments",
            "credit split": "Crediting Rules",
            "dispute": "Dispute Management",
            "draw": "Advanced Payments",
            "guarantee": "Guaranteed Payments",
            "cap": "Payment Caps"
        }
        
        for keyword in provision["keywords"]:
            if keyword in keyword_mapping:
                provision["spm_mapping"]["spm_component"] = keyword_mapping[keyword]
                provision["spm_mapping"]["matched_keyword"] = keyword
                break
    
    return provision

def extract_term_condition(section: Dict[str, Any]) -> Dict[str, Any]:
    """Extract terms and conditions information from a section.
    
    Args:
        section: Document section
        
    Returns:
        Dictionary with terms and conditions information
    """
    term = {
        "keywords": [],
        "description": None,
        "spm_mapping": {
            "spm_process": None,
            "spm_category": None,
            "spm_component": None,
            "matched_keyword": None
        },
        "component_type": None
    }
    
    text = extract_text_content(section)
    
    # Extract keywords
    keyword_patterns = [
        r'eligibility', r'participation', r'amendment', r'modification', r'termination',
        r'disclaimer', r'jurisdiction', r'confidentiality', r'non-compete', r'non-solicitation',
        r'employment', r'at-will', r'tax', r'compliance', r'policy'
    ]
    
    for pattern in keyword_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            term["keywords"].append(pattern)
    
    # Extract description
    term["description"] = text.strip()
    
    # Determine component type
    component_type_patterns = [
        (r'eligibility|participation', 'Eligibility'),
        (r'amendment|modification|change', 'Plan Modification'),
        (r'confidentiality|disclosure', 'Confidentiality'),
        (r'termination|separation|resignation', 'Employment Status'),
        (r'tax|taxation|withholding', 'Tax Implications'),
        (r'dispute|resolution|arbitration', 'Dispute Resolution'),
        (r'compliance|regulatory|legal', 'Compliance')
    ]
    
    for pattern, comp_type in component_type_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            term["component_type"] = comp_type
            break
    
    # Basic SPM mapping based on keywords
    if term["keywords"]:
        # Default mapping
        term["spm_mapping"] = {
            "spm_process": "Incentive Compensation Management",
            "spm_category": "Plan Governance",
            "spm_component": None,
            "matched_keyword": term["keywords"][0]
        }
        
        # Map specific keywords to components
        keyword_mapping = {
            "eligibility": "Eligibility Rules",
            "participation": "Participation Requirements",
            "amendment": "Plan Amendment Process",
            "modification": "Plan Modification Rules",
            "termination": "Plan Termination Provisions",
            "confidentiality": "Confidentiality Requirements",
            "tax": "Tax Implications",
            "compliance": "Compliance Requirements"
        }
        
        for keyword in term["keywords"]:
            if keyword in keyword_mapping:
                term["spm_mapping"]["spm_component"] = keyword_mapping[keyword]
                term["spm_mapping"]["matched_keyword"] = keyword
                break
    
    return term

def get_batch_size_from_settings(db_manager, default_limit=500):
    """
    Retrieve the batch size from pipeline settings or use default.
    
    Args:
        db_manager: Database manager instance
        default_limit: Default limit to use if setting not found
        
    Returns:
        int: Batch size from settings or default
    """
    try:
        db_manager.cursor.execute(
            "SELECT value FROM pipeline_settings WHERE key = 'batch.size';"
        )
        result = db_manager.cursor.fetchone()
        
        if result and result[0]:
            try:
                batch_size = int(result[0])
                logger.info(f"Using batch size from settings: {batch_size}")
                return batch_size
            except ValueError:
                logger.warning(f"Invalid batch size in settings: {result[0]}, using default: {default_limit}")
                return default_limit
        else:
            logger.info(f"No batch size found in settings, using default: {default_limit}")
            return default_limit
    except Exception as e:
        logger.warning(f"Error retrieving batch size from settings: {e}, using default: {default_limit}")
        return default_limit
                
def get_document_content(document_id: str, stage_dir: Path) -> Tuple[str, str]:
    """Get document content from the pipeline directory.
    
    Args:
        document_id: Document identifier
        stage_dir: Directory containing document files
        
    Returns:
        Tuple of (content, file_extension)
    """
    # Match based on loader's naming pattern
    doc_id_short = str(document_id).replace("-", "")[:12]  # Get first 12 characters without dashes
    matching_files = list(stage_dir.glob(f"*doc{doc_id_short}*"))
    
    if not matching_files:
        logger.error(f"❌ No content file found for document {document_id} in {stage_dir}")
        return "", ""
    
    content_file = matching_files[0]  # Take the first match
    file_extension = content_file.suffix.lower()
    logger.info(f"🔎 Found content file: {content_file} with extension {file_extension}")
    
    try:
        # Handle different file types
        if file_extension == '.json':
            with open(content_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, dict) and "content" in data:
                    content = data["content"]
                    # Check if content is a nested JSON string
                    if isinstance(content, str) and content.startswith("{"):
                        try:
                            nested_data = json.loads(content)
                            if isinstance(nested_data, dict) and "content" in nested_data:
                                return nested_data["content"], file_extension
                        except json.JSONDecodeError:
                            pass
                    return content, file_extension
                else:
                    return str(data), file_extension
        else:
            # For non-JSON files, read as text
            with open(content_file, "r", encoding="utf-8") as f:
                content = f.read()
                return content, file_extension
    
    except Exception as e:
        logger.error(f"⚠️ Error reading {content_file}: {e}")
        return "", file_extension
        
def clean_documents(limit: int = 500, use_ai: bool = False):
    """Process documents and apply enhanced cleaning.
    
    Args:
        limit: Maximum number of documents to process
        use_ai: Whether to use AI-guided cleaning
    """
    documents = processor.get_documents_for_stage(current_stage="load", status="completed", limit=limit)
    
    if not documents:
        logger.warning("⚠️ No documents ready for cleaning")
        return
    
    batch_name = f"clean_batch_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    batch_id = processor.record_batch_processing(batch_name=batch_name, document_count=len(documents), status="processing")
    
    # Get directory paths
    dirs = processor.get_base_dirs()
    content_dir = dirs["stage_load"]  # Source files come from the "load" stage
    clean_dir = dirs["stage_clean"]   # Save cleaned files in "clean"
    
    # Check if AI cleaning is enabled in settings
    if use_ai:
        try:
            db_manager.cursor.execute("SELECT value FROM pipeline_settings WHERE key = 'document_cleaner.use_ai'")
            result = db_manager.cursor.fetchone()
            if result and result[0].lower() == 'false':
                logger.info("⚠️ AI cleaning is disabled in settings. Using rule-based cleaning.")
                use_ai = False
        except Exception as e:
            logger.warning(f"⚠️ Could not check AI cleaning settings: {e}")
    
    cleaned_documents = []
    failures = 0
    
    for doc in documents:
        document_id = doc["id"]
        logger.info(f"🔍 Cleaning document {document_id}")
        
        # Get document type
        document_type = db_manager.get_document_type(document_id) or "comp_plan"
        
        # Get document content and file extension
        content, file_extension = get_document_content(document_id, content_dir)
        
        if not content:
            failures += 1
            processor.update_document_stage(document_id=document_id, status="failed", error_message="No content found", batch_id=batch_id)
            continue
        
        # Apply AI-guided cleaning if enabled
        if use_ai:
            try:
                # Check minimum size for AI cleaning
                db_manager.cursor.execute("SELECT value FROM pipeline_settings WHERE key = 'document_cleaner.min_chars_for_ai'")
                result = db_manager.cursor.fetchone()
                min_chars = int(result[0]) if result else 1000
                
                if len(content) >= min_chars:
                    logger.info(f"🧠 Using AI cleaning for document {document_id} ({len(content)} chars)")
                    cleaned_content = ai_guided_cleaning(content, document_type, file_extension)
                else:
                    logger.info(f"ℹ️ Document too small for AI cleaning ({len(content)} chars < {min_chars}). Using rule-based cleaning.")
                    cleaning_result = clean_document(document_id, content, document_type)
                    cleaned_content = cleaning_result["content"]
            except Exception as e:
                logger.error(f"❌ AI cleaning failed: {e}. Falling back to rule-based cleaning.")
                cleaning_result = clean_document(document_id, content, document_type)
                cleaned_content = cleaning_result["content"]
        else:
            # Apply rule-based cleaning
            cleaning_result = clean_document(document_id, content, document_type)
            cleaned_content = cleaning_result["content"]
            
            # Extract SPM components if available
            spm_components = cleaning_result.get("spm_components")
            if spm_components:
                logger.info(f"✅ Extracted SPM components for document {document_id}")
                # Save document sections to database
                try:
                    # First check if document_sections table exists
                    db_manager.cursor.execute("""
                        SELECT EXISTS (
                            SELECT FROM information_schema.tables 
                            WHERE table_name = 'document_sections'
                        );
                    """)
                    table_exists = db_manager.cursor.fetchone()[0]
                    
                    if table_exists:
                        for section_type, section_data in cleaning_result.get("sections", {}).items():
                            # Insert section data
                            db_manager.cursor.execute("""
                                INSERT INTO document_sections 
                                (document_id, section_type, content, cleaned_content, section_order, spm_category)
                                VALUES (%s, %s, %s, %s, %s, %s)
                            """, (
                                document_id, 
                                section_type,
                                section_data.get("original_text", ""),
                                section_data.get("cleaned_text", ""),
                                section_data.get("order", 0),
                                section_data.get("spm_category")
                            ))
                    logger.info(f"✅ Saved document sections to database")
                except Exception as e:
                    logger.error(f"❌ Failed to save document sections: {e}")
        
        # Generate a cleaned filename following the pipeline convention
        new_filename = processor.generate_stage_filename(
            original_filename=doc.get("name", f"doc_{document_id}.txt"),
            document_id=document_id,
            batch_id=batch_id
        )
        
        # Save cleaned content
        clean_file_path = clean_dir / new_filename
        with open(clean_file_path, "w", encoding="utf-8") as f:
            f.write(cleaned_content)
        
        cleaned_documents.append({
            "id": document_id,
            "original_filename": doc.get("original_filename"),
            "pipeline_filename": new_filename,
            "cleaned_content_length": len(cleaned_content),
            "pipeline_stage": "clean",
            "batch_id": batch_id,
            "status": "completed",
        })
        
        logger.info(f"✅ Document {document_id} cleaned ({len(cleaned_content)} chars)")

        # Mark Stage as Completed
        processor.update_document_stage(document_id=document_id, status="completed", batch_id=batch_id)
    
    # Batch update
    if cleaned_documents:
        processor.save_document_batch(cleaned_documents, batch_name=batch_name)
        processor.finalize_batch(batch_id, "completed")
        logger.info(f"✅ Cleaning complete: {len(cleaned_documents)} success, {failures} failed")
    else:
        processor.finalize_batch(batch_id, "failed")
        logger.warning("⚠️ No documents were successfully cleaned")
        
def clean_document(document_id: str, content: str, document_type: str = "comp_plan") -> Dict[str, Any]:
    """Clean document with content-aware processing.
    
    Args:
        document_id: Document identifier
        content: Document content text
        document_type: Type of document (for rule selection)
        
    Returns:
        Dictionary with cleaned content and processing metadata
    """
    start_time = time.time()
    
    # Get applicable cleaning rules for this document type
    cleaning_rules = fetch_cleaning_patterns(document_type)
    logger.info(f"📋 Retrieved {len(cleaning_rules)} cleaning rules for document type '{document_type}'")
    
    # Process document in sections
    sections = identify_document_sections(content)
    logger.info(f"🔍 Identified {len(sections)} document sections")
    
    # Analyze section types
    section_types = {}
    for section in sections:
        section_type = section["type"]
        section_types[section_type] = section_types.get(section_type, 0) + 1
    
    logger.info(f"📊 Section types: {', '.join([f'{k}={v}' for k, v in section_types.items()])}")
    
    # Apply cleaning rules to each section
    cleaned_sections = []
    
    def process_section_tree(section, depth=0):
        """Process a section and its children recursively."""
        # Clean the section text
        section["cleaned_text"] = apply_section_specific_cleaning(section, cleaning_rules)
        
        # Process children if any
        if "children" in section and section["children"]:
            section["cleaned_children"] = []
            for child in section["children"]:
                cleaned_child = process_section_tree(child, depth + 1)
                section["cleaned_children"].append(cleaned_child)
        
        return section
    
    # Process all top-level sections
    for section in sections:
        cleaned_section = process_section_tree(section)
        cleaned_sections.append(cleaned_section)
    
    # Reconstruct the cleaned document
    cleaned_text = ""
    
    def reconstruct_text(section, is_root=False):
        """Recursively reconstruct text from sections."""
        text = section["cleaned_text"] if "cleaned_text" in section else section["text"]
        
        # Add newlines between sections
        if is_root and text:
            text = "\n\n" + text
        
        # Add children's text
        if "cleaned_children" in section and section["cleaned_children"]:
            child_text = "\n".join([reconstruct_text(child) for child in section["cleaned_children"]])
            if child_text:
                text += "\n" + child_text
        
        return text
    
    # Build the cleaned document from all sections
    for section in cleaned_sections:
        cleaned_text += reconstruct_text(section, is_root=True)
    
    # Final document-wide cleaning
    cleaned_text = re.sub(r'\n{3,}', '\n\n', cleaned_text)  # Normalize consecutive newlines
    cleaned_text = cleaned_text.strip()
    
    # Extract SPM components if needed
    spm_components = None
    try:
        # Fetch document schema
        document_schema = fetch_document_schema(document_type)
        if document_schema:
            logger.info(f"🔍 Attempting to extract SPM components based on schema")
            spm_components = extract_spm_components(sections, document_schema)
    except Exception as e:
        logger.error(f"❌ Error extracting SPM components: {e}")
        # Continue without components extraction
    
    # Calculate processing time
    processing_time = time.time() - start_time
    
    result = {
        "document_id": document_id,
        "document_type": document_type,
        "original_length": len(content),
        "cleaned_length": len(cleaned_text),
        "content": cleaned_text,
        "processing_time": processing_time,
        "section_count": len(sections),
        "section_types": section_types,
    }
    
    if spm_components:
        result["spm_components"] = spm_components
    
    logger.info(f"✅ Document cleaned in {processing_time:.2f}s - Original: {len(content)} chars, Cleaned: {len(cleaned_text)} chars")
    
    return result
            
def main():
    """CLI Entry point."""
    parser = argparse.ArgumentParser(description="Enhanced Document Cleaner")
    parser.add_argument("--limit", "-l", type=int, default=None, 
                        help="Max documents to process (overrides DB setting)")
    parser.add_argument("--use-ai", "-ai", action="store_true", 
                        help="Use AI-guided cleaning")
    parser.add_argument("--verbose", "-v", action="store_true",
                        help="Enable verbose logging")
    
    args = parser.parse_args()
    
    # Set verbose logging if requested
    if args.verbose:
        logger.setLevel(logging.DEBUG)
        for handler in logger.handlers:
            handler.setLevel(logging.DEBUG)
        logger.debug("Verbose logging enabled")
    
    # Get batch size from DB or command line
    default_limit = 500
    
    # Command line overrides DB setting
    if args.limit is not None:
        batch_size = args.limit
        logger.info(f"Using command line batch size: {batch_size}")
    else:
        batch_size = get_batch_size_from_settings(db_manager, default_limit)
        
    logger.info(f"Starting document cleaner with limit={batch_size}, use_ai={args.use_ai}")
    
    clean_documents(limit=batch_size, use_ai=args.use_ai)

if __name__ == "__main__":
    main()