#!/usr/bin/env sh
set -eu

envsubst '${NGINX_DOMAIN}' < /etc/nginx/conf.d/nginx.template > /etc/nginx/conf.d/nginx.conf

exec "$@"