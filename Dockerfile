# syntax=docker/dockerfile:1
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

COPY requirements.txt ./
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

ARG PORT=64429
ENV PORT=${PORT}
EXPOSE ${PORT}

CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "${PORT}"]
