import dns.resolver
import CloudFlare
import socket
import sys
import os

def dns_query_specific_nameserver(query, nameserver='1.1.1.1', qtype='A'):
    resolver = dns.resolver.Resolver(configure=False)
    resolver.nameservers = [nameserver]
    answer = resolver.resolve(query, qtype)
    if len(answer) == 0:
        raise Exception(f'{query} can not be resolved from {nameserver}.')
    else:
        return str(answer[0])

local_ip = socket.gethostbyname(os.getenv('LOCAL_DOMAIN'))
if local_ip == dns_query_specific_nameserver(os.getenv('REMOTE_SUBDOMAIN'), nameserver=os.getenv('DNS_SERVER')):
    print(f'{os.getenv("REMOTE_SUBDOMAIN")}: {local_ip} is right.')
    sys.exit(0)

cf = CloudFlare.CloudFlare(token=os.getenv('CF_DNS_API_TOKEN'))

zones = cf.zones.get(params={'name': os.getenv('REMOTE_DOMAIN')})
zone_id = zones[0]['id']

dns_records = cf.zones.dns_records.get(zone_id, params={'name': os.getenv('REMOTE_SUBDOMAIN')})
dns_record_id = dns_records[0]['id']

data = {
    'type': 'A',
    'name': os.getenv('REMOTE_SUBDOMAIN'),
    'content': local_ip,
}

try:
    cf.zones.dns_records.put(zone_id, dns_record_id, data=data)
    print(f'DNS record updated successfully to {local_ip}.')
except CloudFlare.exceptions.CloudFlareAPIError as e:
    print(f'Failed to update DNS record. Error: {e}')
