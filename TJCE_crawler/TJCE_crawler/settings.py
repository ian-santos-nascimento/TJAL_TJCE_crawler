# Scrapy settings for TJCE_crawler project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = "TJCE_crawler"
LOG_LEVEL = 'INFO'
SPIDER_MODULES = ["TJCE_crawler.spiders"]
NEWSPIDER_MODULE = "TJCE_crawler.spiders"


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = "TJCE_crawler (+http://www.yourdomain.com)"

ROBOTSTXT_OBEY = True

CONCURRENT_REQUESTS = 1
#SPIDER_MIDDLEWARES = {
#    "TJCE_crawler.middlewares.TjceCrawlerSpiderMiddleware": 543,
#}

DOWNLOAD_DELAY = 3
# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    "TJCE_crawler.middlewares.TjceCrawlerDownloaderMiddleware": 543,
#}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    "TJCE_crawler.pipelines.TjceCrawlerPipeline": 300,
}

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"
