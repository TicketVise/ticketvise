#!/bin/sh

set -e

postconf -e 'myhostname = ${HOST}'
postconf -e 'myorigin = ${DOMAIN}'
postconf -e 'relay_domains = ${DOMAIN}'

exec "$@"
