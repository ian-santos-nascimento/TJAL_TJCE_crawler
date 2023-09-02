class TjalCrawlerPipeline:
    def process_item(self, item, spider):
        if not item:
            return {}

        return item

