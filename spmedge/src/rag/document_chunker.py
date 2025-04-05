#!/usr/bin/env python3
"""
Document Chunker - Creates semantic chunks from processed documents for RAG.
- Implements intelligent chunking strategies
- Preserves document structure and metadata
- Optimizes chunk size for embedding and retrieval
- Implements content-aware density-based chunking
"""

import re
import json
import logging
import numpy as np
from pathlib import Path
from typing import List, Dict, Any, Tuple, Optional

from config.config import config

# Configure logging
logger = logging.getLogger("document_chunker")
logger.setLevel(logging.INFO)

class DocumentChunker:
    """Handles semantic chunking of documents for the RAG system."""
    
    def __init__(self, 
                 chunk_size: int = 512, 
                 chunk_overlap: int = 50,
                 max_chunks_per_doc: int = 100):
        """
        Initialize chunker with configuration.
        
        Args:
            chunk_size: Target size of each chunk in tokens (approximate)
            chunk_overlap: Number of tokens to overlap between chunks
            max_chunks_per_doc: Maximum chunks to create per document
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.max_chunks_per_doc = max_chunks_per_doc
        self.avg_chars_per_token = 4  # Approximation for token counting
        
        # Patterns for detecting semantic breaks
        self.section_patterns = [
            r'\n\s*#{1,6}\s+',  # Markdown headings
            r'\n\s*[A-Z][A-Z\s]+:',  # ALL CAPS section headers
            r'\n\s*\d+\.\s+[A-Z]',  # Numbered sections
            r'\n\s*•\s+',  # Bullet points
            r'\n\s*\*\s+',  # Asterisk bullet points
            r'\n\s*-\s+',  # Hyphen bullet points
            r'\n\s*[IVX]+\.\s+',  # Roman numeral sections
            r'\n\s*[A-Z]\.\s+',  # Lettered sections
            r'\n\s*Article\s+\d+',  # Legal document articles
            r'\n\s*Section\s+\d+',  # Legal document sections
            r'\n\s*ARTICLE\s+[IVX]+',  # Legal document ARTICLES (Roman numerals)
            r'\n\s*SECTION\s+\d+',  # Legal document SECTIONS
            r'\n\s*Purpose:',  # Common document sections
            r'\n\s*Overview:',
            r'\n\s*Introduction:',
            r'\n\s*Background:',
            r'\n\s*Summary:',
            r'\n\s*Conclusion:',
            r'\n\s*Eligibility:',
            r'\n\s*Compensation:',
            r'\n\s*Commission:',
        ]
        
        # Table patterns
        self.table_patterns = [
            r'(\|\s*[\w\s]+\s*\|)+',  # Markdown tables
            r'(\+[-+]+\+)',  # ASCII tables
            r'(\d+\.?\d*%\s+\d+\.?\d*%)', # Multiple percentages (likely a table row)
            r'(\$\d+\.?\d*\s+\$\d+\.?\d*)', # Multiple dollar amounts (likely a table row)
        ]
        
        # Formula patterns (especially for compensation plans)
        self.formula_patterns = [
            r'(\d+\.?\d*%\s+of\s+[\w\s]+)',  # Percentage formulas
            r'(\$\d+\.?\d*\s+per\s+[\w\s]+)',  # Monetary formulas
            r'(quota.*?attainment)',  # Quota attainment
            r'(target.*?bonus)',  # Target bonus
            r'(bonus.*?calculation)',  # Bonus calculation
            r'(commission.*?rate)',  # Commission rate
        ]
        
        # Compiled regex for better performance
        self.section_regex = re.compile('|'.join(self.section_patterns), re.MULTILINE)
        self.table_regex = re.compile('|'.join(self.table_patterns), re.MULTILINE)
        self.formula_regex = re.compile('|'.join(self.formula_patterns), re.MULTILINE | re.IGNORECASE)
        
    def _estimate_tokens(self, text: str) -> int:
        """Estimate the number of tokens in a text string."""
        return len(text) // self.avg_chars_per_token
    
    def _find_semantic_breaks(self, text: str) -> List[int]:
        """Find positions of semantic breaks in the text."""
        # Find all matches of semantic patterns
        matches = list(self.section_regex.finditer(text))
        break_positions = [m.start() for m in matches]
        
        # Add breaks for tables
        table_matches = list(self.table_regex.finditer(text))
        for match in table_matches:
            # Only add table breaks if they're significant in length
            if match.end() - match.start() > 20:
                break_positions.append(match.start())
        
        # Add breaks for formulas
        formula_matches = list(self.formula_regex.finditer(text))
        break_positions.extend([m.start() for m in formula_matches])
        
        # Always include the start of the document
        if 0 not in break_positions:
            break_positions.insert(0, 0)
            
        # Sort positions (should already be in order, but just to be safe)
        break_positions.sort()
        
        return break_positions
    
    def _create_chunks_from_breaks(self, text: str, break_positions: List[int]) -> List[str]:
        """Create chunks from text using semantic break positions."""
        chunks = []
        
        for i in range(len(break_positions)):
            start_pos = break_positions[i]
            
            # Determine end position (either next break or end of text)
            if i < len(break_positions) - 1:
                end_pos = break_positions[i + 1]
            else:
                end_pos = len(text)
            
            chunk_text = text[start_pos:end_pos].strip()
            
            # Skip empty chunks
            if not chunk_text:
                continue
                
            # If chunk is too large, split it further
            chunk_tokens = self._estimate_tokens(chunk_text)
            if chunk_tokens > self.chunk_size * 1.5:
                # Content is too large for a single chunk
                sub_chunks = self._split_large_chunk(chunk_text)
                chunks.extend(sub_chunks)
            else:
                chunks.append(chunk_text)
                
        return chunks
    
    def _calculate_content_density(self, text: str) -> float:
        """Calculate the information density of a text segment."""
        if not text:
            return 0.0
            
        # Count "information-rich" characters
        special_chars = sum(1 for c in text if c in '0123456789$%.,;:()[]{}')
        numeric_density = special_chars / len(text)
        
        # Count structure indicators
        bullet_points = len(re.findall(r'[•\*\-]\s+', text))
        headings = len(re.findall(r'#+\s+|\n[A-Z][A-Z\s]+[:\n]', text))
        table_rows = len(re.findall(r'\|\s*[\w\s]+\s*\|', text))
        
        # Count key business terms (commonly found in compensation plans)
        business_terms = len(re.findall(r'quota|bonus|commission|revenue|sales|target|goal|payout|incentive', 
                                         text, re.IGNORECASE))
        
        # Weight the indicators (adjust these weights based on testing)
        structure_score = (bullet_points * 0.01 + headings * 0.05 + table_rows * 0.05)
        term_score = business_terms * 0.01
        
        # Combine scores (cap at 1.0)
        density = min(1.0, numeric_density + structure_score + term_score)
        
        return density
    
    def _split_large_chunk(self, text: str) -> List[str]:
        """Split an oversized chunk into smaller chunks based on content density."""
        # First try to split by paragraphs
        paragraphs = re.split(r'\n\s*\n', text)
        
        if len(paragraphs) > 1:
            # We have multiple paragraphs, process them adaptively
            result = []
            current_chunk = ""
            current_tokens = 0
            
            for para in paragraphs:
                para = para.strip()
                if not para:
                    continue
                    
                # Calculate density to determine target size
                density = self._calculate_content_density(para)
                para_tokens = self._estimate_tokens(para)
                
                # Adjust target size based on density - denser content gets smaller chunks
                density_factor = 1.0 - (density * 0.5)  # 0.5 to 1.0 depending on density
                target_size = int(self.chunk_size * density_factor)
                
                # Dense paragraphs get their own chunks
                if density > 0.15 and para_tokens > 100:
                    # If we have a current chunk, add it to results
                    if current_chunk:
                        result.append(current_chunk)
                        current_chunk = ""
                        current_tokens = 0
                    
                    # Put the dense paragraph in its own chunk
                    result.append(para)
                    continue
                
                # If adding this paragraph would make the chunk too large, start a new chunk
                if current_tokens + para_tokens > target_size and current_chunk:
                    result.append(current_chunk)
                    current_chunk = para
                    current_tokens = para_tokens
                else:
                    if current_chunk:
                        current_chunk += "\n\n" + para
                    else:
                        current_chunk = para
                    current_tokens += para_tokens
            
            # Add the last chunk if not empty
            if current_chunk:
                result.append(current_chunk)
                
            return result
        else:
            # No paragraph breaks, fall back to sentence splitting
            return self._split_by_sentences(text)
    
    def _split_by_sentences(self, text: str) -> List[str]:
        """Split text by sentences when no paragraph breaks are available."""
        # More sophisticated sentence detection
        sentence_endings = r'(?<=[.!?])\s+(?=[A-Z])'
        sentences = re.split(sentence_endings, text)
        
        result = []
        current_chunk = ""
        current_tokens = 0
        
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue
                
            sentence_tokens = self._estimate_tokens(sentence)
            
            # If adding this sentence would make the chunk too large, start a new chunk
            if current_tokens + sentence_tokens > self.chunk_size and current_chunk:
                result.append(current_chunk)
                current_chunk = sentence
                current_tokens = sentence_tokens
            else:
                if current_chunk:
                    current_chunk += " " + sentence
                else:
                    current_chunk = sentence
                current_tokens += sentence_tokens
        
        # Add the last chunk if not empty
        if current_chunk:
            result.append(current_chunk)
            
        # If we still have very large chunks, use fixed size chunking as a fallback
        if not result or any(self._estimate_tokens(chunk) > self.chunk_size * 1.5 for chunk in result):
            return self._fixed_size_chunks(text)
        
        return result
    
    def _fixed_size_chunks(self, text: str) -> List[str]:
        """Create fixed-size chunks with overlap as a last resort."""
        target_chars = self.chunk_size * self.avg_chars_per_token
        overlap_chars = self.chunk_overlap * self.avg_chars_per_token
        
        chunks = []
        start = 0
        
        while start < len(text):
            # Calculate end position
            end = start + target_chars
            if end >= len(text):
                end = len(text)
            else:
                # Try to break at a sentence or period to avoid cutting mid-sentence
                sentence_end = text.rfind('. ', start, end)
                if sentence_end > start + (target_chars // 2):
                    end = sentence_end + 1  # Include the period
                else:
                    # Fall back to breaking at a space
                    space = text.rfind(' ', start, end)
                    if space > start + (target_chars // 3):
                        end = space
            
            # Extract the chunk
            chunk = text[start:end].strip()
            if chunk:
                chunks.append(chunk)
            
            # Move start position for next chunk, accounting for overlap
            start = max(start + 100, end - overlap_chars)  # Ensure at least 100 chars progress
                
            # Safety check
            if start >= len(text) or start <= 0:
                break
                
        return chunks
    
    def _create_intelligent_chunks(self, text: str) -> List[str]:
        """Create intelligent chunks based on document structure and content density."""
        # Try to find semantic breaks first
        break_positions = self._find_semantic_breaks(text)
        
        # If we found sufficient breaks, use them
        if len(break_positions) > 3:
            return self._create_chunks_from_breaks(text, break_positions)
        
        # Otherwise, use content density to create variable-sized chunks
        chunks = []
        paragraphs = re.split(r'\n\s*\n', text)
        
        current_chunk = ""
        current_size = 0
        token_density_threshold = 0.7  # Adjust based on content type
        
        for para in paragraphs:
            para = para.strip()
            if not para:
                continue
                
            # Calculate information density
            density = self._calculate_content_density(para)
            
            # Adjust target size based on density
            para_target_size = int(self.chunk_size * (1 - density * token_density_threshold))
            para_tokens = self._estimate_tokens(para)
            
            # If adding this paragraph would exceed chunk size or it's high density content
            if (current_size + para_tokens > para_target_size and current_chunk) or density > 0.2:
                # Save current chunk and start a new one
                chunks.append(current_chunk)
                current_chunk = para
                current_size = para_tokens
            else:
                # Add to current chunk
                if current_chunk:
                    current_chunk += "\n\n" + para
                else:
                    current_chunk = para
                current_size += para_tokens
        
        # Add the last chunk
        if current_chunk:
            chunks.append(current_chunk)
            
        return chunks
        
    def create_chunks(self, 
                     document_id: str,
                     content: str, 
                     metadata: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """
        Create semantic chunks from document content.
        
        Args:
            document_id: ID of the document
            content: Full text content of the document
            metadata: Additional document metadata
            
        Returns:
            List of chunk dictionaries with text and metadata
        """
        # Use intelligent chunking strategy
        initial_chunks = self._create_intelligent_chunks(content)
        
        # Limit number of chunks if needed
        if len(initial_chunks) > self.max_chunks_per_doc:
            logger.warning(f"Document {document_id} has {len(initial_chunks)} chunks, limiting to {self.max_chunks_per_doc}")
            initial_chunks = initial_chunks[:self.max_chunks_per_doc]
        
        # Create chunk objects with metadata
        doc_metadata = metadata or {}
        
        chunk_objects = []
        for i, chunk_text in enumerate(initial_chunks):
            # Prepare chunk metadata
            chunk_metadata = doc_metadata.copy()
            chunk_metadata.update({
                "document_id": document_id,
                "chunk_id": f"{document_id}_chunk_{i+1}",
                "chunk_index": i,
                "total_chunks": len(initial_chunks),
                "tokens": self._estimate_tokens(chunk_text),
                "density": self._calculate_content_density(chunk_text),
                "chunk_type": "semantic"
            })
            
            # Add position info (start/middle/end)
            if i == 0:
                chunk_metadata["position"] = "start"
            elif i == len(initial_chunks) - 1:
                chunk_metadata["position"] = "end"
            else:
                chunk_metadata["position"] = "middle"
            
            chunk_objects.append({
                "text": chunk_text,
                "metadata": chunk_metadata
            })
        
        logger.info(f"🧩 Created {len(chunk_objects)} chunks for document {document_id}")
        return chunk_objects
    
    def chunk_document_from_file(self, 
                                document_path: Path,
                                document_id: str = None) -> List[Dict[str, Any]]:
        """
        Load document from file and create chunks.
        
        Args:
            document_path: Path to document file
            document_id: Optional document ID (defaults to filename)
            
        Returns:
            List of chunk dictionaries
        """
        try:
            # Generate document ID from filename if not provided
            if not document_id:
                document_id = document_path.stem
            
            # Load document content
            with open(document_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Extract metadata if JSON
            metadata = {}
            if document_path.suffix == '.json':
                try:
                    data = json.loads(content)
                    if isinstance(data, dict) and 'content' in data:
                        metadata = {k: v for k, v in data.items() if k != 'content'}
                        content = data['content']
                except json.JSONDecodeError:
                    # If failed to parse as JSON, treat as plain text
                    logger.warning(f"⚠️ Failed to parse JSON: {str(e)} — treating as plain text")
                except Exception as e:
                    # Other errors
                    logger.warning(f"⚠️ Error processing JSON: {str(e)}")
            
            # Add file metadata
            metadata.update({
                "filename": document_path.name,
                "file_path": str(document_path),
                "file_type": document_path.suffix,
                "file_size": document_path.stat().st_size,
                "chunk_method": "intelligent"
            })
            
            return self.create_chunks(document_id, content, metadata)
            
        except Exception as e:
            logger.error(f"❌ Failed to chunk document {document_path}: {e}")
            return []