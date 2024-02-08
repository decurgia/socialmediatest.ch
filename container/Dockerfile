FROM python:3.12.2-alpine

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=8000

RUN apk add --no-cache git
COPY ./app /app/

WORKDIR /app/
RUN pip install --root-user-action=ignore --upgrade pip
RUN pip install --root-user-action=ignore --upgrade --no-cache-dir --requirement requirements.txt --disable-pip-version-check

CMD ["gunicorn", "-w", "4", "socialmediatest:create_app()"]