FROM python:3-slim

WORKDIR /app

# Install CloudFlare library
RUN pip install --no-cache-dir cloudflare dnspython

# Copy the script into the Docker image
COPY update_dns.py .

# Set environment variables
ENV CF_DNS_API_TOKEN=your_cloudflare_api_token
ENV DNS_SERVER=your_dns_server
ENV LOCAL_DOMAIN=your_local_domain
ENV REMOTE_DOMAIN=your_remote_domain
ENV REMOTE_SUBDOMAIN=your_remote_domain

COPY every /usr/bin/every
RUN chmod 755 /usr/bin/every

CMD ["every", "300s", "python", "./update_dns.py"]
