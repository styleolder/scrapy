# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst, Join
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


def return_img_value(value):
    return value


def tags_format(value):
    if u"评论" in value:
        return ""
    else:
        return value


class Article_Join(Join):

    def __init__(self, separator=u' '):
        self.separator = separator

    def __call__(self, values):
        try:
            values = values.remove('')
        except Exception as e:
            print e
        return self.separator.join(values)

class ArticleItem(scrapy.Item):
    article_img = scrapy.Field(
        output_processor=MapCompose(return_img_value)
    )
    title = scrapy.Field()
    article_url = scrapy.Field()
    create_time = scrapy.Field(
        input_processor=MapCompose(date_convert)
    )
    article_content = scrapy.Field()
    article_md5 = scrapy.Field()
    article_tags = scrapy.Field(
        input_processor=MapCompose(tags_format),
        output_processor=Article_Join(',')
    )
