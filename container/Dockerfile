# syntax=docker/dockerfile:1
FROM python:3.12.0-alpine

ARG REQUIREMENTS=requirements-dev.txt
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apk add --no-cache git
COPY requirements.txt requirements-dev.txt /app/

WORKDIR /app/
RUN pip install --root-user-action=ignore --upgrade pip
RUN pip install --root-user-action=ignore --upgrade --no-cache-dir --requirement $REQUIREMENTS --disable-pip-version-check

COPY ./app /app/
WORKDIR /app/socialmediacert/

CMD ["python", "manage.py", "runserver"]