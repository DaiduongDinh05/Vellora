import os
from uuid import UUID


class LocalReportStorage:
    def __init__(self, base_folder: str = "./generated_reports"):
        self.base_folder = base_folder

    def save(self, report_id: UUID, pdf_bytes: bytes) -> str:
        os.makedirs(self.base_folder, exist_ok=True)

        filename = f"report_{report_id}.pdf"
        filepath = os.path.join(self.base_folder, filename)

        with open(filepath, "wb") as f:
            f.write(pdf_bytes)

        return filepath
