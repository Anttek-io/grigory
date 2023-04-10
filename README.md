# Grigory  
  
[![Django CI](https://github.com/Anttek-io/grigory/actions/workflows/django.yml/badge.svg)](https://github.com/Anttek-io/grigory/actions/workflows/django.yml)
[![Docker Image Version (latest semver)](https://img.shields.io/docker/v/harleyking/grigory?sort=semver)](https://hub.docker.com/r/harleyking/grigory)
[![Docker Image Size (latest semver)](https://img.shields.io/docker/image-size/harleyking/grigory?sort=semver)](https://hub.docker.com/r/harleyking/grigory)
[![Docker Pulls](https://img.shields.io/docker/pulls/harleyking/grigory)](https://hub.docker.com/r/harleyking/grigory)  
  
> Grigory is backend for notification service, real-time chats and microservices communication.  
You don't need to implement all the logic for chats and notifications from scratch.  
For example, you can just run Grigory and use it as backend for your chat and notifications.  
It's built on top of Django and Django Channels.  
It's designed to be used as a microservice in a microservice architecture, 
but can be used as a standalone service as well.  
It provides both REST API and WebSockets for clients and microservices.  
  
## Who was this project made for?
  
Everybody who wants to implement chat and notifications in their project.  
For example, frontend developers who needs chat and/or notifications functionality.  
Or backend developers who need to implement chat and notifications in their project.
> If you're main backend is made on Django, you can use Grigory as a part of your microservice architecture.  
> Just add `AUTH_DB_URL` environment variable that points to your main Django database.  
> After that Grigory will use your main Django database for authentication.
  
> #### If you find this project useful, please consider giving it a star.  
  
---
  
## How it works
  
![screenshot](docs/media/scheme.png)  
  
1. Any microservice or client just sends some message via REST API or WebSockets 
with the indication of the chat it belongs to.
If specified chat doesn't exist, it's created automatically.
2. This message first goes to queue to avoid overloading the database.  
3. Then it's processed by the worker and saved to the database.  
4. After that, the message is sent to real-time chat via WebSockets.

Message history can be retrieved via REST API or WebSockets.  
  
### Demo
  
You can try the demo at [https://grigory-demo.anttek.io/admin](https://grigory-demo.anttek.io/admin).  
  
> Demo admin user is `demo` and password is `demo-123`.  
  
API is available at [https://grigory-demo.anttek.io/api](https://grigory-demo.anttek.io/api).  
WebSockets are available at [wss://grigory-demo.anttek.io/ws](wss://grigory-demo.anttek.io/ws).  
  
---
  
## Features implemented

- [x] Expiring Token authentication
- [x] WebSockets with Token authentication
- [x] Microservice architecture-ready (with [DJ-MS Auth Router](https://github.com/dj-ms/dj-ms-auth-router))
- [x] REST API both for clients and for microservices


## Features to be implemented

- [ ] Chat management
- [ ] Using system events as messages in chats
- [ ] Marking messages as read by concrete user
  
---
  
## Quick start
  
First clone the repo
  
```bash
git clone https://github.com/Anttek-io/grigory.git
cd grigory
```
  
Create `.env` file and put at least `DJANGO_WEB_PORT`  
```shell
DJANGO_WEB_PORT=8000
```
  
Run the app  
```bash
docker compose up -d
```
  
> If you'd like to run Grigory without Docker, read [docs](https://anttek-io.github.io/grigory/).
  
---
  
## Postman workspace

There's public Postman workspace with all the requests and collections.
You can import it to your Postman and start testing the API right away.
  
[![View in Postman](https://run.pstmn.io/button.svg)](https://www.postman.com/anttek-io/workspace/grigory)
  
---
  