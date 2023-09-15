class TjalCrawlerPipeline:
    def process_item(self, item, spider):
        if not item:
            return {}
        print(item)
        return item

