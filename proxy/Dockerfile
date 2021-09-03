FROM nginx:stable-alpine

RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.template /etc/nginx/conf.d
COPY compression.conf /etc/nginx
COPY cache.conf /etc/nginx
COPY docker-entrypoint.sh /
RUN chmod +x /docker-entrypoint.sh

ENTRYPOINT ["/docker-entrypoint.sh"]
CMD ["nginx", "-g", "daemon off;"]