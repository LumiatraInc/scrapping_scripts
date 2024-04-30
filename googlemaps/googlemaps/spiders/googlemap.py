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
    allowed_domains = ["google.com", ]
    start_urls = [
        "https://www.google.com/maps/@-1.2082248,36.9218576,15z?entry=ttu"]

    def __init__(self):
        self.driver = webdriver.Chrome()
        self.search_term = "clubs in London"

    def parse(self, response):
        self.driver.get(response.url)
        WebDriverWait(self.driver, 20).until(
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
                (By.CSS_SELECTOR, "div.aIFcqe div.m6QErb div.m6QErb.DxyBCb div.m6QErb.DxyBCb.kA9KIf"))
        )
        print("------------------------------------------------------------> ")
        print(
            f"business sections location {business_listings_section.get_attribute('style')}")
        print(f"business sections id {business_listings_section.id}")
        print("------------------------------------------------------------> ")

        # loading indicator classes
        # end_of_list_element = self.driver.find_element(By.CSS_SELECTOR, "div.m6QErb.tLjsW.eKbjU div.PbZDve p span span.HlvSq")
        # print(f"end of list element {end_of_list_element}")
        time.sleep(5)

        # scroll to load more businesses
        print("------------------------------------------------------------->")
        print("Begin scrolling")
        while True:
            self.driver.execute_script('arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;', business_listings_section)
            time.sleep(5)
            try:
                # if this element becomes visible, stop scrolling
                end_of_list_element = self.driver.find_element(By.CSS_SELECTOR, "div.m6QErb.tLjsW.eKbjU div.PbZDve p span span.HlvSq")
                break
            except Exception as e:
                continue

        print("------------------------------------------------------------>")
        print("End scrolling")


        selector = Selector(text=self.driver.page_source)

        results_section = selector.css(
            'div.m6QErb.DxyBCb.kA9KIf.dS8AEf.ecceSd div')

        businesses = results_section.css(
            "div div.Nv2PK.THOPZb.CpccDe").getall()
        print(f"We have {len(businesses)}")

        self.driver.quit()








