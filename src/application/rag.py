import os
import json
import numpy as np
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings

try:
    from rank_bm25 import BM25Okapi

    BM25_AVAILABLE = True
except ImportError:
    print("Warning: rank-bm25 not available. BM25 retrieval will be disabled.")
    BM25_AVAILABLE = False


@dataclass
class RAGMetrics:
    mrr: float
    top_k_recall: Dict[int, float]
    retrieved_contexts: List[str]
    query: str
    ground_truth: Optional[str] = None


class MathematicalRAGPipeline:
    def __init__(
        self,
        model_name: str = "deepseek-ai/DeepSeek-Prover-V2-7B",
        embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2",
        textbook_path: str = "dataset/converted.txt",
    ):
        self.model_name = model_name
        self.embedding_model = embedding_model
        self.textbook_path = textbook_path

        self._load_models()
        self._load_textbook()
        self._initialize_retrieval_methods()

    def _load_models(self):
        print(f"Loading model: {self.model_name}")

        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token

        # Use GPU if available
        device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Using device: {device}")

        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            torch_dtype=torch.float16,
            device_map="auto" if device == "cuda" else None,
            trust_remote_code=True,
        )

        if device != "cuda":
            self.model = self.model.to(device)

        print(f"Loading embedding model: {self.embedding_model}")
        self.embeddings = HuggingFaceEmbeddings(model_name=self.embedding_model)
        print("Models loaded successfully")

    def _load_textbook(self):
        if not os.path.exists(self.textbook_path):
            raise FileNotFoundError(f"Textbook not found at {self.textbook_path}")

        with open(self.textbook_path, "r", encoding="utf-8") as f:
            self.textbook_content = f.read()

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
        )

        self.text_chunks = text_splitter.split_text(self.textbook_content)
        print(f"Loaded textbook with {len(self.text_chunks)} chunks")

    def _initialize_retrieval_methods(self):
        if BM25_AVAILABLE:
            tokenized_chunks = [chunk.lower().split() for chunk in self.text_chunks]
            self.bm25 = BM25Okapi(tokenized_chunks)
            print("BM25 retrieval initialized")
        else:
            self.bm25 = None
            print("BM25 not available - sparse retrieval disabled")

        self.vectorstore = FAISS.from_texts(self.text_chunks, self.embeddings)
        print("FAISS dense retrieval initialized")

    def retrieve_context(
        self, query: str, method: str = "hybrid", top_k: int = 5
    ) -> List[str]:
        if method == "no_rag":
            return []
        elif method == "bm25":
            return self._bm25_retrieve(query, top_k)
        elif method == "dense":
            return self._dense_retrieve(query, top_k)
        elif method == "hybrid":
            return self._hybrid_retrieve(query, top_k)
        else:
            raise ValueError(f"Unknown retrieval method: {method}")

    def _bm25_retrieve(self, query: str, top_k: int) -> List[str]:
        if not BM25_AVAILABLE or self.bm25 is None:
            return self._dense_retrieve(query, top_k)

        tokenized_query = query.lower().split()
        scores = self.bm25.get_scores(tokenized_query)
        top_indices = np.argsort(scores)[::-1][:top_k]
        return [self.text_chunks[i] for i in top_indices]

    def _dense_retrieve(self, query: str, top_k: int) -> List[str]:
        docs = self.vectorstore.similarity_search(query, k=top_k)
        return [doc.page_content for doc in docs]

    def _hybrid_retrieve(self, query: str, top_k: int) -> List[str]:
        if not BM25_AVAILABLE or self.bm25 is None:
            return self._dense_retrieve(query, top_k)

        bm25_results = self._bm25_retrieve(query, top_k)
        dense_results = self._dense_retrieve(query, top_k)

        combined = list(dict.fromkeys(bm25_results + dense_results))
        return combined[:top_k]

    def generate_lean_code(
        self, query: str, context: Optional[List[str]] = None, max_length: int = 512
    ) -> str:
        if context:
            context_text = "\n\n".join(context)
            prompt = f"""Given the following mathematical context:

{context_text}

Please formalize the following statement in Lean 4:

{query}

Provide only the Lean 4 code without any explanations:"""
        else:
            prompt = f"""Please formalize the following mathematical statement in Lean 4:

{query}

Provide only the Lean 4 code without any explanations:"""

        inputs = self.tokenizer(
            prompt, return_tensors="pt", truncation=True, max_length=2048
        )

        device = next(self.model.parameters()).device
        inputs = {k: v.to(device) for k, v in inputs.items()}

        with torch.no_grad():
            outputs = self.model.generate(
                inputs["input_ids"],
                max_length=max_length,
                temperature=0.1,
                do_sample=True,
                pad_token_id=self.tokenizer.eos_token_id,
            )

        generated_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        lean_code = generated_text[len(prompt) :].strip()
        return lean_code

    def formalize_with_rag(
        self, query: str, method: str = "hybrid", top_k: int = 5
    ) -> Tuple[str, RAGMetrics]:
        context = self.retrieve_context(query, method, top_k)
        lean_code = self.generate_lean_code(query, context)

        metrics = RAGMetrics(
            mrr=0.0,
            top_k_recall={k: 0.0 for k in [1, 3, 5]},
            retrieved_contexts=context,
            query=query,
        )

        return lean_code, metrics

    def formalize_without_rag(self, query: str) -> str:
        return self.generate_lean_code(query, context=None)
