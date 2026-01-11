import os
import time
from typing import List
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_ollama import ChatOllama
from .schema import ReviewBatch

load_dotenv()

class ReviewGenerator:
    def __init__(self, provider: str = "ollama"):
        """
        Initialize with Hybrid Edge-Cloud providers.
        """
        self.provider = provider
        self.parser = PydanticOutputParser(pydantic_object=ReviewBatch)
        
        # Strategy: Hybrid Architecture
        if provider == "ollama":
            # Edge AI: Runs locally on CPU/GPU (Private, Free)
            # base_url is needed if running in a container/codespace sometimes, 
            # but usually defaults work.
            self.llm = ChatOllama(
                model="llama3",
                temperature=0.7,
                # Optional: keep_alive keeps the model loaded for speed
                keep_alive="5m" 
            )
        elif provider == "gemini":
            # Cloud AI: Runs on Google's TPU Pods (Fast, Scalable)
            api_key = os.getenv("GOOGLE_API_KEY")
            if not api_key:
                raise ValueError("Missing GOOGLE_API_KEY in .env")
            
            self.llm = ChatGoogleGenerativeAI(
                model="gemini-1.5-flash", # Flash is optimized for high-volume tasks
                temperature=0.7,
                google_api_key=api_key,
                convert_system_message_to_human=True # Helper for Gemini quirks
            )
        else:
            raise ValueError(f"Unsupported provider: {provider}")

    def generate_batch(self, count: int, persona: dict, rating: int) -> List[dict]:
        """
        Generates reviews using the selected provider.
        """
        # System prompt engineered for technical accuracy
        system_template = """
        You are an expert synthetic data generator for a Vector Database SaaS product.
        Generate {count} distinct user reviews matching:
        
        ROLE: {role}
        TONE: {tone}
        RATING: {rating}/5 stars
        KEYWORDS: {keywords}
        
        CRITICAL INSTRUCTIONS:
        1. Be specific. Use the keywords naturally in technical sentences.
        2. Vary the length. Some short, some long.
        3. OUTPUT PURE JSON ONLY matching the requested schema.
        
        {format_instructions}
        """
        
        prompt = ChatPromptTemplate.from_template(system_template)
        
        messages = prompt.format_messages(
            count=count,
            role=persona['role'],
            tone=persona['tone'],
            keywords=", ".join(persona['keywords']),
            rating=rating,
            format_instructions=self.parser.get_format_instructions()
        )

        try:
            print(f"   [Generating] asking {self.provider}...")
            response = self.llm.invoke(messages)
            
            # Parse the result
            parsed_result = self.parser.parse(response.content)
            
            # Tag the data with the provider name for the final analytics report
            results = []
            for review in parsed_result.reviews:
                r_dict = review.dict()
                r_dict['provider'] = self.provider.upper()
                results.append(r_dict)
                
            return results
            
        except Exception as e:
            print(f"   [Error] {self.provider} failed: {e}")
            # Senior Engineering: Fail gracefully by returning empty list (Supervisor will retry)
            return []