import os
import re
from uuid import uuid4
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse
from dotenv import load_dotenv
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK
from rest_framework.views import APIView
from scrapyd_api import ScrapydAPI
from .models import Processo

load_dotenv()

scrapyd = ScrapydAPI(os.getenv('SCRAPYD_URL'))


class ApiProcessView(APIView):
    def post(self, request):
        processo = request.data.get('processo')
        tribunal = request.data.get('tribunal')
        if not processExists(processo):
            return Response(data={'error': "Numero do processo inválido!"}, status=HTTP_400_BAD_REQUEST)
        url_courts = urlsForCourt(tribunal, processo)
        if not url_courts:
            return Response(data={'error': "Api não possui suporte para esse tribunal"}, status=HTTP_400_BAD_REQUEST)

        json_data = returnItemFromDb(processo)
        if json_data:
            return JsonResponse(json_data, safe=False, status=HTTP_200_OK)

        task, unique_id = scheduleCrawler(processo, tribunal,url_courts)
        status = scrapyd.job_status(os.getenv('SCRAPY_PROJECT_NAME'), task)
        while status != 'finished':
            status = scrapyd.job_status(os.getenv('SCRAPY_PROJECT_NAME'), task)

        json_data = returnItemFromDb(processo)
        return JsonResponse(json_data, safe=False, status=HTTP_200_OK)


def scheduleCrawler(processo, tribunal, url_courts):
    project_name = os.getenv('SCRAPY_PROJECT_NAME')
    crawler_name = os.getenv('CRAWLER_NAME')
    unique_id = str(uuid4())  # create a unique ID.
    settings = {
        'unique_id': unique_id,  # unique ID for each record for DB
        'processo': processo
    }
    task = scrapyd.schedule(project=project_name, spider=crawler_name, settings=settings,
                            numero_processo=processo, tribunal=tribunal, url_first=url_courts[0], url_second=url_courts[1],url_third=url_courts[2])
    return task, unique_id


def returnItemFromDb(processo):
    items = Processo.objects.filter(numero_processo=processo)
    if items.exists():
        serialized_data = list(items.values())
        return serialized_data
    else:
        return None


def processExists(numero):
    pattern = r'^\d{7}-\d{2}\.\d{4}\.\d{1}\.\d{2}\.\d{4}$'
    if re.match(pattern, numero):
        return True
    else:
        return False


def loadJsonConfig():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    configs_dir = os.path.join(current_dir, '../configs/')
    file_path = os.path.join(configs_dir, 'courts.json')
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        print("\n File not found.")
        return None
    except json.JSONDecodeError:
        print("Error loading JSON.")
        return None


def urlsForCourt(tribunal, processo):
    json_data = loadJsonConfig()
    urls = []
    if json_data and tribunal in json_data:
        tribunal_info = json_data[tribunal]
        for instancia in tribunal_info:
            base_url = instancia.get('base_url')
            dynamic_values = instancia.get('dynamic_values')
            dynamic_values['foro'] = processo[-4:]
            dynamic_values['numero'] = processo
            if 'numero_unificado_value' in dynamic_values:
                dynamic_values['numero_unificado_value'] = processo[:14]
            urls.append(replaceDynamicValues(base_url, dynamic_values))

    return urls

def replaceDynamicValues(base_url, dynamic_values):
    replaced_url = base_url
    for key, value in dynamic_values.items():
        replaced_url = replaced_url.replace(f"{{{key}}}", value)
    return replaced_url
