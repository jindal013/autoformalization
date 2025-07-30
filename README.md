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

- Lean 4 must be installed on your system
- Python 3.11+ with uv package manager
- LangChain for RAG implementation
- DSPV downloaded locally (script can be found in download_model.py)

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


## Project Structure
```
autoformalization/
├── src/
│   ├── application/
│   │   ├── generator/       # Formalization generation logic
│   │   ├── evaluator/       # Formalization evaluation logic
│   │   ├── rag/             # RAG implementation with LangChain
│   │   └── pipeline.py      # Main execution pipeline
│   ├── entity/              # Data models
│   └── constant.py          # Configuration constants
├── repl/                    # Lean 4 REPL implementation
├── textbooks/               # Textbook PDFs for RAG
├── generation.py            # Multi-file generation script
├── problem_prepare.ipynb    # Single-file generation script
└── README.md
```

## Credits

This project is inspired by and builds upon the work of the [LeanConjecturer](https://github.com/auto-res/LeanConjecturer).
