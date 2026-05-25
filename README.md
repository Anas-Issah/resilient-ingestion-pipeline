# resilient-ingestion-pipeline
# Resilient Analytical Ingestion Engine

A production-grade, fault-tolerant data pipeline engineered to ingest high-frequency market data from the CoinGecko API, apply vectorized structural cleanups, and batch-load the processed records into an analytical relational warehouse. 

This engine is built entirely using **SQLAlchemy Core 2.0** and **Pandas**, intentionally designed to survive real-world distributed systems failures: transient network lag, strict third-party API rate limitations, upstream data drift, and unexpected database constraints.

---

## 🏗️ System Architecture & Workflow

```mermaid
graph TD
    A[CoinGecko Public API] -->|GET REST Requests| B(Extract: Stream /simple/price)
    B -->|In-Memory Generators| C(Transform: Vectorized Pandas Curation)
    C -->|Dynamic Inspection Safety Check| D(SQLAlchemy Metadata Auditor)
    D -->|Transaction Boundary: engine.begin| E[Load: Multi-Row Dictionary Insert / Upsert]
    E -->|Automated Failure Sync| F[(Target Warehouse Database)]
    
    style B fill:#f9f,stroke:#333,stroke-width:2px
    style D fill:#bbf,stroke:#333,stroke-width:2px
    style E fill:#bfb,stroke:#333,stroke-width:2px
