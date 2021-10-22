# Product Test & Reliability Analytics (PTERA) #

This service aims to make scheduling tasks/running tests on products easy and intuitive.

## Docker ##

A few applications make up the service and they are all launched/managed by docker; docker swarm/compose to be exact (running each application individually is not recommended). 

### Fluentd ###

Fluentd is used to collect logs from all running containers and store them in the specified data store (in this case we use Loki). This is important for monitoring the health of all running applications and alerting when necessary.


### Application (PTERA) ###

Using [tiangolo/uvicorn-gunicorn-fastapi](https://github.com/tiangolo/uvicorn-gunicorn-fastapi-docker) as the base image of choice for the python application as it is a production-ready image built specifically for fastapi.

> **Note**  
> The image consideration may change as the `tiangolo/uvicorn-gunicorn-fastapi` image is slightly over `Gb in size.