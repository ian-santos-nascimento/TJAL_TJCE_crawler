from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from ..items import TjalCrawlerItem
from scrapy import Request
from urllib.parse import urlsplit


class TjalCrawler(CrawlSpider):
    name = 'TjalCrawler'
    rules = ([
        Rule(LinkExtractor(allow=r"cpopg/",
                           deny=["/abrirDocumentoVinculadoMovimentacao", "jsessionid", "#liberarAutoPorSenha"]),
             callback='parse_item'),
        Rule(LinkExtractor(allow=r"cposg5/search.do", deny="cposg5/show.do"), callback='get_codigo_processo')
    ])

    def __init__(self, input_string=None, codigo_processo = None, *a, **kw):
        super().__init__(*a, **kw)
        self.input_string = input_string
        self.codigo_processo = codigo_processo
        self.start_urls = [
            f'https://www2.tjal.jus.br/cpopg/show.do?processo.foro={self.input_string[-4:]}&processo.numero={self.input_string}',
            f'https://esaj.tjce.jus.br/cpopg/show.do?processo.foro={self.input_string[-4:]}&processo.numero={self.input_string}',
            f'https://www2.tjal.jus.br/cposg5/show.do?processo.codigo={self.codigo_processo}',
            f'https://www2.tjal.jus.br/cposg5/search.do?conversationId=&paginaConsulta=0&cbPesquisa=NUMPROC'
            f'&numeroDigitoAnoUnificado={self.input_string[:14]}&foroNumeroUnificado='
            f'{self.input_string[:-4]}&dePesquisaNuUnificado='
            f'{self.input_string}&dePesquisaNuUnificado=UNIFICADO&dePesquisa=&tipoNuProcesso=UNIFICADO']

    custom_settings = {
        "INPUT_STRING": None
    }

    def parse_item(self, response):
        processo = TjalCrawlerItem()
        print("INPUT" + self.input_string)
        processo = self.build_processo(response)
        yield processo

    def get_codigo_processo(self, response):
        self.codigo_processo = response.css("#processoSelecionado ::attr(value)").get()
        print("get_codigo_processo + URL: " + response.url)
        print("get_codigo_processo + codigo do processo: " + self.codigo_processo)
        yield Request(url=f'https://www2.tjal.jus.br/cposg5/show.do?processo.codigo={self.codigo_processo}', callback=self.build_processo_2_grau)


    def build_processo(self, response):
        print("build_processo. URL:" + response.url)
        processo = TjalCrawlerItem()
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
        processo['tribunal'] = self.get_tribunal(response.url)
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
        print("build_processo. URL:" + response.url)
        processo = TjalCrawlerItem()
        numero_processo = response.css('[id="numeroProcesso"]::text').get().strip().replace("\n", "")
        classe = response.css('[id="classeProcesso"] > span::text').get()
        area = response.css('[id="areaProcesso"] > span ::text').get()
        assunto = response.css('[id="assuntoProcesso"]::text').get()
        juiz = response.css('[id="orgaoJulgadorProcesso"] > span::text').get()
        valor_acao = response.css('[id="valorAcaoProcesso"] > span::text').get()
        partes = self.build_partes_processo(response)
        movimentacoes = self.build_movimentacoes_processo(response)
        grau = '1º grau' if 'cpopg' in response.url else '2º grau'

        processo['numero_processo'] = numero_processo if numero_processo is not None else ''
        processo['tribunal'] = self.get_tribunal(response.url)
        processo['grau'] = grau
        processo['classeProcesso'] = classe if classe is not None else ''
        processo['area'] = area if area is not None else ''
        processo['assunto'] = assunto if assunto is not None else ''
        processo['juiz'] = juiz if juiz is not None else ''
        processo['lista_partes_processo'] = partes
        processo['lista_movimentacoes'] = movimentacoes
        processo['valor_acao'] = valor_acao.replace(' ', '') if valor_acao is not None else ''

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
            data_movimentacao = movimento.css(".dataMovimentacao ::text").get()
            descricao = movimento.css(".descricaoMovimentacao ::text").get()

            if data_movimentacao is None:
                data_movimentacao = movimento.css(".dataMovimentacaoProcesso ::text").get()
                descricao = movimento.css(".descricaoMovimentacaoProcesso ::text").get()
            if descricao == "":
                descricao = self.get_url_documento(response, movimento)
            if data_movimentacao not in movimentacoes:
                movimentacoes[data_movimentacao.strip()] = []

            movimentacoes[data_movimentacao.strip()] = descricao.strip().replace("\n", "")
        return movimentacoes

    def get_url_documento(self, response, movimento):
        base_url = response.url[:27]
        url = movimento.css(".descricaoMovimentacao > a::text").get().strip()
        if movimento.css(".descricaoMovimentacao > a::attr(href)").get().strip() not in "#liberarAutoPorSenha":
            url += "| documento: " + base_url + movimento.css(".descricaoMovimentacao > a::attr(href)").get().strip()
        return url

    def get_tribunal(self, url):
        return url[12:16]