import scrapy


class BingmapSpider(scrapy.Spider):
    name = "bingmap"
    allowed_domains = ["bingmap.com"]
    start_urls = ["https://bingmap.com"]

    def parse(self, response):
        pass
