FROM debian:10

VOLUME ["/var/spool/postfix"]

RUN apt update && apt upgrade -y
RUN apt install postfix -y postfix-pgsql

COPY ./transport /etc/postfix/transport
COPY ./postgres-virtual-mailbox-domains.cf /etc/postfix/postgres-virtual-mailbox-domains.cf
COPY ./postgres-virtual-mailbox-maps.cf /etc/postfix/postgres-virtual-mailbox-maps.cf

RUN mkdir -p /var/spool/postfix/pid
RUN mkdir -p /var/spool/postfix/etc

# Disable local mail delivery
RUN postconf -e "mydestination="

# Log to stdout
RUN postconf -e "maillog_file=/dev/stdout"

# Configure Postfix to receive mail on all interfaces, which includes the internet
RUN postconf -e "inet_interfaces = all"

# Setup mapping (to validate incomming emails)
RUN postconf -e "virtual_mailbox_domains=pgsql:/etc/postfix/postgres-virtual-mailbox-domains.cf"
RUN postconf -e "virtual_mailbox_maps=pgsql:/etc/postfix/postgres-virtual-mailbox-maps.cf"

# Redirect all email to web container
RUN postconf -e transport_maps="hash:/etc/postfix/transport" && postmap hash:/etc/postfix/transport

EXPOSE 25/tcp 465/tcp 587/tcp
CMD ["postfix", "start-fg"]
