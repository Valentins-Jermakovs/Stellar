<div align="center">

![Stellar](./banner.png)

# Stellar

**REST API for creating and managing resumes, with PDF export using customizable templates.**

[![Python](https://img.shields.io/badge/Python-3.14-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![SQLModel](https://img.shields.io/badge/SQLModel-e92063?style=flat-square)](https://sqlmodel.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-18-4169E1?style=flat-square&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Redis](https://img.shields.io/badge/Redis-8-DC382D?style=flat-square&logo=redis&logoColor=white)](https://redis.io/)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?style=flat-square&logo=docker&logoColor=white)](https://www.docker.com/)
[![JWT](https://img.shields.io/badge/Auth-JWT-000000?style=flat-square&logo=jsonwebtokens&logoColor=white)](https://jwt.io/)

</div>

## Description

Stellar is a FastAPI service for creating and managing resumes, including personal information,
work experience, education, skills, languages, projects, and certifications. It supports
JWT authentication and PDF generation with six templates and English, Russian, and Latvian.

## Technology stack

Python 3.14 · FastAPI · SQLModel · PostgreSQL 18 · Redis 8 · JWT · WeasyPrint · Docker Compose

## Run with Docker Compose

Create `.env` from the provided example and set your own secure values for
`POSTGRES_PASSWORD` and `JWT_SECRET_KEY`:

```bash
cp .env.example .env
```

If it does not already exist, create the external Docker network required by Compose, then start:

```bash
docker network create back_end
docker compose up --build -d
```

The API and interactive documentation are available at [localhost:8001](http://localhost:8001)
and [localhost:8001/docs](http://localhost:8001/docs). PostgreSQL is exposed on port `5440`;
Redis is exposed on port `6380`.

## Database schema

![Stellar database schema](./erd1.png)
