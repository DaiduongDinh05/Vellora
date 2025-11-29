# Vellora -- "The Value of the Journey"

## Running with Docker

### Prerequisites
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running
- Git

### Quick Start

1. **Clone and navigate to the project:**
```bash
git clone https://github.com/Stack-Underflow-Capstone/Vellora.git
cd Vellora
```

2. **Set up environment variables:**

Create a `.env` file in the `backend/` directory with the following structure:

```bash
# Database
DATABASE_URL=your_db_url

# Security  
JWT_SECRET_KEY=your_jwt_secret_here
FERNET_KEY=your_fernet_key_here

# OAuth (Google)
OAUTH_PROVIDERS__GOOGLE__CLIENT_ID=your_google_client_id
OAUTH_PROVIDERS__GOOGLE__CLIENT_SECRET=your_google_client_secret
OAUTH_PROVIDERS__GOOGLE__REDIRECT_URI=your_google_redirect_uri
OAUTH_PROVIDERS__GOOGLE__SCOPES=your_google_scopes
OAUTH_STATE_TTL_SECONDS=600

# LocalStack AWS Services (for local development)
USE_LOCALSTACK=true
AWS_ACCESS_KEY_ID=test
AWS_SECRET_ACCESS_KEY=test
AWS_REGION=us-east-1
LOCALSTACK_ENDPOINT=http://localstack:4566
REPORTS_BUCKET=vellora-s3-bucket
REPORTS_QUEUE=generateReports-queue

# LocalStack Pro Token
LOCALSTACK_AUTH_TOKEN=your_localstack_token_here
```

**For actual credential values, check our Discord documentation.**

3. **Windows Users - Important Step:**
Before running Docker commands, ensure script files have proper line endings:
- Open `init-resources.sh` and `wait-for-postgres.sh` in VS Code
- Change line endings from CRLF to LF (in VS Code: click "CRLF" in bottom status bar then select "LF")
- Save the files (don't commit these changes)

4. **Build and run the application:**

First time or when dependencies/environment changes:
```bash
docker compose up -d --build
```

Subsequent runs (no changes):
```bash
docker compose up -d
```

5. **Verify LocalStack setup:**

Check if SQS queues were created:
```bash
docker exec -it localstack awslocal sqs list-queues
```

Check if S3 bucket was created:
```bash
docker exec -it localstack awslocal s3 ls
```

6. **Start the background worker:**
```bash
docker exec -it vellora_backend_service python -m app.worker
```

### Access Points
- **Backend API**: http://localhost:8000
- **API Documentation (Swagger)**: http://localhost:8000/docs
- **Frontend**: http://localhost:8081 (Expo development server) --check discord

### Important Notes

**Report Downloads:** When downloading reports via the API, Docker may return URLs starting with `http://localstack:4566/`. These won't work in your browser. Simply replace `localstack` with `localhost` in the URL:
- ❌ `http://localstack:4566/vellora-s3-bucket/report.pdf`
- ✅ `http://localhost:4566/vellora-s3-bucket/report.pdf`

**Stopping the Application:**
```bash
docker compose down
```

