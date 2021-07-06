FROM alpine:3

# Transfer start up script
COPY docker-entrypoint.sh /

# Updating and installing packages
RUN apk update && apk upgrade
RUN apk add --no-cache bash postfix

# Allow receiving emails from subnet
RUN postconf -e "mynetworks_style = subnet"

# Log to stdout to show up in docker logs
RUN postconf -e "maillog_file = /dev/stdout"

# Disable local mail delivery for improved security
RUN postconf -e "mydestination ="
RUN postconf -e "local_recipient_maps ="
RUN postconf -e "local_transport = error:local mail delivery is disabled"

# Relay all incomming mail to web container (only allowing $relay_domains, set in start up script)
RUN postconf -e "relayhost = [web]:2525"

#RUN echo -e "* smtp:[web]:2525\n" > /etc/postfix/transport
#RUN postconf -e "transport_maps = lmdb:/etc/postfix/transport"
#RUN postconf -e "relay_recipient_maps ="
#RUN postmap lmdb:/etc/postfix/transport

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

EXPOSE 25 465 587
ENTRYPOINT ["/docker-entrypoint.sh"]
CMD ["postfix", "start-fg"]
