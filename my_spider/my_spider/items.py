# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MySpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class JoboleItem(scrapy.Item):
    title = scrapy.Field()
    create_date = scrapy.Field()
    url = scrapy.Field()


class JoBoleArticleItem(scrapy.Item):
    article_img = scrapy.Field()            # Field()类型表示任意类型类似于字典
    article_img_path = scrapy.Field()       # 图片的保存地址
    # url = scrapy.Field()                    # 文章url
    url_object_id = scrapy.Field()          # md5url
    article_title = scrapy.Field()          # 文章标题
    date_time = scrapy.Field()              # 文章创建时间
    article_label = scrapy.Field()          # 文章标签
    article_author = scrapy.Field()         # 文章作者
    love_number = scrapy.Field()            # 点赞数
    collection_number =scrapy.Field()       # 收藏数
    diccuss_number =scrapy.Field()          # 评论数

