from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from ..items import TjceCrawlerItem
from scrapy import Request
from utils import get_tribunal

class TjceCrawler(CrawlSpider):
    name = 'TjceCrawler'
    rules = ([
        Rule(LinkExtractor(allow=r"cpopg/",
                           deny=["/abrirDocumentoVinculadoMovimentacao", "/open.do", "jsessionid",
                                 "#liberarAutoPorSenha"]),
             callback='parse_item'),
        Rule(LinkExtractor(allow=r"cposg5/search.do", deny="cposg5/show.do"), callback='get_codigo_processo')
    ])

    def __init__(self, input_string=None, codigo_processo=None, *a, **kw):
        super().__init__(*a, **kw)
        self.input_string = input_string
        self.codigo_processo = codigo_processo
        self.start_urls = [
            f'https://esaj.tjce.jus.br/cpopg/show.do?processo.foro={self.input_string[-4:]}&processo.numero={self.input_string}',
            "https://esaj.tjce.jus.br/cposg5/search.do?conversationId=&paginaConsulta=0&cbPesquisa=NUMPROC&numeroDigitoAnoUnificado=0070337-91.2008&foroNumeroUnificado=0001&dePesquisaNuUnificado=0070337-91.2008.8.06.0001&dePesquisaNuUnificado=UNIFICADO&dePesquisa=&tipoNuProcesso=UNIFICADO"]

    custom_settings = {
        "INPUT_STRING": None
    }

    def parse_item(self, response):
        processo = TjceCrawlerItem()
        processo = self.build_processo(response)
        yield processo

    def get_codigo_processo(self, response):
        self.codigo_processo = response.css("#processoSelecionado ::attr(value)").get()
        url_2_grau = f'https://esaj.tjce.jus.br/cposg5/show.do?processo.codigo={self.codigo_processo}'
        yield Request(url=url_2_grau, callback=self.build_processo_2_grau)

    def build_processo(self, response):
        processo = TjceCrawlerItem()
        numero_processo = response.css('[id="numeroProcesso"]::text').get().strip().replace("\n", "")
        classe = response.css('[id="classeProcesso"]::text').get()
        area = response.css('[id="areaProcesso"] > span ::text').get()
        assunto = response.css('[id="assuntoProcesso"]::text').get()
        data_distribuicao = response.css('[id="dataHoraDistribuicaoProcesso"]::text').get()[:10]
        juiz = response.css('[id="juizProcesso"]::text').get()
        valor_acao = response.css('[id="valorAcaoProcesso"]::text').get()
        partes = self.build_partes_processo(response)
        movimentacoes = self.build_movimentacoes_processo(response)
        grau = '1º grau' if 'cpopg' in response.url else '2º grau'

        processo['numero_processo'] = numero_processo if numero_processo is not None else ''
        processo['tribunal'] = get_tribunal(response.url)
        processo['url'] = response.url
        processo['grau'] = grau
        processo['classeProcesso'] = classe if classe is not None else ''
        processo['area'] = area if area is not None else ''
        processo['assunto'] = assunto if assunto is not None else ''
        processo['data_distribuicao'] = data_distribuicao if data_distribuicao is not None else ''
        processo['juiz'] = juiz if juiz is not None else ''
        processo['lista_partes_processo'] = partes
        processo['lista_movimentacoes'] = movimentacoes
        processo['valor_acao'] = valor_acao.replace(' ', '') if valor_acao is not None else ''

        return processo

    def build_processo_2_grau(self, response):
        processo = TjceCrawlerItem()
        numero_processo = response.css('[id="numeroProcesso"]::text').get().strip().replace("\n", "")
        classe = response.css('[id="classeProcesso"] > span::text').get()
        area = response.css('[id="areaProcesso"] > span ::text').get()
        assunto = response.css('[id="assuntoProcesso"]::text').get()
        juiz = response.css('[id="orgaoJulgadorProcesso"] > span::text').get() if response.css(
            '[id="orgaoJulgadorProcesso"] > span::text').get() else response.css('[id="varaProcesso"] ::text').get()
        valor_acao = response.css('[id="valorAcaoProcesso"] > span::text').get()
        partes = self.build_partes_processo(response)
        movimentacoes = self.build_movimentacoes_processo(response)
        grau = '1º grau' if 'cpopg' in response.url else '2º grau'

        processo['numero_processo'] = numero_processo if numero_processo is not None else ''
        processo['tribunal'] = get_tribunal(response.url)
        processo['url'] = response.url
        processo['grau'] = grau
        processo['classeProcesso'] = classe if classe is not None else ''
        processo['area'] = area if area is not None else ''
        processo['assunto'] = assunto if assunto is not None else ''
        processo['juiz'] = juiz if juiz is not None else ''
        processo['lista_partes_processo'] = partes
        processo['lista_movimentacoes'] = movimentacoes
        processo['valor_acao'] = valor_acao.replace(' ', '') if valor_acao is not None else ''
        processo['data_distribuicao'] = ''
        return processo

    def build_partes_processo(self, response):
        partes_selector = response.css('[id="tablePartesPrincipais"] > tr')
        partes = {}

        for parte in partes_selector:  # tds
            tipo_participacao = parte.css(".tipoDeParticipacao ::text").get().strip()
            nomes_selector = parte.css(".nomeParteEAdvogado ::text").getall()
            nomes = [nome.strip() for nome in nomes_selector]

            if tipo_participacao not in partes:
                partes[tipo_participacao] = []

            partes[tipo_participacao].extend(nomes)
        return partes

    def build_movimentacoes_processo(self, response):
        movimentacoes_selector = response.css('[id="tabelaTodasMovimentacoes"] > tr')
        movimentacoes = {}

        for movimento in movimentacoes_selector:  # trs
            data_movimentacao = movimento.css("td ::text").get()
            descricao = movimento.css(":nth-child(3)::text").get().strip().replace("\n", "")
            if descricao == "":
                descricao = self.get_url_documento(movimento)
            if data_movimentacao not in movimentacoes:
                movimentacoes[data_movimentacao.strip()] = []

            movimentacoes[data_movimentacao.strip()] = descricao
        return movimentacoes

    def get_url_documento(self, movimento):
        url = movimento.css(":nth-child(3) > a::text").get()
        if url is not None:
            url = url.strip().replace("\n", "").replace("\t", "")
        return url

    def closed(self, reason):
        if reason == 'no_page_found':
            self.crawler.stop(reason="no_page_found")
