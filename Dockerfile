FROM python:3.11-slim-bookworm

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

# do not include .env in gh Workflow
ARG ENVIRONMENT=normal
RUN if [ "${ENVIRONMENT}" != "github" ]; then \
    if [ -f .env ]; then cp.env /app/.env; \
    else echo ".env not found, skipping copy."; \
    fi; \
    fi

COPY . .