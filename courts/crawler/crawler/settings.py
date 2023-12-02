import os
import sys

sys.path.append(os.path.dirname(os.path.abspath('.')))
os.environ['DJANGO_SETTINGS_MODULE'] = 'courts.settings'
import django

django.setup()

BOT_NAME = "crawler"

SPIDER_MODULES = ["crawler.crawler.spiders"]
NEWSPIDER_MODULE = "crawler.crawler.spiders"

ROBOTSTXT_OBEY = False

# SPIDER_MIDDLEWARES = {
#    "crawler.middlewares.CrawlerSpiderMiddleware": 543,
# }

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
# DOWNLOADER_MIDDLEWARES = {
#    "crawler.middlewares.CrawlerDownloaderMiddleware": 543,
# }

ITEM_PIPELINES = {
    "crawler.crawler.pipelines.CrawlerPipeline": 300,
}
# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"
