
Create virtual environment and install requirements  
```bash
python3 -m venv venv
source venv/bin/activate # for *nix systems
venv\Scripts\activate # for Windows
pip install -r requirements.txt
```
  
Add database and Redis to your `.env` file  
```bash
DATABASE_URL=postgres://user:password@host:port/db_name
REDIS_URL=redis://host:port
```
  
Run migrations  
```bash
python manage.py migrate
```
  
Create superuser
```bash
python manage.py createsuperuser
```
  
Run server  
```bash
gunicorn -w 1 --threads 1 --bind 127.0.0.1:8000
```