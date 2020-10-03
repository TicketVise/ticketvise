FROM debian:10

VOLUME ["/var/spool/postfix"]

RUN apt update && apt upgrade -y
RUN apt install postfix -y

COPY ./transport /etc/postfix/transport
RUN mkdir -p /var/spool/postfix/pid
RUN mkdir -p /var/spool/postfix/etc

# Disable local mail delivery
RUN postconf -e "mydestination="

# Log to stdout
RUN postconf -e "maillog_file=/dev/stdout"

# Redirect all email to web container
RUN postconf -e transport_maps="hash:/etc/postfix/transport" && postmap hash:/etc/postfix/transport

EXPOSE 25/tcp 465/tcp 587/tcp
CMD ["postfix", "start-fg"]
