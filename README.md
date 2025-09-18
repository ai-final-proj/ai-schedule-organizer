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

Flask backend + Angular frontend served via Gunicorn inside Docker.


 - Ensure frontend/dist exists and is up to date:
```shell
cd frontend && npm install && npm run build
```
 (on host, not in Docker)
  - Build the image skipping the frontend step:
```shell
cd ..
docker rm -f ai_schedule_container 2>/dev/null || true
docker build -t hf_organizer . --build-arg SKIP_FRONTEND_BUILD=true
```
Then Run:

```shell
docker run -d --name ai_schedule_container \
  -p 7860:7860 \
  -e DATABASE_URL="postgresql+psycopg://postgres:postgres@host.docker.internal:5432/ai_schedule_organizer" \
  -e SECRET_KEY=dev \
  -e PORT=7860 \
  -v "$(pwd)/frontend/dist/ai-schedule-organizer-angular:/app/frontend/dist/ai-schedule-organizer-angular:ro" \
  hf_organizer:latest
```
