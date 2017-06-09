# coding=utf-8
from ..models import Proxy
from .checkip import CheckIp

import requests
import re

checkip = CheckIp()

def verify_all():
    ''' verify all proxies which failed_time less than or equals 5 times in the database

    if it is valid , this proxy's field 'Validate_time' will add 1,and
        field 'failed_time' will be reset to 0.
    or , its 'status' will be 'I' , 'failed_time' is about to add 1

    :return: None
    '''

    all_ip = Proxy.objects.filter(failed_time__lte=5).order_by('last_modified_time')

    count = len(all_ip)
    per_hour = count // 24 + 1
    choosed_ip = all_ip[:per_hour]

    valid_count = 0
    invalid_count = 0

    for ip in choosed_ip:
        proxy = {}
        is_https = False
        if ip.head.lower() == 'http,https':
            verify_head(ip)

        elif ip.head.lower() == 'https':
            proxy['https'] = ip.ip + ':' + ip.port
            is_https = True

        else:
            proxy['http'] = ip.ip + ':' + ip.port

        # 引入检查 IP 类
        if checkip.check(proxy, ip.type, is_https):

            ip.Validated_time += 1
            ip.status = 'V'
            ip.failed_time = 0
            valid_count += 1

        else:
            ip.Validated_time = 0
            ip.status = 'I'
            ip.failed_time += 1
            invalid_count += 1

        ip.save()

    return valid_count, invalid_count


def verify_head(ip):

    http_head = {}
    https_head = {}
    count = 0
    http_head['http'] = ip.ip + ':' + ip.port
    https_head['https'] = ip.ip + ':' + ip.port

    res = []

    #  验证两种情况
    if checkip.check(http_head, ip.type):
        res.append(1)

    if checkip.check(https_head, ip.type, is_https=True):
        res.append(2)

    # 根据情况处理结果
    if not res:
        ip.Validated_time = 0
        ip.status = 'I'
        ip.failed_time += 1

    else:
        ip.Validated_time += 1
        ip.status = 'V'
        ip.failed_time = 0

        if len(res) == 2:
            pass
        elif 1 in res:
            ip.head = 'http'

        else:
            ip.head = 'https'

    ip.save()


def verify():
    print('verifying')
    count = verify_all()
    print('verified all {0} proxies,valid proxies occupy {1} and invalid {2}'.format(count[0] + count[1], count[0],
                                                                                     count[1]))