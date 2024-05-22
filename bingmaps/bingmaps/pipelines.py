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
                    if any(t for t in value if ord(t) > 127):
                        business[field] = value.strip()[1:]
                    else:
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
    

class CorrectedBusinessPhotoUrlsPipeline:
    def process_item(self, item, spider):
        business = ItemAdapter(item)

        if "business_photos" in business.keys():
            corrected_urls = []
            for url in business["business_photos"]:
                if url.startswith("https://"):
                    corrected_urls.append(url)
                elif url.startswith("/th?"):
                    corrected_urls.append(f"https://www.bing.com{url}")

            business["business_photos"] = corrected_urls

        return item


class JsonWriterPipeline:
    def open_spider(self, spider):
        search_term = spider.search_term.replace(" ", "_").strip()
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

