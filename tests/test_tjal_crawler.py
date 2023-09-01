from unittest import TestCase
from scrapy.http import HtmlResponse
from scrapy.utils.test import get_crawler

from TJAL_crawler.TJAL_crawler.spiders import TjalCrawler

class TjalCrawlerTest(TestCase):

    def setUp(self):
        self.crawler = get_crawler(TjalCrawler)
        self.input_string = "0710802-55.2018.8.02.0001"
        self.codigo_processo = "P00006BXP0000"
        self.spider = self.crawler._create_spider('TjalCrawler', self.input_string, self.codigo_processo)

    def test_parse_item(self):
        response = HtmlResponse(url='https://www2.tjal.jus.br/cpopg/show.do?processo.codigo=01000O7550000&processo.foro=1&processo.numero=0710802-55.2018.8.02.0001', body=b'')
        parsed_item = next(self.spider.parse_item(response))
        # Assert against the parsed item or its fields

    def test_build_processo(self):
        response = HtmlResponse(url='https://example.com', body=b'')
        parsed_item = self.spider.build_processo(response)
        # Assert against the parsed item or its fields
