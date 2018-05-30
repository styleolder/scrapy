# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WebItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class ArticleItem(scrapy.Item):
    article_img = scrapy.Field()
    title = scrapy.Field()
    article_url = scrapy.Field()
    create_time = scrapy.Field()
    article_content = scrapy.Field()