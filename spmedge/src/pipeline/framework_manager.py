#!/usr/bin/env python3
"""
Framework Manager - Loads and initializes framework data from Excel into the database.
- Supports multiple framework types (SPM, Client, Industry, etc.).
- Reads framework_type_framework_version.xlsx and inserts into the framework table.
- Links data to the latest active framework version.
- Ensures only the latest version remains active.
- Exports frameworks to JSON for pipeline usage.
"""

import os
import json
import logging
import psycopg2
import pandas as pd
from pathlib import Path
from datetime import datetime
from config.config import config
from src.pipeline.db_integration import DBManager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger("framework_manager")

FRAMEWORK_DIR = Path(config.KNOWLEDGE_FILES_DIR)
db_manager = DBManager()

def parse_framework_filename(filename: str):
    """
    Extract framework type and version from filename (e.g., 'SPM_framework_v1.xlsx').
    
    Args:
        filename: The filename to parse
        
    Returns:
        tuple: (framework_type, framework_version) or (None, None) if invalid
    """
    parts = filename.replace(".xlsx", "").split("_framework_v")
    if len(parts) != 2:
        logger.error(f"❌ Invalid framework filename format: {filename}")
        return None, None
    return parts[0], parts[1]

def backup_current_framework(framework_type):
    """
    Create a backup of the current active framework before updating.
    
    Args:
        framework_type: Type of framework to backup
        
    Returns:
        bool: True if backup successful, False otherwise
    """
    try:
        # Get the current active version
        db_manager.cursor.execute(
            """
            SELECT v.version_id, v.version_name 
            FROM framework_versions v
            WHERE v.is_active = TRUE
            ORDER BY v.created_at DESC
            LIMIT 1;
            """
        )
        result = db_manager.cursor.fetchone()
        
        if not result:
            logger.info("ℹ️ No active framework version found to backup.")
            return True
            
        version_id, version_name = result
        
        # Create backup filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = FRAMEWORK_DIR / f"backup_{framework_type}_framework_v{version_name}_{timestamp}.json"
        
        # Export current framework to backup file
        db_manager.cursor.execute(
            """
            SELECT process, category, component, keyword, definition, framework_type
            FROM framework
            WHERE framework_version_id = %s;
            """,
            (version_id,)
        )
        framework_data = db_manager.cursor.fetchall()
        
        if not framework_data:
            logger.info("ℹ️ No framework data found to backup.")
            return True
            
        # Convert data to JSON structure
        json_data = [
            {
                "process": row[0],
                "category": row[1],
                "component": row[2],
                "keyword": row[3],
                "definition": row[4],
                "framework_type": row[5]
            }
            for row in framework_data
        ]
        
        # Save the backup
        with open(backup_file, "w", encoding="utf-8") as f:
            json.dump(json_data, f, indent=4)
            
        logger.info(f"✅ Successfully created framework backup: {backup_file}")
        return True
        
    except Exception as e:
        logger.error(f"❌ Failed to backup framework: {e}")
        return False

def create_new_framework_version(framework_type: str, framework_version: str):
    """
    Create a new framework version and deactivate old ones.
    
    Args:
        framework_type: Type of framework (SPM, Client, etc.)
        framework_version: Version identifier
        
    Returns:
        int: New version ID or None if failed
    """
    try:
        # First, deactivate all previous versions of this framework type
        db_manager.cursor.execute(
            """
            UPDATE framework_versions 
            SET is_active = FALSE 
            WHERE framework_type = %s;
            """,
            (framework_type,)
        )

        # Create the new version
        db_manager.cursor.execute(
            """
            INSERT INTO framework_versions (
                version_name, 
                description, 
                is_active, 
                framework_type
            )
            VALUES (%s, %s, TRUE, %s) 
            RETURNING version_id;
            """,
            (
                framework_version, 
                f"{framework_type} Framework version {framework_version}",
                framework_type
            )
        )
        version_id = db_manager.cursor.fetchone()[0]
        db_manager.conn.commit()

        logger.info(f"✅ Created new framework version: {framework_type} v{framework_version}")
        return version_id

    except Exception as e:
        logger.error(f"❌ Failed to create framework version: {e}")
        db_manager.conn.rollback()
        return None

