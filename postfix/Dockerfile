FROM debian:10

VOLUME ["/var/spool/postfix"]

RUN apt update && apt upgrade -y
RUN apt install postfix -y postfix-pgsql

COPY transport /etc/postfix/transport

RUN mkdir -p /var/spool/postfix/pid
RUN mkdir -p /var/spool/postfix/etc

# Basic config
RUN postconf -e "myhostname = mail.ticketvise.com"
RUN postconf -e "myorigin = ticketvise.com"
RUN postconf -e "inet_protocols = ipv4"

# Log to stdout
RUN postconf -e "maillog_file=/dev/stdout"

# Disable local mail delivery
RUN postconf -e "mydestination ="
RUN postconf -e "local_recipient_maps ="
RUN postconf -e "local_transport = error:local mail delivery is disabled"

# Relay all incomming mail to web container
RUN postconf -e "relay_domains = ticketvise.com"
RUN postconf -e "transport_maps = hash:/etc/postfix/transport"
RUN postconf -e "relay_recipient_maps ="

RUN postmap hash:/etc/postfix/transport

EXPOSE 25/tcp 465/tcp 587/tcp
CMD mkdir -p /var/spool/postfix/etc && cp /etc/resolv.conf /var/spool/postfix/etc/resolv.conf && postfix start-fg
