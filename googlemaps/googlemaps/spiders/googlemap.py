import time
import scrapy
from scrapy.responsetypes import Response
from scrapy.selector import Selector
from selenium import webdriver
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
        # time.sleep(30)

        business_listings_section = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "div.aIFcqe div.m6QErb div.m6QErb.DxyBCb div.m6QErb.DxyBCb.kA9KIf"))
        )

        time.sleep(5)

        # scroll to load more businesses
        while True:
            self.driver.execute_script(
                'arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;', business_listings_section)
            time.sleep(5)
            try:
                # if this element becomes visible, stop scrolling
                end_of_list_element = self.driver.find_element(
                    By.CSS_SELECTOR, "div.m6QErb.tLjsW.eKbjU div.PbZDve p span span.HlvSq")
                break
            except Exception as e:
                continue

        selector = Selector(text=self.driver.page_source)

        results_section = selector.css(
            'div.m6QErb.DxyBCb.kA9KIf.dS8AEf.ecceSd div')

        businesses = results_section.css(
            "div div.Nv2PK.THOPZb.CpccDe")
        print(f"We have {len(businesses)}")

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

            business_address:str = None
            business_about:str = None
            website:str = None
            phone_number:str = None

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

            image_links = self.get_business_photos(business_name=business_name)
            services = self.get_business_services(business_name=business_name)

            rating_section = selector.css("div.PPCwl div.Bd93Zb div.jANrlb")
            ratings = rating_section.css("div.fontDisplayLarge::text").get()
            total_reviews = rating_section.css(
                "button.HHrUdb.fontTitleSmall.rqjGif span::text").get()

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

        return business

    def get_business_photos(self, business_name: str) -> list[str] | None:
        try:
            image_links = None
            all_photos_btn = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "div.cRLbXd div.dryRY div.ofKBgf button.K4UgGe[aria-label='All']"))
            )

            all_photos_btn.click()
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
            cancel_button.click()
            time.sleep(1)


            return image_links

        except Exception as e:
            print(f"An error occurred while getting {business_name} photos")
            return None
        

    def get_business_reviews(self, business_name: str) -> list[dict]:
        raise NotImplementedError("This method is not implemented")
    
    def get_business_services(self, business_name: str) -> dict[str, list[str]] | None:
        try:
            about_btn = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, f"div.RWPxGd[role='tablist'] button[aria-label='About {business_name}']")
                )
            )
            about_btn.click()
            time.sleep(2)

            selector = Selector(text=self.driver.page_source)

            about_sections = selector.css("div.m6QErb.DxyBCb.kA9KIf.dS8AEf div.iP2t7d.fontBodyMedium")
            print("================================================================")
            print(f"ABout sections {len(about_sections)}")
            print("================================================================")


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
                print("***************************************************************")
                print(f"section name {section_name}")
                print("***************************************************************")


                if section_name == "Service options":
                    all_service_options = ["Dine-in", "Delivery", "Takeaway"]
                    services_not_interested = section.css("ul li.hpLkKe.WeoVJe span::text").getall()
                    interested_options = [
                        service 
                        for service in all_service_options 
                        if service in services_not_interested 
                    ]
                    print(f"interested_options {interested_options}")

                elif section_name == "Highlights":
                    highlights_options = section.css("ul li span::attr(aria-label)").getall()
                    print(f"Highlights {highlights_options}")

                elif section_name == "Offerings":
                    offerings_options = section.css("ul li span::attr(aria-label)").getall()
                    print(f"offer {offerings_options}")

                elif section_name == "Amenities":
                    amenities_options = section.css("ul li span::attr(aria-label)").getall()
                    print(f"amenities {amenities_options}")

                elif section_name == "Crowd":
                    crowd_options = section.css("ul li span::attr(aria-label)").getall()
                    print(f"Crowd options {crowd_options}")

                elif section_name == "Planning":
                    planning_options = section.css("ul li span::attr(aria-label)").getall()
                    print(f"planning_options {planning_options}")

                elif section_name == "Payments":
                    payment_options = section.css("ul li span::attr(aria-label)").getall()
                    print(f"payment_options {payment_options}")

                elif section_name == "Accesibility":
                    accesibility_options = section.css("ul li span::attr(aria-label)").getall()

                elif section_name == "Dining options":
                    dining_options = section.css("ul li span::attr(aria-label)").getall()

                elif section_name == "Atmosphere":
                    atmosphere_options = section.css("ul li span::attr(aria-label)").getall()

                elif section_name == "Parking":
                    parking_options = section.css("ul li span::attr(aria-label)").getall()

                else:
                    print(f"Add section name {section_name}")

            overview_btn = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, f"div.RWPxGd[role='tablist'] button[aria-label='Overview of {business_name}']")
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
            print(f"An error occurred while getting {business_name} services: {e}")
            return None
    

