# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BingmapsItem(scrapy.Item):
    business_name = scrapy.Field()
    business_link = scrapy.Field()
    business_status = scrapy.Field()
    address = scrapy.Field()
    phone_number = scrapy.Field()
    website = scrapy.Field()
    socials = scrapy.Field()
    rating = scrapy.Field()
    total_reviews = scrapy.Field()
    total_ratings = scrapy.Field()


    
