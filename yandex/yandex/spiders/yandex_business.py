import time
import scrapy
from scrapy.responsetypes import Response
from scrapy.selector import Selector, SelectorList
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException


class YandexBusinessSpider(scrapy.Spider):
    name = "yandex_business"
    allowed_domains = ["yandex.com"]
    start_urls = ["https://yandex.com/maps"]

    def __init__(self, *args, **kwargs):
        options = Options()
        options.add_argument("--headless")  # prevent the browser from opening
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

    def parse(self, response):
        # open the url
        self.driver.get(response.url)
        WebDriverWait(self.driver, 180).until(
            lambda driver: driver.execute_script(
                "return document.readyState") == "complete"
        )
        time.sleep(20)
        
        business_by_search = False # the opposite is business by category
        if not business_by_search:
            self.get_business_by_category()
        else:
            self.get_business_by_search()

        

        

        # solve the captcha
        '''
        captcha-site-key = "de615aa1-de19cfbf-bc99da5-af1c55d5_2/1718785701/7eded441acedaee5b1c3fcf00673ac0c_bd4ef99090a58d36bfab2b587c586dc8&mt=DF98DC49B184C2D903C670A3B4F1894F9595358AAF2EFAA9883FC1B88E0F454BFD217B528091119447BB4AAD3004AAD8DFC50E531EF91B7ACCA05A4478EDBA6A01EEA8428F7ECB336FF7AABA61A68CB8C2ED316E556DC1A0DD2BB75F1CE31822114FD9F4E55D56C424D85BD425A783EA579B634EB02945EE52E2BA75C77F61FDCC48EA006DCE194E3DE665221CB2F396D3AAFB47248EEAE70E060042747A41CC1143493B0989A98F4ED295813A99CE4BDBE7714E3E3D2870281DF01B7CC2743CF72A7DEFD6AFA95E3D262C9419F53888B03F5B8D66F583D73B71287CAA62&retpath=aHR0cHM6Ly95YW5kZXguY29tL21hcHMvP2xsPTEwLjg1NDE4NiUyQzQ5LjE4MjA3NiZ6PTQ%2C_155e6bddec31f120fbd95b102ca2311f&u=89ba0452-d9903606-86ffbb84-a06bb7a6&s=754b5f9f905d3f3fb36aefbfacb93f8b"
        '''

        # click on the more button using the selector div._id_more > div.catalog-grid-view__icon

        # loop through categories using the selector div.catalog-grid-view__icon
            # click on a category

            # sleep 20 seconds
        
            # maximize window screen
            # scroll through the result section of page using css slector div.scroll__container
                # time.sleep(random(20))
                # stop scrolling when the div div.add-business-view shows on the bottom

            # loop through business
                # get business data id through selector div.search-snippet-view__body _type_business::attr(data-object)
                # get business place coordinate through selector div.search-snippet-view__body _type_business::attr(data-coordinates)
        
                # click at a business for the sidebar view to show. The container is gotten with the selector div.sidebar-view__panel._no-padding
        
                # get the business name with the selector a.card-title-view__title-link::text
                # get the business link a.card-title-view__title-link::attr(href)
                # get if business is verified with selector div.sidebar-view__panel._no-padding span.business-verified-badge span.business-verified-badge
                # get business category with the selector div.sidebar-view__panel._no-padding div.business-card-title-view__categories
                # get total ratings with the selector div.sidebar-view__panel._no-padding div.business-header-rating-view__text._clickable
                # get the rating with the selector div.sidebar-view__panel._no-padding span.business-rating-badge-view__rating-text

                # get business hours time table with selector div.sidebar-view__panel._no-padding span.inline-image._loaded.icon.flip-icon (click)
                    # opens a dialog box with the selector div.dialog__content
                    # get list of days information with selector div.dialog__content div.business-working-intervals-view div.business-working-intervals-view__period
                    # loop through each day 
                        # get day name with selector div.dialog__content div.business-working-intervals-view div.business-working-intervals-view__period div.business-working-intervals-view__day
                        # get the hours with selector div.dialog__content div.business-working-intervals-view__intervals > div
        
                    # close the modal with selector div.dialog__content button[aria-label="Close"]
        
                # get the business website with selector div.sidebar-view__panel._no-padding div._type_web > a[aria-label='Website']
                # get the address with the selector div.sidebar-view__panel._no-padding a.business-contacts-view__address-link
                # get the phonenumber with the selector div.sidebar-view__panel._no-padding span[itemprop="telephone"]

                # get social media name with selector div.sidebar-view__panel._no-padding div.business-contacts-view__social-links div.business-contacts-view__social-button > a::attr(aria-label).split(" ")[-1]
                # get social media links with selector div.sidebar-view__panel._no-padding div.business-contacts-view__social-links div.business-contacts-view__social-button > a::attr(href)
        
                # get reviews box from business with selector div.sidebar-view__panel._no-padding div.business-reviews-card-view__reviews-container div.business-review-view__info
                    # get review author name with selector div[itemprop="author"] span[itemprop="name"]
                    # get author rating with counting selector div.business-rating-badge-view__stars >span._full
                    # get the date of published review with selector span.business-review-view__date > span
                    # get review body with selector span.business-review-view__body-text

                # click on the features box with the selector div.sidebar-view__panel._no-padding div.tabs-select-view__title._name_features > a
                # get feature titles with the selector div.sidebar-view__panel._no-padding div.business-features-view__group-title
                # get feature items with the selector div.sidebar-view__panel._no-padding div.features-cut-view div.business-features-view__bool-list
                    # get each item with div.business-features-view__bool-text
        
                # click on the photos box with the selector div.sidebar-view__panel._no-padding div.tabs-select-view__title._name_gallery
                # scroll the photos section with selector div.sidebar-view__panel._no-padding div.scroll__container
                # get all the photos with the selector div.media-gallery__frame-wrapper img::attr(src)
        

        # close url
        time.sleep(10)
        self.driver.close()
        pass

    def get_business_by_category(self):
        # click on the more button using the selector div._id_more > div.catalog-grid-view__icon
        self.click_category_more_btn()

        # get all categories element using the selector div.catalog-grid-view__icon
        categories_els = self.driver.find_elements(By.CSS_SELECTOR, "div.catalog-grid-view__icon")

        for category_el in categories_els:
            time.sleep(8)
            # get category titles by the selector h3.catalog-grid-view__text
            selector = Selector(text=self.driver.page_source)
            if category_title_el := selector.css("h3.catalog-grid-view__text"):
                category_title = category_title_el.css("::text").get()
                print(f"{category_title=}")
            else:
                print("Couldn't find the category title")
            try:
                # click on each category 
                category_el.click()
            except Exception as e:
                break

            time.sleep(75)

            # go back to the home
            self.driver.back()




        

    def click_category_more_btn(self):
        try:
            more_btn_el = self.driver.find_element(By.CSS_SELECTOR, "div._id_more > div.catalog-grid-view__icon")
            more_btn_el.click()
        except Exception as e:
            print(f"============> Error {e}")
            return
        

    def get_business_by_search(self):
        raise NotImplementedError("Get Business by search isn't implemented")
    
