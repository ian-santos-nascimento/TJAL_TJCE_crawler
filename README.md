## DESAFIO
- O desafio é fazer uma API que busque dados de um processo em todos os graus dos Tribunais de Justiça de Alagoas (TJAL) e do Ceará (TJCE). Geralmente o processo começa no primeiro grau e pode subir para o segundo. Você deve buscar o processo em todos os graus e retornar suas informações.
- Será necessário desenvolver crawlers para coletar esses dados no tribunal e uma API para fazer input e buscar o resultado depois.

## Input
- Você deve criar uma API para receber um JSON contendo o número do processo. Para descobrir o tribunal você pode pedir no input ou usar o padrão CNJ de numeração de processos jurídicos.

## Output
- O cliente tem que ser capaz de pegar o dado quando o processamento termina, então você deve criar um mecanismo que permita isso, retornando sempre um JSON para os processos encontrados em todas as esferas.
- Crawlers / Tribunais onde os dados serão coletados
- Tanto o TJAL como o TJCE tem uma interface web para a consulta de processos. O endereço para essas consultas são:
    - TJAL
    - 1º grau - https://www2.tjal.jus.br/cpopg/open.do
    - 2º grau - https://www2.tjal.jus.br/cposg5/open.do
    - TJCE
    - 1º grau - https://esaj.tjce.jus.br/cpopg/open.do
    - 2º grau - https://esaj.tjce.jus.br/cposg5/open.do
    - 
## Dados a serem coletados:
•	classe
•	área
•	assunto
•	data de distribuição
•	juiz
•	valor da ação
•	partes do processo
•	lista das movimentações (data e movimento)

## Premissas: 
- O projeto já foi feito drop em produção e já foi mapeado todos os processos até então. Sendo assim será desenvolvido com isso em mente.

## Exemplos de processos
- 0070337-91.2008.8.06.0001 - TJCE - Até 2ª instância - Teste realizado com sucesso
- 0004017-94.2018.8.06.0167 - TJCE - Até 2ª instância - Teste realizado com sucesso
- 0710802-55.2018.8.02.0001 - TJAL - Até 2ª instância - Teste realizado com sucesso
- 0034520-06.2010.8.02.0001 - TJAL - Até 1ª instância - Teste realizado com sucesso
- 0010484-60.2011.8.02.0001 - TJAL - Até 1ª instância - Teste realizado com sucesso

## Alguns pontos que serão analisados:
-	Organização do código
-	Testes
-	Facilidade ao rodar o projeto
-	Escalabilidade: o quão fácil é escalar os crawlers.
-	Performance: aqui avaliamos o tempo para crawlear todo o processo jurídico
------------------------------------------------------------------------------------------------------------------------------
## DOCUMENTAÇÃO:

### Para detalhes da documentação vá para o arquivo Documentacao.md

#### Como foi estruturado:
- Foi organizado com a premissa de que cada tribunal possuirá um crawler devido a diferênciação de cada site oficial
- Os principais arquivos são: app.py(arquivo da API Flask), TJAL_crawler e TJCE_crawler(pasta que contém a configuração do projeto scrapy de cada crawler), Dockerfile(arquivo Docker para criação da imagem), tests(pasta que contém os testes)
#### Utilização do multiprocessing.Process: 
- Paralelismo: Usando processos separados, a aplicação consegue rodar concorrentemente. Permitindo a API receber novas chamadas enquanto processa dados.
- Isolamento: Se o crawler encontrar um erro ou repentinamente parar, não irá afetar a aplicação. Fazendo os processos rodarem independente
- Escalabilidade: Se necessário, pode ser escalado os crawlers para rodarem em múltiplas instâncias concorrentemente

### Como rodar o projeto local:
- Você deve possuir instalado: python
- Crie uma pasta para a sua venv com "python -m venv venv"
- Ative sua venv de acordo com o sistema operacional. Para Linux navegue até a pasta bin da venv e uso o comando ". activate"
- Já dentro da venv instale os pacotes necessários com "pip install -r requirements.txt" na raiz do projeto
- Para iniciar a api utilize o "flask run"


### Como testar a aplicação
- Para testar a API utilize o arquivo test_api.py. Tenha certeza que a API esteja de pé para este teste
- Para testar os crawlers navegue até "test_jal_crawler" ou "test_tjce_crawler"

### Como fazer deploy num container docker:
- docker build -t api-crawler .  (https://docs.docker.com/engine/reference/commandline/build/)
- docker run --name crawler_container -p 5000:5000 api_crawler (cria um container na porta 5000 de nome crawler_container com a imagem feita acima) (https://docs.docker.com/engine/reference/commandline/run/)

## Arquitetura ideal:
- O ideal seria a implementação da API e dos crawlers isoladamente em orquertradores scrapyd. 
- Fazendo com que a API ativasse o crawler no container scrapyd, ao finalizar o crwaler o pipeline faria inserção no BD e um listener na API aguardaria a finalização e buscasse o dado no BD
- Entretando acabei "descobrindo" essa arquitetura de forma tardia, já com essa implementação. Caso seja da vontade de todos e possibilitarem um tempo maior, consigo implementar essa ideia

## Limitações:
- Caso ocorra um erro ao executar o crawler, ele retorna um status OK com [] ao invés de 500
- Ao pesquisar um processo, se não existir ele ainda tenta fazer um crawl

## Observações e melhorias:
- Pode ser feito uma integração com um BD, que antes de acionar o crawler ele pesquisa na tabela o processo, e caso não existe ele executa o crawler, retorna pra o usuário e salva na tabela(com pipeline).
- Fazer um schedule no GCP para rodar um script que faça um crawler salvar os processos do dia na tabela
- Para escalabilidade penso em microserviços de cada crawler, pois caso existe alguma alteração que derrube o crawler de um TJ ele não afete o uso dos demais.

### Foi-se organizado o código com a premissa de que: Tribunais podem possuir sites diferentes, sendo o ideal então implementar um crawler pra cada TJ