#!/usr/bin/env python3
"""
PDF to Markdown Converter
This script extracts text from PDFs and saves it as Markdown in the correct directory.
"""

import os
import argparse
import sys
import logging
from pathlib import Path
import fitz  # PyMuPDF for PDF text extraction

# Ensure the project root is in the path
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__) + "/../..")
sys.path.append(PROJECT_ROOT)

from config.config import config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger("pdf_to_md")

def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF file."""
    try:
        doc = fitz.open(pdf_path)
        text = "\n".join([page.get_text() for page in doc])
        return text if text.strip() else None
    except Exception as e:
        logger.error(f"❌ Error extracting text from {pdf_path}: {e}")
        return None

def save_as_markdown(text, output_path):
    """Save extracted text as a Markdown file."""
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(text)
        return True
    except Exception as e:
        logger.error(f"❌ Error saving markdown file {output_path}: {e}")
        return False

def main():
    """Main entry point for the PDF converter script."""
    parser = argparse.ArgumentParser(description="Convert PDF files to Markdown for processing.")
    parser.add_argument("input", type=str, help="PDF file or directory containing PDFs")
    parser.add_argument("--output-dir", type=str, default=None, 
                        help="Output directory for markdown files (default: data/processed_docs)")
    args = parser.parse_args()
    
    # Set up input and output paths
    input_path = Path(args.input)
    
    # Ensure files are saved in `processed_docs/`
    output_dir = Path(args.output_dir) if args.output_dir else Path(config.PROCESSED_DOCS_DIR)
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Process single file or directory
    if input_path.is_file() and input_path.suffix.lower() == ".pdf":
        logger.info(f"🔍 Processing single PDF file: {input_path.name}")
        
        # Extract text
        text = extract_text_from_pdf(input_path)
        if not text:
            logger.error(f"❌ Failed to extract text from {input_path.name}")
            return 1
        
        # Save as markdown
        output_path = output_dir / f"{input_path.stem}.md"
        if save_as_markdown(text, output_path):
            logger.info(f"✅ Markdown saved to: {output_path}")
        else:
            logger.error(f"❌ Failed to save markdown file for {input_path.name}")
            return 1
    
    elif input_path.is_dir():
        logger.info(f"🔍 Processing PDF files in directory: {input_path}")
        
        # Find PDF files
        pdf_files = list(input_path.glob("*.pdf")) + list(input_path.glob("*.PDF"))
        
        if not pdf_files:
            logger.warning(f"⚠ No PDF files found in {input_path}")
            return 1
        
        logger.info(f"✅ Found {len(pdf_files)} PDF files")
        
        processed = 0
        for pdf_file in pdf_files:
            logger.info(f"🔍 Processing {pdf_file.name}")
            
            # Extract text
            text = extract_text_from_pdf(pdf_file)
            if not text:
                logger.error(f"❌ Failed to extract text from {pdf_file.name}")
                continue
            
            # Save as markdown
            output_path = output_dir / f"{pdf_file.stem}.md"
            if save_as_markdown(text, output_path):
                logger.info(f"✅ Markdown saved to: {output_path}")
                processed += 1
            else:
                logger.error(f"❌ Failed to save markdown file for {pdf_file.name}")
        
        logger.info(f"🎯 Processed {processed} out of {len(pdf_files)} PDF files")
    
    else:
        logger.error(f"❌ Invalid input path: {input_path}")
        return 1
    
    logger.info("🎯 PDF conversion complete")
    return 0

if __name__ == "__main__":
    sys.exit(main())