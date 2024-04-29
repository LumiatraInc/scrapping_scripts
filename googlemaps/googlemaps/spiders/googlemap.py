import time
import scrapy
from scrapy.selector import Selector
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class GooglemapSpider(scrapy.Spider):
    name = "googlemap"
    allowed_domains = ["google.com"]
    start_urls = [
        "https://www.google.com/maps/@-1.2082248,36.9218576,15z?entry=ttu"]

    def __init__(self):
        self.driver = webdriver.Chrome()
        self.search_term = "clubs in London"

    def parse(self, response):
        self.driver.get(response.url)
        WebDriverWait(self.driver, 10).until(
            lambda driver: driver.execute_script(
                "return document.readyState") == "complete"
        )

        search_box = self.driver.find_element(By.ID, "searchboxinput")
        search_box.send_keys(self.search_term)
        search_box.send_keys(Keys.RETURN)
        WebDriverWait(self.driver, 10).until(
            lambda driver: driver.execute_script(
                "return document.readyState") == "complete"
        )

        business_listings_section = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "div.k7jAl.miFGmb.lJ3Kh.PLbyfe"))
        )
        print("------------------------------------------------------------> ")
        print(
            f"business sections location {business_listings_section.get_attribute('style')}")
        print(f"business sections id {business_listings_section.id}")
        print("------------------------------------------------------------> ")

        # loading indicator classes

        # scroll to load more businesses

        start_time = time.time()
        while True:
            self.driver.execute_script(
                "arguments[0].scrollBy(0, 500);", business_listings_section)
            try:
                loading_spinner = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located(
                        (By.CSS_SELECTOR, "div div.lXJj5c.Hk4XGb div.qjESne.veYFef"))
                )
                if loading_spinner.is_displayed():
                    start_time = time.time()

            except Exception:
                pass

            if (time.time() - start_time >= 10):
                break

        # selector = Selector(text=self.driver.page_source)

        # results_section = selector.css(
        #     'div.m6QErb.DxyBCb.kA9KIf.dS8AEf.ecceSd div')

        # businesses = results_section.css(
        #     "div div.Nv2PK.THOPZb.CpccDe").getall()
        # print(f"We have {len(businesses)}")

        self.driver.quit()
