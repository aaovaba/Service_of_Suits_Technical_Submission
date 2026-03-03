import os
import json
import time
from openai import OpenAI


EXPECTED_KEYS = [
    "document_type",
    "date_of_loss",
    "policy_number",
    "recipient",
    "claimant",
    "defendant",
    "case_reference"
]


class LLMExtractor:

    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = "gpt-4o-mini"

    def extract(self, text: str):

        start_time = time.time()

        prompt = f"""
Extract the following fields from the legal document and return STRICT JSON:

{{
  "document_type": "Notice | Lawsuit | Legal Correspondence | Non-Legal",
  "date_of_loss": null,
  "policy_number": null,
  "recipient": null,
  "claimant": null,
  "defendant": null,
  "case_reference": null
}}

Rules:
- If a field is missing, return null.
- document_type must be one of the allowed values.
- Do not hallucinate.
"""

        response = self.client.chat.completions.create(
            model=self.model,
            temperature=0,
            response_format={"type": "json_object"},  # 🔒 Force JSON mode
            messages=[
                {"role": "system", "content": "You extract structured data and return only JSON."},
                {"role": "user", "content": prompt + "\n\nDocument:\n" + text}
            ]
        )

        latency_ms = int((time.time() - start_time) * 1000)
        token_usage = response.usage.total_tokens

        raw_output = response.choices[0].message.content.strip()

        structured = self._safe_parse(raw_output)

        return structured, token_usage, latency_ms

    def _safe_parse(self, raw_output: str):
        """
        Bulletproof JSON parsing:
        - Strip markdown fences
        - Parse safely
        - Enforce schema
        """

        # Remove markdown backticks 
        raw_output = raw_output.replace("```json", "").replace("```", "").strip()

        try:
            parsed = json.loads(raw_output)
        except Exception:
            parsed = {}

        # Enforce schema
        clean = {}
        for key in EXPECTED_KEYS:
            clean[key] = parsed.get(key, None)

        allowed_types = [
            "Notice",
            "Lawsuit",
            "Legal Correspondence",
            "Non-Legal"
        ]

        if clean["document_type"] not in allowed_types:
            clean["document_type"] = "Non-Legal"

        return clean