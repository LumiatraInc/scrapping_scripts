# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import re
from itemadapter import ItemAdapter


class GooglemapsPipeline:
    def process_item(self, item, spider):
        business = ItemAdapter(item)

        business_name:str = business["business_name"]
        cleaned_name = business_name.strip()
        business["business_name"] = cleaned_name

        if "business_address" in business and business["business_address"]:
            value:str = business["business_address"]
            cleaned_value = value.replace("Address: ", "").strip()
            business["business_address"] = cleaned_value

        if "phone_number" in business and business["phone_number"]:
            value:str = business["phone_number"]
            cleaned_value = value.replace("Phone: ", "").strip()
            business["phone_number"] = cleaned_value

        if "website" in business and business["website"]:
            value:str = business["website"]
            cleaned_value = value.replace("Website: ", "").strip()
            business["website"] = cleaned_value

        if "total_reviews" in business and business["total_reviews"]:
            value:str = business["total_reviews"]
            cleaned_value = value.replace("reviews", "").strip()
            business["total_reviews"] = cleaned_value
        
        if "ratings" in business and business["ratings"]:
            value:str = business["ratings"]
            cleaned_value = float(value.strip())
            business["ratings"] = cleaned_value

        if "socials" in business and business["socials"]:
            socials:dict = business["socials"]
            if socials.get("instagram"):
                value:str = socials["instagram"]
                cleaned_value = value.replace(" › ", "/") + "/"
                business["socials"]["instagram"] = cleaned_value

            if socials.get("facebook"):
                value:str = socials["facebook"]
                if " › ... › " in value:
                    cleaned_value = value.replace(" › ... › ", "/")
                elif " › " in value:
                    cleaned_value = value.replace(" › ", "/")
                business["socials"]["facebook"] = cleaned_value

            if socials.get("other_links"):
                if business.get("website"):
                    values:list[str] = socials["other_links"]
                    cleaned_data = [value for value in values if business["website"] not in value]
                    business["socials"]["other_links"] = cleaned_data
        
        
        if "photos" in business and business["photos"]:
            values:list[str] = business["photos"]
            
            clean_urls = []
            for value in values:
                pattern = r'https://.*?k-no'
                matches = re.findall(pattern, value)
                if matches:
                    clean_urls.append(matches[0])

            business["photos"] = clean_urls
        return item
    

