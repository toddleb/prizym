#!/usr/bin/env python3
"""
RAG Batch Processing - Extension for SPM RAG Integration
- Processes documents in controlled batches
- Tracks progress in the database
- Supports resuming and reprocessing
"""

import os
import sys
import time
import logging
import argparse
import uuid
from pathlib import Path
from datetime import datetime

# Add the project root to the Python path
project_root = str(Path(__file__).parent.parent.parent)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from config.config import config
from src.pipeline.pipeline_processor import PipelineProcessor, PipelineStage
from src.pipeline.db_integration import DBManager
from src.pipeline.spm_rag_integration import SPMRagIntegration

# Configure logging
logger = logging.getLogger("rag_batch")
logger.setLevel(logging.INFO)
logger.propagate = False

if not logger.handlers:
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler
    log_file = os.path.join(config.LOG_DIR, "rag_batch.log")
    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

class RAGBatchProcessor:
    """Processes documents in batches for RAG indexing with tracking."""
    
    def __init__(self):
        """Initialize the batch processor."""
        self.db_manager = DBManager()
        self.integration = SPMRagIntegration()
        
    def get_unprocessed_documents(self, stage: str, limit: int = 500) -> list:
        """Get unprocessed documents for RAG indexing."""
        try:
            self.db_manager.cursor.execute("""
                SELECT d.id, d.name
                FROM documents d
                JOIN processing_pipeline pp ON d.id = pp.document_id
                WHERE pp.pipeline_stage = %s 
                  AND pp.status = 'completed'
                  AND (d.rag_data IS NULL OR d.rag_data->>'indexed' IS NULL)
                ORDER BY d.id
                LIMIT %s;
            """, (stage, limit))
            
            results = self.db_manager.cursor.fetchall()
            return [(row[0], row[1]) for row in results]
            
        except Exception as e:
            logger.error(f"Error getting unprocessed documents: {e}")
            return []
    
    def mark_document_as_processed(self, document_id: str, chunk_count: int, batch_id: str) -> bool:
        """Mark a document as processed in the database."""
        try:
            self.db_manager.cursor.execute("""
                UPDATE documents
                SET rag_data = jsonb_build_object(
                    'indexed', true,
                    'indexed_at', NOW(),
                    'chunk_count', %s,
                    'rag_batch_id', %s
                )
                WHERE id = %s;
            """, (chunk_count, batch_id, document_id))
            
            self.db_manager.conn.commit()
            return True
            
        except Exception as e:
            logger.error(f"Error marking document {document_id} as processed: {e}")
            self.db_manager.conn.rollback()
            return False
    
    def get_batch_progress(self, batch_id: str = None) -> dict:
        """Get progress statistics for a batch or overall."""
        try:
            if batch_id:
                # Get stats for specific batch
                self.db_manager.cursor.execute("""
                    SELECT COUNT(*) as total,
                           SUM(CASE WHEN d.rag_data IS NOT NULL AND d.rag_data->>'indexed' = 'true' THEN 1 ELSE 0 END) as processed,
                           COALESCE(SUM((d.rag_data->>'chunk_count')::int), 0) as total_chunks
                    FROM documents d
                    WHERE d.rag_data->>'rag_batch_id' = %s;
                """, (batch_id,))
                
                row = self.db_manager.cursor.fetchone()
                batch_stats = {
                    "batch_id": batch_id,
                    "total_documents": row[0],
                    "processed_documents": row[1] or 0,
                    "total_chunks": row[2] or 0,
                    "progress_percentage": round((row[1] / row[0]) * 100 if row[0] > 0 else 0, 2)
                }
                
                return batch_stats
            else:
                # Get overall stats
                self.db_manager.cursor.execute("""
                    SELECT 
                        (SELECT COUNT(*) FROM documents) as total_documents,
                        COUNT(CASE WHEN d.rag_data IS NOT NULL AND d.rag_data->>'indexed' = 'true' THEN 1 END) as processed_documents,
                        COALESCE(SUM((d.rag_data->>'chunk_count')::int), 0) as total_chunks,
                        COUNT(DISTINCT d.rag_data->>'rag_batch_id') as batch_count
                    FROM documents d;
                """)
                
                row = self.db_manager.cursor.fetchone()
                
                # Get documents in clean stage
                self.db_manager.cursor.execute("""
                    SELECT COUNT(*)
                    FROM documents d
                    JOIN processing_pipeline pp ON d.id = pp.document_id
                    WHERE pp.pipeline_stage = 'clean' AND pp.status = 'completed';
                """)
                clean_docs = self.db_manager.cursor.fetchone()[0]
                
                # Get unprocessed documents in clean stage
                self.db_manager.cursor.execute("""
                    SELECT COUNT(*)
                    FROM documents d
                    JOIN processing_pipeline pp ON d.id = pp.document_id
                    WHERE pp.pipeline_stage = 'clean' 
                      AND pp.status = 'completed'
                      AND (d.rag_data IS NULL OR d.rag_data->>'indexed' IS NULL);
                """)
                unprocessed_docs = self.db_manager.cursor.fetchone()[0]
                
                return {
                    "total_documents": row[0],
                    "processed_documents": row[1] or 0,
                    "total_chunks": row[2] or 0,
                    "batch_count": row[3] or 0,
                    "clean_stage_documents": clean_docs,
                    "unprocessed_documents": unprocessed_docs,
                    "progress_percentage": round((row[1] / clean_docs) * 100 if clean_docs > 0 else 0, 2)
                }
                
        except Exception as e:
            logger.error(f"Error getting batch progress: {e}")
            return {}
    
    def list_batches(self) -> list:
        """List all RAG processing batches."""
        try:
            self.db_manager.cursor.execute("""
                SELECT DISTINCT rag_data->>'rag_batch_id' as batch_id,
                       MIN(rag_data->>'indexed_at') as started_at,
                       MAX(rag_data->>'indexed_at') as completed_at,
                       COUNT(*) as document_count,
                       COALESCE(SUM((rag_data->>'chunk_count')::int), 0) as chunk_count
                FROM documents
                WHERE rag_data IS NOT NULL AND rag_data->>'rag_batch_id' IS NOT NULL
                GROUP BY rag_data->>'rag_batch_id'
                ORDER BY MIN(rag_data->>'indexed_at') DESC;
            """)
            
            results = []
            for row in self.db_manager.cursor.fetchall():
                results.append({
                    "batch_id": row[0],
                    "started_at": row[1],
                    "completed_at": row[2],
                    "document_count": row[3],
                    "chunk_count": row[4]
                })
                
            return results
            
        except Exception as e:
            logger.error(f"Error listing batches: {e}")
            return []
    
    def clear_batch(self, batch_id: str) -> bool:
        """Clear a batch to allow reprocessing."""
        try:
            self.db_manager.cursor.execute("""
                UPDATE documents
                SET rag_data = NULL
                WHERE rag_data->>'rag_batch_id' = %s;
            """, (batch_id,))
            
            count = self.db_manager.cursor.rowcount
            self.db_manager.conn.commit()
            
            logger.info(f"Cleared {count} documents from batch {batch_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error clearing batch {batch_id}: {e}")
            self.db_manager.conn.rollback()
            return False
    
    def process_batch(self, stage: str, batch_size: int, batch_id: str = None, pause_seconds: int = 5) -> dict:
        """Process a batch of documents."""
        # Generate batch ID if not provided
        if not batch_id:
            batch_id = str(uuid.uuid4())
            
        logger.info(f"Starting batch {batch_id} with size {batch_size}")
        
        # Get documents to process
        documents = self.get_unprocessed_documents(stage, batch_size)
        
        if not documents:
            logger.info("No unprocessed documents found")
            return {"batch_id": batch_id, "processed": 0, "status": "completed", "message": "No documents to process"}
        
        logger.info(f"Found {len(documents)} documents to process")
        
        processed_count = 0
        failed_count = 0
        
        # Get the pipeline processor for the specified stage
        pipeline_stage = PipelineStage.CLEAN if stage == "clean" else PipelineStage.PROCESS
        processor = PipelineProcessor(pipeline_stage)
        stage_dir = processor.get_base_dirs()[f"stage_{stage}"]
        
        # Process each document
        for i, (doc_id, doc_name) in enumerate(documents):
            try:
                logger.info(f"Processing document {i+1}/{len(documents)}: {doc_id} ({doc_name})")
                
                # Find the document file
                doc_files = list(stage_dir.glob(f"*doc{str(doc_id).replace('-', '')[:12]}*"))
                
                if not doc_files:
                    logger.warning(f"File not found for document {doc_id}")
                    failed_count += 1
                    continue
                
                file_path = doc_files[0]
                
                # Get document type
                doc_type = self.integration.db_manager.get_document_type(doc_id) or "unknown"
                
                # Process the document
                logger.info(f"Indexing document: {file_path.name} (Type: {doc_type})")
                
                # Process the document
                metadata = {
                    "document_type": doc_type,
                    "pipeline_stage": stage,
                    "original_filename": doc_name,
                    "batch_id": batch_id
                }
                
                # Process through RAG engine
                chunks = self.integration.rag_engine.process_document(
                    document_path=file_path,
                    document_id=doc_id,
                    document_metadata=metadata
                )
                
                # Mark as processed in database
                if chunks:
                    chunk_count = len(chunks)
                    self.mark_document_as_processed(doc_id, chunk_count, batch_id)
                    processed_count += 1
                    logger.info(f"Successfully processed document {doc_id}: {chunk_count} chunks")
                else:
                    logger.warning(f"Failed to process document: {doc_id}")
                    failed_count += 1
                
                # Pause between documents to respect rate limits
                if i < len(documents) - 1:
                    time.sleep(1)  # Short pause between documents
                
            except Exception as e:
                logger.error(f"Error processing document {doc_id}: {e}")
                failed_count += 1
            
            # Pause after batch_size/5 documents to avoid rate limits
            if (i + 1) % max(batch_size // 5, 1) == 0 and i < len(documents) - 1:
                logger.info(f"Pausing for {pause_seconds} seconds...")
                time.sleep(pause_seconds)
        
        # Get final batch statistics
        batch_stats = self.get_batch_progress(batch_id)
        
        logger.info(f"Batch {batch_id} completed: {processed_count} processed, {failed_count} failed")
        
        return {
            "batch_id": batch_id,
            "processed": processed_count,
            "failed": failed_count,
            "status": "completed",
            "stats": batch_stats
        }
        
    def process_all(self, stage: str, batch_size: int = 500, pause_seconds: int = 5) -> dict:
        """Process all unprocessed documents in batches."""
        # Get total unprocessed documents
        stats = self.get_batch_progress()
        unprocessed_count = stats.get("unprocessed_documents", 0)
        
        if unprocessed_count == 0:
            logger.info("No unprocessed documents found")
            return {"status": "completed", "message": "No documents to process"}
        
        logger.info(f"Processing all {unprocessed_count} unprocessed documents in batches of {batch_size}")
        
        total_processed = 0
        total_failed = 0
        batch_results = []
        
        # Process in batches
        while unprocessed_count > 0:
            # Generate batch ID
            batch_id = str(uuid.uuid4())
            
            # Process batch
            current_batch_size = min(batch_size, unprocessed_count)
            logger.info(f"Processing batch of {current_batch_size} documents")
            
            result = self.process_batch(stage, current_batch_size, batch_id, pause_seconds)
            batch_results.append(result)
            
            # Update counts
            processed = result.get("processed", 0)
            failed = result.get("failed", 0)
            total_processed += processed
            total_failed += failed
            
            # Update unprocessed count
            unprocessed_count -= (processed + failed)
            
            # Long pause between batches
            if unprocessed_count > 0:
                logger.info(f"Pausing for {pause_seconds*2} seconds between batches...")
                time.sleep(pause_seconds * 2)
            
            logger.info(f"Progress: {total_processed} processed, {total_failed} failed, {unprocessed_count} remaining")
        
        logger.info(f"All processing complete: {total_processed} processed, {total_failed} failed")
        
        return {
            "status": "completed",
            "total_processed": total_processed,
            "total_failed": total_failed,
            "batches": batch_results
        }


if __name__ == "__main__":
    # Parse arguments
    parser = argparse.ArgumentParser(description="RAG Batch Processing")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # Process batch
    batch_parser = subparsers.add_parser("batch", help="Process a batch of documents")
    batch_parser.add_argument("--stage", "-s", type=str, default="clean", choices=["clean", "process"], 
                             help="Pipeline stage to process")
    batch_parser.add_argument("--size", "-n", type=int, default=500, help="Batch size")
    batch_parser.add_argument("--pause", "-p", type=int, default=5, help="Pause between batches (seconds)")
    
    # Process all
    all_parser = subparsers.add_parser("all", help="Process all unprocessed documents")
    all_parser.add_argument("--stage", "-s", type=str, default="clean", choices=["clean", "process"],
                          help="Pipeline stage to process")
    all_parser.add_argument("--size", "-n", type=int, default=500, help="Batch size")
    all_parser.add_argument("--pause", "-p", type=int, default=5, help="Pause between batches (seconds)")
    
    # List batches
    list_parser = subparsers.add_parser("list", help="List all processing batches")
    
    # Clear batch
    clear_parser = subparsers.add_parser("clear", help="Clear a batch to reprocess it")
    clear_parser.add_argument("--batch-id", "-b", type=str, required=True, help="Batch ID to clear")
    
    # Get stats
    stats_parser = subparsers.add_parser("stats", help="Get processing statistics")
    stats_parser.add_argument("--batch-id", "-b", type=str, help="Optional batch ID")
    
    args = parser.parse_args()
    
    # Initialize processor
    processor = RAGBatchProcessor()
    
    # Execute command
    if args.command == "batch":
        result = processor.process_batch(args.stage, args.size, pause_seconds=args.pause)
        print(f"Batch processing completed: {result['processed']} processed, {result.get('failed', 0)} failed")
        print(f"Batch ID: {result['batch_id']}")
        
    elif args.command == "all":
        result = processor.process_all(args.stage, args.size, args.pause)
        print(f"All processing completed: {result['total_processed']} processed, {result['total_failed']} failed")
        
    elif args.command == "list":
        batches = processor.list_batches()
        if batches:
            print("\nRAG Processing Batches:")
            print("-" * 100)
            print(f"{'Batch ID':<36} | {'Started':<20} | {'Completed':<20} | {'Documents':<10} | {'Chunks':<10}")
            print("-" * 100)
            
            for batch in batches:
                print(f"{batch['batch_id']:<36} | {batch['started_at']:<20} | {batch['completed_at']:<20} | {batch['document_count']:<10} | {batch['chunk_count']:<10}")
        else:
            print("No batches found")
            
    elif args.command == "clear":
        success = processor.clear_batch(args.batch_id)
        if success:
            print(f"Successfully cleared batch {args.batch_id}")
        else:
            print(f"Failed to clear batch {args.batch_id}")
            
    elif args.command == "stats":
        stats = processor.get_batch_progress(args.batch_id)
        
        if args.batch_id:
            print(f"\nStats for Batch {args.batch_id}:")
            print(f"Total Documents: {stats.get('total_documents', 0)}")
            print(f"Processed Documents: {stats.get('processed_documents', 0)}")
            print(f"Total Chunks: {stats.get('total_chunks', 0)}")
            print(f"Progress: {stats.get('progress_percentage', 0)}%")
        else:
            print("\nOverall RAG Processing Stats:")
            print(f"Total Documents: {stats.get('total_documents', 0)}")
            print(f"Clean Stage Documents: {stats.get('clean_stage_documents', 0)}")
            print(f"Processed Documents: {stats.get('processed_documents', 0)}")
            print(f"Unprocessed Documents: {stats.get('unprocessed_documents', 0)}")
            print(f"Total Chunks: {stats.get('total_chunks', 0)}")
            print(f"Total Batches: {stats.get('batch_count', 0)}")
            print(f"Progress: {stats.get('progress_percentage', 0)}%")
            
    else:
        parser.print_help()