# Quickstart

## Requirements
  
### With Docker
  
- [Docker with Compose](https://docs.docker.com/compose/install/)
  
### Without Docker
  
- [Python 3.9 or higher](https://www.python.org/downloads/)
- [PostgreSQL 12 or higher](https://www.postgresql.org/download/)
- [Redis](https://redis.io/download)
  
---
  
## Installation
  
First clone the repo
  
```bash
git clone https://github.com/Anttek-io/grigory.git
cd grigory
```
  
### With Docker
  
Create `.env` file and put at least `DJANGO_WEB_PORT`  
```shell
DJANGO_WEB_PORT=8000
```
  
Run the app  
```bash
docker compose up -d
```
  
### Without Docker
  
Create virtual environment and install requirements:  
```bash
python3 -m venv venv
source venv/bin/activate # for *nix systems
venv\Scripts\activate # for Windows
pip install -r requirements.txt
```
  
Create `.env` file in the root directory.  
    
Add database and Redis connection URLs in the `.env` file:  
```bash
DATABASE_URL=postgres://user:password@host:port/db_name
REDIS_URL=redis://host:port
```
  
Run migrations:  
```bash
python manage.py migrate
```
  
Create superuser:  
```bash
python manage.py createsuperuser
```
  
Run server:  
```bash
gunicorn -w 1 --threads 1 --bind 127.0.0.1:8000
```
  
---
  