import scrapy
from scrapy.http import Response


class TrustpilotUkSpider(scrapy.Spider):
    name = "trustpilot_uk"
    allowed_domains = ["uk.trustpilot.com"]
    start_urls = ["https://uk.trustpilot.com/categories"]

    def parse(self, response: Response):
        category_groups = response.css(".paper_paper__1PY90")
        for category_group in category_groups:
            category_name = category_group.css(".link_internal__7XN06::text").extract()
            categories_link = category_group.css(".link_internal__7XN06").xpath("@href").extract()

            for link in categories_link:
                yield response.follow(response.urljoin(link), callback=self.parse_category)

    def parse_category(self, response: Response):
        businesses = response.css(".paper_paper__1PY90")
        _base_url = "https://uk.trustpilot.com"
        for business in businesses:
            business_name = business.css("p.typography_heading-xs__jSwUz::text").extract()
            if business_name:
                business_link = business.css("a.link_internal__7XN06").xpath("@href").extract_first()
                yield response.follow(f"{_base_url}{business_link}", callback=self.parse_business)
                

    
    def parse_business(self, response: Response):
        business_name = response.css("div#business-unit-title h1 span::text").extract_first()
        review_section = response.css(".styles_reviewsContainer__3_GQw")    
        review_header = review_section.css(".styles_header__yrrqf")
        total_reviews = review_header.css("p.typography_body-l__KUYFJ::text").extract_first()
        ratings = review_header.css("h2 span::text").extract_first()
        total_ratings = 5
        
        about_section = response.css(".paper_paper__1PY90.paper_outline__lwsUX.card_card__lQWDv.card_noPadding__D8PcU.styles_sideColumnCard__eyHWa")
        about = about_section.css(".styles_container__9nZxD.customer-generated-content::text").extract_first()

        yield {
            "business_name": business_name,
            "total_reviews": total_reviews,
            "ratings": ratings,
            "total_ratings": total_ratings,
            "about": about,
        }


