# -*- coding: utf-8 -*-
import scrapy
from web.items import XicidialiItem
from scrapy.http import Request


class XicidailiSpider(scrapy.Spider):
    name = 'xicidaili'
    allowed_domains = ['xicidaili.com']
    start_urls = ['http://www.xicidaili.com/nn', 'http://www.xicidaili.com/nt']
    custom_settings = {
        "COOKIES_ENABLED": True,
        "DOWNLOAD_DELAY": 3,
        'DEFAULT_REQUEST_HEADERS': {
            'Host': 'www.xicidaili.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
        }
    }

    def parse(self, response):
        for i in range(1, 30):
            url = response.url + "/" + str(i)
            yield Request(url=url, callback=self.parse_item)

    def parse_item(self, response):
        for base in response.xpath('//tr[@class="odd"]'):
            item = XicidialiItem()
            item['ip'] = base.xpath('.//td[2]/text()').extract_first()
            item['port'] = base.xpath('.//td[3]/text()').extract_first()
            item['addr'] = base.xpath('.//td[4]/a/text()').extract_first()
            item['url'] = response.url
            item['proxy_type'] = base.xpath('.//td[6]/text()').extract_first()
            yield item
