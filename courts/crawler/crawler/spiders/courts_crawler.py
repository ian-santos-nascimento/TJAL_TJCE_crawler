from scrapy import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from datetime import datetime

class Crawler(CrawlSpider):
    name = 'Crawler'
    rules = ([
        Rule(LinkExtractor(allow=r"cpopg/",
                           deny=["/abrirDocumentoVinculadoMovimentacao", "jsessionid", "#liberarAutoPorSenha",
                                 '/open.do'])),
    ])

    def __init__(self, numero_processo=None, tribunal=None, *a, **kw):
        super().__init__(*a, **kw)
        self.input_string = numero_processo
        self.tribunal = tribunal
        self.codigo_processo = ""
        if tribunal == 'tjal':
            self.start_urls = [
                f'https://www2.tjal.jus.br/cpopg/show.do?processo.foro={self.input_string[-4:]}&processo.numero={self.input_string}',
                f'https://www2.tjal.jus.br/cposg5/search.do?conversationId=&paginaConsulta=0&cbPesquisa=NUMPROC'
                f'&numeroDigitoAnoUnificado={self.input_string[:14]}&foroNumeroUnificado='
                f'{self.input_string[:-4]}&dePesquisaNuUnificado='
                f'{self.input_string}&dePesquisaNuUnificado=UNIFICADO&dePesquisa=&tipoNuProcesso=UNIFICADO']
        else:
            self.start_urls = [
                f'https://esaj.tjce.jus.br/cpopg/show.do?processo.foro={self.input_string[-4:]}&processo.numero={self.input_string}',
                f'https://esaj.tjce.jus.br/cposg5/search.do?conversationId=&paginaConsulta=0&cbPesquisa=NUMPROC'
                f'&numeroDigitoAnoUnificado={self.input_string[:14]}&foroNumeroUnificado='
                f'{self.input_string[:-4]}&dePesquisaNuUnificado='
                f'{self.input_string}&dePesquisaNuUnificado=UNIFICADO&dePesquisa=&tipoNuProcesso=UNIFICADO']

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url, callback=self.parse_item)

    def parse_item(self, response):
        self.codigo_processo = response.css("#processoSelecionado ::attr(value)").get()
        if response.url[25:31] == 'cposg5':
            url_2_grau = f'https://www2.tjal.jus.br/cposg5/show.do?processo.codigo={self.codigo_processo}' if self.codigo_processo is not None else self.start_urls[1]
            yield Request(url=url_2_grau, callback=self.build_processo_2_grau, dont_filter=True)
        else:
            yield Request(url=response.url, callback=self.build_processo, dont_filter=True)

    def build_processo(self, response):
        processo ={}
        numero_processo = response.css('[id="numeroProcesso"]::text').get().strip().replace("\n", "")
        classe = response.css('[id="classeProcesso"]::text').get()
        area = response.css('[id="areaProcesso"] > span ::text').get()
        assunto = response.css('[id="assuntoProcesso"]::text').get()
        data_distribuicao = response.css('[id="dataHoraDistribuicaoProcesso"]::text').get()[:10]
        juiz = response.css('[id="juizProcesso"]::text').get()
        valor_acao = response.css('[id="valorAcaoProcesso"]::text').get()
        partes = self.build_partes_processo(response)
        movimentacoes = self.build_movimentacoes_processo(response)
        grau = '1º grau'

        processo['numero_processo'] = numero_processo if numero_processo is not None else ''
        processo['tribunal'] = self.get_tribunal(response.url)
        processo['grau'] = grau
        processo['classe_processo'] = classe if classe is not None else ''
        processo['area'] = area if area is not None else ''
        processo['assunto'] = assunto if assunto is not None else ''
        processo['data_distribuicao'] = self.format_data(data_distribuicao) if data_distribuicao is not None else ''
        processo['juiz'] = juiz if juiz is not None else ''
        processo['lista_partes_processo'] = partes
        processo['lista_movimentacoes'] = movimentacoes
        processo['valor_acao'] = valor_acao.replace(' ', '').replace('R$', '') if valor_acao is not None else ''

        return processo

    def build_processo_2_grau(self, response):
        processo = {}
        numero_processo = response.css('[id="numeroProcesso"]::text').get().strip().replace("\n", "")
        classe = response.css('[id="classeProcesso"] > span::text').get()
        area = response.css('[id="areaProcesso"] > span ::text').get()
        assunto = response.css('[id="assuntoProcesso"] > span ::text').get()
        juiz = response.css('[id="orgaoJulgadorProcesso"] > span::text').get()
        valor_acao = response.css('[id="valorAcaoProcesso"] > span::text').get()
        partes = self.build_partes_processo(response)
        movimentacoes = self.build_movimentacoes_processo(response)
        grau = '2º grau'

        processo['numero_processo'] = numero_processo if numero_processo is not None else ''
        processo['tribunal'] = self.get_tribunal(response.url)
        processo['grau'] = grau
        processo['classe_processo'] = classe if classe is not None else ''
        processo['area'] = area if area is not None else ''
        processo['assunto'] = assunto if assunto is not None else ''
        processo['juiz'] = juiz if juiz is not None else ''
        processo['lista_partes_processo'] = partes
        processo['lista_movimentacoes'] = movimentacoes
        processo['valor_acao'] = valor_acao.replace(' ', '').replace('R$', '') if valor_acao is not None else ''
        processo['data_distribuicao'] = ''

        return processo

    def build_partes_processo(self, response):
        partes_selector = response.css('[id="tablePartesPrincipais"] > tr')
        partes = {}

        for parte in partes_selector:  # tds
            tipo_participacao = parte.css(".tipoDeParticipacao ::text").get().strip()
            nomes_selector = parte.css(".nomeParteEAdvogado ::text").getall()
            nomes = [nome.replace("&nbsp","").strip() for nome in nomes_selector if nome.strip()]

            if tipo_participacao not in partes:
                partes[tipo_participacao] = ''

            partes[tipo_participacao] = nomes
        return partes

    def build_movimentacoes_processo(self, response):
        movimentacoes_selector = response.css('[id="tabelaTodasMovimentacoes"] > tr')
        movimentacoes = {}

        for movimento in movimentacoes_selector:  # trs
            data_movimentacao = movimento.css("td ::text").get()
            descricao = movimento.css(":nth-child(3)::text").get().strip().replace("\n", "")
            if descricao == "":
                descricao = self.get_url_documento(movimento, response)
            if data_movimentacao not in movimentacoes:
                movimentacoes[data_movimentacao.strip()] = []

            movimentacoes[data_movimentacao.strip()] = descricao

        return movimentacoes

    def get_url_documento(self, movimento, response):
        url = movimento.css(":nth-child(3) > a::text").get()
        base_url = response.url[:24]
        if url is not None:
            url = url.strip().replace("\n", "").replace("\t", "") + "| URL: " + base_url + movimento.css(
                ":nth-child(3) > a::attr(href)").get()
        return url

    def get_tribunal(self,url):
        return url[13:17]

    def format_data(self, data):
        data = datetime.strptime(data, '%d/%m/%Y')
        return data.strftime('%Y-%m-%d')

    def closed(self, reason):
        if reason == 'no_page_found':
            self.crawler.stop(reason="no_page_found")

    def clean_and_concat(self,values):
        return ';'.join(filter(None, (v.strip() for v in values)))

