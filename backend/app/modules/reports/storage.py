import uuid
from app.aws_client import get_s3_client
from app.config import settings


class S3ReportStorage:
    def __init__(self):
        self.s3 = get_s3_client()
        self.bucket = settings.REPORTS_BUCKET

    def save(self, report_id: uuid.UUID, file_bytes: bytes) -> str:
        file_name = f"report_{report_id}.pdf"
        
        self.s3.put_object(
            Bucket=self.bucket,
            Key=file_name,
            Body=file_bytes,
            ContentType="application/pdf"
        )

        #will return a public or signed URL later for now returns S3 key path
        return f"s3://{self.bucket}/{file_name}"
