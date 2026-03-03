# Service of Suits – AI-Enabled Document Processing Prototype

This repository contains a proof-of-concept implementation of an AI-assisted legal document handling pipeline, developed for the Service of Suits technical assignment.

The system demonstrates how legal documents can be ingested, semantically parsed using an LLM, validated with deterministic guardrails, and routed with structured observability.

---

##  Overview

The prototype processes mock legal PDF documents and:

- Extracts structured metadata using OpenAI (JSON mode)
- Applies deterministic classification guardrails
- Performs completeness validation
- Computes document-type-aware confidence scores
- Detects policy number inconsistencies
- Stores structured metadata in SQLite
- Generates deterministic draft email notifications
- Emits structured JSON logs with latency and token usage

---

## Architecture Overview

PDF Loader
↓
LLM Structured Extractor (OpenAI JSON Mode)
↓
Deterministic Guardrails
↓
Validation & Confidence Scoring
↓
Policy Variant Detection
↓
SQLite Metadata Repository
↓
Deterministic Email Draft Generator
↓
Structured JSON Logging


### Design Principles

- Hybrid AI + deterministic governance
- Schema-enforced JSON output
- Guardrails to reduce hallucination risk
- Document-type-aware confidence logic
- Context-aware policy inconsistency detection
- Explicit observability (token usage + latency)

---

##  AI Design

### LLM Extraction

- Model: `gpt-4o-mini`
- JSON mode enforced via `response_format={"type": "json_object"}`
- Markdown stripping fallback
- Schema enforcement to prevent parsing failures

### Guardrails

Certain document types are deterministically overridden for high-confidence patterns (e.g., "Scheduling Order" → Lawsuit).

This hybrid design balances semantic AI flexibility with production safety.

---

##  Structured Logging

Each document emits a structured JSON log entry including:

- request_id
- document_type
- confidence_score
- policy_inconsistency
- policy_variant_count
- processing_time_ms
- llm_latency_ms
- token_usage
- email_generated

This enables integration with monitoring tools such as:
- Azure Monitor
- Datadog
- ELK stack
- Splunk

---

## Email Draft Generation

For valid legal documents, the system generates a deterministic draft email and saves it to:

## output_emails


Non-legal documents do not trigger email generation.

---

## Setup Instructions

### 1. Clone Repository


git clone https://github.com/aaovaba/service-of-suits-ai.git

cd service-of-suits-ai


### 2. Create Virtual Environment


python -m venv venv
venv\Scripts\activate


### 3. Install Dependencies


pip install -r requirements.txt


### 4. Set Environment Variable


export OPENAI_API_KEY=your_api_key_here


(Windows PowerShell)


setx OPENAI_API_KEY "your_api_key_here"


### 5. Place Mock PDFs

Place the provided mock PDF documents inside:


Mock PDF Documents/


### 6. Run the Pipeline


python main.py


---

##  Repository Structure


ai/
ingestion/
validation/
storage/
notifications/

main.py
config.py
logging_config.py
requirements.txt
README.md


---


## Production Evolution (Databricks + Azure)

In production, this system could evolve into:

- Azure Blob Storage (Document Intake)
- Event Grid trigger
- Azure Function / Container App
- Databricks orchestration
- Azure OpenAI (private endpoint)
- Delta Lake storage
- Centralized monitoring dashboard

---

##  Assignment Deliverables Covered

- PDF ingestion
- Structured metadata extraction
- Completeness checks
- Metadata repository
- Draft email generation
- Structured logging
- Observability metrics
- Enterprise-grade design discussion

---

## Author

ROOP KUMAR

