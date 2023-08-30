from prisma import Client, Prisma
from prisma import models
from .sql import create_process


class TjalCrawlerPipeline:
    print("PIPELINE")

    def process_item(self, item, spider):
        if not item:
            return {}
        self.insert_in_db(item)
        return item

    async def insert_in_db(self, item):
        await create_process(item)
