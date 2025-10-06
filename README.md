---
title: AI Schedule Organizer
emoji: 📅
colorFrom: purple
colorTo: blue
sdk: docker
app_file: app.py
pinned: false
---

# AI Schedule Organizer

Flask backend + Angular frontend served via Gunicorn inside Docker. The app targets a managed Postgres (Neon) by default and no longer runs Alembic migrations in the container. A full schema + seed script lives at `backend/database/schema_seed.sql` for manual initialization.

## Prerequisites

-   Docker and Docker Compose installed
-   PostgreSQL database (local or remote)

## Quick Start

Run the application container (recommended to pass your own `DATABASE_URL`):

```shell
docker build -t ai-schedule-organizer .

docker run -d --name ai_schedule_container \
  -p 7860:7860 \
  -e DATABASE_URL="postgresql+psycopg://<user>:<pass>@<host>:<port>/<db>?sslmode=require" \
  -e SECRET_KEY=dev \
  -e PORT=7860 \
  ai-schedule-organizer:latest
```

If `DATABASE_URL` is omitted, the app defaults to the Neon DSN baked into the image. Overriding via env is recommended for your deployment.

**Access Points:**

-   Frontend: http://localhost:7860
-   API Documentation: http://localhost:7860/api/docs
-   Health Check: http://localhost:7860/api/hello

## Manual Docker Setup

### 1. Build the Frontend (Optional - can be built in Docker)

```shell
cd frontend
npm install
npm run build
cd ..
```

### 2. Build the Docker Image

```shell
# Build with frontend (recommended for development)
docker build -t ai-schedule-organizer .

# Or build skipping frontend (if you already built it locally)
docker build -t ai-schedule-organizer . --build-arg SKIP_FRONTEND_BUILD=true
```

### 3. Run with PostgreSQL

Managed Postgres (e.g., Neon): pass your `DATABASE_URL` as shown in Quick Start.

Local Postgres (via Docker or installed):

```shell
# Stop any existing container
docker rm -f ai_schedule_container 2>/dev/null || true

# Run the application pointing to local DB (from host)
docker run -d --name ai_schedule_container \
  -p 7860:7860 \
  -e DATABASE_URL="postgresql+psycopg://postgres:postgres@host.docker.internal:5432/ai_schedule_organizer" \
  -e SECRET_KEY=dev \
  -e PORT=7860 \
  ai-schedule-organizer:latest
```

### 4. Optional: Local Postgres with Docker Compose

`docker-compose.yml` starts only Postgres and pgAdmin (no app service). Use this if you want a local database:

```shell
docker-compose up -d

# Initialize schema + sample data into local DB
psql "postgresql://postgres:postgres@localhost:5432/ai_schedule_organizer" \
  -f backend/database/schema_seed.sql

# Then run the app container pointing at local DB
docker run -d --name ai_schedule_container \
  -p 7860:7860 \
  -e DATABASE_URL="postgresql+psycopg://postgres:postgres@host.docker.internal:5432/ai_schedule_organizer" \
  -e SECRET_KEY=dev \
  ai-schedule-organizer:latest
```

## Environment Variables

-   `DATABASE_URL`: PostgreSQL connection string. If not provided, defaults to the preconfigured Neon DSN.
-   `SECRET_KEY`: Flask secret key (default: "dev")
-   `PORT`: Application port (default: 7860)

## Database Setup

The container does not run migrations. To initialize a database (local or managed), apply the SQL script:

```shell
# Example: local Postgres
psql "postgresql://postgres:postgres@localhost:5432/ai_schedule_organizer" \
  -f backend/database/schema_seed.sql
```

This creates the schema (including ENUMs) and seeds: roles, programs, cohorts, ~110 users, and 20 periods.

## Access the Application

-   Frontend: http://localhost:7860
-   API Documentation: http://localhost:7860/api/docs
-   Health Check: http://localhost:7860/api/hello

## Development

For local development without Docker:

```shell
# Install dependencies
pip install -r requirements.txt
cd frontend && npm install && cd ..

# Set environment variables
export DATABASE_URL="postgresql+psycopg://postgres:postgres@localhost:5432/ai_schedule_organizer"
export SECRET_KEY="dev"

# Initialize DB schema/data once (no migrations run by the app)
psql "$DATABASE_URL" -f backend/database/schema_seed.sql

# Start the application
python app.py
```

## 🚀 **Hugging Face Spaces Deployment**

### **Notes for HF Spaces:**

-   Set `DATABASE_URL` as a secret (recommended). If absent, the container defaults to the preconfigured Neon DSN.
-   Set `SECRET_KEY` as a secret.
-   The app listens on port `7860`. Ensure the frontend targets the container host/port (avoid `localhost` in some setups).

## Running n8n on Hugging Face Spaces

This repository includes a bundled n8n installation that will run alongside the Flask backend inside the same Docker container. n8n is exposed under the path `/n8n/` and is proxied by nginx.

Recommended environment variables (set these as Secrets in your HF Space):

- `N8N_BASIC_AUTH_ACTIVE=true` — enable basic auth to protect the n8n editor
- `N8N_BASIC_AUTH_USER` — username for n8n basic auth
- `N8N_BASIC_AUTH_PASSWORD` — password for n8n basic auth
- `PORT` — must remain `7860` for HF Spaces (default: `7860`)

Automatic Postgres wiring for n8n
---------------------------------

This image will configure n8n to use Postgres automatically if you provide database connection information.

Priority order used by the container at startup:

1. If `N8N_DATABASE_URL` is set in the environment (recommended for separating n8n), it will be parsed and used to populate n8n's `N8N_DB_*` variables.
2. Otherwise, if `DATABASE_URL` is present (used by the Flask app), the entrypoint will parse it and export the equivalent `N8N_DB_POSTGRES*` variables so n8n uses the same Neon Postgres instance.
3. If no DB info is provided, n8n will run with in-memory storage (not persistent).

If you want n8n to persist data in your Neon Postgres, add either `N8N_DATABASE_URL` (preferred) or ensure `DATABASE_URL` points to a Neon database with sufficient privileges. The entrypoint will attempt to parse these DSNs and export the `N8N_DB_TYPE=postgresdb` and `N8N_DB_POSTGRES*` env vars that n8n expects.

Recommended HF Secrets to set for persistent n8n:

- `N8N_DATABASE_URL` or `DATABASE_URL` (if you prefer to share the same DB)
- `N8N_BASIC_AUTH_ACTIVE`, `N8N_BASIC_AUTH_USER`, `N8N_BASIC_AUTH_PASSWORD`

Ensure the DB user has permission to create tables; n8n will create its schema on first run.

Access points after deployment on HF Spaces:

- App (frontend + API): https://<your-space>.hf.space/
- n8n editor: https://<your-space>.hf.space/n8n/

Notes and caveats:

- n8n persists its data in-memory by default in this setup. For production-grade persistence, configure n8n's external database (Postgres) and set `N8N_DB_TYPE`, `N8N_DB_POSTGRESDB`, `N8N_DB_POSTGRES_PASSWORD`, etc., as environment variables. This repo keeps the setup minimal to fit inside a single HF Space container.
- If you enable basic auth via `N8N_BASIC_AUTH_*` variables, the nginx proxy will forward requests but n8n will enforce the auth itself.
