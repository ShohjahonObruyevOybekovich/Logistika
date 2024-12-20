FROM python:3.11-slim-bullseye


WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY r.txt .

RUN pip install -r r.txt


COPY . .