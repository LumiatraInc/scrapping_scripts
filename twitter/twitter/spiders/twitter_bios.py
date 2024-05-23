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

from twitter.items import TwitterItem


class TwitterBiosSpider(scrapy.Spider):
    name = "twitter_bios"
    allowed_domains = ["twitter.com", "x.com"]
    start_urls = ["https://twitter.com/tommyhilfiger"]

    def __init__(self, *args, **kwargs):
        self.driver = webdriver.Chrome()

    def parse(self, response):
        self.driver.get(response.url)
        WebDriverWait(self.driver, 180).until(
            lambda driver: driver.execute_script(
                "return document.readyState") == "complete"
        )
        time.sleep(5)

        twitter_profile = TwitterItem()
        profile_photo: str  = None
        cover_photo: str = None
        profile_description: str = None

        selector = Selector(text=self.driver.page_source)

        profile_description_el = selector.css("div[data-testid='UserDescription'] > span")
        if profile_description_el:
            profile_description = profile_description_el.css("::text").get()

        cover_photo_el = selector.css("div > div[style*='profile_banners']")
        if cover_photo_el:
            cover_photo = cover_photo_el.css("::attr(style)").get()

        profile_photo_el = selector.css("div[aria-label='Opens profile photo'] > div[style*='profile_images']")
        if profile_photo_el:
            profile_photo = profile_photo_el.css("::attr(style)").get()

            
        twitter_profile["profile_description"] = profile_description
        twitter_profile["profile_photo"] = profile_photo
        twitter_profile["cover_photo"] = cover_photo
        yield twitter_profile

        time.sleep(5)
        self.driver.close()


