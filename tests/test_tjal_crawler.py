from unittest import TestCase
import requests
import unittest
from scrapy import signals
from scrapy.crawler import CrawlerProcess
from scrapy.signalmanager import dispatcher
from scrapy.utils.project import get_project_settings
from scrapy.utils.test import get_crawler

import app
from TJAL_crawler.TJAL_crawler.spiders import TjalCrawler


class TjalCrawlerTest(TestCase):

    def setUp(self):
        self.crawler = get_crawler(TjalCrawler)
        self.input_string = "0034520-06.2010.8.02.0001"
        self.spider = self.crawler._create_spider(input_string=self.input_string)

    def test_parse_item(self):
        items = []

        def collect_items(item):
            items.append(item)

        process = CrawlerProcess(settings=get_project_settings())
        crawler = process.create_crawler(TjalCrawler)
        dispatcher.connect(collect_items, signal=signals.item_scraped)
        process.crawl(crawler, input_string=self.input_string)
        process.start()

        for item in items:
            assert item is not None
            assert item['numero_processo'] is not None
            assert item['grau'] is not None
            assert item['classeProcesso'] is not None
            assert item['area'] is not None
