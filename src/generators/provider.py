import os
import json
from google import genai  # NEW SDK IMPORT
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

class ReviewGenerator:
    def __init__(self, provider: str = "google"):
        self.provider = provider
        
        if provider == "google":
            # Uses the NEW Gemini 2.5 Flash model
            api_key = os.getenv("GOOGLE_API_KEY") 
            if not api_key: raise ValueError("Missing GOOGLE_API_KEY")
            
            # New Client Initialization
            self.client = genai.Client(api_key=api_key)
            self.model_name = "gemini-2.5-flash"
            
        elif provider == "groq":
            # Uses Llama 3 on Groq
            api_key = os.getenv("GROQ_API_KEY")
            if not api_key: raise ValueError("Missing GROQ_API_KEY")
            
            self.client = Groq(api_key=api_key)
            self.model_name = "llama-3.1-8b-instant" 

    def generate_batch(self, count: int, persona: dict, rating: int) -> list:
        # Prompt designed to return raw JSON
        prompt = f"""
        Act as a synthetic data generator.
        Task: Write {count} reviews for a Vector DB SaaS.
        Persona: {persona['role']} ({persona['tone']})
        Rating: {rating}/5 Stars
        Keywords: {', '.join(persona['keywords'])}
        
        Output Requirement:
        Return ONLY a raw JSON list of objects. No markdown formatting.
        Each object must have: "persona_role", "rating", "title", "content", "pros", "cons".
        """
        
        try:
            text_response = ""
            
            # --- GOOGLE GEMINI 2.5 LOGIC ---
            if self.provider == "google":
                response = self.client.models.generate_content(
                    model=self.model_name,
                    contents=prompt
                )
                text_response = response.text
                
            # --- GROQ LLAMA 3 LOGIC ---
            elif self.provider == "groq":
                chat_completion = self.client.chat.completions.create(
                    messages=[{"role": "user", "content": prompt}],
                    model=self.model_name,
                    temperature=0.7
                )
                text_response = chat_completion.choices[0].message.content

            # --- COMMON CLEANUP ---
            # Remove ```json and ``` markers if the model adds them
            clean_text = text_response.replace("```json", "").replace("```", "").strip()
            
            # Find the JSON list brackets [ ... ]
            start = clean_text.find('[')
            end = clean_text.rfind(']') + 1
            if start != -1 and end != -1:
                clean_text = clean_text[start:end]
                
            data = json.loads(clean_text)
            
            # Tag the data with the provider name
            for item in data:
                item['provider'] = self.provider.upper()
                item['valid'] = True 
                
            return data

        except Exception as e:
            print(f"   [Error] {self.provider} failed: {e}")
            return []