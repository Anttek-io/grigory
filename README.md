# Grigory

Grigory is just another messaging service. It's built on top of Django and Django Channels.  
It's designed to be used as a microservice in a microservice architecture, 
but can be used as a standalone service as well.  
It provides both REST API and WebSockets for clients and microservices.  

![screenshot](docs/media/scheme.png)

### How it works

Any microservice or client just sends some message via REST API or WebSockets with the indication of the chat it belongs to.  
This message first goes to queue to avoid overloading the database.  
Then it's processed by the worker and saved to the database. If specified chat doesn't exist, it's created automatically.
After that, the message is sent to the chat via WebSockets.  

Message history can be retrieved via REST API or WebSockets.  
  
#### Demo
  
You can try the demo at [https://grigory-demo.anttek.io/admin](https://grigory-demo.anttek.io/admin).  
  
Admin user is `demo` and password is `demo-123`.  
  
API is available at [https://grigory-demo.anttek.io/api](https://grigory-demo.anttek.io/api).  
WebSockets are available at [wss://grigory-demo.anttek.io/ws](wss://grigory-demo.anttek.io/ws).  
  
---  
  
### Features implemented

- [x] Expiring Token authentication
- [x] WebSockets with Token authentication
- [x] Microservice architecture-ready (with [DJ-MS Auth Router](https://github.com/dj-ms/dj-ms-auth-router))
- [x] REST API both for clients and for microservices


### Features to be implemented

- [ ] Chat management
- [ ] Using system events as messages in chats
- [ ] Marking messages as read by concrete user


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
  
[Quick start without Docker](docs/RUN_LOCALLY_WITHOUT_DOCKER.md)
  
---  
  
## Postman workspace

There's public Postman workspace with all the requests and collections.
You can import it to your Postman and start testing the API right away.
  
[![View in Postman](https://run.pstmn.io/button.svg)](https://www.postman.com/anttek-io/workspace/grigory)
