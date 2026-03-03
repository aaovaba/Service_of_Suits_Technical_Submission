import re
from collections import Counter


class MetadataExtractor:

    def extract_policy_number(self, text):
        matches = re.findall(r'\bPN[A-Z0-9\-]+\b', text)

        if not matches:
            return None, False, 0

        normalized = [m.replace("-", "") for m in matches]
        most_common = Counter(normalized).most_common(1)[0][0]

        unique_policies = set(normalized)
        policy_variant_count = len(unique_policies)

        policy_inconsistency = False

        if policy_variant_count > 1:
            explanatory_patterns = [
                "appears to be",
                "misk-keyed",
                "mis-keyed",
                "incorrect form",
                "variant",
                "ensure future correspondence uses the correct form"
            ]

            text_lower = text.lower()
            explanation_present = any(
                phrase in text_lower for phrase in explanatory_patterns
            )

            if not explanation_present:
                policy_inconsistency = True

        return most_common, policy_inconsistency, policy_variant_count

    def extract_case_reference(self, text):
        match = re.search(r'\b[A-Z]{2,}-\d{4}-\d+(?:-[A-Z]+)?\b', text)
        return match.group(0) if match else None

    def extract_email_recipient(self, text):
        match = re.search(r'[\w\.-]+@[\w\.-]+', text)
        return match.group(0) if match else None

    def extract_date_of_loss(self, text, document_type):
        if document_type == "Non-Legal":
            return None

        if "Date of Loss: Not applicable" in text:
            return None

        match = re.search(
            r'\b\d{1,2} (January|February|March|April|May|June|July|August|September|October|November|December) \d{4}\b',
            text
        )

        return match.group(0) if match else None

    def extract_parties(self, text):
        match = re.search(
            r'([A-Za-z\s\.]+?)\s+v\.?\s+([A-Za-z\s\.]+?)(?:\n|,|\(|$)',
            text
        )
        if match:
            return match.group(1).strip(), match.group(2).strip()

        match = re.search(
            r'Subject:.*?([A-Za-z\s\.]+?)\s+v\.?\s+([A-Za-z\s\.]+)',
            text,
            re.IGNORECASE
        )
        if match:
            return match.group(1).strip(), match.group(2).strip()

        return None, None

    def extract_metadata(self, text, document_type):

        policy_number, policy_inconsistency, policy_variant_count = self.extract_policy_number(text)
        case_reference = self.extract_case_reference(text)
        recipient = self.extract_email_recipient(text)
        date_of_loss = self.extract_date_of_loss(text, document_type)
        claimant, defendant = self.extract_parties(text)

        return {
            "document_type": document_type,
            "date_of_loss": date_of_loss,
            "policy_number": policy_number,
            "recipient": recipient,
            "claimant": claimant,
            "defendant": defendant,
            "case_reference": case_reference,
            "policy_inconsistency": policy_inconsistency,
            "policy_variant_count": policy_variant_count
        }