# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TwitterItem(scrapy.Item):
    profile_name = scrapy.Field()
    profile_photo = scrapy.Field()
    cover_photo = scrapy.Field()
    profile_hashtag = scrapy.Field()
    is_verified = scrapy.Field()
    profile_description = scrapy.Field()
    company_type = scrapy.Field()
    web_link = scrapy.Field()
    date_joined = scrapy.Field()
    total_followers = scrapy.Field()
    total_following = scrapy.Field()
    total_posts = scrapy.Field()
    user_location = scrapy.Field()

    