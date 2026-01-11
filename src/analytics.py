import pandas as pd
from rich.console import Console
from rich.table import Table

console = Console()

def analyze_bias(csv_path="data/synthetic_reviews.csv"):
    df = pd.read_csv(csv_path)
    
    # Simple Heuristic: Check Rating Distribution
    console.print("[bold cyan]--- Bias Detection Report ---[/bold cyan]")
    
    # 1. Check Rating Skew
    rating_counts = df['rating'].value_counts().sort_index()
    total = len(df)
    
    table = Table(title="Rating Distribution (Sentiment Skew)")
    table.add_column("Stars", justify="center")
    table.add_column("Count", justify="right")
    table.add_column("Percentage", justify="right")
    
    for star, count in rating_counts.items():
        pct = (count / total) * 100
        table.add_row(f"{star} ⭐", str(count), f"{pct:.1f}%")
        
    console.print(table)
    
    # 2. Check for "Perfect" Bias (Unrealistic Patterns)
    # If 100% of reviews are 5 stars, that is bias.
    if rating_counts.get(5, 0) / total > 0.9:
        console.print("[red]⚠️  ALERT: High Positive Bias Detected! (>90% 5-star)[/red]")
    elif rating_counts.get(1, 0) / total > 0.9:
        console.print("[red]⚠️  ALERT: High Negative Bias Detected! (>90% 1-star)[/red]")
    else:
        console.print("[green]✅ Balanced Sentiment Distribution (No extreme skew)[/green]")

    # 3. Domain Realism (Length Check)
    # Real reviews aren't usually 5 words long.
    avg_len = df['content'].str.split().str.len().mean()
    console.print(f"\n[bold]Avg Review Length:[/bold] {avg_len:.1f} words")
    if avg_len < 15:
        console.print("[yellow]⚠️  Warning: Reviews seem too short (Low Realism)[/yellow]")
    else:
        console.print("[green]✅ Length indicates realistic detail[/green]")

if __name__ == "__main__":
    analyze_bias()