import time
import scrapy
from scrapy.responsetypes import Response
from scrapy.selector import Selector, SelectorList
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException


class InstagramInfluencerSpider(scrapy.Spider):
    name = "instagram_influencer"
    allowed_domains = ["instagram.com"]
    start_urls = ["https://www.instagram.com/tommyhilfiger/"]

    def __init__(self, *args, **kwargs):
        options = Options()
        options.add_argument("--headless")  # prevent the browser from opening
        self.driver = webdriver.Chrome()
        self.login_mail = "mardocheejarib64@gmail.com"
        self.login_username = "mardocheelumi"
        self.login_password = "GazelleTu"
        self.all_urls = ["https://www.instagram.com/tommyhilfiger/", "https://instagram.com/burberry", "https://instagram.com/harrypotterny"]

    def parse(self, response):
        # open the url
        self.driver.get(response.url)
        WebDriverWait(self.driver, 180).until(
            lambda driver: driver.execute_script(
                "return document.readyState") == "complete"
        )
        time.sleep(20)

        # check if logged in
        is_logged_in = self.is_logged_in()
        if not is_logged_in:
            successful = self.login_to_instagram()
            if not successful:
                print("Login unsuccessful")
                return 
            
        # remove the dialog
        self.remove_notification_dialog()
            
        # identify each row by xpath //header/parent::*/div/following-sibling::*[1]/div/div
        posts_rows_el = self.driver.find_elements(By.XPATH, "//header/parent::*/div/following-sibling::*[1]/div/div")
        print(f"==========> post rows el {posts_rows_el}")


        # loop through each row
        for posts_row_el in posts_rows_el:
            # identify each post in row
            posts_el = posts_row_el.find_elements(By.XPATH, "/div")
            # loop through each post
            for post_el in posts_el:
                # click on the post
                post_el.click()
                # wait for page to load
                WebDriverWait(self.driver, 180).until(
                    lambda driver: driver.execute_script(
                        "return document.readyState") == "complete"
                )
                time.sleep(10)

                # collect instagram post data

                # close post
                if close_btn_el := self.driver.find_elements(By.XPATH, "//*[@aria-label='Close']/parent::*/parent::*"):
                    close_btn_el[0].click()
                    

                    # wait for page to load
                    WebDriverWait(self.driver, 180).until(
                        lambda driver: driver.execute_script(
                            "return document.readyState") == "complete"
                    )
                    time.sleep(5)

                else:
                    self.driver.back()
                    WebDriverWait(self.driver, 180).until(
                        lambda driver: driver.execute_script(
                            "return document.readyState") == "complete"
                    )
                    time.sleep(10)

        yield {"message": "hello"}
        # close browser
        time.sleep(10)
        self.driver.close()


    
    def login_to_instagram(self) -> bool:
        try:
            # get and click on login button
            login_btn_el = self.driver.find_element(By.CSS_SELECTOR, "a[href*='accounts/login'][role='link']")
            login_btn_el.click()
            time.sleep(5)
            # get input field by input[aria-label='Phone number, username or email address']
            username_input_el = self.driver.find_element(By.CSS_SELECTOR, "input[aria-label='Phone number, username or email address']")
            username_input_el.send_keys(self.login_username)
            time.sleep(2)
            # get password field by input[aria-label='Password']
            password_el = self.driver.find_element(By.CSS_SELECTOR, "input[aria-label='Password']")
            password_el.send_keys(self.login_password)
            time.sleep(2)
            # get the submit button button[type='submit']
            next_btn_el = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            next_btn_el.click()

            # wait to load
            WebDriverWait(self.driver, 180).until(
            lambda driver: driver.execute_script(
                "return document.readyState") == "complete"
            )
            time.sleep(15)

            return True

        except Exception as e:
            print(f"=============> login_to_twitter error {e}")
            return False
        

    def is_logged_in(self) -> bool:
        try:
            # check if login button element exists
            self.driver.find_element(By.CSS_SELECTOR, "a[href*='accounts/login'][role='link']")
            return False
        except NoSuchElementException as ne:
            return True
        except Exception as e:
            return True
        
    def remove_notification_dialog(self):
        # get the not now button with xpath //section//div/section/parent::*/div/div
        try:
            not_now_btn_el = self.driver.find_element(By.XPATH, "//section//div/section/parent::*/div/div")
            not_now_btn_el.click()
            # wait to load
            WebDriverWait(self.driver, 180).until(
            lambda driver: driver.execute_script(
                "return document.readyState") == "complete"
            )
            time.sleep(15)

        except Exception as e:
            return
        
