FROM ubuntu:latest

RUN apt-get update && apt-get install -y nginx libnginx-mod-http-dav-ext apache2-utils && rm -rf /var/lib/apt/lists/*

COPY webdav.conf /etc/nginx/conf.d/default.conf

RUN rm /etc/nginx/sites-enabled/*

COPY entrypoint.sh /

ENTRYPOINT ["bash", "/entrypoint.sh"]
