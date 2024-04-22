import scrapy


class TrustpilotUkSpider(scrapy.Spider):
    name = "trustpilot_uk"
    allowed_domains = ["uk.trustpilot.com"]
    start_urls = ["https://uk.trustpilot.com/categories"]

    def parse(self, response):
        pass
