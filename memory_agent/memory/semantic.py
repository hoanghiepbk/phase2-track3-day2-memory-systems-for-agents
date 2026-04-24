"""
Semantic Memory — ChromaDB-backed vector search over domain knowledge.

Documents are embedded with OpenAI ``text-embedding-3-small`` and stored
in a local ChromaDB collection.  Retrieval returns the top-k most
semantically similar chunks for a given query.
"""

from __future__ import annotations

import hashlib
import logging
from pathlib import Path
from typing import Any

import chromadb
from chromadb.config import Settings as ChromaSettings

from memory_agent.memory.base import MemoryInterface

logger = logging.getLogger(__name__)


class SemanticMemory(MemoryInterface):
    """ChromaDB-backed semantic vector search."""

    def __init__(
        self,
        persist_dir: Path | str,
        collection_name: str = "domain_knowledge",
        embedding_model: str = "text-embedding-3-small",
    ) -> None:
        import os
        from chromadb.utils import embedding_functions
        
        self._persist_dir = Path(persist_dir)
        self._persist_dir.mkdir(parents=True, exist_ok=True)
        self._embedding_model = embedding_model

        # Initialise ChromaDB with persistence
        self._client = chromadb.Client(
            ChromaSettings(
                persist_directory=str(self._persist_dir),
                anonymized_telemetry=False,
                is_persistent=True,
            )
        )
        
        openai_ef = embedding_functions.OpenAIEmbeddingFunction(
            api_key=os.environ.get("OPENAI_API_KEY", ""),
            model_name=self._embedding_model
        )
        
        self._collection = self._client.get_or_create_collection(
            name=collection_name,
            embedding_function=openai_ef,
            metadata={"hnsw:space": "cosine"},
        )
        logger.info(
            "SemanticMemory ready — collection '%s' (%d docs).",
            collection_name,
            self._collection.count(),
        )

    # ------------------------------------------------------------------
    # Interface
    # ------------------------------------------------------------------
    def store(self, key: str, data: Any) -> None:
        """
        Add a document chunk to the collection.

        *key*  — a human-readable source identifier (e.g. filename)
        *data* — the text content to embed and store
        """
        if not isinstance(data, str) or not data.strip():
            raise ValueError("SemanticMemory expects a non-empty string.")

        doc_id = self._make_id(data)

        # Skip duplicates
        existing = self._collection.get(ids=[doc_id])
        if existing and existing["ids"]:
            logger.debug("Document already exists (id=%s), skipping.", doc_id)
            return

        self._collection.add(
            ids=[doc_id],
            documents=[data],
            metadatas=[{"source": key}],
        )
        logger.info("Stored document chunk from '%s' (id=%s).", key, doc_id[:12])

    def retrieve(self, query: str, k: int = 3) -> list[str]:
        """Return the top-*k* semantically similar document chunks."""
        if self._collection.count() == 0:
            return []

        results = self._collection.query(query_texts=[query], n_results=min(k, self._collection.count()))
        documents = results.get("documents", [[]])[0]
        return documents

    def clear(self) -> None:
        """Delete all documents from the collection."""
        if self._collection.count() > 0:
            all_ids = self._collection.get()["ids"]
            if all_ids:
                self._collection.delete(ids=all_ids)
        logger.info("Semantic memory cleared.")

    def delete(self, key: str) -> bool:
        """Delete all documents from source *key*."""
        results = self._collection.get(where={"source": key})
        if results and results["ids"]:
            self._collection.delete(ids=results["ids"])
            logger.info("Deleted %d document(s) from source '%s'.", len(results["ids"]), key)
            return True
        return False

    # ------------------------------------------------------------------
    # Bulk ingestion
    # ------------------------------------------------------------------
    def ingest_directory(self, directory: Path | str, chunk_size: int = 500) -> int:
        """
        Ingest all ``.md`` / ``.txt`` files from *directory*.

        Each file is split into chunks of approximately *chunk_size*
        characters and stored as separate documents.

        Returns the number of chunks ingested.
        """
        directory = Path(directory)
        if not directory.is_dir():
            logger.warning("Directory '%s' does not exist.", directory)
            return 0

        count = 0
        for fp in sorted(directory.glob("*")):
            if fp.suffix not in (".md", ".txt"):
                continue
            text = fp.read_text(encoding="utf-8").strip()
            if not text:
                continue
            chunks = self._chunk_text(text, chunk_size)
            for chunk in chunks:
                self.store(key=fp.name, data=chunk)
                count += 1
        logger.info("Ingested %d chunk(s) from '%s'.", count, directory)
        return count

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    @staticmethod
    def _make_id(text: str) -> str:
        return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]

    @staticmethod
    def _chunk_text(text: str, chunk_size: int = 500) -> list[str]:
        """Split *text* into chunks at paragraph boundaries."""
        paragraphs = text.split("\n\n")
        chunks: list[str] = []
        current_chunk = ""

        for para in paragraphs:
            para = para.strip()
            if not para:
                continue
            if len(current_chunk) + len(para) + 2 > chunk_size and current_chunk:
                chunks.append(current_chunk.strip())
                current_chunk = para
            else:
                current_chunk += ("\n\n" + para) if current_chunk else para

        if current_chunk.strip():
            chunks.append(current_chunk.strip())

        return chunks if chunks else [text]

    def __repr__(self) -> str:
        return f"SemanticMemory(docs={self._collection.count()})"
