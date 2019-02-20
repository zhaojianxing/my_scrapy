# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import re
import datetime
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst, Join
from my_spider.utils.common import get_md5


class MySpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class JoboleItem(scrapy.Item):
    title = scrapy.Field()
    create_date = scrapy.Field()
    url = scrapy.Field()


class JoboleArticleItemLoader(ItemLoader):
    default_output_processor = TakeFirst()


def get_value(value):
    return value

def get_datetime(value):
    try:
        date_time = value.lstrip('\r\n').split(' ')[-4]
        date_time = datetime.datetime.strftime(date_time, "%Y/%m/%d").date()
    except Exception as e:
        date_time = datetime.datetime.now().date()
    return date_time


def get_join(value):
    if "评论" in value:
        value = ""
    else:
        value = value
    return value


def get_author(value):
    if value == "None":
        value = None
    else:
        value = value
    return value


def re_get_number(value):
    comp = re.compile("\d+")
    collection_number = re.match(comp, value.lstrip())  # 收藏数
    if collection_number:
        number = int(collection_number.group())
    else:
        number = 0
    return number


class JoBoleArticleItem(scrapy.Item):
    article_img = scrapy.Field(
        output_processor=MapCompose(get_value)
    )            # Field()类型表示任意类型类似于字典
    article_img_path = scrapy.Field()       # 图片的保存地址
    # url = scrapy.Field()                    # 文章url
    url_object_id = scrapy.Field(
        input_processor=MapCompose(get_md5)
    )          # md5url
    article_title = scrapy.Field()          # 文章标题
    date_time = scrapy.Field(
        input_processor=MapCompose(get_datetime)
    )              # 文章创建时间
    article_label = scrapy.Field(
        input_processor=MapCompose(get_join),
        output_processor=Join(",")
    )          # 文章标签
    article_author = scrapy.Field(
        # input_processor=MapCompose(get_author)
    )         # 文章作者
    love_number = scrapy.Field(
        input_processor=MapCompose(re_get_number)
    )            # 点赞数
    collection_number =scrapy.Field(
        input_processor=MapCompose(re_get_number)
    )       # 收藏数
    diccuss_number =scrapy.Field(
        input_processor=MapCompose(re_get_number)
    )          # 评论数

