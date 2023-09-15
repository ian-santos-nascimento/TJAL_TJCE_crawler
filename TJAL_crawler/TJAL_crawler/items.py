from scrapy import Item, Field
from typing import List, Dict


class TjalCrawlerItem(Item):
    numero_processo: str = Field()
    tribunal: str = Field()
    area: str = Field(default=None)
    classeProcesso: str = Field(default=None)
    assunto: str = Field(default=None)
    data_distribuicao: str = Field(default=None)
    juiz: str = Field(default=None)
    valor_acao: str = Field(default=None)
    lista_partes_processo = Field(default=None)
    lista_movimentacoes = Field(default=None)
    grau  = Field(default=None)

