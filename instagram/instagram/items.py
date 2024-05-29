# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class InstagramItem(scrapy.Item):
    username = scrapy.Field()
    profile_name = scrapy.Field()
    profile_photo = scrapy.Field()
    is_verified = scrapy.Field()
    total_posts = scrapy.Field()
    total_followers = scrapy.Field()
    total_following = scrapy.Field()
    thread_name = scrapy.Field()
    bio_description = scrapy.Field()
    web_link = scrapy.Field()    
    thread_link = scrapy.Field()
    source = scrapy.Field()

