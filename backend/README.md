
## Dev guide

### Setup with Docker

**Prerequisites:**
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running
- Git

#### 1. Clone repo
```bash
git clone https://github.com/Stack-Underflow-Capstone/Vellora.git
cd Vellora
```

#### 2. Set up environment variables
Create a `.env` file in the backend directory with these values (check Discord for latest credentials):

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

**Windows Users:** Before running Docker commands, make sure all `.sh` script files have LF line endings instead of CRLF:
1. Open `init-resources.sh` and `wait-for-postgres.sh` in VS Code
2. Click on "CRLF" in the bottom status bar and change to "LF"
3. Save the files (don't commit these changes)

#### 3. Build and run with Docker
When you change dependencies or environment variables:
```bash
docker compose up -d --build
```

For subsequent runs (no changes to dependencies/env):
```bash
docker compose up -d
```

#### 4. Verify LocalStack setup
Check if SQS queues were created:
```bash
docker exec -it localstack awslocal sqs list-queues
```

Check if S3 bucket was created:
```bash
docker exec -it localstack awslocal s3 ls
```

#### 5. Start the worker process
Run the background worker for report generation:
```bash
docker exec -it vellora_backend_service python -m app.worker
```

#### 6. Access the application
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

**Note about report downloads:** When using the reports download endpoint, Docker might return a URL starting with `http://localstack:4566/`. This won't work from your browser. Simply replace `localstack` with `localhost` in the URL to access the report: `http://localhost:4566/...`

### Setup without Docker (Local Development)

#### 1. Clone repo
```bash
git clone https://github.com/Stack-Underflow-Capstone/Vellora.git
cd Vellora/backend
```

#### 2. Create and activate a virtual environment 
##### Windows:
```bash
python -m venv .venv
.venv\Scripts\activate
```

##### Mac:
  ``` bash
  python -m venv .venv
  source .venv/bin/activate
  ```
You should see (.venv) at the beginning of your terminal line if this worked

#### 3. Install dependencies
```bash
pip install -r requirements.txt
```

If you install any new package later `pip install somepackage`, always update the requirements file:
```bash
pip freeze > requirements.txt
```

#### 4. Set up LocalStack locally
Install and configure LocalStack following the attachment instructions:
1. Install LocalStack CLI
2. Create `C:\dev\localstack` directory  
3. Create a docker-compose.yml file in that directory with:
```yaml
services:
  localstack:
    container_name: localstack
    image: localstack/localstack:latest
    ports:
      - "4566:4566"
    environment:
      - SERVICES=s3,sqs
      - DEBUG=1
      - AWS_DEFAULT_REGION=us-east-1
    volumes:
      - "./data:/var/lib/localstack"

```
4. Configure AWS CLI with profile `localstack`:
```bash
AWS Access Key ID [None]: test
AWS Secret Access Key [None]: test
Default region name [None]: us-east-1
Default output format [None]: json

```
5. Create S3 bucket and SQS queue using LocalStack commands
```bash
aws --endpoint-url=http://localhost:4566 s3api create-bucket --bucket vellora-s3-bucket --profile localstack
aws --endpoint-url=http://localhost:4566 sqs create-queue --queue-name generateReports-queue --profile localstack
```

#### 5. Set up your `.env` file
Create a file named `.env` in the backend root with the environment variables listed above, but change:
- `LOCALSTACK_ENDPOINT=http://localhost:4566` 
- Any database connection strings as needed for your local setup ex: `postgresql+asyncpg://postgres:postgres@localhost:5432/Vellora`

#### 6. Run the app
To run the FastAPI development server:
```bash
fastapi dev app/main.py
```

To run the worker process:
```bash
python -m app.worker
```

**Documentation (Swagger)**: http://127.0.0.1:8000/docs

### Creating a new feature

#### 1. Create folder in module folder

ex:
```
app/modules/trips/
```

#### 2. Inside it, create these files and write your code:

```
router.py        # FastAPI endpoints
service.py       # Business logic
repository.py    # DB queries (using async SQLAlchemy)
models.py        # ORM models (inherit from Base)
schemas.py       # Pydantic request/response models
__init__.py
```

#### 2. Inside it, create these files and write your code:

Alembic only sees your models if they’re imported inside:
```
app/infra/migrations/env.py
```

So add this line at the top:
```python
from app.modules.trips import models  #"app.modules.<name of folder>"
```

That’s all don’t modify anything else in `env.py`.

#### 3. Generating and Applying Migrations

Whenever you add or change a model:

First Generate a migration file
```
alembic revision --autogenerate -m "desc of what u did in model"
```
Then Apply the migration
```
alembic upgrade head
```
You can undo migrations if u ever need to.

#### 4. Registering your router

After creating your router, you must include it in the global API.

Open:
```
app/api/v1/router.py
```
Add:
```python
from app.modules.trips.router import router as trips_router #app.modules.<folder name>.router
router.include_router(trips_router)
```

