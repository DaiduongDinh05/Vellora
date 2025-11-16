# Vellora -- "The Value of the Journey"

## Running with Docker

### Prerequisites
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running

### Quick Start

1. **Clone and navigate to the project:**
```bash
git clone <repository-url>
cd Vellora
```

2. **Set up environment variables:**

Create a .env file in the backend/ dir

Edit the `.env` file with your actual values:
```bash
DATABASE_URL=your_db_url
FERNET_KEY=your_fernet_key_here
JWT_SECRET_KEY=your_jwt_secret_here
OAUTH_PROVIDERS__GOOGLE__CLIENT_ID=your_google_client_id
OAUTH_PROVIDERS__GOOGLE__CLIENT_SECRET=your_google_client_secret
OAUTH_PROVIDERS__GOOGLE__REDIRECT_URI=your_google_redirect_uri
OAUTH_PROVIDERS__GOOGLE__SCOPES=your_google_scopes
OAUTH_STATE_TTL_SECONDS=your_state_ttl_seconds
```

**For actual credential values, check our Discord documentation.**

3. **Run the application:**
```bash
docker compose up --build
```

### Access Points
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Frontend**: Check Discord

