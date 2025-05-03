FROM python:3.12-slim AS base

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app/ .
COPY assets/ ./assets
COPY images/ ./images

CMD ["python", "bot.py"]
