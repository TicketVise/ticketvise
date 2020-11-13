FROM debian:10

VOLUME ["/var/spool/postfix"]

RUN apt update && apt upgrade -y
RUN apt install postfix -y postfix-pgsql

COPY docker-entrypoint.sh /docker-entrypoint.sh

RUN mkdir -p /var/spool/postfix/pid
RUN mkdir -p /var/spool/postfix/etc

# Disable local mail delivery
RUN postconf -e "mydestination="

# Log to stdout
RUN postconf -e "maillog_file=/dev/stdout"

# Configure Postfix to receive mail on all interfaces, which includes the internet
RUN postconf -e "inet_interfaces = all"
RUN postconf -e "mynetworks = 127.0.0.0/8, 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16"
RUN postconf -e "mydomain = ticketvise.com"

# Redirect all email to web container
RUN postconf -e "relayhost = web:2525"

EXPOSE 25/tcp 465/tcp 587/tcp
#ENTRYPOINT ["/docker-entrypoint.sh"]
CMD ["postfix", "start-fg"]
