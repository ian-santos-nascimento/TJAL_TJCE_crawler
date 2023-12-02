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
        if not processoExiste(processo):
            return Response(status=HTTP_400_BAD_REQUEST)

        task, unique_id = scheduleCrawler(processo)
        print("task" + task)
        print("UNIQUE_ID" + unique_id)
        status = scrapyd.job_status(os.getenv('SCRAPY_PROJECT_NAME'), task)
        while status != 'finished':
                status = scrapyd.job_status(os.getenv('SCRAPY_PROJECT_NAME'), task)
        items = Processo.objects.filter(numero_processo=processo)
        serialized_data = list(items.values())
        json_data = json.dumps(serialized_data, cls=DjangoJSONEncoder)
        return JsonResponse(json_data, safe=False,status=HTTP_200_OK)


def scheduleCrawler(processo):
    project_name = os.getenv('SCRAPY_PROJECT_NAME')
    crawler_name = os.getenv('CRAWLER_NAME')
    unique_id = str(uuid4())  # create a unique ID.

    settings = {
        'unique_id': unique_id,  # unique ID for each record for DB
        'processo': processo
    }
    task = scrapyd.schedule(project=project_name,spider=crawler_name, settings=settings,
                            input_string=processo)
    return task, unique_id



def processoExiste(numero):
    padrao = r'^\d{7}-\d{2}\.\d{4}\.\d{1}\.\d{2}\.\d{4}$'
    if re.match(padrao, numero):
        return True
    else:
        return False
