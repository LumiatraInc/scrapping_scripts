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
