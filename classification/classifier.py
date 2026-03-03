class DocumentClassifier:

    def classify(self, text: str) -> str:
        text_lower = text.lower()

        if "scheduling order" in text_lower:
            return "Lawsuit"
        elif "regulatory inquiry" in text_lower:
            return "Notice"
        elif "first notice of loss" in text_lower:
            return "Notice"
        elif "settlement offer" in text_lower:
            return "Legal Correspondence"
        elif "coverage position" in text_lower:
            return "Legal Correspondence"
        elif "expo" in text_lower:
            return "Non-Legal"
        else:
            return "Unknown"