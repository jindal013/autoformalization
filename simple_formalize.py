#!/usr/bin/env python3

import argparse
import json
import sys
import os
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass


@dataclass
class SimpleRAGMetrics:
    retrieved_contexts: List[str]
    query: str


class SimpleMathematicalRAGPipeline:
    def __init__(self, textbook_path: str = "dataset/converted.md"):
        self.textbook_path = textbook_path
        self._load_textbook()

    def _load_textbook(self):
        if not os.path.exists(self.textbook_path):
            raise FileNotFoundError(f"Textbook not found at {self.textbook_path}")

        with open(self.textbook_path, "r", encoding="utf-8") as f:
            self.textbook_content = f.read()

        self.text_chunks = self.textbook_content.split("\n\n")
        print(f"Loaded textbook with {len(self.text_chunks)} chunks")

    def retrieve_context(
        self, query: str, method: str = "keyword", top_k: int = 5
    ) -> List[str]:
        if method != "keyword":
            print(
                f"Warning: Method '{method}' not available in simple version, using 'keyword'"
            )

        query_words = query.lower().split()
        chunk_scores = []

        for i, chunk in enumerate(self.text_chunks):
            score = 0
            chunk_lower = chunk.lower()
            for word in query_words:
                if len(word) > 3:
                    score += chunk_lower.count(word)
            chunk_scores.append((score, i))

        chunk_scores.sort(reverse=True)
        top_indices = [i for score, i in chunk_scores[:top_k] if score > 0]

        return [self.text_chunks[i] for i in top_indices]

    def generate_lean_code(
        self, query: str, context: Optional[List[str]] = None
    ) -> str:
        if context:
            context_text = "\n".join(context[:2])
            lean_code = f"""-- Generated from query: {query}
-- Context used: {len(context)} chunks

-- Placeholder Lean code (replace with actual model output)
theorem example : Prop := sorry

-- Context information:
-- {context_text[:200]}...
"""
        else:
            lean_code = f"""-- Generated from query: {query}
-- No context used

-- Placeholder Lean code (replace with actual model output)
theorem example : Prop := sorry
"""

        return lean_code

    def formalize_with_rag(
        self, query: str, method: str = "keyword", top_k: int = 5
    ) -> Tuple[str, SimpleRAGMetrics]:
        context = self.retrieve_context(query, method, top_k)
        lean_code = self.generate_lean_code(query, context)

        metrics = SimpleRAGMetrics(retrieved_contexts=context, query=query)

        return lean_code, metrics

    def formalize_without_rag(self, query: str) -> str:
        return self.generate_lean_code(query, context=None)


def main():
    parser = argparse.ArgumentParser(
        description="Simple mathematical formalization with RAG"
    )
    parser.add_argument(
        "--query", type=str, required=True, help="Natural language mathematical query"
    )
    parser.add_argument(
        "--method",
        type=str,
        default="keyword",
        choices=["keyword"],
        help="RAG retrieval method (default: keyword)",
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
        default="dataset/converted.md",
        help="Path to textbook markdown file (default: dataset/converted.md)",
    )

    args = parser.parse_args()

    try:
        print("Initializing simple RAG pipeline...")
        pipeline = SimpleMathematicalRAGPipeline(textbook_path=args.textbook)

        if args.no_rag:
            print(f"Generating Lean code without RAG for query: {args.query}")
            lean_code = pipeline.formalize_without_rag(args.query)

            result = {
                "query": args.query,
                "method": "no_rag",
                "lean_code": lean_code,
                "context_used": None,
                "note": "This is a simplified version without ML models",
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
                "note": "This is a simplified version without ML models",
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

        print(f"\nNote: {result['note']}")
        print(f"Results saved to: {args.output}")

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
