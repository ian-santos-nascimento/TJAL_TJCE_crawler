import queue

from flask import Flask, request, jsonify
from multiprocessing import Process, Queue
from scrapy import signals
from scrapy.crawler import CrawlerProcess
from scrapy.signalmanager import dispatcher
from scrapy.utils.project import get_project_settings
from TJAL_crawler.TJAL_crawler.spiders import TjalCrawler
from TJCE_crawler.TJCE_crawler.spiders import TjceCrawler
from utils import processo_existe
import time

app = Flask(__name__)

# ...

items_queue = Queue()  # Queue to collect scraped items

@app.route("/consultas/", methods=['POST'])
def consultar():
    try:
        data = request.get_json()  # Extract JSON data from request
        numero_processo = data['numero_processo']
        tribunal = data['tribunal']
        processo_existe(numero_processo)

        if tribunal == 'tjal':
            p = Process(target=initilize_tjal_crawler, args=(items_queue, numero_processo))
        else:
            p = Process(target=initilize_tjce_crawler, args=(items_queue, numero_processo))

        p.start()
        p.join()  # Wait for the process to finish

        items = []
        while True:
            try:
                item = items_queue.get_nowait()
                items.append(item)
            except queue.Empty:
                break


        formatted_items = []
        for item in items:
            formatted_item = {
                "numero_processo": item['numero_processo'],
                "tribunal": item['tribunal'],
                "area": item['area'],
                "classeProcesso": item['classeProcesso'],
                "data_distribuicao": item['data_distribuicao'],
                "juiz": item['juiz'],
                "valor_acao": item['valor_acao'],
                "lista_partes_processo": item['lista_partes_processo'],
                "lista_movimentacoes": item['lista_movimentacoes'],
                "grau": item['grau'],

            }
            formatted_items.append(formatted_item)

        return jsonify(formatted_items)


    except Exception as e:
        error_message = str(e)
        return jsonify({
            'error': error_message
        }), 400

# ...

def initilize_tjal_crawler(queue, numero_processo):
    def collect_items(item):
        print("Adding item to queue:", item)
        print('AREA' + item['area'])
        queue.put(item)

    process = CrawlerProcess(settings=get_project_settings())
    crawler = process.create_crawler(TjalCrawler)
    dispatcher.connect(collect_items, signal=signals.item_scraped)
    process.crawl(crawler, input_string=numero_processo)
    process.start()

def initilize_tjce_crawler(items_queue, numero_processo):
    def collect_items(item):
        items_queue.append(dict(item))

    process = CrawlerProcess(settings=get_project_settings())
    crawler = process.create_crawler(TjceCrawler)
    dispatcher.connect(collect_items, signal=signals.item_scraped)
    process.crawl(crawler, input_string=numero_processo)
    process.start()

# ...



if __name__ == '__main__':
    app.run()
