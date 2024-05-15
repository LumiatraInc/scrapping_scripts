import time
import scrapy
from scrapy.responsetypes import Response
from scrapy.selector import Selector, SelectorList
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.action_chains import ActionChains

from bingmaps.items import BingmapsItem


class BingmapSpider(scrapy.Spider):
    name = "bingmap"
    allowed_domains = ["bing.com"]
    start_urls = ["https://www.bing.com/maps"]

    def __init__(self, *args, **kwargs):
        self.driver = webdriver.Chrome()
        self.search_term = "shops in London"

    def parse(self, response: Response):
        # self.driver.maximize_window()
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

                businesses_div = selector.css("div.entity-listing-container div.b_rich ul.b_vList.b_divsec li a")
                businesses_div = self.driver.find_elements(By.CSS_SELECTOR, "div.entity-listing-container div.b_rich ul.b_vList.b_divsec li a")


                print(f" We have {len(businesses_div)} businesses")


                for business in businesses_div:
                    yield self.parse_business(business)
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

                next_btn = self.driver.find_element(By.CSS_SELECTOR, "a[aria-label='Next Page']")
                print(f"next_btn {next_btn}")
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

    def open_business_as_new_card(self):
        raise NotImplemented()


    def parse_business(self, business: WebElement) -> BingmapsItem:
        new_business = BingmapsItem()
        business_name:str = None
        business_type: str = None
        socials: dict = {}
        address: str = None
        phone_number: str = None
        website: str = None
        business_status: str = None
        rating: str = None
        total_reviews: str = None
        business_about: str = None
        search_term = self.search_term
        source = "Bing Maps"
        try:

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
                    infos = self.parse_business_info(business_info_box)
                    business_name = infos.get("business_name")
                    business_about = infos.get("business_about")
                    business_type = infos.get("business_type")
                    website = infos.get("website")
                    business_status = infos.get("business_status")
                    address = infos.get("address")
                    phone_number = infos.get("phone_number")

                rating = self.get_business_ratings(selector)

                total_reviews = self.get_total_business_reviews(selector)

                # social media
                socials = self.get_business_social_media(selector)

            
            new_business["business_name"] = business_name
            new_business["business_type"] = business_type
            new_business["business_about"] = business_about
            new_business["business_link"] = self.driver.current_url
            new_business["business_status"] = business_status
            new_business["address"] = address
            new_business["phone_number"] = phone_number
            new_business["website"] = website
            new_business["socials"] = socials
            new_business["rating"] = rating
            new_business["total_reviews"] = total_reviews
            new_business["total_ratings"] = 5
            new_business["source"] = source
            new_business["search_term"] = search_term

        except NoSuchElementException as ne:
                print(f"Parse Business ========= An exception was thrown {ne}")
            

        except TimeoutException as te:
            print(f"Parse Business ========= An exception was thrown {te}")
        

        except Exception as e:
            print(f"Parse Business ========= An exception was thrown {e}")
        

        return new_business
    
    def parse_business_info(self, elements: SelectorList[Selector]) -> dict[str, (str | None)]:
        print("step 1")
        business_name = self.get_business_name(elements)

        print("step 2")
        business_status = self.get_business_status(elements)

        print("step 3")
        address = self.get_business_address(elements)

        print("step 4")
        phone_number = self.get_business_phone_number(elements)

        print("step 5")
        website = self.get_business_website_link(elements)

        print("step 6")
        business_about = self.get_business_about(elements)

        print("step 7")
        business_type = self.get_business_type(elements)

        return {
            "business_name": business_name,
            "business_about": business_about,
            "business_type": business_type,
            "business_status": business_status,
            "address": address,
            "phone_number": phone_number,
            "website": website,
        }
    

    def get_business_name(self, elements: SelectorList[Selector]) -> str | None:
        try:
            business_name_el = elements.css("div.infoModule.b_divsec.bottomBleed.noSeparator div.b_annotate div.bm_annotationRoot h2.nameContainer")
            if business_name_el:
                return business_name_el.css("::text").get()
            
            return None
        except Exception:
            return None
    
    def get_business_type(self, elements: SelectorList[Selector]) -> str | None:
        try:
            # business_type_el = elements.css("div.infoModule.b_divsec.topBleed.noSeparator > div.b_factrow > a + text::text")
            business_type_el = elements.xpath("//div/a/following-sibling::text()")
            if business_type_el:
                return business_type_el.get().replace(".", "").strip()
            
            business_type_el = elements.xpath("//div[contains(@class, 'infoModule'), contains(@class, 'b_divsec')]/div[contains(@class, 'b_factrow')]/text()")
            if business_type_el:
                return business_type_el.get().replace(".", "").strip()
            return None
        except Exception:
            return None
    
    
    def get_business_about(self, elements: SelectorList[Selector]) -> str | None:
        try:
            about_el = elements.css("div.infoModule.b_divsec > div.ed_entity_desc > div.b_snippet_expansion > div.b_expandable_hidden_container.b_inline span")
            if about_el:
                return about_el.css("::attr(title)").get()
            
            # about_el = elements.css("div.infoModule.b_divsec > div.ed_entity_desc::text")
            about_el = elements.xpath("//div[contains(@class, 'infoModule'), contains(@class, 'b_divsec')]/div[contains(@class, 'ed_entity_desc')]/text()")
            if about_el:
                return about_el.get()
            return None
        except Exception:
            return None

    
    def get_business_status(self, elements: SelectorList[Selector]) -> str | None:
        try:
            business_name_el = elements.css("div.infoModule.b_divsec.bottomBleed.noSeparator div.b_annotate div.bm_annotationRoot h2.nameContainer")
            business_status_el = business_name_el.css("div.infobubble_item.isclaimedinfobubble_item")
            if business_status_el:
                return business_status_el.css("::attr(aria-label)").get()
            
            return None
        except Exception:
            return None
    
    def get_business_address(self, elements: SelectorList[Selector]) -> str | None:
        try:
            address_el = elements.css("div[aria-label='Address'] > div.iconDataList::text")
            if address_el:
                return address_el.get()
            
            return None
        except Exception:
            return None

    def get_business_phone_number(self, elements: SelectorList[Selector]) -> str | None:
        try:
            phone_number_el = elements.css("div[aria-label='Phone'] > a::attr(href)")
            if phone_number_el:
                return phone_number_el.get()
            
            return None
        except Exception:
            return None
    
    def get_business_website_link(self, elements: SelectorList[Selector]) -> str | None:
        try:
            website_el = elements.css("div[aria-label='Website'] a")
            if website_el:
                return website_el.css("::attr(href)").get()
            
            return None
        except Exception:
            return None
    
    def get_business_ratings(self, elements: SelectorList[Selector]) -> str | None:
        try:
            rating_el = elements.css("div#slideexp0_B899C6c div.b_slidesContainer div.b_viewport.scrollbar div#slideexp0_B899C6 div.slide a.wr_rv div.wr_rat")
            if rating_el:
                return rating_el.css("::text").get()
                
            return None
        except Exception:
            return None
    
    def get_total_business_reviews(self, elements: SelectorList[Selector]) -> str | None:
        try:
            total_reviews_el = elements.css("div#slideexp0_B899C6c div.b_slidesContainer div.b_viewport.scrollbar div#slideexp0_B899C6 div.slide a.wr_rv div.wr_rev.b_demoteText")
            if total_reviews_el:
                return total_reviews_el.css("::text").get()
                
            return None
        except Exception:
            return None

    def get_business_social_media(self, elements: SelectorList[Selector]) -> dict[str, str]:
        try:
            socials = {}
            social_media_el = elements.css("div[aria-label='Social profiles'] ul.b_hList li a")
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

            return socials
        except Exception:
            return {}
    

