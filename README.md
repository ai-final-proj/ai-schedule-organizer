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


```shell
docker build -t ai_schedule_organizer:latest .
docker run -d --name ai_schedule_container -p 7860:7860 ai_schedule_organizer:latest
```
