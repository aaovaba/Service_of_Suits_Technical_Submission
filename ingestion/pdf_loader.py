import pdfplumber
import time
import uuid
from pathlib import Path


class PDFLoader:

    def load_pdf(self, file_path: str):
        start_time = time.time()
        request_id = str(uuid.uuid4())

        text_content = ""

        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text_content += page.extract_text() or ""

        latency = int((time.time() - start_time) * 1000)

        return {
            "request_id": request_id,
            "file_name": Path(file_path).name,
            "text": text_content,
            "processing_time_ms": latency
        }