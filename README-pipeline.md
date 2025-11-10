# Pipeline & Networking — Quick Start

This repository now supports ingestion pipelines (RSS, API, webhooks) and can access the Internet to fetch and ingest data.

Local quick start (Docker Compose)
1. Copy `.env.example` to `.env` and tweak variables.
2. Build + start:
   docker-compose up --build -d
3. The API will be available at http://localhost:8000.
4. Trigger an RSS ingestion:
   curl -X POST http://localhost:8000/ingest -H "Content-Type: application/json" -d '{"source_type":"rss","source":"https://example.com/feed"}'

Notes on connectivity
- Outbound HTTP(S) access: the container will use host network routing; ensure firewall/NAT allows outbound traffic.
- For public access (mobile apps), expose the server via a public IP/hostname and use HTTPS. For quick testing, use ngrok: ngrok http 8000

Security & production checklist
- Add authentication (API key / OAuth) to /predict, /ingest and webhook endpoints.
- Use HTTPS and a reverse proxy (nginx) with TLS termination.
- Rate-limit ingestion and inference requests.
- Move long-running ingestion to a reliable worker (Celery + Redis/RabbitMQ) for production.
