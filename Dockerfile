FROM python:3.7-slim

WORKDIR /app
COPY . /app

RUN apt-get update -y && apt-get install -y python-pip curl git
RUN pip install pipenv && pipenv install --deploy --system

