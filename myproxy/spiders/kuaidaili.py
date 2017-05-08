#-*- coding:utf-8 -*-

import logging
import requests
import bs4
import re
from selenium import webdriver
from .general_methods import GeneralMethods
import time

logger = logging.getLogger(__name__)
gm = GeneralMethods()

# 快代理请求头# 快代理请求头
headers_kuai = {
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding':'gzip, deflate, sdch',
        'Accept-Language':'zh-CN,zh;q=0.8,zh-TW;q=0.6',
        'Cache-Control':'max-age=0',
        'Cookie':'sessionid=a76e1c82e71492eba1869a1973610bd6; channelid=0; sid=1491370147849899; _ydclearance=cc9a9863170f0895f520b2e4-c32a-4d36-962f-305f58d952d7-1491385315; Hm_lvt_7ed65b1cc4b810e9fd37959c9bb51b31=1491011473,1491139506,1491187701,1491370620; Hm_lpvt_7ed65b1cc4b810e9fd37959c9bb51b31=1491378119; _ga=GA1.2.511320761.1490863522',
        'Host':'www.kuaidaili.com',
        'Proxy-Connection':'keep-alive',
        'Referer':'https://www.google.com.hk/',
        'Upgrade-Insecure-Requests':'1',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.110 Safari/537.36',
}


def req_url_kuai(url,headers,count=1):
    try:
        req = requests.get(url, headers=headers, timeout=2)

    except:
        if count == 3:
            print('多次请求 url: %s 失败'%(url))
            return None
        time.sleep(2)
        count += 1
        return req_url_kuai(url,headers,count)

    source = req.text
    if req.status_code == 521:
        # 提取其中的JS加密函数
        js_func = ''.join(re.findall(r'(function .*?)</script>', source))
        # 提取其中执行JS函数的参数
        js_arg = ''.join(re.findall(r'setTimeout\(\"(\D+\(\d+\))\"', source))
        # 修改JS函数，使其返回Cookie内容
        js_func = js_func.replace('eval("qo=eval;qo(po);")', 'return po')
        # 执行JS获取Cookie
        js_code = js_func + ';' + 'return ' + js_arg
        driver = webdriver.PhantomJS()
        cookie_str = driver.execute_script(js_code)
        cookie_str = cookie_str.replace("document.cookie='", "")
        cookie = cookie_str.split(';')[0]
        headers['Cookie'] = cookie
        return req_url_kuai(url, headers, count=2)
    else:
        return source






def fetch_k1():
    '''下载 快代理 网站IP'''
    urls = ['http://www.kuaidaili.com/free/inha/',
            'http://www.kuaidaili.com/free/intr/',
            'http://www.kuaidaili.com/free/outha/',
            'http://www.kuaidaili.com/free/outtr/']

    KD_IP = []
    for url in urls:

        content = req_url_kuai(url,headers_kuai)
        if not content:
            print('error happened when request url:', url)
            continue
        try:
            soup = bs4.BeautifulSoup(content,'lxml')
            soup_tb = soup.find('tbody')
            soup_tr = soup_tb.find_all('tr')
            for tr in soup_tr:

                all_td = tr.find_all('td')

                ip        = all_td[0].string
                port      = all_td[1].string
                http_type = all_td[2].string
                http_head = all_td[3].string
                district  = all_td[4].string

                if '高匿' in http_type:
                    type = 'G'
                elif '透明' in http_type:
                    type = 'T'
                else:
                    type = 'O'

                # dic = {}
                # dic[http_head] = ip + ':' + port

                if ip in KD_IP:
                    continue
                KD_IP.append(ip)

                # print(dic,http_type,district)
                gm.save_proxy('快代理',ip,port,http_head,district=district,http_type=type)
        except Exception as e:
            print('error happened when request url:{0},error info:{1}'.format(url, e))
            continue
