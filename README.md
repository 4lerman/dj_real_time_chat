# Real-Time Chat Application

This is a real-time chat application built with Django, Django Channels, Celery, RabbitMQ, and PostgreSQL. The application allows users to send and receive messages in real-time.

## Table of Contents
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Running the Application](#running-the-application)
- [Environment Variables](#environment-variables)
- [License](#license)

## Features
- User authentication
- Friend request system
- Real-time messaging
- Celery task queue with RabbitMQ
- PostgreSQL database

## Prerequisites
- Docker and Docker Compose
- Python 3.8+
- PostgreSQL
- RabbitMQ

## Installation

1. **Clone the repository:**
    ```sh
    git clone https://github.com/yourusername/real-time-chat.git
    cd real-time-chat
    ```

2. **Create and activate a virtual environment:**
    ```sh
    python3 -m venv venv
    source venv/bin/activate
    ```

3. **Install the dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

4. **Create a `.env` file in the project root and add the following environment variables by looking at `.env.example` file.

## Running the Application

1. **Build and run Docker containers:**
    ```sh
    docker-compose up --build
    ```

2. **Apply database migrations:**
    ```sh
    docker-compose exec web python manage.py migrate
    ```

3. **Create a superuser:**
    ```sh
    docker-compose exec web python manage.py createsuperuser
    ```

4. **Access the application:**
    - Web application: `http://localhost:8000`
    - RabbitMQ management: `http://localhost:15672`

## Environment Variables

The application uses the following environment variables:

- `DB_NAME`: PostgreSQL database name
- `DB_USER`: PostgreSQL database user
- `DB_PASSWORD`: PostgreSQL database password
- `DB_HOST`: PostgreSQL database host (use `db` for Docker)
- `DB_PORT`: PostgreSQL database port (default is `5432`)
- `DJANGO_SECRET_KEY`: Django secret key
- `DJANGO_DEBUG`: Django debug mode (`True` or `False`)
- `REDIS_URL`: Redis URL (e.g., `redis://redis:6379/0`)
- `RABBITMQ_USER`: RabbitMQ user
- `RABBITMQ_PASSWORD`: RabbitMQ password
- `RABBITMQ_URL`: RabbitMQ URL (e.g., `amqp://user:password@rabbitmq:5672/`)


## License
This project is licensed under the MIT License. See the LICENSE file for details.

