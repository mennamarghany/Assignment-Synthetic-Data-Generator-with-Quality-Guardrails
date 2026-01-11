import yaml
import pandas as pd
import os
import random
import time
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from src.generators.provider import ReviewGenerator
from src.guardrails.quality import QualityGuard

console = Console()

def load_config():
    with open("config/reviews.yaml", "r") as f:
        return yaml.safe_load(f)

def run_generator():
    provider_a = "google"
    provider_b = "groq"
    output_file = "data/synthetic_reviews.csv"
    
    config = load_config()
    target_count = config['generation']['target_count']
    
    console.print(f"[bold green]🚀 Starting Generator (Gemini 2.5 vs Llama 3)[/bold green]")
    
    guard = QualityGuard(threshold=0.6) 
    gen_a = ReviewGenerator(provider=provider_a)
    gen_b = ReviewGenerator(provider=provider_b)
    
    valid_reviews = []
    os.makedirs("data", exist_ok=True)
    
    # --- NEW: Separate counter for attempts to prevent deadlock ---
    attempt_counter = 0

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("{task.percentage:>3.0f}%"),
    ) as progress:
        task = progress.add_task("[cyan]Generating Data...", total=target_count)
        
        while len(valid_reviews) < target_count:
            # FIX: Switch provider based on ATTEMPTS, not SUCCESSES
            # This ensures if Google fails, we try Groq next time no matter what.
            current_gen = gen_a if attempt_counter % 2 == 0 else gen_b
            provider_name = current_gen.provider.upper()
            
            persona = random.choice(config['personas'])
            stars = random.choice([1, 2, 3, 4, 5])

            # Generate batch
            batch = current_gen.generate_batch(2, persona, stars)
            
            # Update counter so next loop uses the OTHER provider
            attempt_counter += 1
            
            # RATE LIMIT / ERROR HANDLER
            if not batch:
                # If Google failed, print and wait briefly, then loop to let Groq run
                console.print(f"[red]! {provider_name} failed. Switching providers...[/red]")
                time.sleep(2) 
                continue      
            
            # Process Success
            for review in batch:
                content = review.get('content', '')
                if guard.is_diverse(content):
                    guard.add_to_index(content)
                    valid_reviews.append(review)
                    progress.advance(task)
                
                if len(valid_reviews) >= target_count: break

    df = pd.DataFrame(valid_reviews)
    df.to_csv(output_file, index=False)
    console.print(f"\n[bold green]✅ Success! Dataset saved to {output_file}[/bold green]")

if __name__ == "__main__":
    run_generator()