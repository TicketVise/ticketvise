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

# Required SMTP client to start with HELO command and comply with the restrictions.
RUN postconf -e "smtpd_helo_required = yes"
RUN postconf -e "smtpd_helo_restrictions =\
                    permit_mynetworks\
                    permit_sasl_authenticated\
                    reject_invalid_helo_hostname\
                    reject_non_fqdn_helo_hostname\
                    reject_unknown_helo_hostname"

# This stops some techniques used to harvest email addresses.
RUN postconf -e "disable_vrfy_command = yes"

# SMTP restriction for antispam.
RUN postconf -e "smtpd_relay_restrictions = \
    permit_mynetworks, \
    permit_sasl_authenticated, \
    reject_unknown_sender_domain, \
    reject_unauth_destination"

RUN postconf -e "smtpd_recipient_restrictions = \
    permit_mynetworks, \
    reject_non_fqdn_helo_hostname, \
    reject_non_fqdn_sender, \
    reject_non_fqdn_recipient, \
    reject_unknown_reverse_client_hostname, \
    reject_invalid_helo_hostname, \
    reject_unknown_helo_hostname, \
    reject_unknown_sender_domain, \
    reject_unknown_recipient_domain, \
    reject_rbl_client cbl.abuseat.org, \
    reject_rbl_client sbl.spamhaus.org, \
    reject_rbl_client pbl.spamhaus.org, \
    permit"

RUN postconf -e "smtpd_data_restrictions = \
    reject_unauth_pipelining, \
    permit"

EXPOSE 25/tcp 465/tcp 587/tcp
CMD mkdir -p /var/spool/postfix/etc && cp /etc/resolv.conf /var/spool/postfix/etc/resolv.conf && postfix start-fg
