import os, json
from itemadapter import ItemAdapter


class InstagramPipeline:
    def process_item(self, item, spider):
        return item


class JsonWriterPipeline:
    def open_spider(self, spider):
        filename = "instagram_profile.json"
        self.file = open(filename, 'w', encoding='utf-8')
        self.file.write("[")

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + ",\n"
        self.file.write(line)
        
        return item

    def close_spider(self, spider):
        self.file.seek(self.file.tell() - 2, os.SEEK_SET)
        self.file.write("]\n")
        self.file.close()

