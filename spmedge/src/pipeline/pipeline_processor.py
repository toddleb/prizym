#!/usr/bin/env python3
"""
Pipeline Processor - Manages document processing across pipeline stages.
- Ensures consistent file naming and tracking
- Manages document metadata updates in the database
- Handles batch processing and error tracking
"""

import os
import re
import json
import logging
from enum import Enum
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, List, Tuple
from config.config import config
from src.pipeline.db_integration import DBManager

# Ensure logs directory exists
os.makedirs(config.LOG_DIR, exist_ok=True)

LOG_FILE = os.path.join(config.LOG_DIR, "pipeline_processor_debug.log")

# Create module-level logger WITHOUT using basicConfig
logger = logging.getLogger("pipeline_processor")
logger.propagate = False  # CRITICAL - prevent propagation to root logger

# Only configure if not already configured
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

class PipelineStage(Enum):
    """Enumeration of pipeline processing stages."""
    INPUT = "input"
    LOAD = "load"
    CLEAN = "clean"
    ANALYZE = "analyze"
    PROCESS = "process"
    EXTRACT = "extract"
    STRUCTURE = "structure"
    REPORT = "report"

class PipelineProcessor:
    """Handles document processing at various pipeline stages."""
    
    def __init__(self, stage: PipelineStage, stage_config: Dict[str, Any] = None):
        """
        Initializes the processor for a specific pipeline stage.
        
        Args:
            stage: The current pipeline stage (Enum).
            stage_config: Optional configuration for the stage.
        """
        self.stage = stage
        self.stage_name = stage.value
        self.stage_config = stage_config or {}
        self.db_manager = DBManager()
        self.datetime = datetime  # Expose datetime for timestamping
        
        # Setup logging for this processor instance
        self.logger = logging.getLogger(f"pipeline_{self.stage_name}")
        
        # CRITICAL - prevent propagation to parent loggers
        self.logger.propagate = False
        
        # Only add handlers if they don't exist
        if not self.logger.handlers:
            formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
            
            # Console handler
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)
            
            # File handler
            log_file = os.path.join(config.LOG_DIR, f"pipeline_{self.stage_name}_debug.log")
            file_handler = logging.FileHandler(log_file, encoding="utf-8")
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)
            
            self.logger.setLevel(logging.INFO)
            
    @staticmethod
    def get_base_dirs() -> Dict[str, Path]:
        """Returns base directories used in pipeline processing."""
        base_dir = Path(config.DATA_DIR)
        
        dirs = {
            # Main directories
            "unprocessed": Path(config.UNPROCESSED_DOCS_DIR),
            "input": Path(config.NEW_DOCS_DIR),  # Keep for backward compatibility
            "processed": Path(config.PROCESSED_DOCS_DIR),
            "storage": Path(config.STORAGE_DIR),
            "archive": Path(config.ARCHIVE_DIR),
            "knowledge": Path(config.KNOWLEDGE_FILES_DIR),
            "logs": Path(config.LOG_DIR),
            "reports": Path(config.REPORTS_DIR),
            "reports_md": Path(config.REPORTS_MD_DIR),
            "reports_json": Path(config.REPORTS_JSON_DIR),
            "reports_raw_json": Path(config.REPORTS_DIR) / "json" / "raw_json",
            
            # Stage-specific directories
            "stage_input": base_dir / "stage_input",
            "stage_load": base_dir / "stage_load",
            "stage_clean": base_dir / "stage_clean",
            "stage_process": base_dir / "stage_process",
            "stage_knowledge": base_dir / "stage_knowledge",
            "stage_report": base_dir / "stage_report",
        }
    
        # Ensure all directories exist
        for dir_path in dirs.values():
            dir_path.mkdir(parents=True, exist_ok=True)
    
        return dirs

    def generate_stage_filename(self, original_filename: str, document_id: str = None, batch_id: str = None) -> str:
        """
        Generates a standardized filename for the pipeline stage.

        Args:
            original_filename: Original document filename.
            document_id: Optional document identifier.
            batch_id: Optional batch identifier.

        Returns:
            A filename string following the pipeline convention.
        """
        base_name = Path(original_filename).stem
        extension = Path(original_filename).suffix

        # Clean and sanitize filename
        base_name = self._sanitize_filename(base_name)

        # Timestamp for tracking
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Construct filename with stage, document ID, and batch ID
        parts = ["pipeline", self.stage_name]
        if document_id:
            doc_id_short = str(document_id).replace('-', '')[:12]
            parts.append(f"doc{doc_id_short}")
        if batch_id:
            parts.append(f"batch{batch_id}")
        parts.append(base_name)
        parts.append(timestamp)

        return "_".join(parts) + extension

    @staticmethod
    def _sanitize_filename(filename: str) -> str:
        """Removes special characters and enforces filename length limits."""
        filename = filename.replace(" ", "_")
        filename = re.sub(r"[^\w\-_.]", "", filename)  # Keep alphanumeric, underscore, dash
        return filename[:100]  # Truncate if filename is too long
            
    def save_document_batch(self, documents: List[Dict[str, Any]], batch_name: str = None) -> Optional[Path]:
        """
        Saves a batch of documents to a JSON file with consistent naming.
    
        Args:
            documents: List of document dictionaries.
            batch_name: Optional batch name for the file.
    
        Returns:
            Path to the saved batch file.
        """
        try:
            # Generate timestamp for batch
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
            # Generate batch name if not provided
            if not batch_name:
                batch_name = f"batch_{timestamp}"
    
            # Create filename
            filename = f"pipeline_{self.stage_name}_{batch_name}.json"
    
            # Determine output path
            dirs = self.get_base_dirs()
            output_path = dirs["processed"] / filename
    
            # Ensure directory exists
            output_path.parent.mkdir(parents=True, exist_ok=True)
    
            # Add pipeline stage to each document
            for doc in documents:
                doc["pipeline_stage"] = self.stage_name
                doc["processed_at"] = datetime.now().isoformat()  # Add timestamp
    
            # Save to file
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(documents, f, indent=2, ensure_ascii=False)
    
            self.logger.info(f"✅ Saved {len(documents)} documents to {output_path}")
    
            return output_path
    
        except Exception as e:
            self.logger.error(f"❌ Failed to save document batch: {e}")
            return None
            
    def record_batch_processing(self, batch_name: str, document_count: int, status: str = "processing") -> Optional[str]:
        """
        Records a batch processing entry in the database.
        
        Args:
            batch_name: Name of the batch.
            document_count: Number of documents in the batch.
            status: Processing status.
        
        Returns:
            The batch ID if successful, else None.
        """
        try:
            self.db_manager.cursor.execute("""
                INSERT INTO processing_batches (batch_name, document_count, created_at, status, pipeline_stage)
                VALUES (%s, %s, NOW(), %s, %s) RETURNING batch_id;
            """, (batch_name, document_count, status, self.stage_name))
            
            batch_id = self.db_manager.cursor.fetchone()[0]
            self.db_manager.conn.commit()
            
            self.logger.info(f"✅ Created processing batch record with ID: {batch_id}")
            return str(batch_id)
        
        except Exception as e:
            self.logger.error(f"❌ Failed to record batch processing: {e}")
            self.db_manager.conn.rollback()
            return None
            
    def load_document_batch(self, batch_file: Path) -> List[Dict[str, Any]]:
        """
        Loads a batch of documents from a JSON file.
    
        Args:
            batch_file: Path to the batch file.
    
        Returns:
            A list of document dictionaries. If loading fails, returns an empty list.
        """
        try:
            if not batch_file.exists():
                self.logger.error(f"❌ Batch file not found: {batch_file}")
                return []
    
            with open(batch_file, "r", encoding="utf-8") as f:
                data = json.load(f)
    
            # Ensure data is a list of documents
            if isinstance(data, list):
                self.logger.info(f"✅ Loaded {len(data)} documents from batch file: {batch_file}")
                return data
            elif isinstance(data, dict):  # If a single document is mistakenly stored as a dict
                self.logger.warning(f"⚠️ Batch file {batch_file} contains a single document, wrapping in a list.")
                return [data]
            else:
                self.logger.error(f"❌ Invalid format in batch file {batch_file}, expected list or dict.")
                return []
    
        except json.JSONDecodeError as e:
            self.logger.error(f"❌ JSON decoding error in batch file {batch_file}: {e}")
            return []
        except Exception as e:
            self.logger.error(f"❌ Failed to load batch file {batch_file}: {e}")
            return []
            
    def get_documents_for_stage(self, current_stage: str, status: str = "completed", limit: int = 500) -> List[Dict[str, Any]]:
        """
        Retrieves documents that have completed the specified pipeline stage.
        
        Args:
            current_stage: The pipeline stage to filter by.
            status: Document status to filter (default is 'completed').
            limit: Maximum number of documents to return.
    
        Returns:
            A list of document dictionaries.
        """
        try:
            self.db_manager.cursor.execute("""
                SELECT d.id, d.name, d.metadata, d.document_type_id, d.batch_id 
                FROM documents d
                JOIN processing_pipeline pp ON d.id = pp.document_id
                WHERE pp.pipeline_stage = %s AND pp.status = %s
                AND NOT EXISTS (
                  SELECT 1 FROM processing_pipeline sub
                  WHERE sub.document_id = d.id AND sub.pipeline_stage = 'rag'
                )
                LIMIT %s;
            """, (current_stage, status, limit))
    
            results = self.db_manager.cursor.fetchall()
    
            if not results:
                self.logger.info(f"ℹ️ No documents found for stage: {current_stage}")
                return []
    
            # Convert query results into a list of dictionaries
            documents = []
            for row in results:
                documents.append({
                    "id": row[0],
                    "name": row[1],
                    "metadata": row[2],
                    "document_type_id": row[3],
                    "batch_id": row[4]
                })
    
            self.logger.info(f"✅ Found {len(documents)} documents ready for {current_stage} stage")
            return documents
    
        except Exception as e:
            self.logger.error(f"❌ Failed to fetch documents for stage {current_stage}: {e}")
            self.db_manager.conn.rollback()
            return []
            
    def update_pipeline_status(self, document_id: str, pipeline_stage: str, status: str, error_message: Optional[str] = None):
        """Update document processing status in the pipeline."""
        try:
            # ✅ Ensure document_type_id is retrieved and set
            self.cursor.execute("SELECT document_type_id FROM documents WHERE id = %s;", (document_id,))
            result = self.cursor.fetchone()
            document_type_id = result[0] if result else None
    
            if not document_type_id:
                logger.error(f"❌ Cannot update pipeline: document_type_id is NULL for document {document_id}")
                return
    
            query = """
                INSERT INTO processing_pipeline (document_id, document_type_id, pipeline_stage, status, error_message, batch_id, updated_at)
                VALUES (%s, %s, %s, %s, %s, (SELECT batch_id FROM documents WHERE id = %s), NOW())
                ON CONFLICT (document_id, pipeline_stage) DO UPDATE 
                SET status = EXCLUDED.status, error_message = EXCLUDED.error_message, updated_at = NOW();
            """
            self.cursor.execute(query, (document_id, document_type_id, pipeline_stage, status, error_message, document_id))
            self.conn.commit()
            logger.info(f"✅ Updated pipeline status: {document_id} | {pipeline_stage} → {status}")
    
        except Exception as e:
            logger.error(f"❌ Error updating pipeline status: {e}")
            self.conn.rollback()
        
    def reset_pipeline_stage(self, stage: str, batch_id: str = None):
        """
        Reset a specific pipeline stage, optionally for a specific batch.
        
        Args:
            stage: Pipeline stage to reset
            batch_id: Optional batch ID to limit reset scope
            
        Returns:
            bool: Success or failure
        """
        try:
            query = "DELETE FROM processing_pipeline WHERE pipeline_stage = %s"
            params = [stage]
            
            if batch_id:
                query += " AND batch_id = %s"
                params.append(batch_id)
                
            self.db_manager.cursor.execute(query, params)
            self.db_manager.conn.commit()
            self.logger.info(f"✅ Reset pipeline stage: {stage}" + (f" for batch {batch_id}" if batch_id else ""))
            
            # Also delete any stage files if needed
            if self.stage_name == stage:
                dirs = self.get_base_dirs()
                stage_dir = dirs.get(f"stage_{stage}")
                
                if stage_dir and stage_dir.exists():
                    # If batch_id is specified, only delete matching files
                    if batch_id:
                        import glob
                        pattern = f"*batch{batch_id}*"
                        for file_path in stage_dir.glob(pattern):
                            file_path.unlink()
                        self.logger.info(f"✅ Deleted files matching pattern {pattern} from {stage_dir}")
                    else:
                        # Otherwise, clear the entire directory
                        import shutil
                        for file_path in stage_dir.glob("*"):
                            if file_path.is_file():
                                file_path.unlink()
                        self.logger.info(f"✅ Cleared all files from {stage_dir}")
            
            return True
        except Exception as e:
            self.logger.error(f"❌ Failed to reset pipeline stage {stage}: {e}")
            self.db_manager.conn.rollback()
            return False
    
    def cleanup_orphaned_documents(self):
        """
        Clean up orphaned documents that have no pipeline entries.
        
        Returns:
            int: Number of documents cleaned up
        """
        try:
            # Find documents with no pipeline entries
            self.db_manager.cursor.execute("""
                DELETE FROM documents d
                WHERE NOT EXISTS (
                    SELECT 1 FROM processing_pipeline p 
                    WHERE p.document_id = d.id
                )
                RETURNING id, name;
            """)
            
            deleted = self.db_manager.cursor.fetchall()
            count = len(deleted)
            
            if count > 0:
                self.db_manager.conn.commit()
                self.logger.info(f"✅ Cleaned up {count} orphaned documents")
                for doc_id, name in deleted:
                    self.logger.debug(f"Deleted orphaned document: {doc_id} ({name})")
            else:
                self.logger.info("No orphaned documents found")
                
            return count
        except Exception as e:
            self.logger.error(f"❌ Failed to clean up orphaned documents: {e}")
            self.db_manager.conn.rollback()
            return 0
    
    def get_batch_status(self, batch_id: str) -> dict:
        """
        Get detailed status information for a specific batch.
        
        Args:
            batch_id: The batch ID to check
            
        Returns:
            dict: Batch status information
        """
        try:
            # Get batch info
            self.db_manager.cursor.execute("""
                SELECT batch_id, batch_name, document_count, status, created_at, completed_at
                FROM processing_batches
                WHERE batch_id = %s
            """, (batch_id,))
            
            batch = self.db_manager.cursor.fetchone()
            if not batch:
                self.logger.warning(f"⚠️ Batch {batch_id} not found")
                return None
                
            # Get document counts by pipeline stage
            self.db_manager.cursor.execute("""
                SELECT pipeline_stage, status, COUNT(*) 
                FROM processing_pipeline
                WHERE batch_id = %s
                GROUP BY pipeline_stage, status
                ORDER BY pipeline_stage, status
            """, (batch_id,))
            
            stage_counts = self.db_manager.cursor.fetchall()
            
            # Compile results
            result = {
                "batch_id": batch[0],
                "batch_name": batch[1],
                "document_count": batch[2],
                "status": batch[3],
                "created_at": batch[4],
                "completed_at": batch[5],
                "pipeline_stages": {}
            }
            
            # Organize pipeline stage data
            for stage, status, count in stage_counts:
                if stage not in result["pipeline_stages"]:
                    result["pipeline_stages"][stage] = {}
                result["pipeline_stages"][stage][status] = count
                
            return result
            
        except Exception as e:
            self.logger.error(f"❌ Failed to get batch status: {e}")
            return None
            
    def finalize_batch(self, batch_id: str, status: str = "completed"):
        """
        Mark a batch as finalized in the database.
        
        Args:
            batch_id: The batch ID to finalize
            status: Status to set (completed, failed, etc.)
            
        Returns:
            bool: Success or failure
        """
        try:
            self.db_manager.cursor.execute(
                "UPDATE processing_batches SET status = %s, completed_at = NOW() WHERE batch_id = %s;",
                (status, batch_id)
            )
            self.db_manager.conn.commit()
            self.logger.info(f"✅ Batch {batch_id} finalized with status: {status}")
            return True
        except Exception as e:
            self.logger.error(f"❌ Failed to finalize batch {batch_id}: {e}")
            self.db_manager.conn.rollback()
            return False
    
    def update_document_stage(self, document_id: str, status: str = "pending", error_message: str = None, batch_id: str = None, document_type_id: str = None):
        """Ensures the document is properly updated in the processing pipeline, inserting it first if necessary."""
        try:
            # If document_type_id was not provided, try to retrieve it
            if document_type_id is None:
                self.db_manager.cursor.execute("SELECT document_type_id FROM documents WHERE id = %s;", (document_id,))
                result = self.db_manager.cursor.fetchone()
                if not result or result[0] is None:
                    self.logger.error(f"❌ Cannot update pipeline: document_type_id is NULL for document {document_id}")
                    return
                document_type_id = result[0]
    
            # Check if an entry already exists in processing_pipeline
            self.db_manager.cursor.execute(
                "SELECT 1 FROM processing_pipeline WHERE document_id = %s AND pipeline_stage = %s;",
                (document_id, self.stage_name)
            )
    
            if self.db_manager.cursor.fetchone() is None:
                # No entry exists, insert it
                self.db_manager.cursor.execute(
                    """
                    INSERT INTO processing_pipeline 
                    (document_id, document_type_id, pipeline_stage, status, error_message, batch_id, updated_at)
                    VALUES (%s, %s, %s, %s, %s, %s, NOW());
                    """,
                    (document_id, document_type_id, self.stage_name, status, error_message, batch_id)
                )
                self.logger.info(f"✅ Inserted new pipeline entry for {document_id} in stage {self.stage_name}")
            else:
                # Entry exists, update it
                self.db_manager.cursor.execute(
                    """
                    UPDATE processing_pipeline 
                    SET status = %s, error_message = %s, updated_at = NOW()
                    WHERE document_id = %s AND pipeline_stage = %s;
                    """,
                    (status, error_message, document_id, self.stage_name)
                )
                self.logger.info(f"✅ Updated existing pipeline entry for {document_id} in stage {self.stage_name}")
    
            self.db_manager.conn.commit()
    
        except Exception as e:
            self.logger.error(f"❌ Error updating document {document_id} in pipeline: {e}")
            self.db_manager.conn.rollback()
            
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

def main():
    """Main entry point for document processing."""
    parser = argparse.ArgumentParser(description="Document Processor - Extract structured data with OpenAI")
    parser.add_argument("--limit", "-l", type=int, default=None, 
                        help="Max documents to process (overrides DB setting)")
    parser.add_argument("--model", "-m", type=str, default=None, 
                        help="OpenAI model to use")
    parser.add_argument("--batch-size", "-b", type=int, default=2, 
                        help="Number of documents per API batch (for rate limiting)")
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
    default_limit = 10  # Smaller default for processor due to API costs
    
    # Command line overrides DB setting
    if args.limit is not None:
        batch_size = args.limit
        logger.info(f"Using command line batch size: {batch_size}")
    else:
        batch_size = get_batch_size_from_settings(db_manager, default_limit)
    
    # API sub-batch size (how many docs to process in one batch to avoid rate limits)
    api_batch_size = args.batch_size
    
    process_documents(limit=batch_size, model=args.model, batch_size=api_batch_size)