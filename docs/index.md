# Grigory  
  
[![Django CI](https://github.com/Anttek-io/grigory/actions/workflows/django.yml/badge.svg)](https://github.com/Anttek-io/grigory/actions/workflows/django.yml)
[![Docker Image Version (latest semver)](https://img.shields.io/docker/v/harleyking/grigory?sort=semver)](https://hub.docker.com/r/harleyking/grigory)
[![Docker Image Size (latest semver)](https://img.shields.io/docker/image-size/harleyking/grigory?sort=semver)](https://hub.docker.com/r/harleyking/grigory)
[![Docker Pulls](https://img.shields.io/docker/pulls/harleyking/grigory)](https://hub.docker.com/r/harleyking/grigory)  
  
Grigory is just another messaging service. It's built on top of Django and Django Channels.  
It's designed to be used as a microservice in a microservice architecture, 
but can be used as a standalone service as well.  
It provides both REST API and WebSockets for clients and microservices.  
  
> If you find this project useful, please consider giving it a star.
  
## How it works
  
![screenshot](media/scheme.png)  
  
Any microservice or client just sends some message via REST API or WebSockets with the indication of the chat it belongs to.  
This message first goes to queue to avoid overloading the database.  
Then it's processed by the worker and saved to the database. If specified chat doesn't exist, it's created automatically.
After that, the message is sent to the chat via WebSockets.  
  
Message history can be retrieved via REST API or WebSockets.  
  
---
  
## Demo
  
You can try the demo at [https://grigory-demo.anttek.io/admin](https://grigory-demo.anttek.io/admin).  
  
> Demo admin user is `demo` and password is `demo-123`.  
  
API is available at [https://grigory-demo.anttek.io/api](https://grigory-demo.anttek.io/api).  
WebSockets are available at [wss://grigory-demo.anttek.io/ws](wss://grigory-demo.anttek.io/ws).  
  
---
  