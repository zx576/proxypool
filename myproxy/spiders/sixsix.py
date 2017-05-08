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

# 66代理网 请求头
headers_66 = {
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding':'gzip, deflate, sdch',
        'Accept-Language':'zh-CN,zh;q=0.8,zh-TW;q=0.6',
        'Connection':'keep-alive',
        'Cookie':'__cfduid=dc82e63a299dce97b98b94d949f5a9bb61484641816;'
                 ' CNZZDATA1253901093=1728273565-1484639487-http%253A%252F%252Fwww.baidu.com%252F%7C1484701785; '
                 'Hm_lvt_1761fabf3c988e7f04bec51acd4073f4=1484646251,1484646378,1484702884,1484703157; '
                 'Hm_lpvt_1761fabf3c988e7f04bec51acd4073f4=1484704429',
        'Host':'www.66ip.cn',
        'Referer':'http://www.66ip.cn/pt.html',
        'Upgrade-Insecure-Requests':'1',
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
            }

def fetch_ss():
    '''取得 66 代理网所有分地区的 url，并传入 fetch_ss_1 处理存入数据'''
    url = 'http://www.66ip.cn'

    content = gm.req_url(url=url,headers=headers_66).encode('ISO-8859-1')
    if not content:
        print('error happened when request url:',url)
        return None
    soup = bs4.BeautifulSoup(content,'lxml')

    if not soup:
        return None

    soup_ul = soup.find('ul',class_='textlarge22')
    for li in soup_ul:
        try:
            _url = li.a['href']
        except:
            continue
        if 'http' in _url:
            fetch_ss_1(_url)
        else:
            _url = url + _url
            fetch_ss_1(_url)



SS_IP = []

def fetch_ss_1(url):
    '''传入某一地区的 url,存储数据'''

    global SS_IP
    content = gm.req_url(url, headers_66)
    if not content:
        print('error happened when request url:',url)
        return None

    content = content.encode('ISO-8859-1')

    try:
        soup = bs4.BeautifulSoup(content, 'lxml')
        soup_table = soup.find('table',bordercolor=True)
        soup_tr = soup_table.find_all('tr')

        for tr in soup_tr[1:]:

            all_td = tr.find_all('td')

            ip        = all_td[0].string
            port      = all_td[1].string
            district  = all_td[2].get_text()
            http_type = all_td[3].get_text()

            if '高匿' in http_type:
                type = 'G'
            elif '透明' in http_type:
                type = 'T'
            else:
                type = 'O'

            # dic = {}
            # dic["http"] = ip +':'+ port

            if ip in SS_IP:
                continue
            SS_IP.append(ip)

            gm.save_proxy('66代理',ip,port,'none',district=district,http_type=type)
    except Exception as e:
        print('fetch_ss_1 请求 %s 报错，错误信息：%s' % (url, e))
        # continue
        return None
