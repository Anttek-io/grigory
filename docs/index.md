# Grigory  

### Requirements
  
#### With Docker
  
- [Docker with Compose](https://docs.docker.com/compose/install/)

#### Without Docker
  
- [Python 3.9 or higher](https://www.python.org/downloads/)
- [PostgreSQL 12 or higher](https://www.postgresql.org/download/)
- [Redis](https://redis.io/download)
  
---  
  
### Quick start

First clone the repo

```bash
git clone https://github.com/Anttek-io/grigory.git
cd grigory
```

#### With Docker
  
Create `.env` file and put at least `DJANGO_WEB_PORT`  
```shell
DJANGO_WEB_PORT=8000
```

Run the app  
```bash
docker compose up -d
```

#### Without Docker
  
[Quick start without Docker](quickstart_no_docker.md)
  
---  
  
### Docker images
  
[DockerHub Page](https://hub.docker.com/r/harleyking/grigory)  
  
There are two versions of the image: base and `-oracle` version.  
Difference between them is that `-oracle` version includes [cx_Oracle](https://pypi.org/project/cx-Oracle/) 
and [Oracle Instant Client](https://www.oracle.com/database/technologies/instant-client/linux-x86-64-downloads.html) libraries.  
If you need to use Oracle database, you should use `-oracle` version.  
  