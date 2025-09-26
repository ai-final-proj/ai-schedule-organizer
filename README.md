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
