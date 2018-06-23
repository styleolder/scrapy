# -*- coding: utf-8 -*-  
__author__ = 'style'
__date__ = '2017/5/24 16:27'
import requests


class GetIP(object):
    def __init__(self, proxy_type, ip, port):
        self.proxy_type = proxy_type
        self.ip = ip
        self.port = port

    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0"}

    def judge_ip(self):
        # 判断ip是否可用
        http_url = "http://www.baidu.com"
        try:
            proxy_url = "{0}://{1}:{2}".format(self.proxy_type.lower(), self.ip, self.port)
            proxy_dict = {
                self.proxy_type.lower(): proxy_url,
            }
            response = requests.get(http_url, proxies=proxy_dict, timeout=10, headers=self.headers)
            code = response.status_code
            print code
            if code >= 200 and code <= 302:
                print "ok ip========{0},{1},{2}".format(self.proxy_type, self.ip, self.port)
                return True
            else:
                print "invalid ip and port"
                return False
        except Exception as e:
            return False
