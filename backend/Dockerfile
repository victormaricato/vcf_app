FROM python:3.9-slim

WORKDIR /app

RUN apt-get update
RUN apt-get install -y python3-dev build-essential

COPY backend/requirements.txt /requirements.txt
RUN pip install -r /requirements.txt && rm /requirements.txt
