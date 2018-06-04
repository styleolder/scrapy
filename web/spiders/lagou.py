# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from web.items import LaGouItem,LaGouItemLoader

class LagouSpider(CrawlSpider):
    name = 'lagou'
    allowed_domains = ['www.lagou.com']
    start_urls = ['https://www.lagou.com/jobs/list_%E8%BF%90%E7%BB%B4?px=default&city=%E8%A5%BF%E5%AE%89#filterBox']

    #LinkExtractor allow允许访问的域名

    rules = (
        # Rule(LinkExtractor(allow=r'zhaopin/.*'), follow=True),
        # Rule(LinkExtractor(allow=r'gongsi/j\d+.html'), follow=True),
        Rule(LinkExtractor(allow=r'jobs/\d+.html'), callback='parse_item', follow=True),
    )

    def parse_start_url(self, response):
        return []

    def process_results(self, response, results):
        return results

    def parse_item(self, response):
        itemloader = LaGouItemLoader(item=LaGouItem(), response=response)
        itemloader.add_xpath("lagou_title", '//div[@class="company"]')
        itemloader.add_value("lagou_url", response.url)
        itemloader.add_xpath("lagou_job_type", '//span[@class="name"]')
        itemloader.add_xpath("lagou_create_time", '//p[@class="publish_time"]')
        itemloader.add_xpath("lagou_desc", '//div[@class="content_l fl"]')
        article_item = itemloader.load_item()
        return article_item