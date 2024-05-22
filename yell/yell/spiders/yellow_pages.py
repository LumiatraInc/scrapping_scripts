import scrapy


class YellowPagesSpider(scrapy.Spider):
    name = "yellow_pages"
    allowed_domains = ["yell.com"]
    start_urls = ["https://www.yell.com/k/popular+searches.html"]

    def parse(self, response):
        pass
