FROM python:3.9-slim

ENV PYTHONUNBUFFERED 1

# APT setup
RUN apt update && apt upgrade -y

# Copy project
RUN mkdir /backend
COPY ../backend /backend
COPY ../requirements.txt /backend/requirements.txt
WORKDIR /backend

# Install dependecies and collect static files
RUN python3 -m pip install -r requirements.txt
RUN python3 manage.py collectstatic --no-input

# Setup cronjob
RUN apt install cron -y
ADD crontab /etc/crontab
RUN chmod 0644 /etc/crontab
