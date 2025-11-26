import asyncio
import json

from app.aws_client import get_sqs_client
from app.config import settings
from app.infra.db import AsyncSessionLocal

from app.modules.reports.repository import ReportRepository
from app.modules.reports.service import ReportsService

from app.modules.reports.models import Report, ReportStatus
from app.modules.trips.models import Trip
from app.modules.expenses.models import Expense
from app.modules.users.models import User
from app.modules.rate_categories.models import RateCategory
from app.modules.rate_customizations.models import RateCustomization
from app.modules.auth.models import RefreshToken

VISIBILITY_TIMEOUT = 60 
MAX_RECEIVE_COUNT = 3 

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
                WaitTimeSeconds=5,
                VisibilityTimeout=VISIBILITY_TIMEOUT,
                AttributeNames=['All'],
                MessageAttributeNames=['All'] 
            )

            messages = response.get("Messages", [])

            if not messages:
                await asyncio.sleep(1)
                continue

            for message in messages:
                body = json.loads(message["Body"])
                receipt = message["ReceiptHandle"]
                retry_count = int(message.get("Attributes", {}).get("ApproximateReceiveCount", "1"))

                print(f"Received message: {body} (Attempt {retry_count})")
                
                if retry_count >= MAX_RECEIVE_COUNT:
                    print(f"Max retries reached for {body['report_id']}. Marking as failed.")
                    async with AsyncSessionLocal() as session:
                        await self.mark_failed(session, body["report_id"])
                    self.sqs.delete_message(QueueUrl=self.queue_url, ReceiptHandle=receipt)
                    continue

                success = await self.process_report(body["report_id"])

                if success:
                    self.sqs.delete_message(QueueUrl=self.queue_url, ReceiptHandle=receipt)
                    print(f"Deleted message from queue: {body}\n")
                    continue

                print(f"Worker failed for {body}. Will retry.\n")

    async def mark_failed(self, session, report_id):
        try:
            repo = ReportRepository()
            report = await repo.get_by_id(session, report_id)
            if report:
                report.status = ReportStatus.failed
                await session.commit()
        except Exception as e:
            print(f"Error marking report {report_id} as failed: {e}")

    async def process_report(self, report_id: str):
        
        repo = ReportRepository()

        try:
            async with AsyncSessionLocal() as session:
                report = await repo.get_by_id(session, report_id)

                if not report:
                    print(f"Report {report_id} not found. Skipping.")
                    return True

                if report.status == ReportStatus.completed:
                    print(f"{report_id} already completed - skipping.")
                    return True

                service = ReportsService(session, repo, None, None, None, None)

                report.status = ReportStatus.processing
                await session.commit()

                print(f"Generating report for {report_id}...")
                await service.generate_now(report_id)
                print(f"Report done: {report.file_name}")
                return True

        except Exception as e:
            try:
                async with AsyncSessionLocal() as session:
                    await self.mark_failed(session, report_id)
            except Exception as commit_error:
                print(f"Error marking report {report_id} as failed: {commit_error}")
                
            print(f"Error generating {report_id}: {e}")
            return False


async def main():
    worker = ReportWorker()
    await worker.start()


if __name__ == "__main__":
    asyncio.run(main())
