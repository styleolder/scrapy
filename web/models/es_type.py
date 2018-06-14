# -*- coding: utf-8 -*-  
__author__ = 'style'
from datetime import datetime
from elasticsearch_dsl import DocType, Date, Integer, Keyword, Text, connections, analyzer, Completion
from elasticsearch_dsl.analysis import CustomAnalyzer as _CustomAnalyzer

connections.create_connection(hosts=['192.168.1.13:9200'])


class CustomAnalyzer(_CustomAnalyzer):
    def get_analysis_definition(self):
        return {}

ik_analysis = CustomAnalyzer("ik_max_word", filter=["lowercase"])


class ArticleType(DocType):
    # 博客在线文章
    article_img = Keyword()
    title = Text(analyzer="ik_max_word")
    article_url = Keyword()
    create_time = Date()
    article_content = Text(analyzer="ik_max_word")
    article_md5 = Keyword()
    article_tags = Text(analyzer="ik_max_word")
    suggest = Completion(analyzer=ik_analysis)

    class Meta:
        index = "jobbole"
        doc_type = "article"


if __name__ == '__main__':
    ArticleType.init()
