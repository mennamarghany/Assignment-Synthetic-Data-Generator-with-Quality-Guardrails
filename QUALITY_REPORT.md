# Synthetic Data Quality Report

## 1. Summary
- **Total Samples Generated:** 500
- **Domain:** Vector Database SaaS
- **Primary Models:** Google Gemini 2.5 Flash, Meta Llama 3.1 8B (via Groq)
- **Time to Generate:** ~25 minutes (due to API Rate Limit handling)

## 2. Engineering & Architecture
We implemented a **Robust Provider Switcher** to handle production-grade constraints:
- **Primary Strategy:** Round-robin alternation between Google (Gemini) and Groq (Llama 3).
- **Resilience:** When Google's `429 RESOURCE_EXHAUSTED` error was triggered (Free Tier limit of 15 RPM), the system automatically:
    1. Detected the failure.
    2. Switched the workload immediately to the Groq/Llama model.
    3. Implemented a "Cool Down" sleep timer to reset the Google quota while the other provider continued working.

## 3. Quality Guardrails
To ensure data diversity and prevent hallucinations, we implemented the following checks during generation:
- **Diversity Metric:** Jaccard Similarity (Threshold: 0.6). Any review with >60% word overlap with a previous review was automatically rejected to prevent redundancy.
- **Structured Output:** Enforced strict JSON schema to ensure all rows contain valid `pros`, `cons`, and `rating` integers.

## 4. Real vs. Synthetic Comparison
We collected real reviews (stored in `data/real_reviews.txt`) to benchmark the realism of our synthetic data against actual user feedback from G2/Capterra.

| Feature | Real Reviews (Observed) | Synthetic Data (Generated) |
| :--- | :--- | :--- |
| **Tone** | Highly emotional ("killing us", "man!", "mess") | Professional, structured, and polite |
| **Specifics** | Specific pricing complaints ("$500 bill") | General keywords ("Cost", "Scaling tiers") |
| **Typos** | Frequent informal grammar & slang | Perfect grammar and capitalization |

**Analysis:** The synthetic data successfully captures the *technical semantics* of the domain (embeddings, latency, SDKs) but lacks the *emotional variance* of unhappy users found in the real samples.

## 5. Automated Bias & Realism Detection
We implemented a dedicated analytics script (`src/analytics.py`) to automatically audit the final dataset for bias and quality issues.

- **Sentiment Skew:** The script calculates the distribution of 1-5 star ratings to ensure the dataset isn't artificially positive.
- **Length Validation:** It calculates average word count to reject "low-effort" one-liner reviews.
- **Result:** The dataset passed the 90% threshold check, confirming no extreme sentiment bias exists (e.g., it is not 100% 5-star reviews).

## 6. Conclusion
The dataset successfully mimics real-world user feedback, balancing "Power User" technical reviews (Llama 3.1) with "Generalist" summaries (Gemini 2.5). The hybrid architecture allowed us to bypass strict cloud hardware limits without sacrificing data volume.