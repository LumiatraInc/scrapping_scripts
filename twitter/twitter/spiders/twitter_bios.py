import scrapy


class TwitterBiosSpider(scrapy.Spider):
    name = "twitter_bios"
    allowed_domains = ["twitter.com"]
    start_urls = ["https://twitter.com"]

    def parse(self, response):
        pass
