# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class GooglemapsItem(scrapy.Item):
    business_name = scrapy.Field()
    map_link = scrapy.Field()
    search_term = scrapy.Field()
    business_about = scrapy.Field()
    business_type = scrapy.Field()
    business_closed = scrapy.Field()
    business_address = scrapy.Field()
    business_hours = scrapy.Field()
    phone_number = scrapy.Field()
    website = scrapy.Field()
    services = scrapy.Field()
    photos = scrapy.Field()
    ratings = scrapy.Field()
    total_ratings = scrapy.Field()
    total_reviews = scrapy.Field()
    reviews = scrapy.Field()
    instagram_link = scrapy.Field()
    x_link = scrapy.Field()
    youtube_link = scrapy.Field()
    facebook_link = scrapy.Field()
    pinterest_link = scrapy.Field()

