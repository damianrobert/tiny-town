# TinyTown 🏙️ — Beginner DevOps Containerized Web App (Ubuntu + Docker + Nginx)

TinyTown is a small containerized web app designed as a **beginner-friendly DevOps learning project**.

The goal is not to build a feature-rich app — the goal is to learn how to **deploy**, **operate**, **secure**, and later **scale** a service like a real production system (but in a homelab-friendly way).

---

## What this project demonstrates

### ✅ Phase 1 — Containerized deployment on Ubuntu Server
- FastAPI web app running in Docker
- PostgreSQL database running in Docker
- Docker Compose orchestrates both services
- Persistent storage via Docker volume (`pgdata`)

### ✅ Phase 1.5 — Configuration hygiene (secrets out of code)
- Database credentials moved into a `.env` file
- `.env` excluded from git via `.gitignore`
- App fails fast if required environment variables are missing (no unsafe defaults)

### ✅ Phase 2 — Reverse proxy front door
- Host Nginx reverse proxies to the app container
- App is bound to localhost only (`127.0.0.1:8000`) so it’s not directly exposed on LAN
- HTTPS enabled using a self-signed certificate (good for homelab learning)

### ✅ Phase 2.5 — Basic traffic protection + hardening
- Nginx rate limiting for normal endpoints
- Separate generous rate limiting for `/health` to avoid throttling monitoring
- Connection limits and basic proxy hardening headers

---

## Architecture (mental model)

Think of this like a nightclub:

- **App container** = the band on stage (private backstage)
- **Postgres container** = the power supply behind the scenes
- **Docker network** = hallway behind the curtain
- **Nginx** = the bouncer at the front door (TLS + routing + limits)
- **Health checks** = staff making sure the band is still alive


Client (LAN / local)
|
HTTPS :443
|
Host Nginx (Reverse Proxy, Rate Limit)
|
Docker: tiny-town-app ---> Docker network ---> tiny-town-db (Postgres)


---

## Endpoints

- `GET /` → hello message
- `GET /health` → health check (always returns ok if app is alive)
- `GET /db` → connectivity check to Postgres (`SELECT 1`)

---

## Repo structure


tinytown/
├─ app/
│ ├─ main.py
│ ├─ requirements.txt
│ └─ Dockerfile
├─ docker-compose.yml
├─ .env # not committed
├─ .env.example # safe template
└─ README.md




---

## Requirements

### Ubuntu Server
- Docker Engine
- Docker Compose plugin

### Host services (Phase 2)
- Nginx installed on Ubuntu host
- Port 80/443 open (UFW if enabled)

---

## Setup & Run (Docker Compose)

### 1) Create your `.env` (from example)

```bash
cp .env.example .env
nano .env

Build and run containers

```bash
docker compose up -d --build
docker compose ps

Test locally


```bash
curl http://localhost:8000/health
curl http://localhost:8000/db
