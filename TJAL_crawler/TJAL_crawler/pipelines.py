from prisma import Client, Prisma
from prisma import models
from .sql import create_process


class TjalCrawlerPipeline:
    def process_item(self, item, spider):
        if not item:
            return {}

        return item

