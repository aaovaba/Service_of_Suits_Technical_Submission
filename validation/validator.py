class MetadataValidator:

    REQUIRED_FIELDS_BY_TYPE = {
        "Lawsuit": ["policy_number", "case_reference"],
        "Notice": ["policy_number"],
        "Legal Correspondence": ["policy_number"],
    }

    EXPECTED_FIELDS_BY_TYPE = {
        "Lawsuit": [
            "policy_number",
            "case_reference",
            "date_of_loss",
            "recipient",
            "claimant",
            "defendant"
        ],
        "Notice": [
            "policy_number",
            "date_of_loss",
            "recipient"
        ],
        "Legal Correspondence": [
            "policy_number",
            "date_of_loss",
            "recipient",
            "claimant",
            "defendant",
            "case_reference"
        ],
    }

    def validate(self, metadata: dict):

        doc_type = metadata.get("document_type")

        if doc_type == "Non-Legal":
            metadata["missing_fields"] = []
            metadata["completeness_status"] = "Rejected - Non Legal Document"
            metadata["confidence_score"] = 0.0
            metadata["validation_level"] = "Rejected"
            return metadata

        required_fields = self.REQUIRED_FIELDS_BY_TYPE.get(doc_type, [])
        expected_fields = self.EXPECTED_FIELDS_BY_TYPE.get(doc_type, [])

        # Completeness Check 
        missing = []

        for field in required_fields:
            if not metadata.get(field):
                missing.append(field)

        metadata["missing_fields"] = missing

        if missing:
            metadata["completeness_status"] = "Incomplete"
        else:
            metadata["completeness_status"] = "Complete"

        metadata["validation_level"] = "Required Fields Only"

        # Confidence Scoring 
        if expected_fields:
            populated = sum(1 for field in expected_fields if metadata.get(field))
            confidence = round(populated / len(expected_fields), 2)
        else:
            confidence = 0.0

        metadata["confidence_score"] = confidence

        return metadata