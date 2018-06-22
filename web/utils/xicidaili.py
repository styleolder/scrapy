# -*- coding: utf-8 -*-
import requests
import os
import sys
import MySQLdb

conn = MySQLdb.connect(host="192.168.1.12", user="root", passwd="l2cplat123456", db="scrapy", charset="utf8")
cursor = conn.cursor()
headers = {
    'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
    'Accept - Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-Hans-CN, zh-Hans; q=0.5',
    'Connection': 'Keep-Alive',
    'Host': 'www.vyuanjy.com/',
    'Referer': 'http://www.vyuanjy.com/plugin.php?id=tom_weixin_zl&act_id=1&zlkey=11&from=timeline&prand=762',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063'}


class GetIP(object):
    def __init__(self,ip,port,proxy_type):
        self.ip = ip
        self.port = port
        self.proxy_type = proxy_type

    def delete_ip(self):
        # 从数据库中删除无效的ip
        delete_sql = """
            delete from xicidaili where ip='{0}'
        """.format(self.ip)
        try:
            cursor.execute(delete_sql)
            conn.commit()
        except Exception as e:
            pass
        return False

    def judge_ip(self):
        # 判断ip是否可用
        http_url = "https://www.baidu.com"
        proxy_url = "{0}://{1}:{2}".format(self.proxy_type, self.ip, self.port)
        try:
            proxy_dict = {
                "http": self.proxy_url,
            }
            response = requests.get(http_url, proxies=proxy_dict, timeout=3, headers=headers)
        except Exception as e:
            print "invalid ip and port"
            self.delete_ip(self.ip)
            return False
        code = response.status_code
        if code >= 200 and code < 300:
            print "ok ip========{0},{1},{2}".format(self.proxy_type, self.ip, port)
            return True
        else:
            print code
            print "invalid ip and port"
            self.delete_ip(self.ip)

    def count_ip(self):
        # 统计总数
        select_sql = """
             select count(*) from xicidaili
         """
        cursor.execute(select_sql)
        if cursor.fetchall() >= 2:
            return True
        else:
            return False

    def get_random_ip(self):
        # 从数据库中随机获取一个可用的ip
        if self.count_ip:
            random_sql = """
                  SELECT ip, port,proxy_type FROM xicidaili
                ORDER BY rand()
                LIMIT 1
                """
            cursor.execute(random_sql)
            for ip_info in cursor.fetchall():
                ip = ip_info[0]
                port = ip_info[1]
                proxy_type = ip_info[2]
                judge_re = self.judge_ip(ip, port, proxy_type)
                if judge_re:
                    return "{0}://{1}:{2}".format(proxy_type, ip, port)
                else:
                    return self.get_random_ip()
            cursor.close()
        else:
            sys.path.append(os.path.dirname(os.path.dirname(os.getcwd())))
            os.system('scrapy crawl xicidaili')
