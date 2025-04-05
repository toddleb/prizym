#!/usr/bin/env python3
"""
SPM Edge RAG Integration - Connects the RAG system to the SPM Edge pipeline.
- Processes documents from clean/process stages
- Indexes framework documents for context
- Adds RAG-powered insights to document processing
"""

import os
import sys
import json
import logging
import argparse
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional

# Add the project root to the Python path
project_root = str(Path(__file__).parent.parent.parent)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Now imports should work
from config.config import config
from src.pipeline.pipeline_processor import PipelineProcessor, PipelineStage
from src.pipeline.db_integration import DBManager
from src.rag.rag_engine import RAGEngine

# Ensure logs directory exists
os.makedirs(config.LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(config.LOG_DIR, "spm_rag_integration.log")

# Configure logging
logger = logging.getLogger("spm_rag_integration")
logger.setLevel(logging.INFO)
logger.propagate = False

if not logger.handlers:
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler
    file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

class SPMRagIntegration:
    """Integrates RAG capabilities with SPM Edge pipeline."""
    
    def __init__(self, 
                embedding_model: str = "openai",
                index_name: str = "spmedge",
                index_type: str = "flat"):
        """
        Initialize the integration.
        
        Args:
            embedding_model: Model to use for embeddings
            index_name: Name for the vector index
            index_type: Type of vector index
        """
        self.db_manager = DBManager()
        
        # Initialize RAG engine
        self.rag_engine = RAGEngine(
            embedding_model=embedding_model,
            index_name=index_name,
            index_type=index_type
        )
        
        # Initialize pipeline processors for different stages
        self.clean_processor = PipelineProcessor(PipelineStage.CLEAN)
        self.process_processor = PipelineProcessor(PipelineStage.PROCESS)
        
        logger.info(f"SPM RAG Integration initialized with {embedding_model} embeddings")
    
    def index_framework_documents(self, framework_type: str = None) -> int:
        """
        Index framework documents from the knowledge files directory.
        
        Args:
            framework_type: Optional framework type filter
            
        Returns:
            Number of documents indexed
        """
        try:
            # Get framework files directory
            framework_dir = Path(config.KNOWLEDGE_FILES_DIR)
            if not framework_dir.exists():
                logger.error(f"Framework directory not found: {framework_dir}")
                return 0
            
            # Find framework files
            framework_files = []
            
            # Look for JSON framework files
            json_files = list(framework_dir.glob("*_knowledge.json"))
            framework_files.extend(json_files)
            
            # Look for Excel framework files
            excel_files = list(framework_dir.glob("*_framework_v*.xlsx"))
            framework_files.extend(excel_files)
            
            # Filter by framework type if specified
            if framework_type:
                filtered_files = []
                for file in framework_files:
                    if framework_type.lower() in file.name.lower():
                        filtered_files.append(file)
                framework_files = filtered_files
            
            logger.info(f"Found {len(framework_files)} framework files to index")
            
            # Process each framework file
            processed_count = 0
            for file_path in framework_files:
                try:
                    # Generate framework ID
                    framework_id = f"framework_{file_path.stem}"
                    
                    # Process the document
                    logger.info(f"Indexing framework: {file_path.name}")
                    chunks = self.rag_engine.process_document(
                        document_path=file_path,
                        document_id=framework_id,
                        document_metadata={"document_type": "framework"}
                    )
                    
                    if chunks:
                        processed_count += 1
                        logger.info(f"Indexed framework {file_path.name}: {len(chunks)} chunks")
                    else:
                        logger.warning(f"Failed to index framework: {file_path.name}")
                        
                except Exception as e:
                    logger.error(f"Error indexing framework {file_path.name}: {e}")
            
            logger.info(f"Successfully indexed {processed_count} framework documents")
            return processed_count
            
        except Exception as e:
            logger.error(f"Error indexing framework documents: {e}")
            return 0
    
    def index_pipeline_documents(self, stage: PipelineStage, limit: int = 100) -> int:
        """
        Index documents from a specific pipeline stage.
        
        Args:
            stage: Pipeline stage to index from
            limit: Maximum number of documents to index
            
        Returns:
            Number of documents indexed
        """
        try:
            # Get appropriate processor for the stage
            if stage == PipelineStage.CLEAN:
                processor = self.clean_processor
                stage_dir = processor.get_base_dirs()["stage_clean"]
            elif stage == PipelineStage.PROCESS:
                processor = self.process_processor
                stage_dir = processor.get_base_dirs()["stage_process"]
            else:
                logger.error(f"Unsupported pipeline stage for indexing: {stage}")
                return 0
            
            # Get documents that completed the stage
            documents = processor.get_documents_for_stage(
                current_stage=stage.value,
                status="completed",
                limit=limit
            )
            
            if not documents:
                logger.warning(f"No documents found in {stage.value} stage")
                return 0
                
            logger.info(f"Found {len(documents)} documents in {stage.value} stage")
            
            # Process each document
            processed_count = 0
            for doc in documents:
                try:
                    document_id = doc["id"]
                    filename = doc["name"]
                    
                    # Find the document file
                    doc_files = list(stage_dir.glob(f"*doc{str(document_id).replace('-', '')[:12]}*"))
                    
                    if not doc_files:
                        logger.warning(f"File not found for document {document_id}")
                        continue
                        
                    file_path = doc_files[0]
                    
                    # Get document type
                    doc_type = self.db_manager.get_document_type(document_id) or "unknown"
                    
                    # Process the document
                    logger.info(f"Indexing document: {file_path.name} (Type: {doc_type})")
                    
                    # Prepare metadata
                    metadata = {
                        "document_type": doc_type,
                        "pipeline_stage": stage.value,
                        "original_filename": filename
                    }
                    
                    # Add any existing metadata from the document
                    if "metadata" in doc and isinstance(doc["metadata"], dict):
                        metadata.update(doc["metadata"])
                    
                    # Process the document
                    chunks = self.rag_engine.process_document(
                        document_path=file_path,
                        document_id=document_id,
                        document_metadata=metadata
                    )
                    
                    if chunks:
                        processed_count += 1
                        logger.info(f"Indexed document {document_id}: {len(chunks)} chunks")
                    else:
                        logger.warning(f"Failed to index document: {document_id}")
                    
                except Exception as e:
                    logger.error(f"Error indexing document {doc.get('id')}: {e}")
            
            logger.info(f"Successfully indexed {processed_count} documents from {stage.value} stage")
            return processed_count
            
        except Exception as e:
            logger.error(f"Error indexing {stage.value} stage documents: {e}")
            return 0
    
    def analyze_document(self, document_id: str, queries: List[str] = None) -> Dict[str, Any]:
        """
        Generate RAG-powered insights for a specific document.
        
        Args:
            document_id: Document ID to analyze
            queries: List of analytical questions to ask about the document
            
        Returns:
            Dictionary with insights
        """
        try:
            # Get document type and metadata
            doc_type = self.db_manager.get_document_type(document_id)
            
            # Default queries based on document type
            if not queries:
                if "compensation" in (doc_type or "").lower():
                    queries = [
                        "What are the main compensation components in this document?",
                        "What is the bonus structure described in this document?",
                        "What are the key performance metrics mentioned?",
                        "Are there any special conditions or exceptions mentioned?"
                    ]
                else:
                    queries = [
                        "What are the key topics covered in this document?",
                        "What are the main findings or conclusions?",
                        "Summarize this document in 3-5 bullet points."
                    ]
            
            # Run queries and collect insights
            insights = {}
            
            for query in queries:
                # Generate insight for this query
                logger.info(f"Analyzing document {document_id} with query: '{query}'")
                
                # Modified to remove filter_fn parameter
                result = self.rag_engine.query(
                    query=query,
                    k=5,
                    mode="hybrid"  # Use hybrid search mode instead of filter_fn
                )
                
                # Store the insight
                insights[query] = {
                    "answer": result.get("answer"),
                    "sources": [
                        doc.get("metadata", {}).get("chunk_id")
                        for doc in result.get("documents", [])[:3]
                    ]
                }
            
            # Create final analysis result
            analysis = {
                "document_id": document_id,
                "document_type": doc_type,
                "analysis_time": datetime.now().isoformat(),
                "insights": insights
            }
            
            logger.info(f"Completed analysis for document {document_id} with {len(insights)} insights")
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error analyzing document {document_id}: {e}")
            return {
                "document_id": document_id,
                "error": str(e),
                "analysis_time": datetime.now().isoformat()
            }
    
    def save_analysis_to_database(self, document_id: str, analysis: Dict[str, Any]) -> bool:
        """
        Save RAG analysis results to the document metadata in the database.
        
        Args:
            document_id: Document ID
            analysis: Analysis results
            
        Returns:
            Success status
        """
        try:
            # Get current metadata
            self.db_manager.cursor.execute(
                "SELECT metadata FROM documents WHERE id = %s",
                (document_id,)
            )
            result = self.db_manager.cursor.fetchone()
            
            if not result:
                logger.error(f"Document {document_id} not found in database")
                return False
                
            # Parse existing metadata
            metadata = result[0] or {}
            if isinstance(metadata, str):
                metadata = json.loads(metadata)
            
            # Add rag_analysis to metadata
            metadata["rag_analysis"] = analysis
            
            # Update database
            self.db_manager.cursor.execute(
                "UPDATE documents SET metadata = %s, updated_at = NOW() WHERE id = %s",
                (json.dumps(metadata), document_id)
            )
            self.db_manager.conn.commit()
            
            logger.info(f"Saved RAG analysis to database for document {document_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error saving analysis to database for document {document_id}: {e}")
            self.db_manager.conn.rollback()
            return False
    
    def query_knowledge_base(self, query: str, k: int = 5) -> Dict[str, Any]:
        """
        Query the entire knowledge base.
        
        Args:
            query: Query string
            k: Number of results to return
            
        Returns:
            Query results
        """
        return self.rag_engine.query(query=query, k=k)
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the RAG integration.
        
        Returns:
            Statistics dictionary
        """
        rag_stats = self.rag_engine.get_stats()
        
        # Get document counts from database
        try:
            self.db_manager.cursor.execute(
                "SELECT COUNT(*) FROM documents"
            )
            total_documents = self.db_manager.cursor.fetchone()[0]
            
            self.db_manager.cursor.execute(
                "SELECT document_type_id, COUNT(*) FROM documents GROUP BY document_type_id"
            )
            document_types = {}
            for type_id, count in self.db_manager.cursor.fetchall():
                doc_type = "unknown"
                try:
                    self.db_manager.cursor.execute(
                        "SELECT name FROM document_types WHERE id = %s",
                        (type_id,)
                    )
                    doc_type = self.db_manager.cursor.fetchone()[0]
                except:
                    pass
                document_types[doc_type] = count
                
            return {
                "rag_engine": rag_stats,
                "database": {
                    "total_documents": total_documents,
                    "document_types": document_types
                }
            }
        except Exception as e:
            logger.error(f"Error getting database stats: {e}")
            return {
                "rag_engine": rag_stats,
                "database": {
                    "error": str(e)
                }
            }

    def get_indexing_stats(self):
        """Get statistics about indexed vs. unindexed documents."""
        try:
            # Get total document count
            self.db_manager.cursor.execute("SELECT COUNT(*) FROM documents")
            total_docs = self.db_manager.cursor.fetchone()[0]
            
            # Get indexed document count
            self.db_manager.cursor.execute("SELECT COUNT(*) FROM documents WHERE rag_data IS NOT NULL")
            indexed_docs = self.db_manager.cursor.fetchone()[0]
            
            return {
                "total_documents": total_docs,
                "indexed_documents": indexed_docs,
                "remaining_documents": total_docs - indexed_docs,
                "progress_percentage": round((indexed_docs / total_docs) * 100, 2) if total_docs > 0 else 0
            }
        except Exception as e:
            logger.error(f"Error getting indexing stats: {e}")
            return None

    def mark_document_as_indexed(self, document_id: str, chunk_count: int) -> bool:
        """Mark a document as indexed in the database."""
        try:
            # Update the rag_data field in the documents table
            self.db_manager.cursor.execute(
                """
                UPDATE documents 
                SET rag_data = jsonb_build_object(
                    'indexed', true,
                    'indexed_at', NOW(),
                    'chunk_count', %s
                )
                WHERE id = %s
                """,
                (chunk_count, document_id)
            )
            self.db_manager.conn.commit()
            logger.info(f"Marked document {document_id} as indexed with {chunk_count} chunks")
            return True
        except Exception as e:
            logger.error(f"Error marking document {document_id} as indexed: {e}")
            self.db_manager.conn.rollback()
            return False
        
# Example usage when run as script
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="SPM Edge RAG Integration")
    
    # Create subparsers for different commands
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # Index framework documents command
    index_framework_parser = subparsers.add_parser("index-framework", help="Index framework documents")
    index_framework_parser.add_argument("--type", "-t", type=str, help="Framework type to index")
    
    # Index pipeline documents command
    index_pipeline_parser = subparsers.add_parser("index-pipeline", help="Index pipeline documents")
    index_pipeline_parser.add_argument("--stage", "-s", type=str, required=True,
                                      choices=["clean", "process"], help="Pipeline stage to index")
    index_pipeline_parser.add_argument("--limit", "-l", type=int, default=100, help="Maximum documents to index")
    # Add this to your command line arguments in spm_rag_integration.py
    process_all_parser = subparsers.add_parser("process-all", help="Process all documents")
    process_all_parser.add_argument("--batch-size", type=int, default=50, help="Documents per batch")
    process_all_parser.add_argument("--stage", type=str, default="clean", choices=["clean", "process"], help="Pipeline stage to process")
                                
    # Analyze document command
    analyze_parser = subparsers.add_parser("analyze", help="Analyze a specific document")
    analyze_parser.add_argument("--document-id", "-d", type=str, required=True, help="Document ID to analyze")
    analyze_parser.add_argument("--save", "-s", action="store_true", help="Save analysis to database")
    
    # Query command
    query_parser = subparsers.add_parser("query", help="Query the knowledge base")
    query_parser.add_argument("--query", "-q", type=str, required=True, help="Query string")
    query_parser.add_argument("--k", "-k", type=int, default=5, help="Number of results")
    
    # Info command
    info_parser = subparsers.add_parser("info", help="Show system information")
    
    args = parser.parse_args()
    
    # Initialize the integration
    integration = SPMRagIntegration()
    
    if args.command == "index-framework":
        # Index framework documents
        count = integration.index_framework_documents(framework_type=args.type)
        print(f"Indexed {count} framework documents")
        
    elif args.command == "index-pipeline":
        # Map string to enum
        stage_map = {
            "clean": PipelineStage.CLEAN,
            "process": PipelineStage.PROCESS
        }
        stage = stage_map.get(args.stage)
        
        if not stage:
            print(f"Error: Invalid stage: {args.stage}")
            exit(1)
            
        # Index pipeline documents
        count = integration.index_pipeline_documents(stage=stage, limit=args.limit)
        print(f"Indexed {count} documents from {args.stage} stage")
        
    elif args.command == "analyze":
        # Analyze a document
        analysis = integration.analyze_document(document_id=args.document_id)
        
        # Print analysis results
        print(f"\nAnalysis for document {args.document_id}:")
        for query, insight in analysis.get("insights", {}).items():
            print(f"\nQ: {query}")
            print(f"A: {insight['answer']}")
            print(f"Sources: {', '.join(insight['sources'][:3])}")
        
        # Save to database if requested
        if args.save:
            success = integration.save_analysis_to_database(args.document_id, analysis)
            if success:
                print(f"\nAnalysis saved to database for document {args.document_id}")
            else:
                print(f"\nFailed to save analysis to database")
        
    elif args.command == "query":
        # Query the knowledge base
        result = integration.query_knowledge_base(query=args.query, k=args.k)
        
        # Print query results
        print(f"\nQuery: {args.query}")
        print(f"\nAnswer:")
        print(f"{result['answer']}")
        
        print(f"\nSources:")
        for i, doc in enumerate(result.get("documents", [])[:3]):
            source = doc.get("metadata", {}).get("chunk_id", "unknown")
            score = doc.get("combined_score", doc.get("similarity", doc.get("match_score", 0.0)))
            print(f"  {i+1}. {source} (Score: {score:.2f})")
        
    elif args.command == "info":
        # Show system information
        stats = integration.get_stats()
        
        print("\nSPM RAG Integration Information:")
        
        rag_stats = stats.get("rag_engine", {})
        print(f"Documents in RAG: {rag_stats.get('documents', 0)}")
        print(f"Chunks in RAG: {rag_stats.get('chunks', 0)}")
        
        db_stats = stats.get("database", {})
        print(f"\nDocuments in Database: {db_stats.get('total_documents', 0)}")
        
        doc_types = db_stats.get("document_types", {})
        if doc_types:
            print("\nDocument Types:")
            for doc_type, count in doc_types.items():
                print(f"  {doc_type}: {count}")
        
    else:
        parser.print_help()