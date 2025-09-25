# Base image for Python backend
FROM python:3.10-slim

# Build arg to optionally skip frontend build (use prebuilt dist)
ARG SKIP_FRONTEND_BUILD=false

# Note: Node.js will be installed later only if frontend build is enabled

# Set working directory
WORKDIR /app

# Install system dependencies including netcat for database connection checks
RUN apt-get update && apt-get install -y netcat-openbsd && rm -rf /var/lib/apt/lists/*

# Copy Python requirements
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# Copy everything
COPY . .

# Optionally build Angular frontend inside the image
RUN if [ "$SKIP_FRONTEND_BUILD" != "true" ]; then \
      echo "[build] Installing Node.js and building Angular frontend" && \
      apt-get update && apt-get install -y curl gnupg && \
      curl -fsSL https://deb.nodesource.com/setup_18.x | bash - && \
      apt-get install -y nodejs && \
      npm install -g @angular/cli && \
      cd /app/frontend && \
      if [ -f package-lock.json ]; then npm ci --no-audit --no-fund --prefer-offline; else npm install --no-audit --no-fund --prefer-offline; fi && \
      npm run build -- --configuration production && \
      rm -rf /var/lib/apt/lists/*; \
    else \
      echo "[build] Skipping frontend build; using existing /app/frontend/dist if present"; \
    fi

# Expose port (HF Spaces requires 7860)
EXPOSE 7860

# Switch back to project root where app.py lives
WORKDIR /app

# Copy entrypoint that will export Hugging Face secrets into a .env file
COPY docker-entrypoint.sh /app/docker-entrypoint.sh
RUN chmod +x /app/docker-entrypoint.sh

ENV PYTHONUNBUFFERED=1 \
    PORT=7860

# Entrypoint writes .env from env vars and applies DB migrations before starting
ENTRYPOINT ["/app/docker-entrypoint.sh"]

# Run Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:7860", "--timeout", "120", "--log-level", "debug", "app:app"]
