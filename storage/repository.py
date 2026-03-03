import sqlite3


class MetadataRepository:

    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.create_table()

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS documents (
                request_id TEXT,
                file_name TEXT,
                document_type TEXT,
                date_of_loss TEXT,
                policy_number TEXT,
                recipient TEXT,
                claimant TEXT,
                defendant TEXT,
                case_reference TEXT,
                completeness_status TEXT,
                confidence_score REAL,
                validation_level TEXT,
                policy_inconsistency INTEGER,
                policy_variant_count INTEGER,
                processing_time_ms INTEGER,
                llm_latency_ms INTEGER,
                token_usage INTEGER
            )
        """)
        self.conn.commit()

    def save(self, request_id, file_name, metadata,
             processing_time_ms, llm_latency_ms, token_usage):

        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO documents VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            request_id,
            file_name,
            metadata.get("document_type"),
            metadata.get("date_of_loss"),
            metadata.get("policy_number"),
            metadata.get("recipient"),
            metadata.get("claimant"),
            metadata.get("defendant"),
            metadata.get("case_reference"),
            metadata.get("completeness_status"),
            metadata.get("confidence_score"),
            metadata.get("validation_level"),
            int(metadata.get("policy_inconsistency", False)),
            metadata.get("policy_variant_count"),
            processing_time_ms,
            llm_latency_ms,
            token_usage
        ))
        self.conn.commit()