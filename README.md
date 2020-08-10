<div align="center">
![Logo of TicketVise](https://i.imgur.com/WJ7aHsH.png)
</div>

## Table of contents
1. [Introduction](#Introduction)
2. [How to get TicketVise running on Ubuntu 20.04](#How-to-get-TicketVise-running-on-Ubuntu-20.04)
    1. [Prerequisites](#Prerequisites)
       1. [Docker](#Docker)
       2. [Docker Compose](#Docker-Compose)
    2. [Setup guide](#Setup-guide)
    3. [Running TicketVise](#Running-TicketVise)
    4. [Stopping TicketVise](#Stopping-TicketVise)
3. [Documentation](#Documentation)
4. [The software license](#The-software-license)

## Introduction
TicketVise is a ticket system that makes answering questions from students easier than ever before.
The currently used mailing list has many flaws, such as confusion about who will answer what.
In addition to that questions are often forgotten and there is a need for a second communication
channel for discussion amongst assistants. TicketVise solves this as it forms a central place for
students to ask questions via tickets, which can be assigned to assistants both automatically
and manually to give more clarity about who answers what. The built-in Canvas integration in
combination with a private discussion section for the teaching team gets rid of coordination
overhead as no second communication channel is required (e.g. Slack or Telegram). TicketVise comes
with many more features, such as a notification system, course/user statistics and markdown support.

## How to get TicketVise running on Ubuntu 20.04
### Prerequisites

#### Docker
The application is run within Docker to ensure it runs the same on every system. We have a
Dockerfile in the root of the project that will create an image for our Django application.
To install Docker, please refer to the [following article](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-20-04) or use the the commands below.

To add the repository with the latest version of Docker run:
```sh
sudo apt install apt-transport-https ca-certificates curl software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu focal stable"
sudo apt update
```

To install the community edition of Docker run:
```sh
sudo apt install docker-ce
```

To add yourself to the Docker group to use Docker without sudo run:
```sh
sudo usermod -aG docker ${USER}
su - ${USER}
```

#### Docker Compose
We use Docker-Compose to make managing all the required containers easier. It can be used
to create a yaml file with all the mounts, ports and parameters. The easiest way to install
this is to use the default package manager of Ubuntu.

To install Docker-Compose run:
```sh
sudo apt install docker-compose
```

### Setup guide
To use TicketVise, a database must be created with the right schemes. This can be done automatically
with our Makefile. We also supply a Python file to seed the database with some default data to give
the users an impression of the product. This step should only be run once.

To setup run:
```sh
make setup
```

### Running TicketVise
To start the application and thus the Docker containers run:
```sh
make start
```

The server will now listen to new connections on [localhost:8000](localhost:8000).

### Stopping TicketVise
To stop the applications and thus the Docker containers run:
```sh
make stop
```

## Documentation
A considerate amount effort has been put into ensuring the documentation of TicketVise is up to
date. Documentation for the Python code can be found on our [docs](https://docs.ticketvise.app/) page. The Javascript
functions and HTML markup have also been documented, but this is only visible in the source code available
on Gitlab.

## Deployment
### Generate SSL certificates
```shell script
docker run -it --rm --name certbot -p 80:80 \
          -v "ticketvise_cert_conf:/etc/letsencrypt" \
          -v "ticketvise_cert_www:/var/www/certbot" \
          certbot/certbot certonly \
          --standalone \
          -w /var/www/certbot \
          --email <EMAIL> \
          -d <DOMAIN>
```
### Deploy to Docker Stack
```shell script
docker stack deploy -c docker-compose.yml -c docker-compose.prod.yml ticketvise
```

## Troubleshooting
#### Cronjobs

Access the docker container running the backend image. You can find the container id by running `docker ps`.
```shell script
docker exec -it <backend_container_id> bash
```

View the cronjob logs.
```shell script
cat /var/log/cron.log
```