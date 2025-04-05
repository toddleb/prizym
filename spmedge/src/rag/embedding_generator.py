#!/usr/bin/env python3
"""
Embedding Generator - Creates vector embeddings for document chunks.
- Supports multiple embedding models (OpenAI, HuggingFace, etc.)
- Optimizes batch processing for efficiency
- Includes caching mechanism to reduce API costs
"""

import os
import json
import time
import logging
import hashlib
import numpy as np
from pathlib import Path
from typing import List, Dict, Any, Tuple, Optional, Union
from functools import lru_cache

from config.config import config
from src.utils.openai_client import OpenAIProcessor

# Configure logging
logger = logging.getLogger("embedding_generator")
logger.setLevel(logging.INFO)

class EmbeddingGenerator:
    """Generates and manages vector embeddings for document chunks."""
    
    EMBEDDING_MODELS = {
        "openai": {
            "dimensions": 1536,
            "max_tokens": 8191,
            "model_name": "text-embedding-ada-002"
        },
        "openai-3": {
            "dimensions": 3072,
            "max_tokens": 8191,
            "model_name": "text-embedding-3-large"
        },
        "openai-3-small": {
            "dimensions": 1536,
            "max_tokens": 8191,
            "model_name": "text-embedding-3-small"
        },
        "huggingface-mpnet": {
            "dimensions": 768,
            "max_tokens": 512,
            "model_name": "sentence-transformers/all-mpnet-base-v2"
        },
        "huggingface-minilm": {
            "dimensions": 384,
            "max_tokens": 512,
            "model_name": "sentence-transformers/all-MiniLM-L6-v2"
        }
    }
    
    def __init__(self, 
                 model_name: str = "openai",
                 cache_dir: Optional[str] = None,
                 use_cache: bool = True,
                 batch_size: int = 20):
        """
        Initialize embedding generator with model settings.
        
        Args:
            model_name: Name of embedding model to use (key in EMBEDDING_MODELS)
            cache_dir: Directory to store embedding cache
            use_cache: Whether to use embedding caching
            batch_size: Number of texts to embed in one batch
        """
        self.model_name = model_name
        
        # Validate model selection
        if model_name not in self.EMBEDDING_MODELS:
            logger.warning(f"Unknown embedding model: {model_name}, falling back to OpenAI")
            self.model_name = "openai"
            
        self.model_config = self.EMBEDDING_MODELS[self.model_name]
        self.dimensions = self.model_config["dimensions"]
        self.max_tokens = self.model_config["max_tokens"]
        self.use_cache = use_cache
        self.batch_size = batch_size
        
        # Initialize cache
        if use_cache:
            self.cache_dir = Path(cache_dir) if cache_dir else Path(config.DATA_DIR) / "embeddings_cache"
            self.cache_dir.mkdir(parents=True, exist_ok=True)
            logger.info(f"Embeddings cache directory: {self.cache_dir}")
        
        # Initialize API clients
        if self.model_name.startswith("openai"):
            try:
                self.openai_client = OpenAIProcessor()
                logger.info(f"Initialized OpenAI client for {self.model_name}")
            except Exception as e:
                logger.error(f"Failed to initialize OpenAI client: {e}")
                raise
        elif self.model_name.startswith("huggingface"):
            try:
                self._init_huggingface_model()
            except Exception as e:
                logger.error(f"Failed to initialize HuggingFace model: {e}")
                raise
    
    def _init_huggingface_model(self):
        """Initialize a HuggingFace transformer model for embeddings."""
        try:
            from sentence_transformers import SentenceTransformer
            model_id = self.model_config["model_name"]
            self.hf_model = SentenceTransformer(model_id)
            logger.info(f"Loaded HuggingFace model: {model_id}")
        except ImportError:
            logger.error("SentenceTransformer not installed. Install with: pip install sentence-transformers")
            raise
    
    def _get_cache_key(self, text: str) -> str:
        """Generate a cache key for a text by hashing its content."""
        return hashlib.md5(text.encode('utf-8')).hexdigest()
    
    def _get_cache_path(self, cache_key: str) -> Path:
        """Get the file path for a cached embedding."""
        return self.cache_dir / f"{cache_key}_{self.model_name}.json"
    
    def _load_from_cache(self, cache_key: str) -> Optional[List[float]]:
        """Load embedding from cache if available."""
        if not self.use_cache:
            return None
            
        cache_path = self._get_cache_path(cache_key)
        
        if cache_path.exists():
            try:
                with open(cache_path, 'r') as f:
                    cached_data = json.load(f)
                    # Verify dimensions match current model
                    if len(cached_data) == self.dimensions:
                        logger.debug(f"Cache hit for {cache_key}")
                        return cached_data
                    else:
                        logger.debug(f"Cache dimensions mismatch: {len(cached_data)} vs {self.dimensions}")
                        return None
            except Exception as e:
                logger.warning(f"Failed to load from cache: {e}")
                return None
        return None
    
    def _save_to_cache(self, cache_key: str, embedding: List[float]):
        """Save embedding to cache."""
        if not self.use_cache:
            return
            
        cache_path = self._get_cache_path(cache_key)
        
        try:
            with open(cache_path, 'w') as f:
                json.dump(embedding, f)
        except Exception as e:
            logger.warning(f"Failed to save to cache: {e}")
    
    def generate_openai_embedding(self, text: str) -> List[float]:
        """Generate an embedding using OpenAI's API."""
        if not self.openai_client:
            raise ValueError("OpenAI client not initialized")
            
        try:
            response = self.openai_client.client.embeddings.create(
                model=self.model_config["model_name"],
                input=text
            )
            embedding = response.data[0].embedding
            return embedding
        except Exception as e:
            logger.error(f"OpenAI embedding error: {e}")
            # Return a zero vector as fallback
            return [0.0] * self.dimensions
    
    def generate_huggingface_embedding(self, text: str) -> List[float]:
        """Generate an embedding using HuggingFace's SentenceTransformer."""
        if not hasattr(self, 'hf_model'):
            raise ValueError("HuggingFace model not initialized")
            
        try:
            embedding = self.hf_model.encode(text)
            return embedding.tolist()
        except Exception as e:
            logger.error(f"HuggingFace embedding error: {e}")
            # Return a zero vector as fallback
            return [0.0] * self.dimensions
    
    def generate_embedding(self, text: str) -> List[float]:
        """
        Generate an embedding for a single text.
        
        Args:
            text: Text to generate embedding for
            
        Returns:
            List of embedding values
        """
        # Check if embedding is in cache
        cache_key = self._get_cache_key(text)
        cached_embedding = self._load_from_cache(cache_key)
        
        if cached_embedding is not None:
            return cached_embedding
        
        # Generate new embedding based on selected model
        if self.model_name.startswith("openai"):
            embedding = self.generate_openai_embedding(text)
        elif self.model_name.startswith("huggingface"):
            embedding = self.generate_huggingface_embedding(text)
        else:
            raise ValueError(f"Unsupported embedding model: {self.model_name}")
        
        # Save to cache
        self._save_to_cache(cache_key, embedding)
        
        return embedding
    
    def generate_embeddings_batch(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for a batch of texts.
        
        Args:
            texts: List of texts to generate embeddings for
            
        Returns:
            List of embedding vectors
        """
        # Check which texts need embedding (not in cache)
        cache_hits = {}
        texts_to_embed = []
        text_indices = []
        
        # Check cache first
        for i, text in enumerate(texts):
            cache_key = self._get_cache_key(text)
            cached_embedding = self._load_from_cache(cache_key)
            
            if cached_embedding is not None:
                cache_hits[i] = cached_embedding
            else:
                texts_to_embed.append(text)
                text_indices.append(i)
        
        logger.info(f"Cache hits: {len(cache_hits)}/{len(texts)} texts")
        
        # If all texts are in cache, return immediately
        if not texts_to_embed:
            # Assemble results in original order
            return [cache_hits[i] for i in range(len(texts))]
        
        # Generate embeddings for uncached texts
        if self.model_name.startswith("openai"):
            # Use OpenAI's batch API
            try:
                # Process in smaller batches to avoid rate limits
                all_embeddings = []
                
                for i in range(0, len(texts_to_embed), self.batch_size):
                    batch = texts_to_embed[i:i + self.batch_size]
                    response = self.openai_client.client.embeddings.create(
                        model=self.model_config["model_name"],
                        input=batch
                    )
                    batch_embeddings = [item.embedding for item in response.data]
                    all_embeddings.extend(batch_embeddings)
                    
                    # Rate limit handling
                    if len(texts_to_embed) > self.batch_size and i + self.batch_size < len(texts_to_embed):
                        time.sleep(0.5)  # Add delay between batches
                    
            except Exception as e:
                logger.error(f"OpenAI batch embedding error: {e}")
                # Fallback to individual embedding
                logger.info("Falling back to individual embedding")
                all_embeddings = []
                for text in texts_to_embed:
                    embedding = self.generate_embedding(text)
                    all_embeddings.append(embedding)
                
        elif self.model_name.startswith("huggingface"):
            # Use HuggingFace batch encoding
            try:
                batch_embeddings = self.hf_model.encode(texts_to_embed)
                all_embeddings = batch_embeddings.tolist()
            except Exception as e:
                logger.error(f"HuggingFace batch embedding error: {e}")
                # Fallback to individual embedding
                all_embeddings = []
                for text in texts_to_embed:
                    embedding = self.generate_embedding(text)
                    all_embeddings.append(embedding)
                    
        else:
            raise ValueError(f"Unsupported embedding model: {self.model_name}")
        
        # Save to cache
        for i, embedding in enumerate(all_embeddings):
            cache_key = self._get_cache_key(texts_to_embed[i])
            self._save_to_cache(cache_key, embedding)
        
        # Merge cache hits and new embeddings
        result = [None] * len(texts)
        
        # Add cache hits
        for i, embedding in cache_hits.items():
            result[i] = embedding
            
        # Add new embeddings
        for i, embedding in zip(text_indices, all_embeddings):
            result[i] = embedding
            
        return result
    
    def embed_chunks(self, chunks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Generate embeddings for a list of document chunks.
        
        Args:
            chunks: List of chunk dictionaries with 'text' and 'metadata' fields
            
        Returns:
            List of chunks with added 'embedding' field
        """
        # Extract text from chunks
        texts = [chunk["text"] for chunk in chunks]
        
        # Generate embeddings
        embeddings = self.generate_embeddings_batch(texts)
        
        # Add embeddings to chunks
        result = []
        for i, chunk in enumerate(chunks):
            chunk_with_embedding = chunk.copy()
            chunk_with_embedding["embedding"] = embeddings[i]
            chunk_with_embedding["metadata"]["embedding_model"] = self.model_name
            chunk_with_embedding["metadata"]["embedding_dimensions"] = self.dimensions
            result.append(chunk_with_embedding)
            
        logger.info(f"Generated embeddings for {len(result)} chunks using {self.model_name}")
        return result
    
    def get_embedding_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the embedding cache.
        
        Returns:
            Dictionary with cache statistics
        """
        if not self.use_cache:
            return {"enabled": False}
            
        try:
            cache_files = list(self.cache_dir.glob(f"*_{self.model_name}.json"))
            
            # Sample some embeddings to verify dimensions
            dimensions = []
            if cache_files:
                for file in cache_files[:5]:
                    try:
                        with open(file, 'r') as f:
                            embedding = json.load(f)
                            dimensions.append(len(embedding))
                    except:
                        pass
            
            return {
                "enabled": True,
                "model": self.model_name,
                "cache_dir": str(self.cache_dir),
                "cache_size": len(cache_files),
                "dimensions": self.dimensions,
                "sampled_dimensions": dimensions
            }
        except Exception as e:
            logger.error(f"Error getting cache stats: {e}")
            return {"enabled": True, "error": str(e)}


# Example usage when run as script
if __name__ == "__main__":
    import argparse
    
    # Configure logging for standalone execution
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    
    parser = argparse.ArgumentParser(description="Embedding generator for RAG pipeline")
    parser.add_argument("--model", "-m", type=str, default="openai", 
                        choices=list(EmbeddingGenerator.EMBEDDING_MODELS.keys()),
                        help="Embedding model to use")
    parser.add_argument("--text", "-t", type=str, help="Text to embed")
    parser.add_argument("--file", "-f", type=str, help="JSON file with chunks to embed")
    parser.add_argument("--output", "-o", type=str, help="Output file for embeddings")
    parser.add_argument("--no-cache", action="store_true", help="Disable embedding cache")
    
    args = parser.parse_args()
    
    # Initialize generator
    generator = EmbeddingGenerator(
        model_name=args.model,
        use_cache=not args.no_cache
    )
    
    # Show cache stats
    print("Embedding Generator initialized:")
    print(f"Model: {generator.model_name}")
    print(f"Dimensions: {generator.dimensions}")
    
    stats = generator.get_embedding_stats()
    if stats["enabled"]:
        print(f"Cache: {stats['cache_size']} embeddings in {stats['cache_dir']}")
    else:
        print("Cache: Disabled")
    
    # Process text or file
    if args.text:
        embedding = generator.generate_embedding(args.text)
        print(f"\nGenerated embedding with {len(embedding)} dimensions")
        print(f"First 5 values: {embedding[:5]}")
        
        if args.output:
            with open(args.output, 'w') as f:
                json.dump(embedding, f)
            print(f"Saved embedding to {args.output}")
    
    elif args.file:
        # Load chunks from file
        with open(args.file, 'r') as f:
            chunks = json.load(f)
            
        if isinstance(chunks, list):
            # Ensure proper format
            if chunks and isinstance(chunks[0], dict) and 'text' in chunks[0]:
                print(f"Processing {len(chunks)} chunks from {args.file}")
                chunks_with_embeddings = generator.embed_chunks(chunks)
                
                if args.output:
                    with open(args.output, 'w') as f:
                        json.dump(chunks_with_embeddings, f, indent=2)
                    print(f"Saved {len(chunks_with_embeddings)} embedded chunks to {args.output}")
                else:
                    # Just print summary
                    print(f"Generated embeddings for {len(chunks_with_embeddings)} chunks")
                    if chunks_with_embeddings:
                        emb = chunks_with_embeddings[0]["embedding"]
                        print(f"Sample embedding dimensions: {len(emb)}")
                        print(f"First 5 values: {emb[:5]}")
            else:
                print("Error: Invalid chunk format. Expected list of dicts with 'text' field")
        else:
            print("Error: Invalid JSON format. Expected list of chunks")
    
    else:
        print("Error: Neither text nor file specified")
        parser.print_help()