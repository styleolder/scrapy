# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from web.items import XicidialiItem


class XicidailiSpider(CrawlSpider):
    name = 'xicidaili'
    allowed_domains = ['xicidaili.com']
    start_urls = ['http://www.xicidaili.com']
    custom_settings = {
        "COOKIES_ENABLED": True,
        "DOWNLOAD_DELAY": 3,
        'DEFAULT_REQUEST_HEADERS': {
            'Host': 'www.xicidaili.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
        }
    }
    rules = (
        Rule(LinkExtractor(allow=r'nt/'), follow=True),
        Rule(LinkExtractor(allow=r'nn/'), follow=True),
        Rule(LinkExtractor(allow=r'wn/'), follow=True),
        Rule(LinkExtractor(allow=r'wt/'), follow=True),
        Rule(LinkExtractor(allow=r'nt/[123456789]'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'nt/[123456789]'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'wt/[123456789]'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'wn/[123456789]'), callback='parse_item', follow=True),
    )

    def parse_start_url(self, response):
        return []

    def process_results(self, response, results):
        return results

    def parse_item(self, response):
        for base in response.xpath('//tr[@class="odd"]'):
            item = XicidialiItem()
            item['ip'] = base.xpath('.//td[2]/text()').extract_first()
            item['port'] = base.xpath('.//td[3]/text()').extract_first()
            item['addr'] = base.xpath('.//td[4]/a/text()').extract_first()
            item['url'] = response.url
            item['proxy_type'] = base.xpath('.//td[6]/text()').extract_first()
            yield item
