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
            return Response(data={'error':"Numero do processo inválido!"},status=HTTP_400_BAD_REQUEST)

        json_data = returnItemFromDb(processo)
        if json_data:
            return JsonResponse(json_data, safe=False, status=HTTP_200_OK)
        task, unique_id = scheduleCrawler(processo, tribunal)
        status = scrapyd.job_status(os.getenv('SCRAPY_PROJECT_NAME'), task)

        while status != 'finished':
                status = scrapyd.job_status(os.getenv('SCRAPY_PROJECT_NAME'), task)

        json_data = returnItemFromDb(processo)
        return JsonResponse(json_data, safe=False,status=HTTP_200_OK)


def scheduleCrawler(processo,tribunal):
    project_name = os.getenv('SCRAPY_PROJECT_NAME')
    crawler_name = os.getenv('CRAWLER_NAME')
    unique_id = str(uuid4())  # create a unique ID.

    settings = {
        'unique_id': unique_id,  # unique ID for each record for DB
        'processo': processo
    }
    task = scrapyd.schedule(project=project_name,spider=crawler_name, settings=settings,
                            numero_processo=processo, tribunal=tribunal)
    return task, unique_id

def returnItemFromDb(processo):
    items = Processo.objects.filter(numero_processo=processo)
    if items.exists():
        serialized_data = list(items.values())
        json_data = json.dumps(serialized_data, cls=DjangoJSONEncoder)
        return json_data
    else:
        return None

def processExists(numero):
    pattern = r'^\d{7}-\d{2}\.\d{4}\.\d{1}\.\d{2}\.\d{4}$'
    if re.match(pattern, numero):
        return True
    else:
        return False
