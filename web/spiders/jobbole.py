# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')

import scrapy
import re
from scrapy.http import Request
from urlparse import urljoin
from datetime import datetime
from web.items import ArticleItem
from scrapy.loader import ItemLoader

class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['jobbole.com']
    start_urls = ['http://www.jobbole.com']
    # start_urls = ['http://python.jobbole.com/all-posts']

    #拼接出所有的URL地址
    def parse(self, response):
        urls = response.xpath('//li[@class="menu-item"]/a/@href').extract()
        for url in urls:
            if re.match(".*jobbole\.com$", url):
                url = urljoin(url, 'all-posts')
                print url
                yield Request(url=url, callback=self.parse_url)

    def parse_url(self, response):
        # def parse(self, response):
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
        article_item = ArticleItem()
        article_item['article_img'] = [response.meta.get("article_img", "")]
        article_item['title'] = response.xpath('//div[@class="entry-header"]/h1/text()').extract_first()
        article_item['article_url'] = response.url
        create_time = response.xpath(
            '//p[@class="entry-meta-hide-on-mobile"]/text()').extract()[0].replace("·", "").strip()
        # create_time = response.css('p.entry-meta-hide-on-mobile').extract_first().strip().replace("·", "")
        try:
            article_item['create_time'] = datetime.strptime(create_time, "%Y/%m/%d").date()
        except Exception as e:
            article_item['create_time'] = datetime.now()
        # article_item['article_content'] = response.xpath("div.entry").extract()[0]
        article_item['article_content'] = response.xpath('//div[@class="entry"]').extract()[0]

        #使用itemloader
        itemloader = ItemLoader(item=ArticleItem(), response=response)
        #itemloader.add_css("title","")
        #itemloader.add_xpath("","")
        #itemloader.add_value("","")
        yield article_item
