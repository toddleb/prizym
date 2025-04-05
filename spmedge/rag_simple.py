#!/usr/bin/env python3
"""
Simple RAG CLI utility - Fixed to use keyword search
"""
import argparse
import sys
from src.rag.rag_engine import RAGEngine

def main():
    parser = argparse.ArgumentParser(description="RAG Query Tool")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # Query command
    query_parser = subparsers.add_parser("query", help="Query the knowledge base")
    query_parser.add_argument("--query", "-q", required=True, help="Query text")
    query_parser.add_argument("--k", type=int, default=5, help="Number of results")
    query_parser.add_argument("--mode", choices=["vector", "keyword", "hybrid"], default="keyword", 
                            help="Search mode (default: keyword)")
    query_parser.add_argument("--preview", "-p", action="store_true", help="Show content previews")
    
    args = parser.parse_args()
    
    # Initialize RAG engine
    rag = RAGEngine()
    
    if args.command == "query":
        print(f"Query: {args.query}")
        result = rag.query(
            query=args.query, 
            k=args.k, 
            mode=args.mode  # Now defaults to keyword
        )
        
        print("\nAnswer:")
        print(result["answer"])
        
        print("\nSources:")
        for i, doc in enumerate(result.get("documents", [])[:args.k]):
            source = doc.get("metadata", {}).get("chunk_id", "unknown")
            if args.mode == "hybrid":
                score = doc.get("combined_score", 0.0)
            elif args.mode == "vector":
                score = doc.get("similarity", 0.0)
            else:
                score = doc.get("match_score", 0.0)
            print(f"  {i+1}. {source} (Score: {score:.2f})")
            
            # Show preview if requested
            if args.preview:
                text = doc.get("text", "")
                if text:
                    print(f"     Preview: {text[:150]}...")
    else:
        parser.print_help()
        return 1
        
    return 0

if __name__ == "__main__":
    sys.exit(main())
