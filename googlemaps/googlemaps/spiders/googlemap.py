import time
import scrapy
from scrapy.responsetypes import Response
from scrapy.selector import Selector
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# items
from googlemaps.items import GooglemapsItem


class GooglemapSpider(scrapy.Spider):
    name = "googlemap"
    allowed_domains = ["google.com", ]
    start_urls = [
        "https://www.google.com/maps/@-1.2082248,36.9218576,15z?entry=ttu"]

    def __init__(self):
        self.driver = webdriver.Chrome()
        self.search_term = "clubs in London"

    def parse(self, response: Response):
        self.driver.get(response.url)
        WebDriverWait(self.driver, 180).until(
            lambda driver: driver.execute_script(
                "return document.readyState") == "complete"
        )
        # time.sleep(120)

        search_box = self.driver.find_element(By.ID, "searchboxinput")
        search_box.send_keys(self.search_term)
        search_box.send_keys(Keys.RETURN)
        WebDriverWait(self.driver, 10).until(
            lambda driver: driver.execute_script(
                "return document.readyState") == "complete"
        )
        # time.sleep(60)

        business_listings_section = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "div.aIFcqe div.m6QErb div.m6QErb.DxyBCb div.m6QErb.DxyBCb.kA9KIf"))
        )

        time.sleep(5)

        # scroll to load more businesses
        # while True:
        #     self.driver.execute_script(
        #         'arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;', business_listings_section)
        #     time.sleep(5)
        #     try:
        #         # if this element becomes visible, stop scrolling
        #         end_of_list_element = self.driver.find_element(
        #             By.CSS_SELECTOR, "div.m6QErb.tLjsW.eKbjU div.PbZDve p span span.HlvSq")
        #         break
        #     except Exception as e:
        #         continue

        selector = Selector(text=self.driver.page_source)

        results_section = selector.css(
            'div.m6QErb.DxyBCb.kA9KIf.dS8AEf.ecceSd div')

        businesses = results_section.css(
            "div div.Nv2PK.THOPZb.CpccDe")
        print(f"We have {len(businesses)} businesses")

        for business in businesses:
            time.sleep(5)
            business_link = business.css("a.hfpxzc::attr(href)").get()
            yield self.parse_business(business_link, self.search_term)

        self.driver.quit()

    def parse_business(self, url: str, search_term: str) -> GooglemapsItem:
        self.driver.get(url)
        WebDriverWait(self.driver, 180).until(
            lambda driver: driver.execute_script(
                "return document.readyState") == "complete"
        )
        # time.sleep(120)

        selector = Selector(text=self.driver.page_source)
        business = GooglemapsItem()

        business_section = selector.css("div.aIFcqe div.m6QErb.WNBkOb").get()
        if business_section:
            business_name = selector.css(
                "div.tAiQdd div.lMbq3e div h1.DUwDvf.lfPIob::text").get()
            business_type = selector.css(
                "div.LBgpqf div.skqShb div.fontBodyMedium span span button.DkEaL::text").get()

            business_address: str = None
            business_about: str = None
            website: str = None
            phone_number: str = None
            socials = None
            reviews: list[dict] = None

            business_about_div = selector.css(
                f"div.y0K5Df[aria-label='About {business_name}'] button.XJ8h0e div div div.PYvSYb")
            business_address_btn = selector.css(
                "div.m6QErb div.RcCsl button.CsEnBe[data-item-id='address']")
            website_link = selector.css(
                "div.m6QErb div.RcCsl a.CsEnBe[data-item-id='authority']")
            phone_number_btn = selector.css(
                "div button.CsEnBe[aria-label*='Phone:']")

            if business_about_div:
                business_about = business_about_div.css("::text").get()

            if business_address_btn:
                business_address = business_address_btn.css(
                    "::attr(aria-label)").get()

            if website_link:
                website = website_link.css("::attr(aria-label)").get()

            if phone_number_btn:
                phone_number = phone_number_btn.css("::attr(aria-label)").get()

            services = self.get_business_services(business_name=business_name)

            rating_section = selector.css("div.PPCwl div.Bd93Zb div.jANrlb")
            ratings = rating_section.css("div.fontDisplayLarge::text").get()

            total_reviews = rating_section.css(
                "button.HHrUdb.fontTitleSmall.rqjGif span::text").get()

            # get business photos

            print("=================== get business photos")

            image_links = self.get_business_photos(business_name=business_name)

            # get business reviews

            reviews = self.get_business_reviews()
            

            # get business socials

            print("==================== get business socials")

            socials = self.get_business_socials()

            self.driver.back()
            time.sleep(5)

            selector = Selector(text=self.driver.page_source)

            business["search_term"] = search_term
            business["business_name"] = business_name
            business["business_about"] = business_about
            business["services"] = services
            business["map_link"] = url
            business["business_type"] = business_type
            business["business_address"] = business_address
            business["phone_number"] = phone_number
            business["website"] = website
            business["total_ratings"] = 5
            business["ratings"] = ratings
            business["total_reviews"] = total_reviews
            business["photos"] = image_links
            business["socials"] = socials
            business["reviews"] = reviews

        return business

    def get_business_photos(self, business_name: str) -> list[str] | None:
        try:
            business_div = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "div.w6VYqd div.bJzME.tTVLSc div.k7jAl.miFGmb.lJ3Kh  div.e07Vkf.kA9KIf"))
            )

            all_photos_btn = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "div.cRLbXd div.dryRY div.ofKBgf button.K4UgGe[aria-label='All']"))
            )

            # scroll to the photos section
            while True:
                self.driver.execute_script(
                    'arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;', business_div)
                try:
                    if all_photos_btn.is_enabled() and all_photos_btn.is_displayed():
                        break
                except Exception as e:
                    time.sleep(1)

            time.sleep(5)

            all_photos_btn.click()

            image_links = None

            business_photos_section = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, f"div.aIFcqe div.m6QErb.Hk4XGb[aria-label='Photos of {business_name}'] div.m6QErb.DxyBCb.kA9KIf.dS8AEf div.m6QErb"))
            )
            time.sleep(1)

            selector = Selector(text=self.driver.page_source)
            image_divs = selector.css(
                f"div.aIFcqe div.m6QErb.Hk4XGb[aria-label='Photos of {business_name}'] div.m6QErb.DxyBCb.kA9KIf.dS8AEf div.m6QErb div div a div.U39Pmb[role='img']")
            if image_divs:
                image_links = image_divs.css("::attr(style)").getall()

            cancel_button = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "div#image-header div button.b3vVFf")
                )
            )
            
            time.sleep(1)
            cancel_button.click()
            return image_links

        except Exception as e:
            print("An error occurred while getting {business_name} photos {e}")
            cancel_button.click()
            return None

    def get_business_reviews(self) -> list[dict]:
        business_div = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "div.w6VYqd div.bJzME.tTVLSc div.k7jAl.miFGmb.lJ3Kh  div.e07Vkf.kA9KIf"))
        )

        while True:
                self.driver.execute_script(
                    'arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;', business_div)
                try:
                    about_this_data = self.driver.find_element(
                        By.CSS_SELECTOR, "div.ZM8Zp div div iframe.rvN3ke")
                    time.sleep(5)
                    if about_this_data.is_displayed() and about_this_data.is_enabled():
                        break
                except Exception as e:
                    time.sleep(1)

        selector = Selector(text=self.driver.page_source)

        review_list = selector.css("div.aIFcqe > div.m6QErb.WNBkOb > div.jftiEf.fontBodyMedium")
        print(f"=============================== We have {len(review_list)} reviews")

        reviews:list[dict] = []
        for review in review_list:
            reviewer_name = review.css("div div.jJc9Ad div.GHT2ce.NsCY4 div div.WNxzHc.qLhwHc button.al6Kxe div.d4r55::text").get()
            review_duration = review.css("div div.jJc9Ad div.GHT2ce div.DU9Pgb span.rsqaWe::text").get()
            review_stars = review.css("div div.jJc9Ad div.GHT2ce div.DU9Pgb span.kvMYJc::attr(aria-label)").get()
            review_comment = review.css("div div.jJc9Ad div.GHT2ce div div.MyEned span.wiI7pd::text").get()
            reviews.append({
                "reviewer_name": reviewer_name,
                "reviewer_duration": review_duration,
                "review_stars": review_stars,
                "review_comment": review_comment,
            })

        return reviews

    def get_business_services(self, business_name: str) -> dict[str, list[str]] | None:
        try:
            about_btn = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR,
                     f"div.RWPxGd[role='tablist'] button[aria-label='About {business_name}']")
                )
            )
            about_btn.click()
            time.sleep(2)

            selector = Selector(text=self.driver.page_source)

            about_sections = selector.css(
                "div.m6QErb.DxyBCb.kA9KIf.dS8AEf div.iP2t7d.fontBodyMedium")

            interested_options = []
            highlights_options = []
            offerings_options = []
            amenities_options = []
            crowd_options = []
            planning_options = []
            payment_options = []
            accesibility_options = []
            dining_options = []
            atmosphere_options = []
            parking_options = []

            for section in about_sections:
                section_name = section.css("h2::text").get()

                if section_name == "Service options":
                    all_service_options = ["Dine-in", "Delivery", "Takeaway"]
                    services_not_interested = section.css(
                        "ul li.hpLkKe.WeoVJe span::text").getall()
                    interested_options = [
                        service
                        for service in all_service_options
                        if service in services_not_interested
                    ]

                elif section_name == "Highlights":
                    highlights_options = section.css(
                        "ul li span::attr(aria-label)").getall()

                elif section_name == "Offerings":
                    offerings_options = section.css(
                        "ul li span::attr(aria-label)").getall()

                elif section_name == "Amenities":
                    amenities_options = section.css(
                        "ul li span::attr(aria-label)").getall()

                elif section_name == "Crowd":
                    crowd_options = section.css(
                        "ul li span::attr(aria-label)").getall()

                elif section_name == "Planning":
                    planning_options = section.css(
                        "ul li span::attr(aria-label)").getall()

                elif section_name == "Payments":
                    payment_options = section.css(
                        "ul li span::attr(aria-label)").getall()

                elif section_name == "Accesibility":
                    accesibility_options = section.css(
                        "ul li span::attr(aria-label)").getall()

                elif section_name == "Dining options":
                    dining_options = section.css(
                        "ul li span::attr(aria-label)").getall()

                elif section_name == "Atmosphere":
                    atmosphere_options = section.css(
                        "ul li span::attr(aria-label)").getall()

                elif section_name == "Parking":
                    parking_options = section.css(
                        "ul li span::attr(aria-label)").getall()

                else:
                    print(f"Add section name {section_name}")

            overview_btn = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR,
                     f"div.RWPxGd[role='tablist'] button[aria-label='Overview of {business_name}']")
                )
            )
            overview_btn.click()
            time.sleep(2)

            return {
                "service_options": interested_options,
                "highlights_options": highlights_options,
                "offerings_options": offerings_options,
                "amenities_options": amenities_options,
                "crowd_options": crowd_options,
                "planning_options": planning_options,
                "payment_options": payment_options,
                "accesibility_options": accesibility_options,
                "dining_options": dining_options,
                "atmospheric_conditions": atmosphere_options,
                "parking_options": parking_options,
            }

        except Exception as e:
            print(
                f"An error occurred while getting {business_name} services: {e}")
            return None

    def get_business_socials(self) -> dict:
        selector = Selector(text=self.driver.page_source)
        
        source_url = selector.css("iframe.rvN3ke::attr(src)").get()
        socials: dict = {}

        print(f"maps.google.com{source_url}")

        if source_url:
            try:
                url = "https://maps.google.com" + source_url
                self.driver.get(url)
                WebDriverWait(self.driver, 180).until(
                    lambda driver: driver.execute_script(
                        "return document.readyState") == "complete"
                )

                selector = Selector(text=self.driver.page_source)
                web_results_section = selector.css(
                    "div.HTomEb.P0BCpd.GLttn.wFAQK")

                results_texts = web_results_section.css(
                    "div.u2OlCc span::text").getall()

                for result in results_texts:
                    if "instagram.com" in result:
                        socials["instagram"] = result
                    elif "facebook.com" in result:
                        socials["facebook"] = result
                    elif "twitter.com" in result:
                        socials["twitter"] = result
                    elif "tiktok.com" in result:
                        socials["tiktok"] = result
                    elif "youtube.com" in result:
                        socials["youtube"] = result
                    else:
                        if "other_links" in socials.keys():
                            socials["other_links"].append(result)
                        else:
                            socials["other_links"] = [result,]
                        print(f"website {result}")

            except Exception as e:
                print(f"Error occured ===================== {e}")

        return socials
