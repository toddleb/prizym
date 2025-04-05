"""
Compensation Plans Excel Generator CLI
-------------------------------------
Convert Medtronic compensation plan JSON files to a formatted Excel report.
"""

import argparse
import json
import os
import glob
import sys
from datetime import datetime

# Adjust imports for project structure
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.utils.comp_plans_excel import create_excel_from_json


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Convert compensation plan JSON files to an Excel report."
    )
    parser.add_argument(
        "input", 
        nargs="*", 
        help="JSON files or directory containing JSON files"
    )
    parser.add_argument(
        "-o", "--output", 
        default=f"compensation_plans_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
        help="Output Excel file name (default: compensation_plans_<timestamp>.xlsx)"
    )
    parser.add_argument(
        "-r", "--recursive", 
        action="store_true",
        help="Recursively search for JSON files in subdirectories"
    )
    parser.add_argument(
        "-p", "--pattern", 
        default="*_SIP_*.json,*_Spec_*.json",
        help="Comma-separated file patterns to match (default: *_SIP_*.json,*_Spec_*.json)"
    )
    
    return parser.parse_args()


def find_json_files(inputs, recursive=False, patterns=None):
    """Find JSON files based on inputs and patterns."""
    if patterns:
        pattern_list = patterns.split(',')
    else:
        pattern_list = ["*.json"]
    
    json_files = []
    
    for input_path in inputs:
        if os.path.isfile(input_path) and input_path.endswith('.json'):
            # If input is a file, add it directly
            json_files.append(input_path)
        elif os.path.isdir(input_path):
            # If input is a directory, search for matching files
            for pattern in pattern_list:
                if recursive:
                    file_pattern = os.path.join(input_path, "**", pattern)
                    matches = glob.glob(file_pattern, recursive=True)
                else:
                    file_pattern = os.path.join(input_path, pattern)
                    matches = glob.glob(file_pattern)
                json_files.extend(matches)
    
    # Remove duplicates while preserving order
    unique_files = []
    for file in json_files:
        if file not in unique_files:
            unique_files.append(file)
    
    return unique_files


def validate_json_files(file_list):
    """Validate JSON files to ensure they have required fields."""
    valid_files = []
    
    for file_path in file_list:
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
            
            # Check if file has required fields for our processor
            if (
                "plan_info" in data and 
                "compensation_components" in data and 
                "effective_dates" in data
            ):
                valid_files.append(file_path)
            else:
                print(f"Warning: {file_path} doesn't have required fields and will be skipped.")
        except json.JSONDecodeError:
            print(f"Error: {file_path} is not a valid JSON file and will be skipped.")
        except Exception as e:
            print(f"Error processing {file_path}: {str(e)}")
    
    return valid_files


def main():
    """Main entry point."""
    args = parse_args()
    
    # Use current directory if no inputs provided
    inputs = args.input if args.input else ["."]
    
    # Find and validate JSON files
    json_files = find_json_files(inputs, args.recursive, args.pattern)
    valid_files = validate_json_files(json_files)
    
    if not valid_files:
        print("Error: No valid JSON files found.")
        return 1
    
    print(f"Found {len(valid_files)} valid compensation plan JSON files:")
    for file in valid_files:
        print(f"  - {file}")
    
    # Generate Excel report
    try:
        create_excel_from_json(valid_files, args.output)
        print(f"✅ Success! Excel report generated: {args.output}")
        return 0
    except Exception as e:
        print(f"❌ Error generating Excel report: {str(e)}")
        return 1


if __name__ == "__main__":
    exit(main())