import os
import json
import numpy as np
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import re
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
import logging

try:
    from rank_bm25 import BM25Okapi

    BM25_AVAILABLE = True
except ImportError:
    print("Warning: rank-bm25 not available. BM25 retrieval will be disabled.")
    print("Install with: pip install rank-bm25")
    BM25_AVAILABLE = False

try:
    from sklearn.metrics.pairwise import cosine_similarity

    SKLEARN_AVAILABLE = True
except ImportError:
    print("Warning: scikit-learn not available. Some metrics may not work.")
    SKLEARN_AVAILABLE = False

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


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
        model_name: str = "DeepSeek-Prover-V2-7B",
        embedding_model: str = "math-similarity/Bert-MLM_arXiv-MP-class_zbMath",
        textbook_path: str = "dataset/converted.md",
    ):
        self.model_name = model_name
        self.embedding_model = embedding_model
        self.textbook_path = textbook_path

        self._load_models()
        self._load_textbook()
        self._initialize_retrieval_methods()

    def _load_models(self):
        logger.info(f"Loading model: {self.model_name}")

        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            torch_dtype=torch.float16,
            device_map="auto",
            trust_remote_code=True,
        )

        logger.info(f"Loading embedding model: {self.embedding_model}")
        self.embeddings = HuggingFaceEmbeddings(
            model_name=self.embedding_model,
            model_kwargs={"device": "cuda" if torch.cuda.is_available() else "cpu"},
        )

        logger.info("Models loaded successfully")

    def _load_textbook(self):
        if not os.path.exists(self.textbook_path):
            raise FileNotFoundError(f"Textbook not found at {self.textbook_path}")

        with open(self.textbook_path, "r", encoding="utf-8") as f:
            self.textbook_content = f.read()

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            separators=["\n\n", "\n", ".", "!", "?", ";", ":", " "],
        )

        self.text_chunks = text_splitter.split_text(self.textbook_content)
        logger.info(f"Loaded textbook with {len(self.text_chunks)} chunks")

    def _initialize_retrieval_methods(self):
        if BM25_AVAILABLE:
            tokenized_chunks = [chunk.lower().split() for chunk in self.text_chunks]
            self.bm25 = BM25Okapi(tokenized_chunks)
            logger.info("BM25 retrieval initialized")
        else:
            self.bm25 = None
            logger.warning("BM25 not available - sparse retrieval disabled")

        self.vectorstore = FAISS.from_texts(self.text_chunks, self.embeddings)
        logger.info("FAISS dense retrieval initialized")

        logger.info("Retrieval methods initialized")

    def retrieve_context(
        self, query: str, method: str = "hybrid", top_k: int = 5
    ) -> List[str]:
        if method == "bm25":
            return self._bm25_retrieve(query, top_k)
        elif method == "dense":
            return self._dense_retrieve(query, top_k)
        elif method == "hybrid":
            return self._hybrid_retrieve(query, top_k)
        else:
            raise ValueError(f"Unknown retrieval method: {method}")

    def _bm25_retrieve(self, query: str, top_k: int) -> List[str]:
        if not BM25_AVAILABLE or self.bm25 is None:
            logger.warning("BM25 not available, falling back to dense retrieval")
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
            logger.warning("BM25 not available for hybrid retrieval, using dense only")
            return self._dense_retrieve(query, top_k)

        bm25_results = self._bm25_retrieve(query, top_k)
        dense_results = self._dense_retrieve(query, top_k)

        combined = list(dict.fromkeys(bm25_results + dense_results))
        return combined[:top_k]

    def calculate_mrr(
        self, query: str, relevant_chunks: List[str], method: str = "hybrid"
    ) -> float:
        retrieved_chunks = self.retrieve_context(
            query, method, top_k=len(self.text_chunks)
        )

        for i, chunk in enumerate(retrieved_chunks):
            if chunk in relevant_chunks:
                return 1.0 / (i + 1)

        return 0.0

    def calculate_top_k_recall(
        self,
        query: str,
        relevant_chunks: List[str],
        method: str = "hybrid",
        k_values: List[int] = [1, 3, 5],
    ) -> Dict[int, float]:
        retrieved_chunks = self.retrieve_context(query, method, top_k=max(k_values))

        recall_scores = {}
        for k in k_values:
            top_k_chunks = retrieved_chunks[:k]
            relevant_found = sum(
                1 for chunk in top_k_chunks if chunk in relevant_chunks
            )
            recall_scores[k] = (
                relevant_found / len(relevant_chunks) if relevant_chunks else 0.0
            )

        return recall_scores

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

        with torch.no_grad():
            outputs = self.model.generate(
                inputs.input_ids,
                max_length=max_length,
                temperature=0.1,
                do_sample=True,
                pad_token_id=self.tokenizer.eos_token_id,
            )

        generated_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        lean_code = generated_text[len(prompt) :].strip()

        return lean_code

    def evaluate_rag(
        self, query: str, relevant_chunks: List[str], method: str = "hybrid"
    ) -> RAGMetrics:
        mrr = self.calculate_mrr(query, relevant_chunks, method)
        top_k_recall = self.calculate_top_k_recall(query, relevant_chunks, method)
        retrieved_contexts = self.retrieve_context(query, method, top_k=5)

        return RAGMetrics(
            mrr=mrr,
            top_k_recall=top_k_recall,
            retrieved_contexts=retrieved_contexts,
            query=query,
            ground_truth=relevant_chunks,
        )

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
