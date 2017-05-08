#-*- coding:utf-8 -*-
from ..models import Proxy
import logging

import requests
from selenium import webdriver


logger = logging.getLogger(__name__)
# ALL_ADDR = []

class GeneralMethods():
    def __init__(self):
        self.ALL_ADDR = []
        self.extract_addr()

    def extract_addr(self):
        all_items = Proxy.objects.filter(status='V')
        for i in all_items:
            self.ALL_ADDR.append(i.ip)

    def save_proxy(self,resource,ip,port,head, district='其他', http_type='O'):
        '''verifies and saves a IP
    
        :param resource: which website this IP comes from
        :param ip:  IP in string
        :param port : IP port
        :param head : IP head , http or https
        :param district : where this IP's location
        :param http_type: which type this IP is, 'O' stands for 其他 ,'G' for 高匿,'T' for 透明
        :return:
        '''

        if ip in self.ALL_ADDR:
            return

        if head == 'none' or ',' in head :
            head = ['http','https']
            res = []
            for i in head:
                proxy = {}
                proxy[i] = ip + ':' + port
                if self.verify_ip(proxy):
                    res.append(True)
                else:
                    res.append(False)

            if res.count(True) == 2:
                head = ','.join(head)
            elif res[0] == True:
                head = 'http'
            elif res[1] == True:
                head = 'https'
            else:
                head = None


        else:
            head = head.lower()
            proxy = {}
            proxy[head] = ip + ':' + port
            if not self.verify_ip(proxy):
                head = None
        if head:
            # 验证可用后存入数据库
            Proxy.objects.create(
                # addr=proxy,
                resourse=resource,
                ip = ip,
                port = port,
                head = head,
                status='V',
                district=district,
                type=http_type
            )


    # 首次验证 ip 是否可用
    def verify_ip(self,dic):
        '''
    
        :param dic: 字典形式的 IP
        :return: 如果请求成功则返回 True,反之则 False
        '''
        fixed_url = 'http://www.baidu.com/'
        try:
            res = requests.get(fixed_url, proxies=dic, timeout=1)
            assert res.status_code == 200
            return True
        except:
            return False


    def get_cookie_by_selenium(self,url):
        '''使用 selenium 获取 cookie
    
        :param url: 获取 cookie 的地址
        :return: 返回字符串形式的
        '''
        driver = webdriver.PhantomJS()
        driver.get(url)
        cookie = [item["name"] + "=" + item["value"] for item in driver.get_cookies()]
        cookiestr = ';'.join(item for item in cookie)
        driver.quit()
        return cookiestr


    def req_url(self,url, headers, rep_count=1):
        ''' 请求网页，返回 bs 处理过的字符串
    
        请求过程如果对方拒绝或者状态码不为 200 ，调用 selenium 重新获取 cookie,然后再次请求
        再失败，就直接返回 None
    
        :param url: 请求地址
        :param headers: 请求头
        :param rep_count: 请求次数，默认为 1，
        :return: bs4 处理过的网页
        '''
        try:
            req = requests.get(url, headers=headers, timeout=2)
            assert req.status_code == 200
        except Exception as e:

            if rep_count == 1:
                # logging.warning('url：%s 第一次报错，已经跳转重新获取 Cookie,报错信息：%s' %(url,e))
                cookie = self.get_cookie_by_selenium(url)
                headers['Cookie'] = cookie
                return self.req_url(url, headers, rep_count=2)
            else:
                print('url：%s 第二次报错，报错信息：%s' %(url,e))
                return None

        else:
            # soup = bs4.BeautifulSoup(req.text,'lxml')
            return req.text
