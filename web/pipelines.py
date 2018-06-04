# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.pipelines.images import ImagesPipeline
import codecs
import json

from twisted.enterprise import adbapi
import MySQLdb.cursors


class WebPipeline(object):
    def process_item(self, item, spider):
        return item


#自定义图片下载
class Article_ImagesPipeline(ImagesPipeline):
    def item_completed(self, results, item, info):
        if "article_img" in item:
            for k, v in results:
                image_file_path = v["path"]
                item["article_img"] = image_file_path
                return item


# 自定义文件导出
class Article_JsonPipeline(object):
    def __init__(self):
        self.file = codecs.open('Article.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        lins = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(lins)
        return item

    # 捕捉关闭信号
    def spider_closed(self, spider):
        self.file.close()


class Article_MysqlPipeline(ImagesPipeline):
    def item_completed(self, results, item, info):
        for k, v in results:
            image_file_path = v["path"]
            item["article_img"] = image_file_path
            return item


class MySQL_Twisted_Pipelines(object):
    # 基于twisted.enterprise.adbapi的异步MySQL管道
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbparams = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            charset='utf8',  # 编码要加上，否则可能出现中文乱码问题
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=False,
        )
        dbpool = adbapi.ConnectionPool('MySQLdb', **dbparams)  # **表示将字典扩展为关键字参数,相当于host=xxx,db=yyy....
        return cls(dbpool)  # 相当于dbpool付给了这个类，self中可以得到

    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_error, item, spider)
        return item

    def do_insert(self, cursor, item):
        # 执行具体的插入
        # 根据不同的item 构建不同的sql语句并插入到mysql中
        insert_sql, params = item.get_insert_sql()
        cursor.execute(insert_sql, params)

    def handle_error(self, failure, item, spider):
        print failure
