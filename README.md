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

Flask backend + Angular frontend served via Gunicorn inside Docker with PostgreSQL database.

## Prerequisites

-   Docker and Docker Compose installed
-   PostgreSQL database (local or remote)

## Quick Start with Docker Compose

The easiest way to run the application:

```shell
# Start PostgreSQL, pgAdmin, and the application
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the application
docker-compose down
```

**Access Points:**

-   Frontend: http://localhost:7860
-   API Documentation: http://localhost:7860/api/docs
-   Health Check: http://localhost:7860/api/hello
-   pgAdmin: http://localhost:8080 (admin@example.com / admin)
-   PostgreSQL: localhost:5432 (postgres / postgres)

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

```shell
# Stop any existing container
docker rm -f ai_schedule_container 2>/dev/null || true

# Run the application
docker run -d --name ai_schedule_container \
  -p 7860:7860 \
  -e DATABASE_URL="postgresql+psycopg://postgres:postgres@host.docker.internal:5432/ai_schedule_organizer" \
  -e SECRET_KEY=dev \
  -e PORT=7860 \
  ai-schedule-organizer:latest
```

### 4. Run with Local PostgreSQL

If you have PostgreSQL running locally:

```shell
docker run -d --name ai_schedule_container \
  -p 7860:7860 \
  -e DATABASE_URL="postgresql+psycopg://postgres:postgres@localhost:5432/ai_schedule_organizer" \
  -e SECRET_KEY=dev \
  -e PORT=7860 \
  --network host \
  ai-schedule-organizer:latest
```

## Environment Variables

-   `DATABASE_URL`: PostgreSQL connection string (required)
-   `SECRET_KEY`: Flask secret key (default: "dev")
-   `PORT`: Application port (default: 7860)

## Database Setup

The application uses Alembic for database migrations. Migrations run automatically on startup and include:

-   Schema creation with proper ENUM types
-   Seed data with 5 roles, 2 programs, 2 cohorts, 110 users, and 20 periods

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

# Run migrations
alembic upgrade head

# Start the application
python app.py
```

## 🚀 **Hugging Face Spaces Deployment**

### **Important Notes for HF Spaces:**

-   **Frontend API Calls**: Use `docker.internal.host:7860` instead of `localhost:7860` for API calls
-   **Database Connection**: Ensure your `DATABASE_URL` points to an accessible PostgreSQL instance
-   **Environment Variables**: Set `DATABASE_URL` as a secret in your Space settings
-   **Required Secrets**:
-   `DATABASE_URL`: PostgreSQL connection string (e.g., `postgresql+psycopg://user:pass@host:port/db`)
-   `SECRET_KEY`: Flask secret key for sessions
-   **Setting Secrets**: Go to Space Settings → Variables and secrets → Add new secret
-   **Network**: The Docker build includes netcat for database connection checks
-   **Fallback**: If `DATABASE_URL` is not set, the app will show a clear error message
