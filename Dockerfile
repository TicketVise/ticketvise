FROM python:3.8

ENV PYTHONUNBUFFERED 1

# Copy project
RUN mkdir /backend
COPY ./backend /backend
COPY ./requirements.txt /backend/requirements.txt
WORKDIR /backend

# Install dependecies
RUN python3 -m pip install -r requirements.txt

EXPOSE 8000
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]