def export_framework_to_json(version_id, framework_type):
    """
    Export the latest framework version to a JSON file for pipeline usage.
    
    Args:
        version_id: Database ID of the framework version
        framework_type: Type of framework to export
    """
    try:
        db_manager.cursor.execute(
            """
            SELECT process, category, component, keyword, definition, framework_type
            FROM framework
            WHERE framework_version_id = %s;
            """,
            (version_id,)
        )
        framework_data = db_manager.cursor.fetchall()

        if not framework_data:
            logger.warning("⚠ No framework data found to export.")
            return

        # Convert data to JSON structure
        json_data = [
            {
                "version": 1,
                "spm_process": row[0],
                "spm_category": row[1],
                "spm_component": row[2],
                "spm_keyword": row[3],
                "spm_definition": row[4],
                "spm_user_type": "",
                "spm_prompt": "",
                "spm_complexity_level": "",
                "spm_analysis_00": "",
                "spm_analysis_01": "",
                "spm_analysis_02": "",
                "spm_analysis_03": "",
                "spm_contextual_example": "",
                "spm_traceability_code": ""
            }
            for row in framework_data
        ]

        # Define the JSON file path
        json_file_path = Path(config.KNOWLEDGE_FILES_DIR) / f"{framework_type.lower()}_knowledge.json"

        # Save the JSON file
        with open(json_file_path, "w", encoding="utf-8") as f:
            json.dump(json_data, f, indent=2, ensure_ascii=False)

        logger.info(f"✅ Successfully exported framework to JSON: {json_file_path}")

    except Exception as e:
        logger.error(f"❌ Failed to export framework to JSON: {e}")

def validate_excel_structure(df):
    """
    Validate that the Excel file has the required structure.
    
    Args:
        df: Pandas DataFrame of the Excel file
        
    Returns:
        bool: True if valid, False otherwise
    """
    # Ensure required columns exist
    required_columns = {
        "process", "category", "component", "keyword", "definition", "framework_type"
    }
    
    if not required_columns.issubset(df.columns):
        missing = required_columns - set(df.columns)
        logger.error(f"❌ Missing required columns: {missing}")
        return False
        
    # Check for empty values in critical columns
    for col in ["process", "category", "component", "keyword"]:
        if df[col].isna().any():
            empty_rows = df[df[col].isna()].index.tolist()
            logger.error(f"❌ Empty values in '{col}' column at rows: {empty_rows}")
            return False
            
    # Validate framework type consistency
    framework_types = df["framework_type"].unique()
    if len(framework_types) > 1:
        logger.warning(f"⚠ Multiple framework types in one file: {framework_types}")
        
    return True

