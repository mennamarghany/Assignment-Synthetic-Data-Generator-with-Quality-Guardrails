import numpy as np
from typing import List
from sentence_transformers import SentenceTransformer
import faiss

class QualityGuard:
    def __init__(self, threshold: float = 0.85):
        """
        Initialize the Quality Guardrail using FAISS for vector similarity.
        """
        print("   [Guardrail] Loading embedding model (all-MiniLM-L6-v2)...")
        # Lightweight model for fast embeddings
        self.encoder = SentenceTransformer('all-MiniLM-L6-v2')
        self.threshold = threshold
        
        # Initialize FAISS Index (L2 Distance)
        self.dimension = 384  # Output dim of MiniLM
        self.index = faiss.IndexFlatIP(self.dimension) # Inner Product (Cosine Sim for normalized vectors)
        self.stored_vectors = 0

    def is_diverse(self, text: str) -> bool:
        """
        Check if the new review is sufficiently different from existing ones.
        Returns True if diverse, False if redundant.
        """
        if self.stored_vectors == 0:
            return True

        # 1. Embed the new text
        vector = self.encoder.encode([text])
        faiss.normalize_L2(vector) # Normalize for cosine similarity

        # 2. Search FAISS index for nearest neighbors
        # k=1 means "find the single most similar existing review"
        D, I = self.index.search(vector, 1)
        
        # D[0][0] is the similarity score (0.0 to 1.0)
        similarity = D[0][0]
        
        if similarity > self.threshold:
            print(f"   [REJECTED] Too similar to existing review (Score: {similarity:.2f})")
            return False
        
        return True

    def add_to_index(self, text: str):
        """Add a valid review to the vector store."""
        vector = self.encoder.encode([text])
        faiss.normalize_L2(vector)
        self.index.add(vector)
        self.stored_vectors += 1