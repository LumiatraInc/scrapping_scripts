# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TrustpilotItem(scrapy.Item):
    business_name = scrapy.Field()
    business_about = scrapy.Field()
    business_logo = scrapy.Field()
    business_categories = scrapy.Field()
    is_verified = scrapy.Field()
    business_address = scrapy.Field()
    website = scrapy.Field()
    phone_number = scrapy.Field()
    ratings = scrapy.Field()
    total_ratings = scrapy.Field()
    total_reviews = scrapy.Field()
    business_email = scrapy.Field()

