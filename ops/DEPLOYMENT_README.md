# Zimmer – Production Deployment (Docker Compose)

## Pre-reqs
- Docker & Docker Compose
- DNS set:
  - api.zimmerai.com → your server IP
  - panel.zimmerai.com → your server IP
  - dashboard.zimmerai.com → your server IP

## Build & Run
```bash
docker compose -f docker-compose.prod.yml build
docker compose -f docker-compose.prod.yml up -d
```
