
# ==============================
# Base Image
# ==============================

FROM python:3.14-slim


# ==============================
# Environment Configuration
# ==============================

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/project/app


# ==============================
# Working Directory
# ==============================

WORKDIR /project


# ==============================
# System Dependencies
# ==============================

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpango-1.0-0 \
    libharfbuzz0b \
    libpangoft2-1.0-0 \
    libharfbuzz-subset0 \
    && rm -rf /var/lib/apt/lists/*


# ==============================
# Python Dependencies
# ==============================

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt


# ==============================
# Application User
# ==============================

RUN groupadd --system app \
    && useradd --system \
        --gid app \
        --home-dir /home/app \
        --create-home \
        --shell /usr/sbin/nologin \
        app


# ==============================
# Application Files
# ==============================

COPY app ./app

RUN chmod -R a+rX /project/app


# ==============================
# Application Port
# ==============================

EXPOSE 8001


# ==============================
# Runtime User
# ==============================

USER app


# ==============================
# Application Startup
# ==============================

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]
