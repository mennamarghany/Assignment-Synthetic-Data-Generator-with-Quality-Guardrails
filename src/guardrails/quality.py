class QualityGuard:
    def __init__(self, threshold: float = 0.5):
        # We use Jaccard Similarity (Word Overlap)
        # 0.0 = Different, 1.0 = Identical
        self.threshold = threshold
        self.stored_reviews = []

    def is_diverse(self, text: str) -> bool:
        """
        Check if the new review is sufficiently different using Jaccard Similarity.
        This fulfills the 'Diversity Metric' requirement without heavy AI models.
        """
        # Simple tokenization
        new_words = set(text.lower().split())
        
        # Check against all stored reviews
        for existing in self.stored_reviews:
            existing_words = set(existing.lower().split())
            
            # Math: Intersection / Union
            if len(new_words.union(existing_words)) == 0: continue
            
            similarity = len(new_words.intersection(existing_words)) / len(new_words.union(existing_words))
            
            if similarity > self.threshold:
                return False # Reject (Too similar)
        
        return True

    def add_to_index(self, text: str):
        self.stored_reviews.append(text)