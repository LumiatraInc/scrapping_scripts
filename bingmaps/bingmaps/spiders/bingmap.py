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
from selenium.common.exceptions import NoSuchElementException, TimeoutException

from bingmaps.items import BingmapsItem


class BingmapSpider(scrapy.Spider):
    name = "bingmap"
    allowed_domains = ["bing.com"]
    start_urls = ["https://www.bing.com/maps"]

    def __init__(self, *args, **kwargs):
        self.driver = webdriver.Chrome()
        self.search_term = "shops in London"

    def parse(self, response: Response):
        self.driver.get(response.url)
        WebDriverWait(self.driver, 180).until(
            lambda driver: driver.execute_script(
                "return document.readyState") == "complete"
        )

        search_box = self.driver.find_element(By.CSS_SELECTOR, "input#maps_sb")
        search_box.send_keys(self.search_term)
        search_box.send_keys(Keys.RETURN)

        WebDriverWait(self.driver, 10).until(
            lambda driver: driver.execute_script(
                "return document.readyState") == "complete"
        )

        result_box = self.driver.find_element(By.CSS_SELECTOR, "div#taskArea div.taskLayoutContainer.slideout div.bm_scrollbarMask div.custom-scroll.sticky div.outer-container div.inner-container")

        page_count = 1

        # go to next page until there is no more page to go to
        while True:
            try:
                time.sleep(5)
                selector = Selector(text=self.driver.page_source)

                # businesses_div = selector.css("div.entity-listing-container div.b_rich ul.b_vList.b_divsec li")
                businesses_div = self.driver.find_elements(By.CSS_SELECTOR, "div.entity-listing-container div.b_rich ul.b_vList.b_divsec li a")


                print(f" We have {len(businesses_div)} businesses")


                for index, business in enumerate(businesses_div):
                    new_business = BingmapsItem()

                    print(f"Business {index}")
                    business_name:str = None
                    socials: dict = {}
                    address: str = None
                    phone_number: str = None
                    website: str = None
                    business_status: str = None
                    rating: str = None
                    total_reviews: str = None

                    if business.is_displayed() and business.is_enabled():
                        print(" ================> clicked on business")
                        business.click()
                        WebDriverWait(self.driver, 10).until(
                            lambda driver: driver.execute_script(
                                "return document.readyState") == "complete"
                        )
                        time.sleep(5)

                        selector = Selector(text=self.driver.page_source)

                        business_info_box = selector.css("div#wpc_tp.wpc_tp div.tp_tasks div.wpc_module.sb_meta div.compInfo.b_localDesktopInfoCard")

                        print(f"business info box {business_info_box}")

                        if business_info_box:
                            print("=================> found business info box")
                            business_name_el = business_info_box.css("div.infoModule.b_divsec.bottomBleed.noSeparator div.b_annotate div.bm_annotationRoot h2.nameContainer")
                            if business_name_el:
                                business_name = business_name_el.css("::text").get()
                                print(f"============> business_name {business_name}")

                            print("step 1")

                            business_status_el = business_name_el.css("div.infobubble_item.isclaimedinfobubble_item")
                            if business_status_el:
                                business_status = business_status_el.css("::attr(aria-label)").get()
                                print(f"============> business_status {business_status}")

                            print("step 2")


                            address_el = business_info_box.css("div#IconItem_2 > div.iconDataList::text")
                            if address_el:
                                address = address_el.get()
                                print(f"============> address {address}")

                            print("step 4")

                            phone_number_el = business_info_box.css("div#IconItem_3 > a.longNum::attr(href)")
                            if phone_number_el:
                                phone_number = phone_number_el.get()
                                print(f"============> phone_number {phone_number}")

                            print("step 5")
                            
                            website_el = business_info_box.css("div#IconItem_4 a")
                            if website_el:
                                website = website_el.css("::attr(href)").get()
                                print(f"============> website {website}")

                            print("step 6")

                        rating_el = selector.css("div#slideexp0_B899C6c div.b_slidesContainer div.b_viewport.scrollbar div#slideexp0_B899C6 div.slide a.wr_rv div.wr_rat")
                        if rating_el:
                            rating = rating_el.css("::text").get()
                            print(f"==============> rating {rating}")

                        print("step 7")

                        total_reviews_el = selector.css("div#slideexp0_B899C6c div.b_slidesContainer div.b_viewport.scrollbar div#slideexp0_B899C6 div.slide a.wr_rv div.wr_rev.b_demoteText")
                        if total_reviews_el:
                            total_reviews = total_reviews_el.css("::text").get()
                            print(f"==============> total_reviews {total_reviews}")

                        # social media
                        social_media_el = selector.css("div[aria-label='Social profiles'] ul.b_hList li a")
                        if social_media_el:
                            for media in social_media_el:
                                if "facebook.com" in media.css("::attr(href)").get():
                                    socials["facebook"] = media.css("::attr(href)").get()

                                elif "twitter.com" in media.css("::attr(href)").get():
                                    socials["twitter"] = media.css("::attr(href)").get()

                                elif "instagram.com" in media.css("::attr(href)").get():
                                    socials["instagram"] = media.css("::attr(href)").get()

                                elif "linkedin.com" in media.css("::attr(href)").get():
                                    socials["linkedin"] = media.css("::attr(href)").get()

                                elif "youtube.com" in media.css("::attr(href)").get():
                                    socials["youtube"] = media.css("::attr(href)").get()

                                else:
                                    print(media.css("::attr(href)").get())


                        print("step 8")
                    
                    new_business["business_name"] = business_name
                    new_business["business_link"] = self.driver.current_url
                    new_business["business_status"] = business_status
                    new_business["address"] = address
                    new_business["phone_number"] = phone_number
                    new_business["website"] = website
                    new_business["socials"] = socials
                    new_business["rating"] = rating
                    new_business["total_reviews"] = total_reviews
                    new_business["total_ratings"] = 5
                
                    yield new_business


                    # close the business card
                    close_business_card_btn = self.driver.find_element(By.CSS_SELECTOR, "div.taskCard.focus div.cardFace.front div.cardContent div.contentRoot div a.commonButton.backArrowButton.overlayButton")
                    close_business_card_btn.click()
                    # self.driver.back()
                    WebDriverWait(self.driver, 10).until(
                            lambda driver: driver.execute_script(
                                "return document.readyState") == "complete"
                    )

                    time.sleep(4)

                time.sleep(2)

                next_btn = self.driver.find_element(By.CSS_SELECTOR, "a.bm_rightChevron[aria-label='Next Page']")
                print(f"")
                if next_btn.is_displayed() and next_btn.is_enabled():
                    next_btn.click()
                    WebDriverWait(self.driver, 10).until(
                        lambda driver: driver.execute_script(
                            "return document.readyState") == "complete"
                    )

                    page_count +=1

                else:
                    print("==========> Button is either not enabled or visible")
                    break

            except NoSuchElementException as ne:
                print(f"========= An exception was thrown {ne}")
                break

            except TimeoutException as te:
                print(f"========= An exception was thrown {te}")
                break

            except Exception as e:
                print(f"========= An exception was thrown {e}")
                break

        time.sleep(5)
        self.driver.quit()


