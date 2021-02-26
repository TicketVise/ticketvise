FROM ticketvise/backend

# Setup cronjob
RUN apt install cron -y
ADD crontab /etc/crontab
RUN chmod 0644 /etc/crontab
