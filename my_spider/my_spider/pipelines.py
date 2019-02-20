# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import MySQLdb
import MySQLdb.cursors
from scrapy.exporters import JsonItemExporter
from scrapy.pipelines.images import ImagesPipeline
from twisted.enterprise import adbapi
import codecs

class MySpiderPipeline(object):
    def process_item(self, item, spider):
        return item

class ArticleImagePipeline(ImagesPipeline):
    # 获取图片的保存路径results为tuple
    def item_completed(self, results, item, info):
        for ok, value in results:
            image_file_path = value["path"]
        item["article_img_path"] = image_file_path
        return item

class JsonWithEncodingPipeline(object):
    """
    自定义的item写入json文件
    """
    def __init__(self):
        self.file = codecs.open("article.json", "w", encoding="utf-8")

    def process_item(self, item, spider):
        lines = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(lines)
        return item

    def spider_closed(self, spider):
        self.file.close()

class JsonExportPipline(object):
    """
    利用scrapy 自带的JsonItemPipline 类将item写入接送文件
    """
    def __init__(self):
        self.file = open("scrapy_srticle.json", "wb")
        self.expore = JsonItemExporter(self.file, encoding="utf-8")
        self.expore.start_exporting()

    def close_spider(self):
        self.expore.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.expore.export_item(item)
        return item

class MysqlPipeline(object):
    def __init__(self):
        self.coon = MySQLdb.connect("localhost", "root", "178178", "JobBole", charset="utf8", use_unicode=True)
        self.cursor = self.coon.cursor()

    def process_item(self, item, spider):
        insert_sql = """
        insert into jobbole_article(article_img, url_object_id, artiicle_title, date_time, article_label, article_author, love_nummber, collection_number, diiccuss_number, artiicle_img_path)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        self.cursor.execute(insert_sql, (item["article_img"][0],item["url_object_id"], item["article_title"], item["date_time"], item["article_label"], item["article_author"], item["love_number"], item["collection_number"], item["diccuss_number"], item["article_img_path"]))
        self.coon.commit()


class MysqlTwistedPipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbparms = dict(
            host=settings["MYSQL_HOST"],
            user=settings["MYSQL_USER"],
            db=settings["MYSQL_DBNAME"],
            passwd=settings["MYSQL_PASSWORD"],
            cursorclass = MySQLdb.cursors.DictCursor,
            charset="utf8",
            use_unicode=True
        )
        dbpool = adbapi.ConnectionPool("MySQLdb", **dbparms)
        return cls(dbpool)

    def process_item(self, item, spider):
        # 使用twisted将mysql插入变成异步执行
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_error)

    def handle_error(self, failure):
        # 处理异步插入的异常
        print(failure)

    def author(self, item):
        author = ''
        if item["article_author"] == "None":
            author = None
        else:
            author = item["article_author"]
        return author

    def do_insert(self,cursor, item):
        # 执行具体的插入
        insert_sql = """
        insert into jobbole_article_tw(article_img, url_object_id, artiicle_title, date_time, article_label, article_author, love_nummber, collection_number, diiccuss_number, artiicle_img_path)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        author = self.author(item)
        cursor.execute(insert_sql, (item["article_img"][0],item["url_object_id"], item["article_title"], item["date_time"], item["article_label"], author, item["love_number"], item["collection_number"], item["diccuss_number"], item["article_img_path"]))