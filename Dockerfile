# Base image for Python backend
FROM python:3.10-slim

# Install Node.js + Angular CLI
RUN apt-get update && apt-get install -y curl gnupg \
    && curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs \
    && npm install -g @angular/cli \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy Python requirements
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# Copy everything
COPY . .

# Build Angular frontend
WORKDIR /app/frontend
RUN npm install && npm run build --configuration production

# Expose port (HF Spaces requires 7860)
EXPOSE 7860

# Switch back to project root where app.py lives
WORKDIR /app

# Run Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:7860", "--timeout", "120", "--log-level", "debug", "app:app"]