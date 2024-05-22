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

class YellowPagesSpider(scrapy.Spider):
    name = "yellow_pages"
    allowed_domains = ["yell.com"]
    start_urls = ["https://www.yell.com/k/popular+searches.html"]

    def __init__(self, *args, **kwargs):
        self.driver = webdriver.Chrome()

    def parse(self, response):
        self.driver.get(response.url)
        WebDriverWait(self.driver, 180).until(
            lambda driver: driver.execute_script(
                "return document.readyState") == "complete"
        )
