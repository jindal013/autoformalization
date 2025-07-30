#!/usr/bin/env python3

import argparse
import json
import sys
from pathlib import Path
from src.application.rag import MathematicalRAGPipeline


def main():
    parser = argparse.ArgumentParser(description="Mathematical formalization with RAG")
    parser.add_argument(
        "--query", type=str, required=True, help="Natural language mathematical query"
    )
    parser.add_argument(
        "--method",
        type=str,
        default="hybrid",
        choices=["bm25", "dense", "hybrid"],
        help="RAG retrieval method (default: hybrid)",
    )
    parser.add_argument(
        "--no-rag", action="store_true", help="Run without RAG (direct generation)"
    )
    parser.add_argument(
        "--top-k",
        type=int,
        default=5,
        help="Number of context chunks to retrieve (default: 5)",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="output.json",
        help="Output file for results (default: output.json)",
    )
    parser.add_argument(
        "--textbook",
        type=str,
        default="dataset/converted.txt",
        help="Path to textbook markdown file (default: dataset/converted.txt)",
    )
    parser.add_argument(
        "--model",
        type=str,
        default="deepseek-ai/DeepSeek-Prover-V2-7B",
        help="HuggingFace model name",
    )

    args = parser.parse_args()

    try:
        print("Initializing RAG pipeline...")
        pipeline = MathematicalRAGPipeline(
            model_name=args.model, textbook_path=args.textbook
        )

        if args.no_rag:
            print(f"Generating Lean code without RAG for query: {args.query}")
            lean_code = pipeline.formalize_without_rag(args.query)

            result = {
                "query": args.query,
                "method": "no_rag",
                "lean_code": lean_code,
                "context_used": None,
                "metrics": None,
            }
        else:
            print(
                f"Generating Lean code with RAG (method: {args.method}) for query: {args.query}"
            )
            lean_code, metrics = pipeline.formalize_with_rag(
                args.query, method=args.method, top_k=args.top_k
            )

            result = {
                "query": args.query,
                "method": args.method,
                "lean_code": lean_code,
                "context_used": metrics.retrieved_contexts,
                "metrics": None,
            }

        with open(args.output, "w") as f:
            json.dump(result, f, indent=2)

        print("\n" + "=" * 50)
        print("RESULTS")
        print("=" * 50)
        print(f"Query: {args.query}")
        print(f"Method: {result['method']}")
        print(f"Generated Lean Code:\n{result['lean_code']}")

        if result["context_used"]:
            print(f"\nRetrieved Context ({len(result['context_used'])} chunks):")
            for i, context in enumerate(result["context_used"], 1):
                print(f"{i}. {context[:200]}...")

        print(f"\nResults saved to: {args.output}")

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
