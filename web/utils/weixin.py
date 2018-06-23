# -*- coding: utf-8 -*-
# import os
# import re
#
# cmd_dir = "F:\迅雷下载"
# num_list = [str(i) for i in range(1, 15)]
#
# def searchMum(cmd_dir):
#     num_list = []
#     for (root, dirs, files) in os.walk(cmd_dir):
#         for filename in files:
#             reg_match = '[0-9]+'
#             if re.findall(reg_match, filename):
#                 for i in re.findall(reg_match, filename):
#                     if i != "":
#                         num_list.append(i)
#                         print(os.path.join(root, filename))
#     return sorted(list(set(num_list)))
#
# find_list = searchMum(cmd_dir)
# print(sorted(list(set(num_list).difference(set(find_list)))))
# a = []
# b = []
# num = 0
# with open('test.txt', 'r') as f:
#     for line in f.readlines():
#         num += 1
#         if num % 2 == 0:
#             a.append(int(line.strip('\n')))
#         else:
#             b.append(int(line.strip('\n')))
#         print(num)
# print(a, b)
# for i in map(lambda x, y: x - y, a, b):
#     print(i)


# import os
# print(os.path.dirname(os.path.dirname(os.getcwd())))


# import requests
#
# response = requests.get('http://www.xicidaili.com/', proxies={"http": "http://61.135.217.7"})
# print(response.status_code)
# from collections import namedtuple
# User = namedtuple('User', ['name', 'sex', 'age'])
# user = User._make(['kongxx', 'male', 21])
# print(user)
# print(user.name)
# username = {"token": [{"token": "1"}, {"token": "2"}]}
# for i in username["token"]:
#     print(i["token"])
import requests
import time
from lxml import etree

headers = {
    "Host": "www.vyuanjy.com",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3393.4 Safari/537.36",
    "Referer": "http://www.vyuanjy.com/plugin.php?id=tom_weixin_zl&act_id=1&zlkey=11&from=timeline&prand=762",
    "X-Requested-With": "XMLHttpRequest",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Accept-Encoding": "gzip, deflate",
    "Accept": "application/json, text/javascript, */*; q=0.01",
}
import MySQLdb


def GetIP():
    db = MySQLdb.connect("192.168.1.12", "root", "l2cplat123456", "scrapy", charset='utf8')
    try:
        cursor = db.cursor()
        cursor.execute("select ip, port,proxy_type from xicidaili order by rand() LIMIT 1  ")
        for ip_info in cursor.fetchall():
            ip = ip_info[0]
            port = ip_info[1]
            proxy_type = ip_info[2]
            weixin(ip, port, proxy_type)
        db.close()
    except Exception as e:
        print e


def weixin(ip, port, proxy_type):
    proxy_url = "{0}://{1}:{2}".format(proxy_type.lower(), ip, port)
    print proxy_url
    proxy_dict = {
        proxy_type.lower(): proxy_url,
    }
    s = requests.session()
    print s.cookies.get_dict()
    print "===============start==============="
    respone = s.get("http://www.vyuanjy.com/plugin.php?id=tom_weixin_zl&act_id=1&zlkey=11&from=timeline&prand=762",
                    headers=headers, timeout=60, proxies=proxy_dict)
    dom_tree = etree.HTML(respone.content)
    ###XPath匹配
    formhash = dom_tree.xpath('//input[@name="formhash"]/@value')[0]
    print s.cookies.get_dict()
    print formhash
    num = dom_tree.xpath('//p[@class="num"]/text()')[0]
    print u"当前票数为{num}".format(num=num)
    time.sleep(5)
    url = "http://www.vyuanjy.com/plugin.php?id=tom_weixin_zl:ajax&act=zhuli&act_id=1&zlkey=11&openid=&subscribe=1&formkey=f267db478e54552744c1aa4116f356e7&formhash={formhash}".format(
        formhash=formhash)
    print url
    try:
        content = s.get(
            url,
            headers=headers, timeout=60)
        if content.status_code >=200 & content.status_code <=302:
            print content.content
            print u"我为自己加油。增加一票"
        else:
            print u"访问失败了"
    except Exception as e:
        print e
    print "===============end==============="


if '__name__' == '__main__':
    while True:
        GetIP()
