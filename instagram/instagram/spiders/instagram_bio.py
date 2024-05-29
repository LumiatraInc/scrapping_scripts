import scrapy


class InstagramBioSpider(scrapy.Spider):
    name = "instagram_bio"
    allowed_domains = ["instagram.com"]
    start_urls = ["https://instagram.com"]

    def parse(self, response):
        pass
