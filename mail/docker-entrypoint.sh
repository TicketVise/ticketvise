#!/bin/sh

set -e

postconf -e "myhostname = ${HOST:=mail.ticketvise}"
postconf -e "myorigin = ${DOMAIN:=ticketvise}"
postconf -e "relay_domains = ${DOMAIN:=ticketvise}"
