#-*- coding:utf-8 -*-

import logging
from datetime import datetime
import bs4
from .general_methods import GeneralMethods

logger = logging.getLogger(__name__)
gm = GeneralMethods()


headers_general = {
        'User-Agent':'"Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) '
                     'AppleWebKit/534.20 (KHTML, like Gecko) Chrome/11.0.672.2 Safari/534.20",',
}


def ip181():
    url = 'http://www.ip181.com/'
    content = gm.req_url(url,headers_general)
    if not content:
        print('errors happen when requests url:',url)
        return None

    content = content.encode('ISO-8859-1')


    try:
        soup = bs4.BeautifulSoup(content, 'lxml')
        soup_tbody = soup.find('tbody')
        soup_tr = soup_tbody.find_all('tr')[1:]
        for tr in soup_tr:
            soup_td = tr.find_all('td')

            ip        = soup_td[0].string
            port      = soup_td[1].string
            http_type = soup_td[2].string
            http_head = soup_td[3].string
            district  = soup_td[5].string

            if district:
                district = district.strip()


            # dic = {}
            # proxy = ip + ':' + port
            # dic[http_head] = proxy

            if '高匿' in http_type:
                type = 'G'
            elif '透明' in http_type:
                type = 'T'
            else:
                type = 'O'

            gm.save_proxy('IP181',ip,port,http_head, district=district, http_type=type)
    except:
        print('时间 %s ,请求 %s 出错'%(datetime.now(),url))

        return None
