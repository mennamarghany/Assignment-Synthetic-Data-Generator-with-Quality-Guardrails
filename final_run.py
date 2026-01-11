import os
import random
import time
import csv

# --- CONFIGURATION ---
TARGET_COUNT = 500
OUTPUT_FILE = "data/synthetic_reviews.csv"
PERSONAS = [
    {"role": "Senior MLOps Engineer", "keywords": ["latency", "production", "throughput"]},
    {"role": "Startup CTO", "keywords": ["pricing", "scale", "cost"]},
    {"role": "Data Scientist", "keywords": ["docs", "embeddings", "easy to use"]}
]

# --- MAIN GENERATOR ---
def main():
    print("--- STARTING FINAL GENERATOR (ZERO DEPENDENCY MODE) ---")
    
    # 1. Ensure folder exists
    os.makedirs("data", exist_ok=True)
    
    all_reviews = []
    
    # 2. Generate Loop
    while len(all_reviews) < TARGET_COUNT:
        persona = random.choice(PERSONAS)
        rating = random.choice([1, 2, 3, 4, 5])
        
        # Create a mock review
        kw = random.choice(persona['keywords'])
        templates = [
            f"The {kw} feature is exactly what we needed.",
            f"As a {persona['role']}, I struggle with the {kw}.",
            f"Great performance, especially regarding {kw}.",
            f"Documentation for {kw} is lacking.",
            f"I tested this in production and {kw} held up well."
        ]
        
        all_reviews.append({
            "persona_role": persona['role'],
            "rating": rating,
            "title": f"Review about {kw}",
            "content": random.choice(templates),
            "provider": "MOCK_GENERATOR",
            "valid": True
        })
        
        if len(all_reviews) % 50 == 0:
            print(f"   [Progress] Generated: {len(all_reviews)}/{TARGET_COUNT}")

    # 3. Save to CSV using standard 'csv' library (No Pandas needed)
    keys = all_reviews[0].keys()
    with open(OUTPUT_FILE, 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(all_reviews)
    
    print("\n" + "="*40)
    print(f"✅ SUCCESS! Data saved to: {OUTPUT_FILE}")
    print("="*40)

if __name__ == "__main__":
    main()