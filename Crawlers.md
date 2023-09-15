# Sumário

    Introdução
    Objetivo
    Funcionalidades
    Requisitos
    Instruções de Uso
    Estrutura do Código

1. Introdução:

Esta documentação descreve um script de web crawler desenvolvido para coletar informações de páginas da web. O script foi projetado para atender às necessidades específicas de coleta de dados dos tribunais TJAL e TJCE.

2. Objetivo <a name="objetivo"></a>

O objetivo principal deste script é adquirir informações de processos no 1º e 2º grau.

O script do web crawler possui as seguintes funcionalidades:

    Coleta de campos de processos em tribunais específicos.
    Identificação de informações como número do processo, classe, área, assunto, juiz, valor da ação, partes envolvidas e movimentações do processo.
    Suporte para adquirição de informações em diferentes graus judiciais (1º grau e 2º grau).

4. Requisitos

Antes de usar o script do web crawler, é necessário ter os seguintes requisitos instalados:

    Python (versão 3.1.0)
    Scrapy (versão 2.10.0)
    Outras dependências necessárias (arquivo requirements.txt)

5. Instruções de Uso

Para usar o script do web crawler, siga estas instruções:

    Configuração do Ambiente: Certifique-se de que você tenha o Python e o Scrapy instalados em seu ambiente.

    Execução do Script: Execute o script do web crawler, fornecendo o parâmetro "input_string" com o número do processo. e.g scrapy crawl TjalCrawler -a input_string=0710802-55.2018.8.02.0001

    Coleta de Dados: O script irá acessar a página da web do tribunal, coletar as informações especificadas e armazená-las em uma estrutura de dados.

    Saída de Dados: As informações coletadas são imprimidas no console

6. Estrutura do Código

O script do web crawler está organizado em várias funções que realizam as seguintes tarefas:

    Inicialização e configuração do crawler.
    Definição de regras de raspagem.
    Coleta de informações do processo.
    Construção das partes envolvidas e das movimentações do processo.
    Tratamento de exceções e encerramento adequado do crawler.


# Estruturação dos Crawlers:
    
    Para melhor exclusividade do crawler na página do processo, foi-se criado "Rules" para controlar o acesso do crawler a determinados links. Foi feito o mapeaemnto dos links para que seja negado tudo que não seja processo em si
    Utilizamos a variável reservada do scrapy "start_urls" para passar a url de todos os sites que iremos fazer o crawler. Com isso foi visto 3 possibildades ao se pesquisar num processo
   - Ele pode possuir apenas 1° grau
   - Ele pode estar no 2° grau entretanto ele é redirecionado antes para um modal para escolher o processo
   - Ele pode ir direto para o processo de 2° grau
   - Com isso temos 3 urls para verificarmos no total
     
### Pensando nesse formato, o código foi escrito para que:
- Primeiro busca o processo no 1°, que num cenário perfeito irá sempre retornar
- Tenta verificar no link de redirecionamento se existe um modal para ser observado, obtendo o self.codigo_processo
- Caso exista um código do processo, ele é usado para acessar o 2° grau do processo. Caso não exista, ele acessa diretamente utilizando o index 1 do array de urls
- O método que constrói o processo no 1° grau é diferente do 2° porque existem campos que apenas estão presentes nos de 2º
