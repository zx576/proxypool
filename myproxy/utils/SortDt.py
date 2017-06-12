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

def delete():
    all_ip = Proxy.objects.filter(failed_time__gte=5)
    all_ip.delete() 

    return len(all_ip)

def sort():
    print('deduplicaing proxies')
    deduplicate_count = deduplicate()
    delete_count = delete()
    print('deduplicated {0} items, delete {1} invalid ip .'.format(deduplicate_count, delete_count))

