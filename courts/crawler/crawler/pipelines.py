import logging
from django.db import transaction
from asgiref.sync import sync_to_async
from api.models import Processo
import json


logger = logging.getLogger(__name__)


class CrawlerPipeline:

    def __init__(self, unique_id, processo, *args, **kwargs):
        self.unique_id = unique_id
        self.processo = processo
        self.item = {}

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            unique_id=crawler.settings.get('unique_id'),
            processo=crawler.settings.get('processo')  # this will be passed from django view
        )

    async def process_item(self, item, spider):
        self.item = item
        json_string = json.dumps(self.item)
        # Decode the JSON string to remove escape characters
        decoded_data = json.loads(json_string)
        my_model_instance = Processo(
            numero_processo=self.processo,
            data =  decoded_data
        )

        await self.saveDB(my_model_instance)
        return item

    @sync_to_async
    def saveDB(self, item):
        item.save()