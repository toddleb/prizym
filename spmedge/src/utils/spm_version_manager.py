#!/usr/bin/env python3
"""
SPM Framework Version Manager
"""

import argparse
import logging
from src.pipeline.db_integration import DBManager

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("spm_version_manager")

def list_versions():
    """List all available framework versions"""
    db = DBManager()
    try:
        # Get all versions
        db.cursor.execute("""
            SELECT 
                v.version_id, 
                v.version_name, 
                v.created_at, 
                v.description, 
                v.is_active,
                COUNT(f.framework_version_id) as entry_count
            FROM spm_framework_versions v
            LEFT JOIN spm_framework f ON v.version_id = f.framework_version_id
            GROUP BY v.version_id, v.version_name, v.created_at, v.description, v.is_active
            ORDER BY v.created_at DESC
        """)
        
        versions = db.cursor.fetchall()
        
        if not versions:
            print("No framework versions found.")
            return
            
        print("\n📋 SPM Framework Versions:")
        print("-" * 100)
        print(f"{'ID':<5} {'Name':<15} {'Created':<25} {'Active':<8} {'Entries':<8} {'Description'}")
        print("-" * 100)
        
        for v in versions:
            active_marker = "✅" if v[4] else "❌"
            print(f"{v[0]:<5} {v[1]:<15} {v[2]:<25} {active_marker:<8} {v[5]:<8} {v[3] or ''}")
            
        print("-" * 100)
        
    except Exception as e:
        logger.error(f"Error listing versions: {e}")
    finally:
        db.close_connection()

def create_version(name, description=None, active=False):
    """Create a new framework version"""
    db = DBManager()
    try:
        # Start transaction
        db.conn.autocommit = False
        
        # If making active, set all other versions to inactive
        if active:
            db.cursor.execute("""
                UPDATE spm_framework_versions SET is_active = FALSE
            """)
        
        # Create new version
        db.cursor.execute("""
            INSERT INTO spm_framework_versions (version_name, description, is_active)
            VALUES (%s, %s, %s)
            RETURNING version_id
        """, (name, description, active))
        
        new_id = db.cursor.fetchone()[0]
        
        # Get current active version to copy from
        if active:
            # Find the previous active version (if any)
            db.cursor.execute("""
                SELECT framework_version_id 
                FROM spm_framework 
                GROUP BY framework_version_id 
                ORDER BY COUNT(*) DESC 
                LIMIT 1
            """)
            result = db.cursor.fetchone()
            
            if result:
                source_version = result[0]
                # Copy entries from previous version to new version
                db.cursor.execute("""
                    INSERT INTO spm_framework (
                        framework_version_id, version, spm_process, spm_category, 
                        spm_component, spm_keyword, spm_definition, spm_user_type, 
                        spm_prompt, spm_complexity_level, spm_analysis_00, 
                        spm_analysis_01, spm_analysis_02, spm_analysis_03, 
                        spm_contextual_example, spm_traceability_code
                    )
                    SELECT 
                        %s, version, spm_process, spm_category, 
                        spm_component, spm_keyword, spm_definition, spm_user_type, 
                        spm_prompt, spm_complexity_level, spm_analysis_00, 
                        spm_analysis_01, spm_analysis_02, spm_analysis_03, 
                        spm_contextual_example, spm_traceability_code
                    FROM spm_framework
                    WHERE framework_version_id = %s
                """, (new_id, source_version))
                
                # Get count of copied entries
                db.cursor.execute("""
                    SELECT COUNT(*) FROM spm_framework WHERE framework_version_id = %s
                """, (new_id,))
                
                entry_count = db.cursor.fetchone()[0]
                print(f"✅ Copied {entry_count} entries from previous version")
        
        # Commit transaction
        db.conn.commit()
        print(f"✅ Created new framework version: {name} (ID: {new_id})")
        if active:
            print("✅ This is now the active version")
        
    except Exception as e:
        db.conn.rollback()
        logger.error(f"Error creating version: {e}")
    finally:
        db.conn.autocommit = True
        db.close_connection()

def activate_version(version_id):
    """Set a version as the active version"""
    db = DBManager()
    try:
        # Check if version exists
        db.cursor.execute("""
            SELECT version_name FROM spm_framework_versions WHERE version_id = %s
        """, (version_id,))
        
        result = db.cursor.fetchone()
        if not result:
            print(f"❌ Version ID {version_id} not found")
            return
            
        version_name = result[0]
        
        # Start transaction
        db.conn.autocommit = False
        
        # Set all versions to inactive
        db.cursor.execute("""
            UPDATE spm_framework_versions SET is_active = FALSE
        """)
        
        # Set requested version to active
        db.cursor.execute("""
            UPDATE spm_framework_versions SET is_active = TRUE WHERE version_id = %s
        """, (version_id,))
        
        # Commit transaction
        db.conn.commit()
        print(f"✅ Version {version_name} (ID: {version_id}) is now active")
        
    except Exception as e:
        db.conn.rollback()
        logger.error(f"Error activating version: {e}")
    finally:
        db.conn.autocommit = True
        db.close_connection()

def fix_typo():
    """Fix the 'Inisghts' typo in all framework versions"""
    db = DBManager()
    try:
        # Check if there are entries with the typo
        db.cursor.execute("""
            SELECT COUNT(*) FROM spm_framework WHERE spm_category LIKE '%Inisghts%'
        """)
        
        count = db.cursor.fetchone()[0]
        if count == 0:
            print("No typos found in spm_category field.")
            return
        
        # Update the field
        db.cursor.execute("""
            UPDATE spm_framework 
            SET spm_category = REPLACE(spm_category, 'Inisghts', 'Insights')
            WHERE spm_category LIKE '%Inisghts%'
        """)
        
        print(f"✅ Fixed 'Inisghts' typo in {count} records")
        db.conn.commit()
        
    except Exception as e:
        logger.error(f"Error fixing typo: {e}")
    finally:
        db.close_connection()

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="SPM Framework Version Manager")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # List command
    list_parser = subparsers.add_parser("list", help="List all versions")
    
    # Create command
    create_parser = subparsers.add_parser("create", help="Create a new version")
    create_parser.add_argument("name", help="Version name (e.g., 'v2.0')")
    create_parser.add_argument("--description", "-d", help="Version description")
    create_parser.add_argument("--active", "-a", action="store_true", help="Set as active version")
    
    # Activate command
    activate_parser = subparsers.add_parser("activate", help="Set a version as active")
    activate_parser.add_argument("version_id", type=int, help="Version ID to activate")
    
    # Fix typo command
    fix_parser = subparsers.add_parser("fix-typo", help="Fix the 'Inisghts' typo")
    
    args = parser.parse_args()
    
    if args.command == "list":
        list_versions()
    elif args.command == "create":
        create_version(args.name, args.description, args.active)
    elif args.command == "activate":
        activate_version(args.version_id)
    elif args.command == "fix-typo":
        fix_typo()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()