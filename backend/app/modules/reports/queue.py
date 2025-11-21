import json
from app.config import settings
from app.aws_client import get_sqs_client

class ReportQueue:
    def __init__(self):
        self.client = get_sqs_client()
        self.queue_url = self.client.get_queue_url(QueueName=settings.REPORTS_QUEUE)["QueueUrl"]

    def send(self, report_id: str):
        message = json.dumps({"report_id": report_id})

        self.client.send_message(QueueUrl=self.queue_url, MessageBody=message)
