from pydantic import BaseModel, Field
from typing import List, Optional

class Review(BaseModel):
    """Schema for a single synthetic review."""
    persona_role: str = Field(description="The role of the person writing the review (e.g., 'Senior MLOps Engineer')")
    rating: int = Field(description="Star rating from 1 to 5")
    title: str = Field(description="A short, catchy title for the review")
    content: str = Field(description="The main body of the review")
    pros: List[str] = Field(description="List of specific positive points")
    cons: List[str] = Field(description="List of specific negative points")
    verified_purchase: bool = Field(default=True)
    
class ReviewBatch(BaseModel):
    """A collection of reviews generated in one go."""
    reviews: List[Review]