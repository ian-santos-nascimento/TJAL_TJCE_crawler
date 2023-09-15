- Documentação da API
- Sumário
- Introdução
- Endpoints da API
    Consultas
- Formato de Requisições e Respostas
- Exemplos de Uso
- Estrutura do Código
- Crawlers


1. Introdução:
Este documento fornece documentação para a API implementada no código. A API permite que os usuários solicitem informações sobre processos até 2 grau de diferentes tribunais (TJAL e TJCE) fornecendo um número de processo e selecionando o tribunal desejado.


2. Endpoints da API 
- Os endpoints estão descritos no link http://127.0.0.1:5000/apidocs/

Consultas
    
    URL: /consultas/
    Método: POST
    Descrição: Inicia um processo de crawler no site do tribunal escolhido para coletar informações sobre um processo até 2 grau.
    Parâmetros da Requisição:
        numero_processo (string, obrigatório): O número do processo a ser pesquisado.
        tribunal (string, obrigatório): O tribunal para coletar dados (pode ser 'tjal' ou 'tjce').

3. Formato de Requisições e Respostas:
- Formato de Requisição


    URL: /consultas/
    Método: POST
    Corpo da Requisição:
    json
    {
        "numero_processo": "string",
        "tribunal": "string"
    }

Formato de Resposta
    Resposta de Sucesso (200 OK):
    json

    [
    {
        "numero_processo": "string",
        "tribunal": "string",
        "area": "string",
        "classeProcesso": "string",
        "assunto": "string",
        "data_distribuicao": "string",
        "juiz": "string",
        "valor_acao": "string",
        "lista_partes_processo": [],
        "lista_movimentacoes": [],
        "grau": "string"
    }
    ]

Resposta de Erro (400 Bad Request):


    {
        "error": "string"
    }

4. Exemplos de Uso
Exemplo 1: Solicitar Informações sobre um processo



    Requisição:
    http
    
    POST /consultas/
    Content-Type: application/json
    
    {
        "numero_processo": "123456789",
        "tribunal": "tjal"
    }

Resposta (Sucesso):

    [
      {
        "area": "Cívil",
        "assunto": "Energia Elétrica",
        "classeProcesso": "Procedimento Comum",
        "data_distribuicao": "29/04/2010",
        "grau": "1 grau",
        "juiz": "Marcelo Guimarães de Aguiar",
        "lista_movimentacoes": {
          "01/04/2014": "Recebidos os autos",
          "01/06/2015": "Conclusos",
          "02/12/2015": "Visto em correi\u00e7\u00e3o| URL: https://www2.tjal.jus.br/cpopg/abrirDocumentoVinculadoMovimentacao.do?processo.codigo=01000BJE00000&cdDocumento=16036154&nmRecursoAcessado=Visto+em+correi%C3%A7%C3%A3o",
          "03/02/2011": "Decurso de Prazo",
          "03/09/2018": "Visto em correi\u00e7\u00e3o| URL: https://www2.tjal.jus.br/cpopg/abrirDocumentoVinculadoMovimentacao.do?processo.codigo=01000BJE00000&cdDocumento=25548520&nmRecursoAcessado=Visto+em+correi%C3%A7%C3%A3o",
          "05/01/2022": "Conclusos",
          "05/08/2011": "Mandado Expedido| URL: https://www2.tjal.jus.br#liberarAutoPorSenha",
          "05/09/2011": "Juntada de Peti\u00e7\u00e3o",
          "06/02/2012": "Certid\u00e3o",
          "06/04/2016": "Despacho de Mero Expediente| URL: https://www2.tjal.jus.br/cpopg/abrirDocumentoVinculadoMovimentacao.do?processo.codigo=01000BJE00000&cdDocumento=16778244&nmRecursoAcessado=Despacho+de+Mero+Expediente",
          "06/05/2013": "Juntada de Peti\u00e7\u00e3o",
          "06/06/2016": "Juntada de Peti\u00e7\u00e3o",
          "06/08/2021": "Visto em Correi\u00e7\u00e3o - CGJ| URL: https://www2.tjal.jus.br/cpopg/abrirDocumentoVinculadoMovimentacao.do?processo.codigo=01000BJE00000&cdDocumento=39288180&nmRecursoAcessado=Visto+em+Correi%C3%A7%C3%A3o+-+CGJ",
          "07/04/2016": "Audi\u00eancia Designada",
          "08/02/2012": "Despacho de Mero Expediente| URL: https://www2.tjal.jus.br/cpopg/abrirDocumentoVinculadoMovimentacao.do?processo.codigo=01000BJE00000&cdDocumento=7010594&nmRecursoAcessado=Despacho+de+Mero+Expediente",
          "08/04/2016": "Disponibiliza\u00e7\u00e3o no Di\u00e1rio da Justi\u00e7a Eletr\u00f4nico",
          "09/11/2011": "Ato ordinat\u00f3rio praticado| URL: https://www2.tjal.jus.br#liberarAutoPorSenha",
          "11/03/2013": "Despacho de Mero Expediente| URL: https://www2.tjal.jus.br/cpopg/abrirDocumentoVinculadoMovimentacao.do?processo.codigo=01000BJE00000&cdDocumento=9344053&nmRecursoAcessado=Despacho+de+Mero+Expediente",
          ...
    },
        "lista_partes_processo": {
          "Autor": [
            "Maia Hamburgueria e Choperia Ltda - ME",
            "Advogado:",
            "Vagner Paes Cavalcanti Filho",
            "Advogado:",
            "Gustavo Ten\u00f3rio Accioly",
            "Representa:",
            "Francisco Edilson Maia da Costa"
          ],
          "Réu": [
            "Companhia Energ\u00e9tica de Alagoas - CEAL",
            "Advogado:",
            "Danielle Ten\u00f3rio Toledo Cavalcante"
          ]
        },
        "numero_processo": "0034520-06.2010.8.02.0001",
        "tribunal": "tjal",
        "valor_acao": "R$510,00"
      }
    ]


Resposta (Erro):
json

    {
        "error": "Número do processo inválido!"
    }

5. Estrutura do Código

O código está estruturado da seguinte forma:

    Importações: Importação de módulos e dependências necessárias.
    Configuração da Aplicação Flask: Criação de uma aplicação web Flask.
    items_queue: Inicialização de uma fila de multiprocessamento para coletar os dados dos crawlers.
    Rota /consultas/: Definição da rota principal para iniciar solicitações de raspagem.
    Funções initilize_tjal_crawler e initilize_tjce_crawler: Funções para inicializar os crawlers do Scrapy.
    Bloco Principal: Inicialização da aplicação Flask quando o script é executado.
    Projetos TJAL e TJCE: Projetos scrapy criados para uso de crawlers em cada tribunal. O principal arquivo está dentro da pasta "spiders", chamada "__init__"

