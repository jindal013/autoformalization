# Autoformalization

A tool for formalizing mathematical concepts using AI models, featuring built-in Retrieval-Augmented Generation (RAG) from textbooks and integration with Lean 4. While the original plan was to pursue post-training via Group Relative Policy Optimization (GRPO), the development of LeanConjecturer (2025) shifted the focus toward addressing foundational challenges in mathematical formalization. In particular, context retrieval remains a pressing problem: effective formalization requires not only retrieving relevant information, but also representing and relating mathematical objects and their roles within proofs. This ongoing challenge is central to advancing automated reasoning in mathematics.

## Environment Setup

### Prerequisites

- Lean 4 must be installed on your system
- Python 3.11+ with uv package manager
- LangChain for RAG implementation
- OpenAI API key for AI model access

### Installation Steps

1. **Clone the repository**

   ```bash
   git clone --recursive git@github.com:your-username/autofmralization.git
   cd autofmralization
   ```

2. **If you've already cloned without submodules:**

   ```bash
   git submodule update --init --recursive
   ```

3. **Build the Lean REPL**

   ```bash
   cd repl
   lake exe cache get
   lake build
   cd ..
   ```

4. **Install Python dependencies**
   ```bash
   uv sync
   ```

## Execution Procedures

### Formalization Generation from Multiple Files

Use the main generation script to process multiple target files:

```bash
uv run generation.py [options]
```

**Available Options:**

- `--model_name`: AI model to use for generation (default: "o3")
- `--api_key`: OpenAI API key (can be set via .env file)
- `--target`: Path to file containing target Lean files (one per line)
- `--max_iter`: Maximum number of iterations (default: 1)
- `--rag_method`: RAG retrieval method (default: "dense") - options: "dense", "sparse", "hybrid"
- `--textbook_path`: Path to textbook PDF for RAG (required)

**Example:**

```bash
uv run generation.py --model_name o3 --target target_files.txt --max_iter 5 --rag_method hybrid --textbook_path textbooks/analysis.pdf
```

### Formalization Generation from Single File

For processing a single Lean file:

```bash
uv run problem_prepare.py [options]
```

**Available Options:**

- `--model_name`: AI model to use (default: "o3")
- `--api_key`: OpenAI API key (can be set via .env file)
- `--target`: Path to the target Lean file (default: "./InterClosureExercise.lean")
- `--max_iter`: Maximum number of iterations (default: 15)
- `--rag_method`: RAG retrieval method (default: "dense")
- `--textbook_path`: Path to textbook PDF for RAG (required)

**Example:**

```bash
uv run problem_prepare.py --target my_theorem.lean --max_iter 10 --rag_method dense --textbook_path textbooks/linear_algebra.pdf
```

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

## Environment Configuration

You can set your OpenAI API key in a `.env` file:

```
OPENAI_API_KEY=your_api_key_here
```

## Execution Results

The tool generates formalizations and evaluates them using Lean 4. Results are saved in the `data/` directory:

- `formalization.jsonl`: Generated formalizations
- `formalization_eval_result.jsonl`: Evaluation results
- `grpo_problem.jsonl`: Non-trivial problems that couldn't be automatically formalized

## Project Structure

```
autofmralization/
├── src/
│   ├── application/
│   │   ├── generator/     # Formalization generation logic
│   │   ├── evaluator/     # Formalization evaluation logic
│   │   ├── rag/          # RAG implementation with LangChain
│   │   └── pipeline.py    # Main execution pipeline
│   ├── entity/           # Data models
│   └── constant.py       # Configuration constants
├── repl/                 # Lean 4 REPL implementation
├── data/                 # Generated results (gitignored)
├── textbooks/           # Textbook PDFs for RAG
├── generation.py         # Multi-file generation script
├── problem_prepare.py    # Single-file generation script
└── README.md
```

## Notes

- The `data/` directory is gitignored to avoid committing large generated files
- Make sure Lean 4 is properly installed and accessible in your PATH
- The tool requires an active internet connection for API calls to OpenAI
- Textbook PDFs should be placed in the `textbooks/` directory for RAG functionality

## Credits

This project is inspired by and builds upon the excellent work of the [LeanConjecturer](https://github.com/auto-res/LeanConjecturer) project by the auto-res team.
