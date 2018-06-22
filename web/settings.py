# -*- coding: utf-8 -*-

# Scrapy settings for web project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
# http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
import os
import sys

sys.path.insert(0, os.path.abspath('.'))
sys.path.insert(0, os.path.abspath('..'))

BOT_NAME = 'web'

SPIDER_MODULES = ['web.spiders']
NEWSPIDER_MODULE = 'web.spiders'
# 全局设置下载等待时间
DOWMLOAD_DELY = 3
# 是否保存cookies
COOKIES_ENABLED = False
# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'web (+http://www.yourdomain.com)'

# Obey robots.txt rules
# 是否遵守爬取规则
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
# }

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
SPIDER_MIDDLEWARES = {
    'web.middlewares.WebSpiderMiddleware': 543,
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'scrapy_fake_useragent.middleware.RandomUserAgentMiddleware': 400,
    #'web.middlewares.RandomIpSpiderMiddleware': 399,
}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
# DOWNLOADER_MIDDLEWARES = {
#    # 'web.middlewares.MyCustomDownloaderMiddleware': 543,
#    'web.middlewares.JsPageSpiderMiddleware': 1
# }

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html

# 获取数据后的操作,数字越小提前处理
ITEM_PIPELINES = {
    'web.pipelines.WebPipeline': 300,
    # 'scrapy.pipelines.images.ImagesPipeline': 1,
    # 'web.pipelines.Article_ImagesPipeline': 1,
    # 'web.pipelines.Article_JsonPipeline': 2
    'web.pipelines.MySQL_Twisted_Pipelines': 10
    #'web.pipelines.ElasticsearchPipeline': 10
}
IMAGES_URLS_FIELD = "article_img"
IMAGES_STORE = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'images')
# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
##MYSQL连接设置
MYSQL_HOST = '192.168.1.12'
MYSQL_DBNAME = 'scrapy'  # 数据库名字，请修改
MYSQL_USER = 'root'  # 数据库账号，请修改
MYSQL_PASSWD = 'l2cplat123456'  # 数据库密码，请修改
MYSQL_PORT = 3306

#允许设置代理IP，其代理IP的Middleware优先于RandomUserAgentMiddleware
RANDOM_UA_PER_PROXY = True
#时间格式转化
SQL_DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
SQL_DATE_FORMAT = "%Y-%m-%d"