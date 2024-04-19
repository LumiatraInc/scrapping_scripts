import scrapy
from scrapy import Spider
from scrapy.http import Response


class YellowPagesUKSpider(Spider):
    name = "yellow_pages_uk"
    start_urls = [
        "https://www.yell.com/k/popular+searches.html",
    ]

    def parse(self, response: Response):
        searches = response.css("div.findLinks--item")
        for search in searches:
            search_term = search.css("a::text").extract_first()
            search_term_link = search.css("a").xpath("@href").extract()
            yield {
                "search_term": search_term,
                "search_term_link": search_term_link,
            }

