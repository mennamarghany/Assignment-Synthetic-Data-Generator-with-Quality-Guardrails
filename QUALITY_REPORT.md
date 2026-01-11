# Synthetic Data Quality Report

## 1. Summary
- **Total Samples Generated:** 500
- **Domain:** Vector Database SaaS
- **Primary Models:** Google Gemini 2.5 Flash, Meta Llama 3.1 8B (via Groq)
- **Time to Generate:** ~25 minutes (due to API Rate Limit handling)

## 2. Engineering & Architecture
We implemented a **Robust Provider Switcher** to handle production-grade constraints:
- **Primary Strategy:** Round-robin alternation between Google and Groq.
- **Resilience:** When Google's `429 RESOURCE_EXHAUSTED` error was triggered (Free Tier limit of 15 RPM), the system automatically:
    1. Detected the failure.
    2. Switched the workload immediately to the Groq/Llama model.
    3. Implemented a "Cool Down" sleep timer to reset the Google quota.

## 3. Quality Guardrails
To ensure data diversity and prevent hallucinations, we implemented the following checks:
- **Diversity Metric:** Jaccard Similarity (Threshold: 0.6). Any review with >60% word overlap with a previous review was automatically rejected.
- **Structured Output:** Enforced strict JSON schema to ensure all rows contain valid `pros`, `cons`, and `rating` integers.

## 4. Conclusion
The dataset successfully mimics real-world user feedback, balancing "Power User" technical reviews (Llama 3.1) with "Generalist" summaries (Gemini 2.5). The hybrid architecture allowed us to bypass strict cloud hardware limits without sacrificing data volume.