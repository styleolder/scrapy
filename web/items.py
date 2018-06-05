# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst, Join
from scrapy.loader import ItemLoader
import datetime
from web.settings import SQL_DATETIME_FORMAT
import re

class WebItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class ArticleItemLoader(ItemLoader):
    default_output_processor = TakeFirst()


def date_convert(value):
    try:
        create_date = datetime.datetime.strptime(value.split(" ")[0], '%Y/%m/%d').date()
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


def tags_format2(value):
    if "/" in value:
        return value.replace("/", "")
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
        output_processor=MapCompose(return_img_value),
    )
    title = scrapy.Field()
    article_url = scrapy.Field()
    create_time = scrapy.Field(
        input_processor=MapCompose(date_convert),
    )
    article_content = scrapy.Field()
    article_md5 = scrapy.Field()
    article_tags = scrapy.Field(
        input_processor=MapCompose(tags_format),
        output_processor=Article_Join(','),
    )

    def get_insert_sql(self):
        sql_insert = 'INSERT INTO jobbole(article_img,lagou_url,article_url,create_time,article_content,article_tags,article_md5) VALUES (%s,%s,%s,%s,%s,%s,%s)'
        params = (self['article_img'], self['title'], self['article_url'], self['create_time'], self['article_content'], self['article_tags'], self['article_md5'])
        return sql_insert, params

class LaGouItemLoader(ItemLoader):
    default_output_processor = TakeFirst()


class LaGouItem(scrapy.Item):
    lagou_title = scrapy.Field()
    lagou_url = scrapy.Field()
    lagou_job_type = scrapy.Field()
    lagou_create_time = scrapy.Field()
    lagou_desc = scrapy.Field(
        input_processor=MapCompose(tags_format2),
        output_processor=Article_Join(','),
    )

    def get_insert_sql(self):
        match_time1 = re.match("(\d+):(\d+).*", self["lagou_create_time"])
        match_time2 = re.match("(\d+)天前.*", self["lagou_create_time"])
        match_time3 = re.match("(\d+)-(\d+)-(\d+)", self["lagou_create_time"])
        if match_time1:
            today = datetime.datetime.now()
            hour = int(match_time1.group(1))
            minutues = int(match_time1.group(2))
            time = datetime.datetime(
                today.year, today.month, today.day, hour, minutues)
            self["lagou_create_time"] = time.strftime(SQL_DATETIME_FORMAT)
        elif match_time2:
            days_ago = int(match_time2.group(1))
            today = datetime.datetime.now() - datetime.timedelta(days=days_ago)
            self["lagou_create_time"] = today.strftime(SQL_DATETIME_FORMAT)
        elif match_time3:
            year = int(match_time3.group(1))
            month = int(match_time3.group(2))
            day = int(match_time3.group(3))
            today = datetime.datetime(year, month, day)
            self["lagou_create_time"] = today.strftime(SQL_DATETIME_FORMAT)
        else:
            self["lagou_create_time"] = datetime.datetime.now(
            ).strftime(SQL_DATETIME_FORMAT)

        sql_insert = 'INSERT INTO lagou(lagou_title,lagou_url,lagou_job_type,lagou_create_time,lagou_desc) VALUES (%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE lagou_create_time=VALUES(lagou_create_time) '
        params = (self['lagou_title'], self['lagou_url'], self['lagou_job_type'], self['lagou_create_time'], self['lagou_desc'])
        return sql_insert, params