def load_framework_from_excel(filename: str):
    """
    Load framework data from an Excel file into the database.
    
    Args:
        filename: Excel filename to load
    """
    framework_file = FRAMEWORK_DIR / filename
    framework_type, framework_version = parse_framework_filename(filename)

    if not framework_file.exists():
        logger.error(f"❌ Framework file not found: {framework_file}")
        return

    if not framework_type or not framework_version:
        logger.error(f"❌ Unable to determine framework type/version from filename: {filename}")
        return

    try:
        # Read Excel file
        logger.info(f"📊 Reading Excel file: {framework_file}")
        df = pd.read_excel(framework_file)
        
        # Clean up data
        for col in df.columns:
            if df[col].dtype == 'object':
                df[col] = df[col].fillna('').astype(str).str.strip()
        
        # Validate Excel structure
        if not validate_excel_structure(df):
            return
            
        # Backup current framework
        if not backup_current_framework(framework_type):
            logger.warning("⚠ Proceeding without backup due to backup failure")
        
        # Get the latest active framework version
        version_id = create_new_framework_version(framework_type, framework_version)
        if version_id is None:
            return

        # Begin transaction
        db_manager.conn.autocommit = False
        
        # Clear existing data for this version if needed
        db_manager.cursor.execute(
            "DELETE FROM framework WHERE framework_version_id = %s;",
            (version_id,)
        )

        # Prepare data for bulk insert
        records = []
        for _, row in df.iterrows():
            records.append((
                row["process"], 
                row["category"], 
                row["component"], 
                row["keyword"], 
                row["definition"],
                row.get("user_type", ""), 
                row.get("prompt", ""), 
                row.get("complexity_level", ""),
                row.get("analysis_00", ""), 
                row.get("analysis_01", ""), 
                row.get("analysis_02", ""), 
                row.get("analysis_03", ""),
                row.get("contextual_example", ""), 
                row.get("traceability_code", ""),
                version_id, 
                row["framework_type"]
            ))
        
        # Bulk insert for better performance
        psycopg2.extras.execute_batch(
            db_manager.cursor,
            """
            INSERT INTO framework (
                process, category, component, keyword, definition, 
                user_type, prompt, complexity_level, analysis_00, analysis_01, 
                analysis_02, analysis_03, contextual_example, traceability_code, 
                framework_version_id, framework_type
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            records
        )

        # Commit the transaction
        db_manager.conn.commit()
        db_manager.conn.autocommit = True
        
        logger.info(f"✅ Successfully loaded {len(records)} records from {framework_type} framework (Version {framework_version}).")

        # Export framework to JSON after successful DB insertion
        export_framework_to_json(version_id, framework_type)

    except Exception as e:
        logger.error(f"❌ Failed to load framework from Excel: {e}")
        db_manager.conn.rollback()
        db_manager.conn.autocommit = True

def list_framework_versions():
    """List all available framework versions in the database."""
    try:
        db_manager.cursor.execute(
            """
            SELECT 
                v.version_id, 
                v.version_name, 
                v.framework_type,
                v.is_active,
                v.created_at,
                COUNT(f.id) as entry_count
            FROM 
                framework_versions v
            LEFT JOIN 
                framework f ON v.version_id = f.framework_version_id
            GROUP BY 
                v.version_id, v.version_name, v.framework_type, v.is_active, v.created_at
            ORDER BY 
                v.framework_type, v.created_at DESC;
            """
        )
        versions = db_manager.cursor.fetchall()
        
        if not versions:
            logger.info("ℹ️ No framework versions found in the database.")
            return
            
        logger.info("\n🔍 Framework Versions:")
        logger.info("-" * 80)
        logger.info(f"{'ID':<5} {'Type':<10} {'Version':<10} {'Status':<10} {'Created':<20} {'Entries':<10}")
        logger.info("-" * 80)
        
        for v in versions:
            status = "✅ ACTIVE" if v[3] else "❌ INACTIVE"
            logger.info(f"{v[0]:<5} {v[2]:<10} {v[1]:<10} {status:<10} {v[4].strftime('%Y-%m-%d %H:%M'):<20} {v[5]:<10}")
            
    except Exception as e:
        logger.error(f"❌ Failed to list framework versions: {e}")

def main():
    """Main framework initialization script."""
    import argparse
    import psycopg2.extras

    parser = argparse.ArgumentParser(description="Framework Manager for SPM Knowledge")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # Load framework from Excel
    load_parser = subparsers.add_parser("load", help="Load framework from Excel file")
    load_parser.add_argument("filename", type=str, help="Framework file to load (e.g., SPM_framework_v1.xlsx)")
    
    # List framework versions
    list_parser = subparsers.add_parser("list", help="List available framework versions")
    
    # Export framework to JSON
    export_parser = subparsers.add_parser("export", help="Export active framework to JSON")
    export_parser.add_argument("framework_type", type=str, help="Framework type to export (e.g., SPM)")

    args = parser.parse_args()
    
    if args.command == "load":
        load_framework_from_excel(args.filename)
    elif args.command == "list":
        list_framework_versions()
    elif args.command == "export":
        # Find active version ID for the specified type
        db_manager.cursor.execute(
            """
            SELECT version_id
            FROM framework_versions
            WHERE framework_type = %s AND is_active = TRUE
            """,
            (args.framework_type,)
        )
        result = db_manager.cursor.fetchone()
        if result:
            export_framework_to_json(result[0], args.framework_type)
        else:
            logger.error(f"❌ No active framework found for type: {args.framework_type}")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()