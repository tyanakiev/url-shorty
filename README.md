# 🚀 URL-Shorty

**URL-Shorty** is a scalable and modular URL shortener built with **FastAPI**, **async SQLAlchemy**, and **Redis**.  
It converts long URLs into compact short codes with caching, analytics, and expiration support — designed for performance, clean architecture, and cloud-readiness.

---

## 🧠 Features

- 🔗 Shorten long URLs into unique short codes  
- ⚡ Fast redirects powered by Redis caching  
- 📊 Track click counts and last access time  
- ⏳ Optional URL expiration support  
- 🧩 Modular and async architecture (FastAPI + SQLAlchemy + Redis)  
- 🐳 Docker Compose setup for local development  
- ☁️ Cloud-ready: can be deployed to GCP, AWS, or any container platform

---

## 🏗️ Architecture Overview

FastAPI (Async)  
│  
├── PostgreSQL  ← Persistent storage  
│  
├── Redis       ← Hot URL caching  
│  
└── Docker Compose orchestration  

<img width="1536" height="1024" alt="04c03c7f-cbb5-4023-a758-b119804c7896" src="https://github.com/user-attachments/assets/ec259989-5eeb-44ad-95d7-b9a8bdcec9d5" />


**Request Flow**
1. Client sends a long URL → `/api/shorten`  
2. The API generates a short code (Base62)  
3. The mapping is stored in PostgreSQL  
4. On redirect `/r/{short_code}`, FastAPI checks Redis cache → DB fallback  
5. Click count updated asynchronously

---

## ⚙️ Tech Stack

| Component | Technology                           |
|------------|--------------------------------------|
| API Framework | FastAPI                              |
| Database | PostgreSQL 16 (via SQLAlchemy Async) |
| Caching | Redis 7 (via redis-py asyncio)       |
| Containerization | Docker & Docker Compose              |
| Config | pydantic-settings                    |
| Language | Python 3.13                          |

---

## 🚀 Running Locally

### 1️⃣ Clone the repo
```
git clone https://github.com/<your-username>/url-shorty.git
cd url-shorty
```

### 2️⃣ Create `.env`
```
DATABASE_URL=postgresql+asyncpg://postgres:postgres@db:5432/url_shortener
REDIS_URL=redis://redis:6379
BASE_URL=http://localhost:8000
```

### 3️⃣ Start with Docker Compose
```
docker compose up --build
```

The app will be available at:  
http://localhost:8000/docs

---

## 🧩 Project Structure

```
url-shorty/
├── app/
│   ├── api/
│   │   ├── routes/
│   │   │   ├── shorten.py
│   │   │   └── redirect.py
│   ├── core/
│   │   ├── config.py
│   ├── db/
│   │   ├── models.py
│   │   ├── session.py
│   │   ├── init_db.py
│   ├── services/
│   │   ├── cache.py
│   │   └── shortener.py
│   ├── main.py
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── README.md
```

---

## 🧮 System Design Highlights

- **Async I/O:** Non-blocking DB and cache operations.  
- **Caching Layer:** Redis used for ultra-fast redirects.  
- **Persistence:** PostgreSQL stores all URLs and metadata.  
- **Scalability:** Stateless app layer, horizontally scalable.  
- **Extensibility:** Easy to add analytics, vanity URLs, or auth.  

---

## ☁️ Cloud Deployment (Optional)

While this repo runs locally via Docker, the same architecture can be deployed to:
- Google Cloud Run or AWS Fargate  
- Neon, Supabase, or PlanetScale for managed databases  
- Upstash Redis for managed caching  

Simply update your `.env` with the cloud connection strings — no code changes required.
