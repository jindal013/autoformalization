#!/usr/bin/env python3

import json
from src.application.rag import MathematicalRAGPipeline


def test_formalization():
    test_queries = [
        "The sum of two real numbers is commutative",
        "A function is continuous at a point if for every epsilon greater than zero, there exists a delta greater than zero such that for all x with absolute value of x minus c less than delta, the absolute value of f of x minus f of c is less than epsilon",
        "The derivative of a function at a point is the limit as h approaches zero of f of a plus h minus f of a divided by h",
        "The mean value theorem states that if f is continuous on the closed interval a to b and differentiable on the open interval a to b, then there exists a point c in the open interval such that f prime of c equals f of b minus f of a divided by b minus a",
    ]

    print("Initializing RAG pipeline...")
    pipeline = MathematicalRAGPipeline()

    print("\n" + "=" * 60)
    print("TESTING FORMALIZATION WITH RAG")
    print("=" * 60)

    for i, query in enumerate(test_queries, 1):
        print(f"\n--- Test {i} ---")
        print(f"Query: {query}")

        for method in ["bm25", "dense", "hybrid"]:
            print(f"\nMethod: {method.upper()}")
            try:
                lean_code, metrics = pipeline.formalize_with_rag(
                    query, method=method, top_k=3
                )
                print(f"Generated Lean Code:\n{lean_code}")
                print(f"Retrieved {len(metrics.retrieved_contexts)} context chunks")
            except Exception as e:
                print(f"Error with {method}: {e}")

    print("\n" + "=" * 60)
    print("TESTING FORMALIZATION WITHOUT RAG")
    print("=" * 60)

    for i, query in enumerate(test_queries, 1):
        print(f"\n--- Test {i} ---")
        print(f"Query: {query}")
        try:
            lean_code = pipeline.formalize_without_rag(query)
            print(f"Generated Lean Code:\n{lean_code}")
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    test_formalization()
