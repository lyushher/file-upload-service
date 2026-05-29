# Secure File Upload & Presigned URL API


![Python](https://img.shields.io/badge/python-3.11-blue)
![Docker](https://img.shields.io/badge/docker-ready-blue)
![License](https://img.shields.io/badge/License-Apache%202.0-green.svg)
![Contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg)


This project provides a scalable backend service for securely uploading files using **presigned URLs** to AWS S3, backed by a PostgreSQL database and built with FastAPI. 

It is designed with clean architecture, production-readiness, and developer ergonomics in mind—ideal for real-world SaaS, internal tools, and cloud-native deployments.
The service is containerized using Docker and supports environment-based configuration for seamless deployment.

## 📌 Project Objectives

- Enable **secure and efficient file uploads** to AWS S3 without exposing backend credentials.
- Provide **presigned URL generation** for direct browser uploads (PUT) and downloads (GET).
- Store metadata about uploaded files in a **PostgreSQL database**.
- Ensure clean **separation of concerns** between API layer, service logic, and database models.
- Allow **environment-based configuration** for deployment across different environments (local, staging, production).
- Versioned schema migrations powered by **Alembic** for consistent database evolution.
- Ensure reproducible deployment across environments using **Docker** and **Docker Compose**.

---

## Tech Stack

| Layer           | Technology                          |
|----------------|--------------------------------------|
| Framework       | [FastAPI](https://fastapi.tiangolo.com/) |
| Cloud Storage   | [AWS S3](https://aws.amazon.com/s3/)       |
| Database        | PostgreSQL + SQLAlchemy             |
| Migrations      | Alembic                             |
| Environment     | pydantic-settings + `.env` file     |
| Containerization| Docker & docker-compose             |
| Presigned URLs  | Boto3 (`put_object`, `get_object`)  |

---

## Directory Structure

```
file-upload-service/
│
├── app/
│   ├── main.py                  # FastAPI entrypoint
│   ├── init_db.py               # Script to initialize DB tables
│   ├── core/
│   │   ├── database.py          # SQLAlchemy engine, session, Base
│   │   ├── settings.example.py  # Sample environment config
│   │   └── validators.py        # Pydantic field-level validators
│   └── services/
│       └── s3.py                # S3 utils: presigned URLs, path logic
│
├── migrations/                  # Alembic migrations folder
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md 
```

---

## Features

- Generate presigned PUT/GET URLs with content-type control
- Enforce allowed MIME types via Pydantic
- Use UUID and date-based pathing for S3 object keys
- Secure `.env`-based configuration (hidden via `.gitignore`)
- Database metadata persistence (optional extension)
- Dockerized environment for dev and prod parity
- Alembic-powered versioned migrations

---

## ⚙️ Environment Configuration

Create a `.env` file in the project root (ignored by Git):

```bash
# .env (Not committed to Git)
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
AWS_REGION=eu-central-1
S3_BUCKET=my-upload-bucket

POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=file_upload_service
POSTGRES_HOST=db
POSTGRES_PORT=5432

ALLOWED_ORIGINS=http://localhost:3000
MAX_UPLOAD_MB=25
```

You can find a sample at:
```txt
app/core/settings.example.py
```

## Running with Docker

1. Build and Start Containers

```bash
docker-compose up --build
```

2. Access the API Docs

Once running, go to:

```bash
http://localhost:8000/docs
```

to access the interactive Swagger UI provided by FastAPI.

---

## API Endpoints
| Method | Endpoint              | Description                |
|--------|-----------------------|----------------------------|
| GET    | /health               | Basic health check         |
| POST   | /presign/upload       | Generate presigned PUT URL |
| GET    | /presign/download/{key} | Generate presigned GET URL  |

Each endpoint validates file types and request payload using [Pydantic](https://docs.pydantic.dev/latest/) schemas.

Example Request (Presigned Upload)
```http
POST /presign/upload
Content-Type: application/json
```
```json
{
  "filename": "document.pdf",
  "content_type": "application/pdf"
}
```
Example Response:
```json
{
  "url": "https://your-bucket.s3.amazonaws.com/2025/08/14/uuid-filename.pdf",
  "key": "2025/08/14/uuid-filename.pdf"
}
```
Security Note: 
> **Ensure that only validated content types are accepted** to avoid uploading malicious files.

---

## Alembic Migrations

Initialize and apply migrations:

```bash
alembic init migrations
alembic revision --autogenerate -m "Initial schema"
alembic upgrade head
```

Migrations are tracked in the `migrations/versions/` folder.


## Security Notes

- No AWS credentials are ever exposed to the client.
- Only allowed MIME types can be uploaded.
- File names are sanitized to remove dangerous characters.
- Large files are capped via environment-configured byte limit.
- Only presigned requests can access/upload files.


## Checklist for Production

- Do not commit .env — only settings.example.py
- Set DEBUG=False in production
- Secure AWS permissions via least-privilege IAM role
- Use HTTPS-only endpoints in production

## ⚠️ Disclaimer

> **Note:** This project is a public showcase of the overall architecture, structure, and functionality of a secure file upload backend.
The actual production implementation, including critical components, secrets, and internal logic, is private and maintained in a separate repository.

- All credentials and sensitive configurations are omitted or replaced with mock values.
- Any resemblance to production behavior is for demonstration purposes only.
- This repository is not intended for direct deployment in production environments without further security validation.

## License

This project is licensed under the **Apache License 2.0**.  
You may use, modify, and distribute it in accordance with the terms of the license.

See the full [LICENSE](./LICENSE) file for details.
