FROM python:3-slim

WORKDIR /app

# Install CloudFlare library.
# `cloudflare` on PyPI changed meaning at 3.0.0: the legacy python-cloudflare
# package (module CloudFlare, the one update_dns.py imports) only exists below
# 3.0.0, from 3.0.0 on the same name serves the new official SDK whose module
# is `cloudflare` (lowercase). Unpinned, the image builds fine and then dies at
# runtime with ModuleNotFoundError: No module named 'CloudFlare'.
# The import check makes that a build failure instead of a broken image.
RUN pip install --no-cache-dir 'cloudflare<3' dnspython \
 && python -c "import CloudFlare, dns.resolver"

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
