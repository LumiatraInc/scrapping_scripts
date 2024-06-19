import scrapy


class YandexBusinessSpider(scrapy.Spider):
    name = "yandex_business"
    allowed_domains = ["yandex.com"]
    start_urls = ["https://yandex.com/maps"]

    def parse(self, response):
        pass
