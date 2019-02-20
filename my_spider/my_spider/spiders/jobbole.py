# -*- coding: utf-8 -*-
import datetime

import scrapy
import re
from urllib.parse import urljoin

from my_spider.items import JoBoleArticleItem
from my_spider.utils.common import get_md5


class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/']

    def parse(self, response):
        all_posts = response.xpath('//li[@id="menu-item-33406"]/a/@href').get()
        all_posts = urljoin(response.url, all_posts)
        yield scrapy.Request(url=all_posts, callback=self.all_posts)

    def all_posts(self, response):
        li_lists = response.xpath('//div[@id="archive"]/div[@class="post floated-thumb"]')
        for list in li_lists:
            file_url = list.xpath('./div[@class="post-thumb"]/a/@href').get()
            file_url = urljoin(response.url, file_url)
            file_img = list.xpath('./div[@class="post-thumb"]/a/img/@src').get()
            file_img_url = urljoin(response.url, file_img)
            yield scrapy.Request(url=file_url, callback=self.article, meta={"file_img": file_img_url})
        next_url = response.xpath('//div[@id="archive"]/div[@class="navigation margin-20"]/a[@class="next page-numbers"]/@href').get()
        if next_url:
            yield scrapy.Request(url=next_url, callback=self.all_posts)

    def article(self, response):
        article_item = JoBoleArticleItem()
        article_img = response.meta.get("file_img", "")   # 封面图片url
        article_title = response.xpath('//div[@class="entry-header"]/h1/text()').get()    # 文章标题
        date1 = response.xpath('//div[@class="entry-meta"]/p/text()').get()
        date_time =date1.lstrip('\r\n').split(' ')[-4]
        try:
            date_time = datetime.datetime.strftime(date_time, "%Y/%m/%d").date()
        except Exception as e:
            date_time = datetime.datetime.now().date()
    # 发布日期
        article_label = response.xpath('//div[@class="entry-meta"]/p/a/text()').get()    # 文章标签
        article_author = response.xpath('//div[@id="author-bio"]/h3/a/text()').get()     # 文章作者
        love_number = response.xpath('//h10[@id="114655votetotal"]/text()').get()        # 点赞数
        if love_number:
            fav_num = int(love_number)
        else:
            fav_num = 0
        collection = response.xpath('//div[@class="post-adds"]/span[2]/text()').get()
        comp = re.compile("\d+")
        collection_number = re.match(comp, collection.lstrip())                      # 收藏数
        if collection_number:
            collection_num = int(collection_number.group())
        else:
            collection_num = 0
        diccuss = response.xpath('//div[@class="post-adds"]/a/span[last()]/text()').get()
        diccuss_number = re.match(comp, diccuss.lstrip())                                # 评论数
        if diccuss_number:
            diccuss_num = int(diccuss_number.group())
        else:
            diccuss_num = 0

        article_item["article_img"] = [article_img]
        article_item["article_title"] = article_title
        article_item["date_time"] = date_time
        article_item["article_label"] = article_label
        article_item["article_author"] = article_author
        article_item["love_number"] = fav_num
        article_item["collection_number"] = collection_num
        article_item["diccuss_number"] = diccuss_num
        article_item["url_object_id"] = get_md5(response.url)
        yield article_item         # article_item 会传递进pipelines

