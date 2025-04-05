#!/usr/bin/env python3
"""
Vector Store - Stores and retrieves vector embeddings for RAG.
- Supports in-memory FAISS & persistent storage
- Implements similarity search with filtering
- Enables hybrid search combining vector & keyword search
"""

import os
import json
import logging
import numpy as np
import pickle
from pathlib import Path
from typing import List, Dict, Any, Tuple, Optional, Union, Callable

# Import FAISS conditionally to handle environments where it's not installed
try:
    import faiss
    FAISS_AVAILABLE = True
except ImportError:
    FAISS_AVAILABLE = False
    logging.warning("FAISS not available. Install with: pip install faiss-cpu or faiss-gpu")

from config.config import config

# Configure logging
logger = logging.getLogger("vector_store")
logger.setLevel(logging.INFO)

class VectorStore:
    """Stores and retrieves document embeddings for RAG."""
    
    def __init__(self, 
                 dimensions: int = 1536,
                 index_type: str = "flat",
                 store_dir: Optional[str] = None,
                 index_name: str = "default"):
        """
        Initialize vector store.
        
        Args:
            dimensions: Embedding vector dimensions
            index_type: Type of index ('flat', 'ivf', 'hnsw')
            store_dir: Directory to store index files
            index_name: Name of the index
        """
        self.dimensions = dimensions
        self.index_type = index_type
        self.index_name = index_name
        self.store_dir = Path(store_dir) if store_dir else Path(config.DATA_DIR) / "vector_store"
        self.store_dir.mkdir(parents=True, exist_ok=True)
        
        # Make sure FAISS is available
        if not FAISS_AVAILABLE:
            raise ImportError("FAISS is required for vector store. Install with: pip install faiss-cpu")
        
        # Initialize empty index
        self.index = self._create_empty_index()
        
        # Storage for document metadata
        self.documents = {}
        self.doc_ids = []
        
        logger.info(f"Initialized vector store with {dimensions} dimensions, type: {index_type}")
    
    def _create_empty_index(self) -> faiss.Index:
        """Create an empty FAISS index based on configuration."""
        if self.index_type == "flat":
            # Simple flat index - exact but slower for large datasets
            return faiss.IndexFlatL2(self.dimensions)
        elif self.index_type == "ivf":
            # IVF index - faster but approximate
            quantizer = faiss.IndexFlatL2(self.dimensions)
            # Number of centroids - rule of thumb: sqrt(n) where n is expected dataset size
            nlist = 100  # Can be adjusted based on expected dataset size
            return faiss.IndexIVFFlat(quantizer, self.dimensions, nlist, faiss.METRIC_L2)
        elif self.index_type == "hnsw":
            # HNSW index - very fast, good accuracy, but memory-intensive
            return faiss.IndexHNSWFlat(self.dimensions, 32)  # 32 is M parameter (connections per layer)
        else:
            logger.warning(f"Unknown index type: {self.index_type}, using flat index")
            return faiss.IndexFlatL2(self.dimensions)
    
    def _get_index_path(self) -> Path:
        """Get path for the FAISS index file."""
        return self.store_dir / f"{self.index_name}.faiss"
    
    def _get_metadata_path(self) -> Path:
        """Get path for the metadata file."""
        return self.store_dir / f"{self.index_name}.pickle"
    
    def add_documents(self, documents: List[Dict[str, Any]]) -> List[str]:
        """
        Add documents with embeddings to the vector store.
        
        Args:
            documents: List of document dicts with 'embedding', 'text', and 'metadata'
            
        Returns:
            List of document IDs
        """
        if not documents:
            logger.warning("No documents to add")
            return []
            
        # Extract embeddings
        embeddings = []
        doc_ids = []
        
        # Track if we need to train an IVF index
        needs_training = self.index_type == "ivf" and not self.index.is_trained
        
        for doc in documents:
            # Verify document structure
            if "embedding" not in doc:
                logger.warning(f"Document missing embedding, skipping: {doc.get('metadata', {}).get('chunk_id')}")
                continue
                
            if len(doc["embedding"]) != self.dimensions:
                logger.warning(f"Embedding dimension mismatch: {len(doc['embedding'])} vs {self.dimensions}")
                continue
            
            # Generate ID if not present
            doc_id = doc.get("metadata", {}).get("chunk_id")
            if not doc_id:
                # Use length as a simple way to generate a unique ID
                doc_id = f"doc_{len(self.documents)}"
            
            # Store document
            self.documents[doc_id] = {
                "text": doc.get("text", ""),
                "metadata": doc.get("metadata", {})
            }
            
            embeddings.append(doc["embedding"])
            doc_ids.append(doc_id)
        
        if not embeddings:
            logger.warning("No valid embeddings to add")
            return []
        
        # Convert to numpy array
        embeddings_array = np.array(embeddings).astype('float32')
        
        # Train if needed (for IVF index)
        if needs_training and len(embeddings) > 0:
            logger.info(f"Training IVF index with {len(embeddings)} vectors")
            self.index.train(embeddings_array)
        
        # Add vectors to index
        self.index.add(embeddings_array)
        
        # Store ids
        self.doc_ids.extend(doc_ids)
        
        logger.info(f"Added {len(embeddings)} documents to index, total: {len(self.doc_ids)}")
        
        return doc_ids
    
    def similarity_search(self, 
                         query_embedding: List[float], 
                         k: int = 5,
                         filter_fn: Optional[Callable] = None) -> List[Dict[str, Any]]:
        """
        Search for similar documents by vector similarity.
        
        Args:
            query_embedding: The query vector
            k: Number of results to return
            filter_fn: Optional function to filter results
            
        Returns:
            List of document dictionaries with similarity scores
        """
        if len(self.doc_ids) == 0:
            logger.warning("Index is empty")
            return []
            
        if len(query_embedding) != self.dimensions:
            logger.error(f"Query embedding dimension mismatch: {len(query_embedding)} vs {self.dimensions}")
            return []
        
        # Convert to numpy array
        query_vector = np.array([query_embedding]).astype('float32')
        
        # Adjust k if we have fewer documents than requested
        k = min(k, len(self.doc_ids))
        
        # Search for similar vectors
        try:
            # Get more results than needed to allow for filtering
            search_k = k * 2 if filter_fn else k
            search_k = min(search_k, len(self.doc_ids))
            
            distances, indices = self.index.search(query_vector, search_k)
            
            # Prepare results
            results = []
            for i, idx in enumerate(indices[0]):
                if idx == -1:  # FAISS returns -1 for empty slots
                    continue
                    
                doc_id = self.doc_ids[idx]
                doc = self.documents.get(doc_id)
                
                if not doc:
                    logger.warning(f"Document with id {doc_id} not found in metadata")
                    continue
                
                # Calculate similarity score (convert distance to similarity)
                similarity = 1.0 / (1.0 + distances[0][i])
                
                # Create result object
                result = {
                    "id": doc_id,
                    "text": doc["text"],
                    "metadata": doc["metadata"],
                    "similarity": similarity,
                    "distance": float(distances[0][i])
                }
                
                # Apply filter if provided
                if filter_fn and not filter_fn(result):
                    continue
                    
                results.append(result)
                
                # Stop once we have enough results
                if len(results) >= k:
                    break
            
            return results
        except Exception as e:
            logger.error(f"Error searching index: {e}")
            return []
    
    def keyword_search(self, 
                      query: str, 
                      k: int = 5,
                      fields: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """
        Search for documents by keyword matching.
        
        Args:
            query: Keyword query string
            k: Number of results to return
            fields: Fields to search in (defaults to text only)
            
        Returns:
            List of document dictionaries with match scores
        """
        if len(self.doc_ids) == 0:
            logger.warning("Index is empty")
            return []
            
        # Simple keyword search implementation
        # This could be replaced with a more sophisticated search like BM25
        keywords = query.lower().split()
        if not keywords:
            return []
            
        # Default to searching only in text field
        if not fields:
            fields = ["text"]
            
        results = []
        
        for doc_id in self.doc_ids:
            doc = self.documents.get(doc_id)
            if not doc:
                continue
                
            # Calculate simple match score across specified fields
            match_score = 0
            for field in fields:
                if field == "text":
                    text = doc["text"].lower()
                elif field in doc["metadata"]:
                    text = str(doc["metadata"][field]).lower()
                else:
                    continue
                    
                # Count keyword matches
                for keyword in keywords:
                    match_score += text.count(keyword)
            
            # Only include documents with at least one match
            if match_score > 0:
                results.append({
                    "id": doc_id,
                    "text": doc["text"],
                    "metadata": doc["metadata"],
                    "match_score": match_score
                })
        
        # Sort by match score (descending)
        results.sort(key=lambda x: x["match_score"], reverse=True)
        
        # Return top k results
        return results[:k]
    
    def hybrid_search(self,
                     query: str,
                     query_embedding: List[float],
                     k: int = 5,
                     alpha: float = 0.5,
                     filter_fn: Optional[Callable] = None) -> List[Dict[str, Any]]:
        """
        Combined vector and keyword search for best results.
        
        Args:
            query: Keyword query string
            query_embedding: Vector embedding of the query
            k: Number of results to return
            alpha: Weight of vector search vs keyword search (0.0 = all keyword, 1.0 = all vector)
            filter_fn: Optional function to filter results
            
        Returns:
            List of document dictionaries with combined scores
        """
        # Perform both searches
        vector_results = self.similarity_search(query_embedding, k=k*2, filter_fn=filter_fn)
        keyword_results = self.keyword_search(query, k=k*2)
        
        # Early exit if no results
        if not vector_results and not keyword_results:
            return []
            
        # Create a map of doc_id to result for both result sets
        vector_map = {r["id"]: r for r in vector_results}
        keyword_map = {r["id"]: r for r in keyword_results}
        
        # Combine results and scores
        all_ids = set(vector_map.keys()) | set(keyword_map.keys())
        combined_results = []
        
        for doc_id in all_ids:
            # Get results from both searches if available
            vector_result = vector_map.get(doc_id)
            keyword_result = keyword_map.get(doc_id)
            
            # Calculate combined score
            vector_score = vector_result["similarity"] if vector_result else 0.0
            
            # Normalize keyword score (if we have any keyword results)
            max_keyword_score = max([r["match_score"] for r in keyword_results]) if keyword_results else 1
            keyword_score = (keyword_result["match_score"] / max_keyword_score) if keyword_result else 0.0
            
            # Combine scores with alpha weighting
            combined_score = (alpha * vector_score) + ((1 - alpha) * keyword_score)
            
            # Use the result object that exists, prioritize vector result
            result = vector_result if vector_result else keyword_result
            result["combined_score"] = combined_score
            
            # Add both scores for transparency
            result["vector_score"] = vector_score
            result["keyword_score"] = keyword_score
            
            combined_results.append(result)
        
        # Sort by combined score
        combined_results.sort(key=lambda x: x["combined_score"], reverse=True)
        
        # Apply filter if provided
        if filter_fn:
            combined_results = [r for r in combined_results if filter_fn(r)]
            
        # Return top k results
        return combined_results[:k]
    
    def save(self) -> bool:
        """
        Save index and metadata to disk.
        
        Returns:
            Success status
        """
        try:
            # Save FAISS index
            index_path = self._get_index_path()
            faiss.write_index(self.index, str(index_path))
            
            # Save metadata (documents and doc_ids)
            metadata_path = self._get_metadata_path()
            with open(metadata_path, 'wb') as f:
                pickle.dump({
                    "documents": self.documents,
                    "doc_ids": self.doc_ids,
                    "dimensions": self.dimensions,
                    "index_type": self.index_type
                }, f)
                
            logger.info(f"Saved index with {len(self.doc_ids)} documents to {index_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error saving index: {e}")
            return False
    
    def load(self) -> bool:
        """
        Load index and metadata from disk.
        
        Returns:
            Success status
        """
        index_path = self._get_index_path()
        metadata_path = self._get_metadata_path()
        
        if not index_path.exists() or not metadata_path.exists():
            logger.warning(f"Index or metadata file not found at {index_path}")
            return False
            
        try:
            # Load FAISS index
            self.index = faiss.read_index(str(index_path))
            
            # Load metadata
            with open(metadata_path, 'rb') as f:
                metadata = pickle.load(f)
                
            self.documents = metadata["documents"]
            self.doc_ids = metadata["doc_ids"]
            self.dimensions = metadata.get("dimensions", self.dimensions)
            self.index_type = metadata.get("index_type", self.index_type)
            
            logger.info(f"Loaded index with {len(self.doc_ids)} documents from {index_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error loading index: {e}")
            return False
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the vector store.
        
        Returns:
            Dictionary with stats
        """
        return {
            "index_type": self.index_type,
            "dimensions": self.dimensions,
            "document_count": len(self.doc_ids),
            "index_size": self.index.ntotal if hasattr(self.index, "ntotal") else len(self.doc_ids),
            "index_file": str(self._get_index_path()),
            "is_trained": self.index.is_trained if hasattr(self.index, "is_trained") else True
        }


# Example usage when run as script
if __name__ == "__main__":
    import argparse
    import random
    
    # Configure logging for standalone execution
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    
    parser = argparse.ArgumentParser(description="Vector store for RAG pipeline")
    parser.add_argument("--dims", "-d", type=int, default=1536, help="Vector dimensions")
    parser.add_argument("--store-dir", type=str, help="Directory to store index files")
    parser.add_argument("--index-name", type=str, default="default", help="Name of the index")
    parser.add_argument("--index-type", type=str, default="flat", 
                        choices=["flat", "ivf", "hnsw"], help="Type of index")
    
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # Create command
    create_parser = subparsers.add_parser("create", help="Create a new index")
    
    # Add command
    add_parser = subparsers.add_parser("add", help="Add documents to index")
    add_parser.add_argument("--input", "-i", required=True, help="Input JSON file with embeddings")
    
    # Search command
    search_parser = subparsers.add_parser("search", help="Search the index")
    search_parser.add_argument("--query", "-q", required=True, help="Query text or embedding file")
    search_parser.add_argument("--mode", "-m", default="hybrid", 
                              choices=["vector", "keyword", "hybrid"], help="Search mode")
    search_parser.add_argument("--k", "-k", type=int, default=5, help="Number of results")
    search_parser.add_argument("--alpha", "-a", type=float, default=0.5, 
                              help="Weight of vector vs keyword search (hybrid mode)")
    
    # Info command
    info_parser = subparsers.add_parser("info", help="Show information about the index")
    
    # Parse arguments
    args = parser.parse_args()
    
    # Initialize vector store
    vs = VectorStore(
        dimensions=args.dims,
        index_type=args.index_type,
        store_dir=args.store_dir,
        index_name=args.index_name
    )
    
    if args.command == "create":
        # Create a new empty index
        vs.save()
        print(f"Created empty index: {vs.get_stats()}")
    
    elif args.command == "add":
        # Load existing index if available
        vs.load()
        
        # Load documents with embeddings
        with open(args.input, 'r') as f:
            documents = json.load(f)
        
        print(f"Adding {len(documents)} documents to index")
        doc_ids = vs.add_documents(documents)
        
        # Save updated index
        vs.save()
        print(f"Added {len(doc_ids)} documents to index. New stats: {vs.get_stats()}")
    
    elif args.command == "search":
        # Load index
        if not vs.load():
            print("Error: Failed to load index")
            exit(1)
        
        # Check if query is a file (embedding) or text
        query_is_file = os.path.exists(args.query)
        query_embedding = None
        
        if query_is_file:
            try:
                with open(args.query, 'r') as f:
                    query_embedding = json.load(f)
                print(f"Loaded query embedding from file: {args.query}")
            except:
                print(f"Error: Failed to load embedding from {args.query}")
                exit(1)
        else:
            # For hybrid and keyword search, use query text
            # For vector search with text input, we need embedding service
            if args.mode == "vector":
                print("Error: Vector search requires query embedding file")
                exit(1)
        
        # Perform search based on mode
        if args.mode == "vector":
            results = vs.similarity_search(query_embedding, k=args.k)
        elif args.mode == "keyword":
            results = vs.keyword_search(args.query, k=args.k)
        else:  # hybrid mode
            # For demo, generate a random embedding if none provided
            if query_embedding is None:
                query_embedding = [random.random() for _ in range(args.dims)]
                
            results = vs.hybrid_search(args.query, query_embedding, k=args.k, alpha=args.alpha)
        
        # Display results
        print(f"\nFound {len(results)} results for '{args.query}' using {args.mode} search:\n")
        
        for i, result in enumerate(results):
            print(f"{i+1}. Score: {result.get('combined_score', result.get('similarity', result.get('match_score', 0.0))):.4f}")
            print(f"   ID: {result['id']}")
            
            # Show document metadata
            metadata = result.get("metadata", {})
            if metadata:
                print(f"   Metadata: {', '.join([f'{k}={v}' for k, v in list(metadata.items())[:3]])}")
            
            # Show text preview
            text = result.get("text", "")
            if text:
                preview = text[:100] + "..." if len(text) > 100 else text
                print(f"   Text: {preview}")
            
            print()
    
    elif args.command == "info":
        # Load index
        vs.load()
        
        # Show detailed info
        stats = vs.get_stats()
        print("\nVector Store Information:")
        print(f"Index name: {args.index_name}")
        print(f"Index type: {stats['index_type']}")
        print(f"Dimensions: {stats['dimensions']}")
        print(f"Document count: {stats['document_count']}")
        print(f"Index size: {stats['index_size']}")
        print(f"Index file: {stats['index_file']}")
        print(f"Is trained: {stats['is_trained']}")
        
        # Sample some documents if available
        if vs.documents:
            sample_size = min(3, len(vs.documents))
            sample_ids = list(vs.documents.keys())[:sample_size]
            
            print("\nSample documents:")
            for doc_id in sample_ids:
                doc = vs.documents[doc_id]
                print(f"  ID: {doc_id}")
                print(f"  Metadata: {list(doc['metadata'].keys())}")
                
                # Show text preview
                text = doc.get("text", "")
                if text:
                    preview = text[:100] + "..." if len(text) > 100 else text
                    print(f"  Text: {preview}\n")
    
    else:
        parser.print_help()