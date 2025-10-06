# Base image for Python backend
FROM python:3.10-slim

# Build arg to optionally skip frontend build (use prebuilt dist)
ARG SKIP_FRONTEND_BUILD=false

# Note: Node.js will be installed later only if frontend build is enabled

# Set working directory
WORKDIR /app

# (Optional) system utils; Postgres is not required when using Neon
RUN apt-get update && apt-get install -y \
  ca-certificates curl gnupg gnupg2 lsb-release \
  build-essential \
  nginx supervisor \
  && rm -rf /var/lib/apt/lists/*

# Copy Python requirements
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# Copy everything
COPY . .

# Optionally build Angular frontend inside the image
RUN if [ "$SKIP_FRONTEND_BUILD" != "true" ]; then \
      echo "[build] Installing Node.js and building Angular frontend" && \
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

# Install n8n globally so we can run it inside the container. We install only when building final image.
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
  && apt-get install -y nodejs \
  && npm install -g n8n@1.0.0 \
  && rm -rf /var/lib/apt/lists/* /root/.npm

# Expose port (HF Spaces requires 7860)
EXPOSE 7860

# Switch back to project root where app.py lives
WORKDIR /app

# Copy entrypoint that will export Hugging Face secrets into a .env file
COPY docker-entrypoint.sh /app/docker-entrypoint.sh
RUN chmod +x /app/docker-entrypoint.sh

# Copy supervisor and nginx configs
COPY docker/supervisor/ai-services.conf /etc/supervisor/conf.d/ai-services.conf
COPY docker/nginx/ai.conf /etc/nginx/sites-available/ai.conf
RUN ln -sf /etc/nginx/sites-available/ai.conf /etc/nginx/sites-enabled/ai.conf
RUN rm -f /etc/nginx/sites-enabled/default || true

ENV PYTHONUNBUFFERED=1 \
    PORT=7860

# Entrypoint writes .env from env vars before starting. Then start supervisord which manages services.
ENTRYPOINT ["/app/docker-entrypoint.sh"]

# Supervisor will run nginx, gunicorn (on 127.0.0.1:7861) and n8n (default 5678). Expose 7860 externally.
CMD ["/usr/bin/supervisord", "-n", "-c", "/etc/supervisor/supervisord.conf"]
