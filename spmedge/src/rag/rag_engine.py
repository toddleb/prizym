#!/usr/bin/env python3
"""
RAG Engine - Orchestrates the RAG (Retrieval Augmented Generation) pipeline.
- Manages document processing, embedding, and retrieval
- Integrates with OpenAI for query embedding and response generation
- Provides hybrid search capabilities
- Implements token counting and limiting to prevent rate limits
- Controls response size for efficient processing
"""

import os
import re
import json
import logging
import time
from pathlib import Path
from typing import List, Dict, Any, Tuple, Optional, Union, Callable

from config.config import config
from src.utils.openai_client import OpenAIProcessor
from src.rag.document_chunker import DocumentChunker
from src.rag.embedding_generator import EmbeddingGenerator
from src.rag.vector_store import VectorStore

# Configure logging
logger = logging.getLogger("rag_engine")
logger.setLevel(logging.INFO)

class RAGEngine:
    """Main engine for Retrieval Augmented Generation (RAG)."""
    
    def __init__(self, 
                embedding_model: str = "openai",
                index_type: str = "flat",
                index_name: str = "spmedge",
                data_dir: Optional[str] = None,
                chunk_size: int = 512,
                chunk_overlap: int = 50):
        """
        Initialize the RAG engine.
        
        Args:
            embedding_model: Embedding model to use
            index_type: Vector index type
            index_name: Name for the vector index
            data_dir: Base directory for data storage
            chunk_size: Target size for document chunks
            chunk_overlap: Overlap between chunks
        """
        # Set up directories
        self.data_dir = Path(data_dir) if data_dir else Path(config.DATA_DIR) / "rag_data"
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize components
        logger.info("Initializing RAG Engine components...")
        
        # Initialize OpenAI client for query processing
        self.openai_client = OpenAIProcessor()
        
        # Initialize document chunker
        self.chunker = DocumentChunker(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )
        
        # Initialize embedding generator
        self.embedding_generator = EmbeddingGenerator(
            model_name=embedding_model,
            cache_dir=str(self.data_dir / "embeddings_cache")
        )
        
        # Get dimensions from embedding model
        self.dimensions = self.embedding_generator.dimensions
        
        # Initialize vector store with matching dimensions
        self.vector_store = VectorStore(
            dimensions=self.dimensions,
            index_type=index_type,
            store_dir=str(self.data_dir / "vector_store"),
            index_name=index_name
        )
        
        # Try to load existing index
        self.vector_store.load()
        
        logger.info(f"RAG Engine initialized with {embedding_model} embeddings ({self.dimensions} dimensions)")
        logger.info(f"Vector store contains {len(self.vector_store.doc_ids)} documents")
    
    def estimate_tokens(self, text: str) -> int:
        """Estimate the number of tokens in a text string."""
        # Simple estimation: ~4 characters per token
        return len(text) // 4
    
    def process_document(self, 
                        document_path: Path, 
                        document_id: Optional[str] = None,
                        document_metadata: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Process a document through the RAG pipeline (chunk, embed, store).
        
        Args:
            document_path: Path to the document file
            document_id: Optional document ID (generated from filename if not provided)
            document_metadata: Optional additional metadata
            
        Returns:
            List of processed chunks
        """
        try:
            logger.info(f"Processing document: {document_path}")
            
            # Generate ID from filename if not provided
            if not document_id:
                document_id = document_path.stem
            
            # Add provided metadata
            metadata = document_metadata or {}
            
            # 1. Chunk the document
            chunks = self.chunker.chunk_document_from_file(document_path, document_id)
            logger.info(f"Created {len(chunks)} chunks from document {document_id}")
            
            # 2. Generate embeddings for chunks
            chunks_with_embeddings = self.embedding_generator.embed_chunks(chunks)
            logger.info(f"Generated embeddings for {len(chunks_with_embeddings)} chunks")
            
            # 3. Add to vector store
            doc_ids = self.vector_store.add_documents(chunks_with_embeddings)
            logger.info(f"Added {len(doc_ids)} chunks to vector store")
            
            # 4. Save vector store
            self.vector_store.save()
            
            return chunks_with_embeddings
            
        except Exception as e:
            logger.error(f"Error processing document {document_path}: {e}")
            return []
    
    def process_directory(self, 
                         directory_path: Path,
                         file_types: List[str] = None,
                         recursive: bool = True) -> int:
        """
        Process all documents in a directory.
        
        Args:
            directory_path: Path to directory containing documents
            file_types: List of file extensions to process (e.g., ['.txt', '.pdf'])
            recursive: Whether to process subdirectories
            
        Returns:
            Number of documents processed
        """
        try:
            directory_path = Path(directory_path)
            if not directory_path.exists() or not directory_path.is_dir():
                logger.error(f"Directory not found: {directory_path}")
                return 0
                
            # Default file types if not specified
            if file_types is None:
                file_types = ['.txt', '.json', '.md', '.csv']
                
            # Convert to lowercase for case-insensitive matching
            file_types = [ft.lower() if not ft.startswith('.') else ft for ft in file_types]
            file_types = [ft if ft.startswith('.') else f'.{ft}' for ft in file_types]
            
            # Get list of files
            if recursive:
                all_files = list(directory_path.glob('**/*'))
            else:
                all_files = list(directory_path.glob('*'))
                
            # Filter by file type
            files_to_process = [f for f in all_files if f.is_file() and f.suffix.lower() in file_types]
            
            logger.info(f"Found {len(files_to_process)} files to process in {directory_path}")
            
            # Process each file
            processed_count = 0
            for file_path in files_to_process:
                doc_id = f"{file_path.parent.name}_{file_path.stem}"
                chunks = self.process_document(file_path, document_id=doc_id)
                if chunks:
                    processed_count += 1
            
            logger.info(f"Successfully processed {processed_count} documents from {directory_path}")
            return processed_count
            
        except Exception as e:
            logger.error(f"Error processing directory {directory_path}: {e}")
            return 0
            
    def generate_query_embedding(self, query: str) -> List[float]:
        """
        Generate embedding for a query string.
        
        Args:
            query: Query text
            
        Returns:
            Query embedding vector
        """
        return self.embedding_generator.generate_embedding(query)
    
    def search(self, 
              query: str,
              k: int = 5,
              mode: str = "hybrid",
              alpha: float = 0.5,
              filter_fn: Optional[Callable] = None) -> List[Dict[str, Any]]:
        """
        Search for relevant documents using the query.
        
        Args:
            query: Search query text
            k: Number of results to return
            mode: Search mode ('vector', 'keyword', or 'hybrid')
            alpha: Weight of vector vs. keyword search in hybrid mode
            filter_fn: Optional function to filter results
            
        Returns:
            List of retrieved documents
        """
        try:
            logger.info(f"Searching with query: '{query}' (mode: {mode})")
            
            # Generate embedding for query if needed
            query_embedding = None
            if mode in ["vector", "hybrid"]:
                query_embedding = self.generate_query_embedding(query)
                
            # Perform search based on mode
            if mode == "vector":
                results = self.vector_store.similarity_search(query_embedding, k=k, filter_fn=filter_fn)
            elif mode == "keyword":
                results = self.vector_store.keyword_search(query, k=k)
            else:  # hybrid mode
                results = self.vector_store.hybrid_search(query, query_embedding, k=k, alpha=alpha, filter_fn=filter_fn)
            
            logger.info(f"Found {len(results)} results for query")
            return results
            
        except Exception as e:
            logger.error(f"Error searching with query '{query}': {e}")
            return []
    
    def generate_answer(self, 
                       query: str,
                       retrieved_docs: List[Dict[str, Any]],
                       max_tokens: int = 500,
                       temperature: float = 0.0,
                       use_summarization: bool = True) -> Dict[str, Any]:
        """
        Generate an answer with controls for context and response size.
        
        Args:
            query: User query
            retrieved_docs: Documents retrieved from search
            max_tokens: Maximum tokens in response
            temperature: Response temperature (0.0 = deterministic)
            use_summarization: Whether to summarize long chunks
            
        Returns:
            Dictionary with answer and metadata
        """
        try:
            # Prepare context from retrieved documents
            context_chunks = []
            total_tokens = 0
            
            for doc in retrieved_docs:
                metadata = doc.get("metadata", {})
                
                # Format this chunk with metadata
                chunk_text = doc.get("text", "").strip()
                score = doc.get("combined_score", doc.get("similarity", doc.get("match_score", 0.0)))
                
                # Count tokens
                chunk_tokens = self.estimate_tokens(chunk_text)
                
                # Add only a summary for long chunks if enabled
                if use_summarization and chunk_tokens > 500:
                    # Create a compact representation instead of full text
                    first_para = chunk_text.split('\n\n')[0] if '\n\n' in chunk_text else chunk_text[:500]
                    formatted_chunk = f"--- Document: {metadata.get('chunk_id', 'unknown')} (Score: {score:.2f}) ---\n{first_para}\n[Document continues...]"
                else:
                    formatted_chunk = f"--- Document: {metadata.get('chunk_id', 'unknown')} (Score: {score:.2f}) ---\n{chunk_text}\n"
                
                # Track token count
                format_tokens = self.estimate_tokens(formatted_chunk)
                total_tokens += format_tokens
                
                context_chunks.append(formatted_chunk)
            
            # Join all context chunks
            context = "\n".join(context_chunks)
            
            # Prepare system message with instructions
            system_message = """You are an AI assistant specialized in SPM Edge pipeline processing. 
            Answer the question based ONLY on the provided context. If the answer cannot be determined 
            from the context, say "I don't have enough information to answer that." Don't make up information.
            Be clear and concise. If the context is very large, focus on the most relevant information."""
            
            # Prepare user message with context and query
            user_message = f"""
            Context information is below:
            ----------------
            {context}
            ----------------
            
            Given the context information and not prior knowledge, answer the question: {query}
            """
            
            # Log token usage estimate
            user_tokens = self.estimate_tokens(user_message)
            system_tokens = self.estimate_tokens(system_message)
            total_estimated_tokens = user_tokens + system_tokens + max_tokens
            
            logger.info(f"Estimated token usage: {total_estimated_tokens} (context: {total_tokens}, query: {self.estimate_tokens(query)})")
            
            # Call the OpenAI API
            start_time = time.time()
            response = self.openai_client.generate_completion(
                prompt=user_message,
                system_prompt=system_message,
                max_tokens=max_tokens,
                temperature=temperature
            )
            end_time = time.time()
            
            # Prepare result
            result = {
                "answer": response,
                "metadata": {
                    "sources": [doc.get("metadata", {}).get("chunk_id") for doc in retrieved_docs],
                    "processing_time": end_time - start_time,
                    "estimated_input_tokens": user_tokens + system_tokens,
                    "estimated_output_tokens": self.estimate_tokens(response),
                    "query": query,
                    "retrieved_docs": len(retrieved_docs)
                }
            }
            
            logger.info(f"Generated answer for query '{query}' in {result['metadata']['processing_time']:.2f}s")
            return result
            
        except Exception as e:
            logger.error(f"Error generating answer for query '{query}': {e}")
            return {
                "answer": "Sorry, I encountered an error while generating the answer.",
                "metadata": {
                    "error": str(e),
                    "query": query
                }
            }
    
    def query(self, 
         query: str,
         k: int = 5,
         mode: str = "hybrid",
         temperature: float = 0.0,
         max_tokens: int = 500,
         max_input_tokens: int = 16000) -> Dict[str, Any]:
        """
        Complete RAG pipeline with improved document handling.
        
        Args:
            query: User query
            k: Number of documents to retrieve
            mode: Search mode ('vector', 'keyword', 'hybrid')
            temperature: Response temperature
            max_tokens: Maximum tokens in response
            max_input_tokens: Maximum tokens in the input (context + query)
            
        Returns:
            Dictionary with answer, sources, and metadata
        """
        try:
            # 1. Search for relevant documents
            retrieved_docs = self.search(query, k=k*3, mode=mode)  # Get more to filter duplicates
            
            # 2. Filter out duplicate content
            unique_docs = []
            seen_content = set()
            
            for doc in retrieved_docs:
                # Use first 100 chars as a fingerprint to detect duplicates
                text = doc.get("text", "")
                content_hash = text[:100] if text else ""
                
                if content_hash and content_hash not in seen_content:
                    seen_content.add(content_hash)
                    unique_docs.append(doc)
            
            logger.info(f"After deduplication: {len(unique_docs)}/{len(retrieved_docs)} unique documents")
            
            # 3. Select documents within token budget
            included_docs = []
            context_tokens = 0
            
            for doc in unique_docs:
                doc_text = doc.get("text", "")
                
                # For very large documents, extract most relevant sections
                if len(doc_text) > 5000:
                    # Try to find sections most relevant to query
                    query_terms = query.lower().split()
                    
                    # Split into paragraphs
                    paragraphs = re.split(r'\n\s*\n', doc_text)
                    
                    # Score paragraphs by relevance to query
                    scored_paragraphs = []
                    for para in paragraphs:
                        if len(para.strip()) < 20:
                            continue  # Skip very short paragraphs
                            
                        score = 0
                        for term in query_terms:
                            if term in para.lower():
                                score += 1
                        
                        if score > 0:
                            scored_paragraphs.append((para, score))
                    
                    # Sort by relevance score
                    scored_paragraphs.sort(key=lambda x: x[1], reverse=True)
                    
                    # Take top paragraphs up to ~2000 chars
                    focused_text = ""
                    for para, _ in scored_paragraphs:
                        if len(focused_text) + len(para) < 3000:
                            focused_text += para + "\n\n"
                        else:
                            break
                    
                    # Use focused text if we found relevant paragraphs
                    if focused_text:
                        doc_text = focused_text
                
                # Estimate tokens
                doc_tokens = self.estimate_tokens(doc_text)
                format_overhead = 100
                
                # Check if adding this document exceeds our token budget
                if context_tokens + doc_tokens + format_overhead > max_input_tokens:
                    break
                    
                # Create a new document with the possibly shortened text
                processed_doc = doc.copy()
                processed_doc["text"] = doc_text
                
                included_docs.append(processed_doc)
                context_tokens += doc_tokens + format_overhead
                
                if len(included_docs) >= k:
                    break
                    
            logger.info(f"Using {len(included_docs)}/{len(unique_docs)} docs, ~{context_tokens} tokens")
            
            # 4. Generate answer with prepared context
            result = self.generate_answer(
                query=query,
                retrieved_docs=included_docs,
                temperature=temperature,
                max_tokens=max_tokens,
                use_summarization=False  # Already handled document focusing
            )
            
            # 5. Add retrieved documents to result
            result["documents"] = included_docs
            
            return result
            
        except Exception as e:
            logger.error(f"Error processing query '{query}': {e}")
            return {
                "answer": "Sorry, I encountered an error while processing your query.",
                "error": str(e),
                "query": query
            }
        
    def get_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the RAG engine.
        
        Returns:
            Dictionary with system statistics
        """
        vector_stats = self.vector_store.get_stats()
        embedding_stats = self.embedding_generator.get_embedding_stats()
        
        return {
            "vector_store": vector_stats,
            "embedding_generator": embedding_stats,
            "documents": len(self.vector_store.doc_ids),
            "chunks": vector_stats.get("document_count", 0),
            "data_dir": str(self.data_dir)
        }