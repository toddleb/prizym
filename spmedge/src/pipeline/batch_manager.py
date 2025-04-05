#!/usr/bin/env python3
"""
Batch Manager - Manages document batches by type and initializes processing pipeline.
- Processes documents from unprocessed directory
- Requires document type specification
- Standardizes file naming and organization
- Registers documents in the database
- Prepares batches for the document loader stage
- Provides pipeline management and reset capabilities
"""

import os
import sys
import json
import logging
import argparse
import shutil
import re
import time
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Dict, Any, Tuple

# Fix the import path issue - use absolute imports
sys.path.insert(0, '/Users/toddlebaron/prizym/spmedge')

# Now import using the absolute path
from config.config import config
from src.pipeline.db_integration import DBManager
from src.pipeline.pipeline_processor import PipelineProcessor, PipelineStage

# Ensure logs directory exists
LOG_DIR = config.LOG_DIR
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "batch_manager.log")

# Configure logging
logger = logging.getLogger("batch_manager")
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

class BatchManager:
    """Manages document batches by type and initializes processing pipeline."""
    
    def __init__(self):
        """Initialize BatchManager with database connection and processor."""
        self.db_manager = DBManager()
        self.processor = PipelineProcessor(PipelineStage.INPUT)
        
    # Add batch_size parameter to the run_pipeline function in batch_manager.py
    def run_pipeline(self, doc_type: str, batch_size: int = 500):
        """
        Run the complete pipeline for a document type.
        
        Args:
            doc_type: Document type to process
            batch_size: Maximum number of documents to process in each stage
        """
        try:
            # Process the batch
            batch_id = self.process_document_batch(doc_type)
            
            if not batch_id:
                self.logger.warning("⚠️ Batch processing failed, cannot continue pipeline")
                return False
            
            # Store batch size in the database for other pipeline components to use
            self.db_manager.cursor.execute(
                """
                INSERT INTO pipeline_settings (key, value, updated_at)
                VALUES ('batch.size', %s, NOW())
                ON CONFLICT (key) DO UPDATE 
                SET value = EXCLUDED.value, updated_at = NOW();
                """, 
                (str(batch_size),)
            )
            self.db_manager.conn.commit()
            
            # Call document loader with the batch size
            loader_cmd = f"{config.PYTHON_PATH} src/pipeline/document_loader.py --limit {batch_size}"
            self.logger.info(f"Running document loader with batch size: {batch_size}")
            # Execute loader
            # ... existing code ...
            
            # Call document cleaner with the same batch size
            cleaner_cmd = f"{config.PYTHON_PATH} src/pipeline/document_cleaner.py --limit {batch_size}"
            self.logger.info(f"Running document cleaner with batch size: {batch_size}")
            # Execute cleaner
            # ... existing code ...
            
            # Continue with other pipeline stages, passing the batch size
            # ... existing code ...
            
            return True
        except Exception as e:
            self.logger.error(f"❌ Pipeline execution failed: {e}")
            return False
    
    # Update the run_pipeline function in pipeline.sh to accept the batch_size parameter
    
    def sanitize_filename(self, filename: str) -> str:
        """Clean and standardize filenames for processing."""
        # Get base name and extension
        base_name = Path(filename).stem
        extension = Path(filename).suffix
        
        # Remove special characters, replace spaces with underscores
        clean_name = re.sub(r'[^\w\-\.]', '_', base_name)
        # Remove multiple underscores
        clean_name = re.sub(r'_+', '_', clean_name)
        # Limit length
        clean_name = clean_name[:100]
        
        return f"{clean_name}{extension}"
    
    def verify_document_type(self, doc_type: str) -> int:
        """Verify document type exists in database and return its ID."""
        try:
            # Check if document type exists
            self.db_manager.cursor.execute("SELECT id FROM document_types WHERE name = %s;", (doc_type,))
            result = self.db_manager.cursor.fetchone()
            
            if not result:
                logger.error(f"❌ Invalid document type: {doc_type}")
                raise ValueError(f"Document type '{doc_type}' does not exist in the database")
            
            return result[0]  # Return document type ID
            
        except Exception as e:
            logger.error(f"❌ Error verifying document type: {e}")
            raise
    
    def process_single_document(self, file_path: Path, doc_type: str, doc_type_id: int, 
                               batch_id: str, stage_input_dir: Path, archive_dir: Path, 
                               archive: bool = False, delete: bool = False) -> Optional[Dict[str, Any]]:
        """Process a single document with minimal transformation."""
        start_time = time.time()
        
        try:
            # Get basic file metadata
            file_size = file_path.stat().st_size
            file_ext = file_path.suffix.lower()[1:]  # Remove the leading dot
            creation_time = datetime.fromtimestamp(os.path.getctime(file_path))
            modification_time = datetime.fromtimestamp(os.path.getmtime(file_path))
            
            # Clean and standardize filename
            clean_filename = self.sanitize_filename(file_path.name)
            
            # Register in database
            self.db_manager.cursor.execute(
                """
                INSERT INTO documents 
                (id, name, original_filename, document_type_id, batch_id, file_size, file_type) 
                VALUES (gen_random_uuid(), %s, %s, %s, %s, %s, %s) 
                RETURNING id;
                """,
                (clean_filename, file_path.name, doc_type_id, batch_id, file_size, file_ext)
            )
            document_id = self.db_manager.cursor.fetchone()[0]
            self.db_manager.conn.commit()
            
            logger.info(f"✅ Registered document {document_id}: {clean_filename} (originally {file_path.name})")
            
            # Copy file to stage_input directory
            stage_file_path = stage_input_dir / clean_filename
            shutil.copy2(str(file_path), str(stage_file_path))
            logger.info(f"📁 Copied to stage directory: {stage_file_path}")
            
            # Create a small metadata JSON with just registration info
            metadata_path = stage_input_dir / f"{Path(clean_filename).stem}.meta.json"
            metadata = {
                "document_id": document_id,
                "original_filename": file_path.name,
                "file_type": file_ext,
                "file_size": file_size,
                "creation_time": creation_time.isoformat(),
                "modification_time": modification_time.isoformat(),
                "document_type": doc_type,
                "document_type_id": doc_type_id,
                "registration_time": datetime.now().isoformat(),
                "batch_id": batch_id,
                "processing_time": round(time.time() - start_time, 3)
            }
            
            with open(metadata_path, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2)
            logger.info(f"📄 Created metadata file: {metadata_path}")
            
            # Handle original file based on options
            if archive:
                archive_path = archive_dir / file_path.name
                shutil.copy2(str(file_path), str(archive_path))
                logger.info(f"📦 Archived original file to: {archive_path}")
    
            if delete or archive:  # If archived, we can also delete
                os.unlink(str(file_path))
                logger.info(f"🗑️ Deleted original file: {file_path}")
            
            # Return document metadata
            processing_time = time.time() - start_time
            return {
                "id": document_id,
                "name": clean_filename,
                "original_filename": file_path.name,
                "file_path": str(stage_file_path),
                "file_size": file_size,
                "file_type": file_ext,
                "document_type_id": doc_type_id,
                "document_type": doc_type,
                "status": "completed",
                "processing_time": processing_time,
                "created_at": datetime.now().isoformat()
            }
    
        except Exception as e:
            logger.error(f"❌ Failed to process {file_path.name}: {e}")
            return None
                                
    def update_pipeline_entries(self, processed_documents: List[Dict[str, Any]], batch_id: str, document_type_id: int):
        """
        Update pipeline entries for multiple documents in a separate transaction.
        
        Args:
            processed_documents: List of document dictionaries
            batch_id: The batch ID
            document_type_id: The document type ID
        
        Returns:
            int: Number of successful updates
        """
        success_count = 0
        
        # Create a separate cursor for this operation
        connection = self.db_manager.conn
        previous_autocommit = connection.autocommit
        connection.autocommit = True
        
        try:
            cursor = connection.cursor()
            
            for doc in processed_documents:
                try:
                    document_id = doc["id"]
                    # Insert pipeline entry
                    cursor.execute(
                        """
                        INSERT INTO processing_pipeline 
                        (document_id, document_type_id, pipeline_stage, status, batch_id, updated_at)
                        VALUES (%s, %s, %s, %s, %s, NOW())
                        ON CONFLICT (document_id, pipeline_stage) 
                        DO UPDATE SET status = EXCLUDED.status, updated_at = NOW();
                        """,
                        (document_id, document_type_id, "input", "completed", batch_id)
                    )
                    success_count += 1
                except Exception as e:
                    logger.error(f"❌ Failed to update pipeline for document {doc.get('id')}: {e}")
                    # Continue with next document
            
            logger.info(f"✅ Updated pipeline entries for {success_count} of {len(processed_documents)} documents")
            return success_count
            
        finally:
            # Restore autocommit mode
            connection.autocommit = previous_autocommit
    
    def process_document_batch(self, doc_type: str, archive: bool = False, delete: bool = False) -> Optional[str]:
        """
        Process a batch of documents of the specified type.

        Args:
            doc_type: Document type for this batch
            archive: Whether to archive original files
            delete: Whether to delete original files

        Returns:
            str: Batch ID if successful, None otherwise
        """
        if not doc_type:
            logger.error("❌ Document type must be specified!")
            return None

        batch_id = None

        try:
            # Verify document type exists in database
            document_type_id = self.verify_document_type(doc_type)

            # Get directories
            dirs = self.processor.get_base_dirs()
            unprocessed_dir = dirs["unprocessed"]
            stage_input_dir = dirs["stage_input"]
            archive_dir = dirs["archive"]

            # Ensure directories exist
            unprocessed_dir.mkdir(parents=True, exist_ok=True)
            stage_input_dir.mkdir(parents=True, exist_ok=True)
            archive_dir.mkdir(parents=True, exist_ok=True)

            # Find files in unprocessed directory
            files = list(unprocessed_dir.glob("*.*"))

            if not files:
                logger.info("ℹ️ No documents found in unprocessed directory.")
                return None

            logger.info(f"🔍 Found {len(files)} documents in: {unprocessed_dir}")

            # Create batch with auto-commit to ensure it's available
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            batch_name = f"batch_{doc_type}_{timestamp}"
            batch_id = self.processor.record_batch_processing(
                batch_name=batch_name,
                document_count=len(files),
                status="processing"
            )
            
            # Create a batch summary file
            batch_summary = {
                "batch_id": batch_id,
                "batch_name": batch_name,
                "document_type": doc_type,
                "document_count": len(files),
                "created_at": datetime.now().isoformat(),
                "status": "processing",
                "file_types": {}
            }
            
            processed_documents = []
            success_count = 0
            total_size = 0
            file_types = {}

            # Process each document individually
            for file_path in files:
                doc_metadata = self.process_single_document(
                    file_path=file_path,
                    doc_type=doc_type,
                    doc_type_id=document_type_id,
                    batch_id=batch_id,
                    stage_input_dir=stage_input_dir,
                    archive_dir=archive_dir,
                    archive=archive,
                    delete=delete
                )
                
                if doc_metadata:
                    processed_documents.append(doc_metadata)
                    success_count += 1
                    
                    # Update batch statistics
                    total_size += doc_metadata.get("file_size", 0)
                    file_type = doc_metadata.get("file_type", "unknown")
                    file_types[file_type] = file_types.get(file_type, 0) + 1

            # If we have processed documents, save batch metadata
            if processed_documents:
                # Update batch summary
                batch_summary["file_types"] = file_types
                batch_summary["total_size_bytes"] = total_size
                batch_summary["success_count"] = success_count
                batch_summary["average_size_bytes"] = round(total_size / success_count) if success_count > 0 else 0
                
                # Save batch summary to stage input directory
                summary_path = stage_input_dir / f"batch_summary_{batch_id}.json"
                with open(summary_path, 'w', encoding='utf-8') as f:
                    json.dump(batch_summary, f, indent=2)
                
                # Save detailed document metadata
                self.processor.save_document_batch(documents=processed_documents, batch_name=batch_name)
                logger.info(f"🎉 Successfully processed {success_count} of {len(files)} documents of type '{doc_type}'")

                # Update pipeline entries
                pipeline_updates = self.update_pipeline_entries(
                    processed_documents=processed_documents,
                    batch_id=batch_id,
                    document_type_id=document_type_id
                )
                
                # Finalize batch status
                if success_count == len(files):
                    self.processor.finalize_batch(batch_id, "completed")
                    batch_summary["status"] = "completed"
                elif success_count > 0:
                    self.processor.finalize_batch(batch_id, "partial")
                    batch_summary["status"] = "partial"
                else:
                    self.processor.finalize_batch(batch_id, "failed")
                    batch_summary["status"] = "failed"
                    batch_id = None
                
                # Update summary file with final status
                with open(summary_path, 'w', encoding='utf-8') as f:
                    json.dump(batch_summary, f, indent=2)
            else:
                logger.warning("⚠️ No documents were successfully processed.")
                batch_id = None
                    
            logger.info("🏁 Batch processing complete")
            return batch_id

        except Exception as e:
            logger.error(f"❌ Batch processing failed: {e}")
            return None
    
    def reset_pipeline(self, stage: str = None, batch_id: str = None):
        """
        Reset the pipeline - either a specific stage or the entire pipeline.
        
        Args:
            stage: Specific stage to reset (None for all stages)
            batch_id: Optional batch ID to limit the reset scope
        
        Returns:
            bool: Success or failure
        """
        try:
            if batch_id:
                logger.info(f"Resetting pipeline for batch: {batch_id}")
            
            if stage:
                # Reset only the specified stage
                result = self.processor.reset_pipeline_stage(stage, batch_id)
                logger.info(f"✅ Reset pipeline stage: {stage}" + (f" for batch {batch_id}" if batch_id else ""))
            else:
                # Reset all stages in reverse order (to prevent foreign key issues)
                for s in ["report", "process", "clean", "load", "input"]:
                    self.processor.reset_pipeline_stage(s, batch_id)
                logger.info("✅ Reset entire pipeline" + (f" for batch {batch_id}" if batch_id else ""))
            
            if batch_id:
                # Keep track of autocommit state
                previous_autocommit = self.db_manager.conn.autocommit
                self.db_manager.conn.autocommit = False
                
                try:
                    # Delete the batch if no documents reference it
                    self.db_manager.cursor.execute(
                        "SELECT COUNT(*) FROM documents WHERE batch_id = %s;", 
                        (batch_id,)
                    )
                    doc_count = self.db_manager.cursor.fetchone()[0]
                    
                    if doc_count == 0:
                        # Safe to delete the batch
                        self.db_manager.cursor.execute(
                            "DELETE FROM processing_batches WHERE batch_id = %s;", 
                            (batch_id,)
                        )
                        self.db_manager.conn.commit()
                        logger.info(f"✅ Deleted batch: {batch_id}")
                    else:
                        logger.warning(f"⚠️ Batch {batch_id} still has {doc_count} documents, not deleting batch record")
                except Exception as e:
                    logger.error(f"❌ Failed to delete batch: {e}")
                    self.db_manager.conn.rollback()
                finally:
                    # Restore autocommit mode
                    self.db_manager.conn.autocommit = previous_autocommit
                    
            return True
        except Exception as e:
            logger.error(f"❌ Failed to reset pipeline: {e}")
            return False

    def list_active_batches(self):
        """List all active batches in the pipeline."""
        try:
            self.db_manager.cursor.execute("""
                SELECT b.batch_id, b.batch_name, b.document_count, b.status, b.created_at, b.completed_at,
                      (SELECT COUNT(*) FROM documents d WHERE d.batch_id = b.batch_id) as doc_count
                FROM processing_batches b
                WHERE b.status IN ('processing', 'partial')
                ORDER BY b.created_at DESC;
            """)
            
            batches = self.db_manager.cursor.fetchall()
            
            if not batches:
                logger.info("No active batches found")
                return
                
            logger.info("Active batches:")
            logger.info(f"{'ID':<36} | {'Batch Name':<30} | {'Status':<12} | {'Doc Count':<9} | {'Created At'}")
            logger.info("-" * 100)
            
            for batch in batches:
                batch_id = batch[0]
                batch_name = batch[1]
                status = batch[3]
                doc_count = batch[6]
                created_at = batch[4].strftime("%Y-%m-%d %H:%M") if batch[4] else "Unknown"
                
                logger.info(f"{batch_id:<36} | {batch_name:<30} | {status:<12} | {doc_count:<9} | {created_at}")
                
            # Also list counts by pipeline stage
            logger.info("\nPipeline stage document counts:")
            self.db_manager.cursor.execute("""
                SELECT pipeline_stage, status, COUNT(*)
                FROM processing_pipeline
                GROUP BY pipeline_stage, status
                ORDER BY pipeline_stage, status;
            """)
            
            stage_counts = self.db_manager.cursor.fetchall()
            
            if stage_counts:
                logger.info(f"{'Stage':<10} | {'Status':<12} | {'Count'}")
                logger.info("-" * 40)
                
                for stage, status, count in stage_counts:
                    logger.info(f"{stage:<10} | {status:<12} | {count}")
            
        except Exception as e:
            logger.error(f"❌ Failed to list active batches: {e}")

    def cleanup_orphans(self) -> Tuple[int, int]:
        """Clean up orphaned documents and records."""
        try:
            # Keep track of autocommit state
            previous_autocommit = self.db_manager.conn.autocommit
            self.db_manager.conn.autocommit = False
            
            try:
                # First, clean up documents with no pipeline entries
                doc_count = self.processor.cleanup_orphaned_documents()
                
                # Clean up empty batches
                self.db_manager.cursor.execute("""
                    DELETE FROM processing_batches pb
                    WHERE NOT EXISTS (
                        SELECT 1 FROM documents d
                        WHERE d.batch_id = pb.batch_id
                    )
                    RETURNING batch_id, batch_name;
                """)
                
                deleted_batches = self.db_manager.cursor.fetchall()
                batch_count = len(deleted_batches)
                
                if batch_count > 0:
                    logger.info(f"✅ Cleaned up {batch_count} orphaned batches")
                    for batch_id, name in deleted_batches:
                        logger.debug(f"Deleted orphaned batch: {batch_id} ({name})")
                
                self.db_manager.conn.commit()
                return doc_count, batch_count
            except Exception as e:
                logger.error(f"❌ Failed to clean up orphans: {e}")
                self.db_manager.conn.rollback()
                return 0, 0
            finally:
                # Restore autocommit mode
                self.db_manager.conn.autocommit = previous_autocommit
                
        except Exception as e:
            logger.error(f"❌ Failed to clean up orphans: {e}")
            return 0, 0

    def batch_status(self, batch_id: str):
        """Display detailed status for a specific batch."""
        status = self.processor.get_batch_status(batch_id)
        
        if not status:
            logger.error(f"❌ Batch {batch_id} not found or error occurred")
            return
            
        logger.info(f"Batch Status: {status['batch_name']} ({status['batch_id']})")
        logger.info(f"Status: {status['status']}")
        logger.info(f"Documents: {status['document_count']}")
        logger.info(f"Created: {status['created_at']}")
        
        if status['completed_at']:
            logger.info(f"Completed: {status['completed_at']}")
        
        logger.info("\nPipeline Stage Status:")
        
        if not status['pipeline_stages']:
            logger.info("No pipeline stage data found")
        else:
            for stage, stage_data in status['pipeline_stages'].items():
                stage_str = f"{stage}: "
                for status_name, count in stage_data.items():
                    stage_str += f"{status_name}={count} "
                logger.info(stage_str)

