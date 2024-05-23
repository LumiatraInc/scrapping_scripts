# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import os, json
from itemadapter import ItemAdapter


class TwitterPipeline:
    def process_item(self, item, spider):
        return item


class JsonWriterPipeline:
    def open_spider(self, spider):
        filename = "twitter_profile.json"
        self.file = open(filename, 'w')
        self.file.write("[")

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + ",\n"
        self.file.write(line)
        
        return item

    def close_spider(self, spider):
        self.file.seek(self.file.tell() - 2, os.SEEK_SET)
        self.file.write("]\n")
        self.file.close()

