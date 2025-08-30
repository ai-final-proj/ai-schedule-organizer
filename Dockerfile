# Base image for Python backend
FROM python:3.10-slim

# Install Node.js for Angular frontend
RUN apt-get update && apt-get install -y curl gnupg \
    && curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs \
    && npm install -g @angular/cli \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Install Python dependencies
COPY backend/requirements.txt backend/requirements.txt
RUN pip install --no-cache-dir -r backend/requirements.txt gunicorn

# Copy project files
COPY . .

# Build Angular frontend
WORKDIR /app/frontend
RUN npm install && ng build --configuration production

# Move build output to backend static folder
RUN mkdir -p /app/backend/static
RUN cp -r dist/* /app/backend/static/

# Expose Hugging Face required port
EXPOSE 7860

# Run with Gunicorn (bind to 0.0.0.0:7860 for HF Spaces)
WORKDIR /app/backend
CMD ["gunicorn", "--bind", "0.0.0.0:7860", "--timeout", "120", "--log-level", "debug", "app:app"]