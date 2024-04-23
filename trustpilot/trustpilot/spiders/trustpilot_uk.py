import scrapy
from scrapy.http import Response
# items
from trustpilot.items import TrustpilotItem


class TrustpilotUkSpider(scrapy.Spider):
    name = "trustpilot_uk"
    # allowed_domains = ["uk.trustpilot.com"]
    start_urls = [
        "https://de.trustpilot.com/categories",
        "https://uk.trustpilot.com/categories", 
        "https://dk.trustpilot.com/categories",
        "https://at.trustpilot.com/categories",
        "https://ch.trustpilot.com/categories",
        "https://au.trustpilot.com/categories",
        "https://ca.trustpilot.com/categories",
        "https://uk.trustpilot.com/categories"
        "https://ie.trustpilot.com/categories",
        "https://nz.trustpilot.com/categories",
        "https://www.trustpilot.com/categories",
        "https://es.trustpilot.com/categories",
        "https://fi.trustpilot.com/categories",
        "https://fr-be.trustpilot.com/categories",
        "https://nl-be.trustpilot.com/categories",
        "https://fr.trustpilot.com/categories",
        "https://it.trustpilot.com/categories",
        "https://jp.trustpilot.com/categories",
        "https://no.trustpilot.com/categories",
        "https://pl.trustpilot.com/categories",
        "https://nl.trustpilot.com/categories",
        "https://br.trustpilot.com/categories",
        "https://pt.trustpilot.com/categories",
        "https://se.trustpilot.com/categories",
    ]

    def parse(self, response: Response):
        category_groups = response.css(".paper_paper__1PY90")
        for category_group in category_groups:
            category_name = category_group.css(
                ".link_internal__7XN06::text").extract()
            categories_link = category_group.css(
                ".link_internal__7XN06").xpath("@href").extract()

            for link in categories_link:
                yield response.follow(response.urljoin(link), callback=self.parse_category)

    def parse_category(self, response: Response):
        businesses = response.css(".paper_paper__1PY90")
        _base_url = "https://uk.trustpilot.com"
        for business in businesses:
            business_name = business.css(
                "p.typography_heading-xs__jSwUz::text").extract()
            if business_name:
                business_link = business.css(
                    "a.link_internal__7XN06").xpath("@href").extract_first()
                yield response.follow(f"{_base_url}{business_link}", callback=self.parse_business)

    def parse_business(self, response: Response):
        business = TrustpilotItem()

        business_name = response.css(
            "div#business-unit-title h1 span::text").get()
        review_section = response.css(".styles_reviewsContainer__3_GQw")
        review_header = review_section.css(".styles_header__yrrqf")
        total_reviews = review_header.css(
            "p.typography_body-l__KUYFJ::text").get()
        ratings = review_header.css("h2 span::text").get()
        total_ratings = 5

        about_section = response.css(
            ".paper_paper__1PY90.paper_outline__lwsUX.card_card__lQWDv.card_noPadding__D8PcU.styles_sideColumnCard__eyHWa")
        about = about_section.css(
            ".styles_container__9nZxD.customer-generated-content::text").get()

        image_link = response.css(
            ".profile-image_imageWrapper__kDdWe picture img.business-profile-image_image__jCBDc::attr(src)").get()

        business_info = response.css(".styles_businessInformation__6ks_E")
        website_badge = business_info.css(".styles_badgesWrapper__6VasU")
        website_link = website_badge.css(
            ".styles_cardBadge__LeaaQ a::attr(href)").get()

        about_section = response.css(
            ".card_cardContent__sFUOe.styles_cardContent__sQHcU")
        contact_section = about_section[1]
        contact_links: list = contact_section.css("a::attr(href)").getall()
        email = None
        phone_number = None
        if contact_links:
            email, phone_number = contact_links

        is_verified = None
        verified_section = response.css(
            ".styles_mainContent__nFxAv aside .paper_outline__lwsUX .styles_listItem__7beWu span button span::text").getall()
        if len(verified_section) > 1:
            is_verified = verified_section[1]

        business_categories = None
        category_names = response.css("nav li a::text").getall()
        if category_names:
            business_categories = category_names[:-1]

        category_links = response.css("nav li a::attr(href)").getall()

        category_name_link: list[dict] = []
        for name, link in zip(business_categories, category_links):
            category_name_link.append(
                {"category_name": name, "category_link": link})

        address = None
        address_list = contact_section.css("ul li ul li::text").getall()
        if address_list:
            address = ",".join(address_list)

        business["business_name"] = business_name
        business["total_reviews"] = total_reviews
        business["ratings"] = ratings
        business["total_ratings"] = total_ratings
        business["business_about"] = about
        business["business_logo"] = image_link
        business["website"] = website_link
        business["business_email"] = email
        business["phone_number"] = phone_number
        business["is_verified"] = is_verified
        business["business_categories"] = category_name_link
        business["business_address"] = address

        yield business
