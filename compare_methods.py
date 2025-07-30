#!/usr/bin/env python3

import json
import sys
import signal
from datetime import datetime
from src.application.rag import MathematicalRAGPipeline


class TimeoutError(Exception):
    pass


def timeout_handler(signum, frame):
    raise TimeoutError("Operation timed out")


def run_comparison(query: str, output_dir: str = "comparison_results"):
    """Run the same query with all available methods and save results"""

    import os

    os.makedirs(output_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    print(f"Running comparison for query: {query}")
    print(f"Results will be saved to: {output_dir}")

    print("Initializing RAG pipeline...")
    pipeline = MathematicalRAGPipeline()

    methods = ["no_rag", "hybrid"]

    all_results = {}
    context_details = {}

    for method in methods:
        print(f"\n--- Testing method: {method.upper()} ---")

        try:
            # Set timeout for generation (5 minutes)
            signal.signal(signal.SIGALRM, timeout_handler)
            signal.alarm(300)

            if method == "no_rag":
                lean_code = pipeline.formalize_without_rag(query)
                context_used = None
            else:
                lean_code, metrics = pipeline.formalize_with_rag(
                    query, method=method, top_k=5
                )
                context_used = metrics.retrieved_contexts

            # Cancel timeout
            signal.alarm(0)

            all_results[method] = {
                "query": query,
                "method": method,
                "lean_code": lean_code,
                "timestamp": timestamp,
            }

            context_details[method] = {
                "query": query,
                "method": method,
                "context_used": context_used,
                "context_count": len(context_used) if context_used else 0,
                "timestamp": timestamp,
            }

            print(f"✅ {method.upper()} completed successfully")

        except TimeoutError:
            print(f"⏰ Timeout for {method} (5 minutes)")
            all_results[method] = {
                "query": query,
                "method": method,
                "lean_code": "TIMEOUT: Generation took too long (>5 minutes)",
                "timestamp": timestamp,
            }
            context_details[method] = {
                "query": query,
                "method": method,
                "context_used": None,
                "context_count": 0,
                "error": "Timeout",
                "timestamp": timestamp,
            }
        except Exception as e:
            print(f"❌ Error with {method}: {e}")
            all_results[method] = {
                "query": query,
                "method": method,
                "lean_code": f"ERROR: {e}",
                "timestamp": timestamp,
            }
            context_details[method] = {
                "query": query,
                "method": method,
                "context_used": None,
                "context_count": 0,
                "error": str(e),
                "timestamp": timestamp,
            }
        finally:
            # Cancel timeout
            signal.alarm(0)

    lean_output_file = f"{output_dir}/lean_code_comparison_{timestamp}.txt"
    with open(lean_output_file, "w") as f:
        f.write("=" * 80 + "\n")
        f.write("LEAN CODE COMPARISON\n")
        f.write("=" * 80 + "\n")
        f.write(f"Query: {query}\n")
        f.write(f"Timestamp: {timestamp}\n")
        f.write("=" * 80 + "\n\n")

        for method in methods:
            f.write(f"METHOD: {method.upper()}\n")
            f.write("-" * 40 + "\n")
            f.write(all_results[method]["lean_code"])
            f.write("\n\n" + "=" * 80 + "\n\n")

    context_output_file = f"{output_dir}/context_details_{timestamp}.txt"
    with open(context_output_file, "w") as f:
        f.write("=" * 80 + "\n")
        f.write("CONTEXT DETAILS\n")
        f.write("=" * 80 + "\n")
        f.write(f"Query: {query}\n")
        f.write(f"Timestamp: {timestamp}\n")
        f.write("=" * 80 + "\n\n")

        for method in methods:
            f.write(f"METHOD: {method.upper()}\n")
            f.write("-" * 40 + "\n")

            if method == "no_rag":
                f.write("No context used (direct generation)\n")
            else:
                context_info = context_details[method]
                f.write(f"Context chunks retrieved: {context_info['context_count']}\n")
                f.write("\nRetrieved Context:\n")

                if context_info["context_used"]:
                    for i, context in enumerate(context_info["context_used"], 1):
                        f.write(f"\n{i}. {context}\n")
                        f.write("-" * 60 + "\n")
                else:
                    f.write("No context retrieved\n")

            f.write("\n" + "=" * 80 + "\n\n")

    json_output_file = f"{output_dir}/summary_{timestamp}.json"
    with open(json_output_file, "w") as f:
        json.dump(
            {
                "query": query,
                "timestamp": timestamp,
                "results": all_results,
                "context_details": context_details,
            },
            f,
            indent=2,
        )

    print(f"\n" + "=" * 60)
    print("COMPARISON COMPLETE!")
    print("=" * 60)
    print(f"📄 Lean code comparison: {lean_output_file}")
    print(f"📄 Context details: {context_output_file}")
    print(f"📄 JSON summary: {json_output_file}")

    return lean_output_file, context_output_file, json_output_file


def main():
    test_queries = [
        "The fundamental group of the circle is isomorphic to the integers",
        "A continuous map between topological spaces induces a homomorphism between their fundamental groups",
        "The torus is a topological space whose fundamental group is isomorphic to the product of two copies of the integers",
    ]

    print("Autoformalization Method Comparison")
    print("=" * 50)

    for i, query in enumerate(test_queries, 1):
        print(f"\n🔄 Running comparison {i}/3")
        print(f"Query: {query[:100]}...")

        try:
            lean_file, context_file, json_file = run_comparison(query)
            print(f"✅ Comparison {i} completed successfully")
        except Exception as e:
            print(f"❌ Error in comparison {i}: {e}")

    print(f"\n🎉 All comparisons completed!")
    print("Check the 'comparison_results' directory for output files.")


if __name__ == "__main__":
    main()
