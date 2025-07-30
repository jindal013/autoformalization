# Autoformalization

A tool for formalizing mathematical concepts using AI models, featuring built-in Retrieval-Augmented Generation (RAG) from textbooks and integration with Lean 4. While the original plan was to pursue post-training via Group Relative Policy Optimization (GRPO), the development of LeanConjecturer (2025) shifted the focus toward addressing foundational challenges in mathematical formalization. In particular, context retrieval remains a pressing problem: effective formalization requires not only retrieving relevant information, but also representing and relating mathematical objects and their roles within proofs. This ongoing challenge is central to advancing automated reasoning in mathematics.

## Note

This project currently implements a locally saved DeepSeekProver 7B model, integrated with a RAG (Retrieval-Augmented Generation) context pipeline that extracts relevant information from a provided textbook. The system is designed for ongoing development and experimentation.

For semantic search and dense retrieval, the pipeline uses the [math-similarity/Bert-MLM_arXiv-MP-class_zbMath](https://huggingface.co/math-similarity/Bert-MLM_arXiv-MP-class_zbMath) embedding model, which is well-suited for mathematical and scientific text.

Looking ahead, the plan is to build upon the model and methodology provided by LeanConjecturer (2025), with the goal of experimenting with GRPO (Guided Retrieval and Proof Optimization) and advanced context retrieval strategies. This will enable exploration of how retrieval methods and context quality affect formalization performance, as well as comparison of different embedding models.

The pipeline is connected to a Lean 4 server, enabling real-time verification and interactive proof development. The system has been tested on both real and synthetically generated natural language to formal language (NL-to-FL) examples, providing a foundation for future research and experimentation.

If you are interested in contributing or have suggestions for embedding models or retrieval strategies, feel free to open an issue or pull request.

## Environment Setup

### Prerequisites

- Python 3.11+ with pip
- CUDA-compatible GPU (recommended for faster inference)
- HuggingFace account for model access

### Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/your-username/autoformalization.git
   cd autoformalization
   ```

2. **Install dependencies**

   ```bash
   python setup.py
   ```

   Or manually:

   ```bash
   pip install -r requirements.txt
   ```

3. **Models will be downloaded automatically on first use**
   - DeepSeek Prover V2 7B: `DeepSeek-Prover-V2-7B`
   - Math embedding model: `math-similarity/Bert-MLM_arXiv-MP-class_zbMath`

## RAG Implementation

The system uses LangChain to implement different RAG retrieval methods:

- **Dense Retrieval**: Uses embeddings for semantic search
- **Sparse Retrieval**: Uses keyword-based search
- **Hybrid Retrieval**: Combines both dense and sparse methods

The RAG system extracts relevant content from uploaded textbooks to provide context for formalization tasks.

## Lean Server Integration

The system includes a Lean 4 server for:

- Real-time theorem verification
- Interactive formalization assistance
- Automated proof checking

## Usage

### Basic Usage

**With RAG (recommended):**

```bash
python formalize.py --query "The sum of two real numbers is commutative" --method hybrid
```

**Without RAG:**

```bash
python formalize.py --query "A function is continuous at a point if..." --no-rag
```

### Available Options

- `--query`: Natural language mathematical statement (required)
- `--method`: RAG retrieval method (`bm25`, `dense`, `hybrid`) - default: `hybrid`
- `--no-rag`: Run without RAG (direct generation)
- `--top-k`: Number of context chunks to retrieve (default: 5)
- `--output`: Output file for results (default: output.json)
- `--textbook`: Path to textbook markdown file (default: dataset/converted.md)
- `--model`: HuggingFace model name (default: DeepSeek-Prover-V2-7B)

### Test the System

Run the test script to see examples:

```bash
python test_formalize.py
```

## Project Structure

```
autoformalization/
├── src/
│   ├── application/
│   │   ├── rag.py          # RAG pipeline implementation
│   │   ├── generator.py    # Formalization generation logic
│   │   ├── evaluator.py    # Formalization evaluation logic
│   │   └── pipeline.py     # Main execution pipeline
│   ├── entity/             # Data models
│   └── constant.py         # Configuration constants
├── dataset/
│   └── converted.md        # Sample textbook for testing
├── formalize.py            # Main execution script
├── test_formalize.py       # Test script with examples
├── setup.py                # Installation script
├── requirements.txt         # Python dependencies
└── README.md
```

## Credits

This project is inspired by and builds upon the work of the [LeanConjecturer](https://github.com/auto-res/LeanConjecturer).