# Update the main function in batch_manager.py to accept a batch_size parameter

def main():
    """Main function to handle batch document processing."""
    batch_manager = BatchManager()
    
    parser = argparse.ArgumentParser(description="Batch Manager for Document Processing Pipeline")
    
    # Create subparsers for different commands
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # Process command
    process_parser = subparsers.add_parser("process", help="Process a batch of documents")
    process_parser.add_argument("doc_type", help="Document type to process (REQUIRED)")
    process_parser.add_argument("--archive", action="store_true", help="Archive original files after processing")
    process_parser.add_argument("--delete", action="store_true", help="Delete original files after processing")
    process_parser.add_argument("--batch-size", "-b", type=int, default=500, 
                               help="Batch size for document processing (default: 500)")
    
    # Run-all command
    run_all_parser = subparsers.add_parser("run-all", help="Run complete pipeline for a document type")
    run_all_parser.add_argument("doc_type", help="Document type to process (REQUIRED)")
    run_all_parser.add_argument("--batch-size", "-b", type=int, default=500, 
                               help="Batch size for document processing (default: 500)")
    
    # Reset command
    reset_parser = subparsers.add_parser("reset", help="Reset pipeline stages")
    reset_parser.add_argument("--stage", choices=["input", "load", "clean", "process", "report"], 
                              help="Specific stage to reset (omit for all stages)")
    reset_parser.add_argument("--batch", help="Specific batch ID to reset (optional)")
    
    # List command
    list_parser = subparsers.add_parser("list", help="List active batches")
    
    # Cleanup command
    cleanup_parser = subparsers.add_parser("cleanup", help="Clean up orphaned documents and batches")
    
    # Status command
    status_parser = subparsers.add_parser("status", help="Check status of a specific batch")
    status_parser.add_argument("batch_id", help="ID of the batch to check")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
        
    if args.command == "process":
        if not args.doc_type:
            process_parser.error("Document type is required")
            
        # Store batch size in settings
        batch_manager.db_manager.cursor.execute(
            """
            INSERT INTO pipeline_settings (key, value, description, updated_at)
            VALUES ('batch.size', %s, 'Maximum documents to process per pipeline stage', NOW())
            ON CONFLICT (key) DO UPDATE 
            SET value = EXCLUDED.value, updated_at = NOW();
            """, 
            (str(args.batch_size),)
        )
        batch_manager.db_manager.conn.commit()
        logger.info(f"Set batch size in pipeline settings: {args.batch_size}")
        
        # Process batch
        batch_manager.process_document_batch(args.doc_type, args.archive, args.delete)
    
    elif args.command == "run-all":
        if not args.doc_type:
            run_all_parser.error("Document type is required")
            
        # Store batch size in settings
        batch_manager.db_manager.cursor.execute(
            """
            INSERT INTO pipeline_settings (key, value, description, updated_at)
            VALUES ('batch.size', %s, 'Maximum documents to process per pipeline stage', NOW())
            ON CONFLICT (key) DO UPDATE 
            SET value = EXCLUDED.value, updated_at = NOW();
            """, 
            (str(args.batch_size),)
        )
        batch_manager.db_manager.conn.commit()
        logger.info(f"Set batch size in pipeline settings: {args.batch_size}")
        
        # Run pipeline
        batch_manager.run_pipeline(args.doc_type, args.batch_size)
    
    elif args.command == "reset":
        batch_manager.reset_pipeline(args.stage, args.batch)
    
    elif args.command == "list":
        batch_manager.list_active_batches()
    
    elif args.command == "cleanup":
        doc_count, batch_count = batch_manager.cleanup_orphans()
        logger.info(f"Cleanup completed: {doc_count} documents and {batch_count} batches removed")
    
    elif args.command == "status":
        batch_manager.batch_status(args.batch_id)
        
if __name__ == "__main__":
    main()