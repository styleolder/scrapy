# -*- coding: utf-8 -*-
import requests
import os
import sys
import MySQLdb

conn = MySQLdb.connect(host="192.168.1.12", user="root", passwd="l2cplat123456", db="scrapy", charset="utf8")
cursor = conn.cursor()


class GetIP(object):
    def delete_ip(self, ip):
        # 从数据库中删除无效的ip
        delete_sql = """
            delete from xicidaili where ip='{0}'
        """.format(ip)
        cursor.execute(delete_sql)
        conn.commit()
        return True

    def judge_ip(self, ip, port, proxy_type):
        # 判断ip是否可用
        http_url = "https://www.baidu.com"
        proxy_url = "{0}://{1}:{2}".format(proxy_type, ip, port)
        try:
            proxy_dict = {
                "http": proxy_url,
            }
            response = requests.get(http_url, proxies=proxy_dict, timeout=2)
        except Exception as e:
            print "invalid ip and port"
            self.delete_ip(ip)
            return False
        else:
            code = response.status_code
            if code >= 200 and code < 300:
                print "ok ip========{0},{1},{2}".format(proxy_type, ip, port)
                return True
            else:
                print "invalid ip and port"
                self.delete_ip(ip)
                return False

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
