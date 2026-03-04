import os
import re
from ingestion.pdf_loader import PDFLoader
from ai.llm_extractor import LLMExtractor
from validation.validator import MetadataValidator
from storage.repository import MetadataRepository
from notifications.email_generator import EmailGenerator
from logging_config import logger
from config import PDF_PATHS, DATABASE_NAME


OUTPUT_EMAIL_DIR = "output_emails"


def enforce_classification_guardrails(text, llm_type):
    text_lower = text.lower()

    if "scheduling order" in text_lower:
        return "Lawsuit"

    if "first notice of loss" in text_lower:
        return "Notice"

    if "settlement offer" in text_lower:
        return "Legal Correspondence"

    if "regulatory inquiry" in text_lower:
        return "Notice"

    return llm_type


def detect_policy_quality(text):
    """

    Flags inconsistency only when:
    - Multiple distinct normalized policy numbers exist
    AND
    - No explanatory language is present
    """

    matches = re.findall(r'\bPN[A-Z0-9\-]+\b', text)

    if not matches:
        return False, 0

    normalized = [m.replace("-", "") for m in matches]
    unique_policies = set(normalized)

    policy_variant_count = len(unique_policies)

    if policy_variant_count <= 1:
        return False, policy_variant_count

    # Context aware suppression logic 
    explanatory_patterns = [
        "mis-keyed",
        "misk-keyed",
        "appears to be",
        "incorrect form",
        "variant",
        "ensure future correspondence uses the correct form"
    ]

    text_lower = text.lower()

    explanation_present = any(
        phrase in text_lower for phrase in explanatory_patterns
    )

    # Only flag inconsistency if there is no explanatory context
    policy_inconsistency = not explanation_present

    return policy_inconsistency, policy_variant_count


def save_email_to_file(request_id, email_draft):
    os.makedirs(OUTPUT_EMAIL_DIR, exist_ok=True)

    file_path = os.path.join(
        OUTPUT_EMAIL_DIR,
        f"{request_id}_draft_email.txt"
    )

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(f"To: {email_draft['recipient']}\n")
        f.write(f"Subject: {email_draft['subject']}\n\n")
        f.write(email_draft["body"])

    return file_path


def main():
    loader = PDFLoader()
    extractor = LLMExtractor()
    validator = MetadataValidator()
    repository = MetadataRepository(DATABASE_NAME)
    email_generator = EmailGenerator()

    for path in PDF_PATHS:
        try:
            raw_doc = loader.load_pdf(path)

            structured, token_usage, llm_latency = extractor.extract(raw_doc["text"])

            structured["document_type"] = enforce_classification_guardrails(
                raw_doc["text"],
                structured.get("document_type")
            )

            policy_inconsistency, policy_variant_count = detect_policy_quality(
                raw_doc["text"]
            )

            structured["policy_inconsistency"] = policy_inconsistency
            structured["policy_variant_count"] = policy_variant_count

            validated_metadata = validator.validate(structured)

            repository.save(
                raw_doc["request_id"],
                raw_doc["file_name"],
                validated_metadata,
                raw_doc["processing_time_ms"],
                llm_latency,
                token_usage
            )

            # Email generation only for valid documents
            email_generated = False
            email_file_path = None
            email_subject = None

            if validated_metadata["document_type"] != "Non-Legal":
                email_draft = email_generator.generate(validated_metadata)
                email_file_path = save_email_to_file(
                    raw_doc["request_id"],
                    email_draft
                )
                email_subject = email_draft["subject"]
                email_generated = True

            logger.info(
                "document_processed",
                extra={
                    "extra_data": {
                        "request_id": raw_doc["request_id"],
                        "file_name": raw_doc["file_name"],
                        "document_type": validated_metadata["document_type"],
                        "confidence_score": validated_metadata["confidence_score"],
                        "policy_inconsistency": validated_metadata["policy_inconsistency"],
                        "policy_variant_count": validated_metadata["policy_variant_count"],
                        "processing_time_ms": raw_doc["processing_time_ms"],
                        "llm_latency_ms": llm_latency,
                        "token_usage": token_usage,
                        "email_generated": email_generated,
                        "email_subject": email_subject,
                        "email_file": email_file_path
                    }
                }
            )

        except Exception as e:
            logger.error(f"processing_failed: {str(e)}")


if __name__ == "__main__":
    main()
