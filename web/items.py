# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
import scrapy
from scrapy.loader.processors import MapCompose,TakeFirst
from scrapy.loader import ItemLoader
import datetime


class WebItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class ArticleItemLoader(ItemLoader):
    default_output_processor = TakeFirst()


def date_convert(value):
    try:
        create_date = datetime.datetime.strptime(value, '%Y/%m/%d').date()
    except Exception as e:
        create_date = datetime.datetime.now().date()
    return create_date


def return__img_value(value):
    return value


class ArticleItem(scrapy.Item):
    article_img = scrapy.Field(
        output_processor=MapCompose(return__img_value)
    )
    title = scrapy.Field()
    article_url = scrapy.Field()
    create_time = scrapy.Field(
        input_processor=MapCompose(date_convert)
    )
    article_content = scrapy.Field()
