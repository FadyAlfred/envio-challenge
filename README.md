Envio Challenge
---

### Introduction

Envio Challenge API is a simple project that have the following functionality:

  - User can add new reading 
  - User can aggregate readings and can filter it as well

### Technologies

Envio Challenge API uses a number of open source projects to work properly:

* [Python](https://www.python.org) - is a class-based, object-oriented programming language that is designed to have as few implementation dependencies as possible.
* [Pip](https://pypi.org/project/pip/) - is a package-management system written in Python used to install and manage software packages.
* [Django](https://www.djangoproject.com/) - Django is a Python-based free and open-source web framework that follows the model-template-views architectural pattern.
* [Restful APIs](https://restfulapi.net/) - is architectural style for distributed hypermedia systems.
* [Postgresql](https://www.postgresql.org/) -  is a powerful, open source object-relational database system.
* [Docker](https://www.docker.com/) - is a set of platform as a service (PaaS) products that use OS-level virtualization.
* [Docker Compose](https://docs.docker.com/compose/) - is a tool for running multi-container applications on Docker.
* [Swagger](https://swagger.io/) - Swagger is an Interface Description Language for describing RESTful APIs expressed using JSON.

### Install and run

```sh
$ cd /envio_challenge
$ docker-compose up
$ docker-compose exec server python manage.py makemigrations
$ docker-compose exec server python manage.py migrate

The app should be up and running on localhost:8000
```

### Run tests
```sh
$ docker-compose up
$ docker-compose exec server python manage.py test
```


### API documentation
```sh
Open http://127.0.0.1:8000/swagger/
For Redoc documentation use http://127.0.0.1:8000/redoc/
```


### TODOs
```
- Add Authentication to the APIs using API key.
- Add more test cases.
```