from .models import Proxy

import requests


def verify_all():
    ''' verify all proxy in the database
        
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
        proxy[ip.head] = ip.ip + ':' + ip.port

        if verify_proxy(proxy):
            ip.Validated_time += 1
            ip.status = 'V'
            ip.failed_time = 0
            valid_count += 1

        else:
            ip.status = 'I'
            ip.failed_time += 1
            invalid_count += 1

        ip.save()

    return valid_count,invalid_count


def verify_proxy(dic):
    ''' verify if this IP is valid
    
    :param dic: proxy
    :return: True if it passes verifying or it will return False
    '''
    fixed_url = 'http://www.baidu.com/'
    try:
        res = requests.get(fixed_url, proxies=dic, timeout=1)
        assert res.status_code == 200
        return True
    except:
        return False


def verify():
    print('verifying')

    count = verify_all()

    print('verified all {0} proxies,valid proxies occupy {1} and invalid {2}'.format(count[0]+count[1],count[0],count[1]))