# -*- coding: utf-8 -*-
import scrapy


class MxSpider(scrapy.Spider):
    name = 'mx'
    allowed_domains = ['www.mingxing.com']
    start_urls = ['http://www.mingxing.com/']

    def parse(self, response):
        pass
