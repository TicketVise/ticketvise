#!/bin/sh

postconf -e smtputf8_enable="no" \
  mynetworks="0.0.0.0/0" \
  inet_interfaces="all" \
  mydomain="$DOMAIN" \
  mynetworks="127.0.0.0/8, 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16"

exec "$@"