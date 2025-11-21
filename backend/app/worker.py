import asyncio
import json

from app.aws_client import get_sqs_client
from app.config import settings


class ReportWorker:

    def __init__(self):
        self.sqs = get_sqs_client()
        self.queue_url = self.sqs.get_queue_url(QueueName=settings.REPORTS_QUEUE)["QueueUrl"]

    async def start(self):
        print("Worker is running and listening for messages...\n")

        while True:
            response = self.sqs.receive_message(
                QueueUrl=self.queue_url,
                MaxNumberOfMessages=1,
                WaitTimeSeconds=5
            )

            messages = response.get("Messages", [])

            if not messages:
                await asyncio.sleep(1)
                continue

            for message in messages:
                body = json.loads(message["Body"])
                print(f"Received message: {body}")

                # delete after processing
                self.sqs.delete_message(
                    QueueUrl=self.queue_url,
                    ReceiptHandle=message["ReceiptHandle"]
                )

                print(f"Deleted message: {body}\n")


async def main():
    worker = ReportWorker()
    await worker.start()


if __name__ == "__main__":
    asyncio.run(main())
