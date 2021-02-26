![Logo of TicketVise](backend/ticketvise/static/img/logo/banner.png)

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
NOTE: IPv6 has to be disabled, because Docker Swawrm does not support it.

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
