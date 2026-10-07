FROM python:3-slim

WORKDIR /app

# Install the official Cloudflare SDK plus dnspython.
# `cloudflare` on PyPI means two different things: the maintained official SDK
# (module `cloudflare`, 3.0.0 and up) and the legacy python-cloudflare package
# (module `CloudFlare`, only below 3.0.0). update_dns.py uses the official SDK,
# so keep it inside the 5.x major and assert the import at build time: a wrong
# or renamed module must fail the build, not the running container.
RUN pip install --no-cache-dir 'cloudflare>=5,<6' dnspython \
 && python -c "import cloudflare, dns.resolver"

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
