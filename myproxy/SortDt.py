
from .models import Proxy


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


def delete_invalid():

    invalid_ip = Proxy.objects.filter(failed_time__gte=5)
    count = len(invalid_ip)
    invalid_ip.delete()
    return count

def sort():
    print('deduplicaing and delete invalid proxies')

    deduplicate_count = deduplicate()
    invalid_count = delete_invalid()

    print('deduplicated {0} items'.format(deduplicate_count))
    print('delete {0} proxies which failed_times exceed 5'.format(invalid_count))

