# -*- coding: utf-8 -*-
import sys
import scrapy
import re
from scrapy.http import Request
from urlparse import urljoin
from web.items import ArticleItem
from web.items import ArticleItemLoader
import hashlib
from selenium import webdriver
from scrapy.http import HtmlResponse
import time
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals

reload(sys)
sys.setdefaultencoding('utf8')


class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['jobbole.com']
    start_urls = ['http://111.jobbole.com/11123']

    # def __init__(self):
    #     self.driver = webdriver.Chrome()
    #     super(JobboleSpider, self).__init__()
    #     dispatcher.connect(self.splider_close(), signals.spider_closed)
    #
    # def splider_close(self):
    #     self.driver.close()
    # 收集404所有页面
    handle_httpstatus_list = [404]

    def __init__(self):
        self.fail_urls = []
        dispatcher.connect(self.handle_spider_closed, signals.spider_closed)

    def handle_spider_closed(self, spider, reason):
        self.crawler.stats.set_value("failed_urls ", ",".join(self.fail_urls))

    # 拼接出所有的URL地址
    def parse(self, response):
        if response.status == 404:
            self.fail_urls.append(response.url)
            self.crawler.stats.inc_value("failed_url_num")

        urls = response.xpath('//li[@class="menu-item"]/a/@href').extract()
        for url in urls:
            if re.match(".*jobbole\.com$", url):
                url = urljoin(url, 'all-posts')
                print url
                yield Request(url=url, callback=self.parse_url)

    def parse_url(self, response):
        post_divs = response.xpath('//div[@class="post floated-thumb"]')
        for post_div in post_divs:
            article_img = post_div.xpath('./div[@class="post-thumb"]/a/img/@src').extract_first()
            print article_img
            post_url = post_div.xpath('./div[@class="post-meta"]/p/a/@href').extract_first()
            yield Request(url=post_url, callback=self.parse_details, meta={'article_img': article_img})
        next_page_url = response.xpath(
            '//div[@class="navigation margin-20"]/a[@class="next page-numbers"]/@href').extract_first()
        if next_page_url:
            yield Request(url=next_page_url, callback=self.parse_url)

    def parse_details(self, response):
        itemloader = ArticleItemLoader(item=ArticleItem(), response=response)
        itemloader.add_xpath("title", '//div[@class="entry-header"]/h1/text()')
        itemloader.add_xpath("create_time", '//p[@class="entry-meta-hide-on-mobile"]/text()')
        itemloader.add_xpath("article_content", '//div[@class="entry"]')
        itemloader.add_xpath("article_tags", '//p[@class="entry-meta-hide-on-mobile"]/a/text()')
        itemloader.add_value("article_url", response.url)
        itemloader.add_value("article_md5", hashlib.md5(response.url.encode('utf-8')).hexdigest())
        itemloader.add_value("article_img", [response.meta.get("article_img", "")])
        article_item = itemloader.load_item()
        yield article_item
