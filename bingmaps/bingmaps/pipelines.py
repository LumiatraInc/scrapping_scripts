import os, json
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem

class BingmapsPipeline:
    def process_item(self, item, spider):
        business = ItemAdapter(item)

        for field, value in business.items():
            if field == "business_name":
                if value is None:
                    raise DropItem(f"Dropped the business")
                else:
                    business[field] = value.strip()
            
            elif field == "business_type":
                if value == ".":
                    business[field] = ""
                if value:
                    business[field] = value.strip()
            
            elif field == "business_about":
                if value is None:
                    business[field] = ""
                else:
                    business[field] = value.strip()
            
            elif field == "phone_number":
                if value is None:
                    business[field] = ""
                else:
                    business[field] = value.replace("tel:", "").strip()
            
        return item


class JsonWriterPipeline:
    def open_spider(self, spider):
        search_term = spider.search_term.replace(" ", ",").strip()
        filename = f"{search_term}.json"
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

