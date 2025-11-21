import asyncio
import json

from app.aws_client import get_sqs_client
from app.config import settings
from app.infra.db import AsyncSessionLocal

from app.modules.reports.repository import ReportRepository
from app.modules.reports.service import ReportsService

from app.modules.reports.models import Report
from app.modules.trips.models import Trip
from app.modules.expenses.models import Expense
from app.modules.users.models import User
from app.modules.rate_categories.models import RateCategory
from app.modules.rate_customizations.models import RateCustomization
from app.modules.auth.models import RefreshToken


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

                await self.process_report(body["report_id"])

                self.sqs.delete_message(
                    QueueUrl=self.queue_url,
                    ReceiptHandle=message["ReceiptHandle"]
                )

                print(f"Deleted message from queue: {body}\n")

    async def process_report(self, report_id: str):
        async with AsyncSessionLocal() as session:
            service = ReportsService(session, ReportRepository())
            print(f"Generating report for {report_id}...")
            report = await service.generate_now(report_id)

            print(f"Report generated: file={report.file_name}")


async def main():
    worker = ReportWorker()
    await worker.start()


if __name__ == "__main__":
    asyncio.run(main())
