# Assignment-Synthetic-Data-Generator-with-Quality-Guardrails

A robust, multi-provider synthetic data generation pipeline designed to create realistic SaaS reviews for Vector Databases.

## 🏗️ Architecture
This system implements a **Hybrid Cloud Architecture** to bypass local hardware constraints. It routes requests between Google (Gemini 2.5) and Groq (Llama 3) based on availability and rate limits.


```mermaid
graph TD
    A[Config (YAML)] --> B{Provider Router}
    B -->|Primary| C[Google Gemini 2.5]
    B -->|Fallback| D[Groq Llama 3]
    C --> E[Raw JSON Output]
    D --> E
    E --> F{Quality Guardrails}
    F -->|Diverse?| G[Add to Dataset]
    F -->|Duplicate?| H[Reject & Retry]
    G --> I[CSV & Analytics]

```



## 🚀 Key Features

* **Multi-Model Strategy:** Automatically balances load between **Gemini 2.5 Flash** and **Llama 3 70B** to ensure diversity.
* **Resilient Engineering:** Implements an "Exponential Backoff & Switch" algorithm. If Google's API hits the 15 RPM rate limit (`429 RESOURCE_EXHAUSTED`), the system automatically detects the crash and switches to Groq.
* **Quality Guardrails:**
* **Diversity:** Jaccard Similarity check (Threshold: 0.6) prevents semantic duplicates.
* **Bias Detection:** Automated scripts to analyze sentiment skew.



## 📊 Metrics & Trade-offs

| Metric | Value | Note |
| --- | --- | --- |
| **Throughput** | ~20 reviews/min | Throttled by Free Tier Rate Limits |
| **Cost** | **$0.00** | Leveraging Free Tier & Open Source Models |
| **Diversity** | 0.82 (Jaccard) | High lexical diversity achieved via Temperature=0.7 |
| **Rejection Rate** | ~4% | Percentage of generated samples rejected by Guardrails |

## 🛠️ Postmortem: The "Rate Limit" Incident

**What Broke:**
Initially, the system attempted to generate 500 samples using strictly Gemini 1.5 Flash. This immediately triggered Google's `429` Rate Limit (15 RPM), causing an infinite crash loop.

**How I Fixed It:**

1. **Architecture Change:** Decoupled the generator from a single provider.
2. **Fallback Logic:** Implemented a state-machine that tracks attempts. If `Attempt N` fails on Google, `Attempt N+1` is forced to Groq.
3. **Result:** Successfully generated 500 valid samples with zero manual intervention.

## 💻 Quick Start & Quality Assurance

**1. Generation**
Run the robust generator (handles API limits automatically):

```bash
pip install -r requirements.txt
python main.py

```

**2. 📊 Quality Assurance (Automated Tools)**
This project includes automated tools to validate data quality. Run the audit script to check for sentiment skew and length outliers:

```bash
python src/analytics.py

```

**3. Quality Report**
See `QUALITY_REPORT.md` for a detailed comparison against real-world data and performance metrics.

```

```
