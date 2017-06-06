# coding=utf-8
from .models import Proxy
from .checkip import CheckIp

import requests
import re

checkip = CheckIp()

def verify_all():
    ''' verify all proxies in the database

    if it is valid , this proxy's field 'Validate_time' will add 1,and
        field 'failed_time' will be reset to 0.
    or , its 'status' will be 'I' , 'failed_time' is about to add 1

    :return: None
    '''

    all_ip = Proxy.objects.all()
    valid_count = 0
    invalid_count = 0
    for ip in all_ip:
        proxy = {}
        is_https = False
        if ip.head.lower() == 'http,https':
            proxy['http'] = 'http://' + ip.ip + ':' + ip.port
            proxy['https'] = 'http://' + ip.ip + ':' + ip.port

        elif ip.head.lower() == 'https':
            proxy['https'] = 'http://' + ip.ip + ':' + ip.port
            is_https = True

        else:
            proxy['http'] = 'http://' + ip.ip + ':' + ip.port

        # 引入检查 IP 类
        if checkip.check(proxy, ip.type, is_https):
            ip.Validated_time += 1
            ip.status = 'V'
            ip.failed_time = 0
            valid_count += 1

        else:
            ip.status = 'I'
            ip.failed_time += 1
            invalid_count += 1

        ip.save()

    return valid_count, invalid_count


def verify():
    print('verifying')

    count = verify_all()

    print('verified all {0} proxies,valid proxies occupy {1} and invalid {2}'.format(count[0] + count[1], count[0],
                                                                                     count[1]))