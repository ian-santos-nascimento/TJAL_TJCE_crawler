# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field


class TjceCrawlerItem(scrapy.Item):
    numero_processo: str = Field()
    tribunal: str = Field()
    url: str = Field(default=None)
    area: str = Field(default=None)
    classeProcesso: str = Field(default=None)
    assunto: str = Field(default=None)
    data_distribuicao: str = Field(default=None)
    juiz: str = Field(default=None)
    valor_acao: str = Field(default=None)
    lista_partes_processo = Field(default=None)
    lista_movimentacoes = Field(default=None)
    grau = Field(default=None)

