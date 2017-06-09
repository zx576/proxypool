from ..models import Proxy


def deduplicate():

    all_ip = Proxy.objects.filter(status='V')
    list_ip = []
    count = 0
    for ip in all_ip:
        if ip.ip in list_ip:
            count += 1
            ip.delete()
        list_ip.append(ip.ip)

    return count


def sort():
    print('deduplicaing proxies')
    deduplicate_count = deduplicate()
    print('deduplicated {0} items'.format(deduplicate_count))

