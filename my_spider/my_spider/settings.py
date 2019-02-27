# -*- coding: utf-8 -*-
import os

# Scrapy settings for my_spider project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'my_spider'

SPIDER_MODULES = ['my_spider.spiders']
NEWSPIDER_MODULE = 'my_spider.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'my_spider (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'my_spider.middlewares.MySpiderSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'my_spider.middlewares.MySpiderDownloaderMiddleware': None,
    'my_spider.middlewares.RandomUserAgentMiddlware': 543      # 自己写的"user-agent"中间件
}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    # 'my_spider.pipelines.MySpiderPipeline': 300,
    'scrapy.pipelines.images.ImagesPipeline': 1,
    'my_spider.pipelines.ArticleImagePipeline': 2,
    # 'my_spider.pipelines.JsonWithEncodingPipeline': 3,
    'my_spider.pipelines.JsonExportPipline': 3,
    # 'my_spider.pipelines.MysqlPipeline': 4,
    'my_spider.pipelines.MysqlTwistedPipeline': 4,
}
IMAGES_URLS_FIELD = "article_img" # 配置从item中获取下载地址
file_path = os.path.dirname(__file__) # 获取当前文件的目录名称
project_dir = os.path.abspath(file_path)
IMAGES_STORE = os.path.join(project_dir, "images")  # 配置图片保存路径
# IMAGES_MIN_WIDTH = 100                            # 设置筛选的下载的图片大小
# IMAGES_MIN_HEIGHT = 100

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
MYSQL_HOST = "localhost"
MYSQL_PASSWORD = "178178"
MYSQL_DBNAME = "JobBole"
MYSQL_USER = "root"

# 设置随机ua的信息
RANDOM_UA_TYPE = "random"