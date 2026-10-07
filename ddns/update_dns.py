"""Keep the Cloudflare A record for REMOTE_SUBDOMAIN pointed at this host.

Runs on a loop inside the container (see CMD in the Dockerfile).
"""

import os
import socket
import sys

import cloudflare
import dns.resolver


def dns_query_specific_nameserver(query, nameserver='1.1.1.1', qtype='A'):
    resolver = dns.resolver.Resolver(configure=False)
    resolver.nameservers = [nameserver]
    answer = resolver.resolve(query, qtype)
    if len(answer) == 0:
        raise Exception(f'{query} can not be resolved from {nameserver}.')
    else:
        return str(answer[0])


def main():
    local_domain = os.getenv('LOCAL_DOMAIN')
    remote_domain = os.getenv('REMOTE_DOMAIN')
    remote_subdomain = os.getenv('REMOTE_SUBDOMAIN')
    dns_server = os.getenv('DNS_SERVER')

    local_ip = socket.gethostbyname(local_domain)
    current_ip = dns_query_specific_nameserver(remote_subdomain, nameserver=dns_server)
    if local_ip == current_ip:
        print(f'{remote_subdomain}: {local_ip} is right.')
        return 0

    client = cloudflare.Cloudflare(api_token=os.getenv('CF_DNS_API_TOKEN'))

    zones = client.zones.list(name=remote_domain).result
    if not zones:
        print(f'No Cloudflare zone found for {remote_domain}.', file=sys.stderr)
        return 1
    zone = zones[0]

    records = client.dns.records.list(zone_id=zone.id, name=remote_subdomain, type='A').result
    if not records:
        print(f'No A record named {remote_subdomain} in zone {remote_domain}.', file=sys.stderr)
        return 1
    record = records[0]

    # edit() is a PATCH: only the fields passed here are sent, so settings such as
    # proxied/comment/tags survive. update() would overwrite the whole record, and
    # the legacy script's PUT had the same problem. The SDK requires name/ttl/type
    # for an A record even on PATCH, hence echoing the values already on the record.
    client.dns.records.edit(
        dns_record_id=record.id,
        zone_id=zone.id,
        type='A',
        name=record.name,
        ttl=record.ttl,
        content=local_ip,
    )
    print(f'DNS record {remote_subdomain} updated: {current_ip} -> {local_ip}.')
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except cloudflare.CloudflareError as error:
        print(f'Cloudflare API error: {error}', file=sys.stderr)
        sys.exit(1)
