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

from twitter.items import TwitterItem


class TwitterBiosSpider(scrapy.Spider):
    name = "twitter_bios"
    allowed_domains = ["twitter.com", "x.com"]
    start_urls = ["https://twitter.com/harrypotterny", "https://twitter.com/SimplyCaleno"]

    def __init__(self, *args, **kwargs):
        options = Options()
        options.add_argument("--headless")  # prevent the browser from opening
        self.driver = webdriver.Chrome(options=options)

        self.login_mail = "jaribwetshi7@gmail.com"
        self.login_username = "Jay349086050367"
        self.login_password = "GazelleTu"

    def parse(self, response):
        self.driver.get(response.url)
        WebDriverWait(self.driver, 180).until(
            lambda driver: driver.execute_script(
                "return document.readyState") == "complete"
        )
        time.sleep(20)

        if "redirect_after_login" in self.driver.current_url:
            self.login_to_twitter()

        twitter_profile = TwitterItem()
        profile_photo: str  = None
        profile_name: str = None
        cover_photo: str = None
        profile_description: str = None
        profile_hashtag: str = None
        is_verified: bool = None
        company_type: str = None
        web_link: str = None
        date_joined: str = None
        total_followers: str = None
        total_following: str = None
        total_posts: str = None
        user_location: str = None

        selector = Selector(text=self.driver.page_source)

    
        if profile_description_el:= selector.css("div[data-testid='UserDescription'] > span"):
            profile_description = profile_description_el.css("::text").get()

        if cover_photo_el:= selector.css("div > div[style*='profile_banners']"):
            cover_photo = cover_photo_el.css("::attr(style)").get()

        if profile_photo_el:= selector.css("div[aria-label='Opens profile photo'] > div[style*='profile_images']"):
            profile_photo = profile_photo_el.css("::attr(style)").get()

        if selector.css("button[aria-label='Provides details about verified accounts.']"):
            is_verified = True
        else:
            is_verified = False

        if following_el:= selector.css("a[href*='following'] > span > span"):
            total_following = following_el.css("::text").get()

        if followers_el:= selector.css("a[href*='followers'] > span > span"):
            total_followers = followers_el.css("::text").get()

        if username_el:=selector.css("div[data-testid='UserName'] span.css-1jxf684.r-bcqeeo.r-1ttztb7.r-qvutc0.r-poiln3"):
            username_texts = username_el.css("::text").getall()
            for username in username_texts:
                if username.startswith("@"):
                    profile_hashtag = username
                else:
                    profile_name = username

        if company_type_el:= selector.css("span[data-testid='UserProfessionalCategory'] button > span"):
            company_type = company_type_el.css("::text").get()

        if user_location_el:= selector.css("span[data-testid='UserLocation'] span > span"):
            user_location = user_location_el.css("::text").get()

        
        if user_url_el := selector.css("a[data-testid='UserUrl'] > span"):
            web_link = user_url_el.css("::text").get()


        if user_join_date_el := selector.css("span[data-testid='UserJoinDate'] > span"):
            date_joined = user_join_date_el.css("::text").get()

        
        if total_post_el := selector.xpath("//h2/following-sibling::div"):
            total_posts = total_post_el.css("::text").get()


        twitter_profile["profile_name"] = profile_name
        twitter_profile["profile_hashtag"] = profile_hashtag
        twitter_profile["profile_description"] = profile_description
        twitter_profile["profile_photo"] = profile_photo
        twitter_profile["cover_photo"] = cover_photo
        twitter_profile["is_verified"] = is_verified
        twitter_profile["total_following"] = total_following
        twitter_profile["total_followers"] = total_followers
        twitter_profile["company_type"] = company_type
        twitter_profile["user_location"] = user_location
        twitter_profile["web_link"] = web_link
        twitter_profile["date_joined"] = date_joined
        twitter_profile["total_posts"] = total_posts
        twitter_profile["search_term"] = "Twitter"
        
        yield twitter_profile

        time.sleep(10)
        self.driver.close()


    def login_to_twitter(self):
        try:
            email_input_el = self.driver.find_element(By.CSS_SELECTOR, "input[autocomplete='username']")
            email_input_el.send_keys(self.login_mail)
            time.sleep(2)
            next_btn_el = self.driver.find_element(By.XPATH, "//button[descendant::text()='Next']")
            next_btn_el.click()
            WebDriverWait(self.driver, 180).until(
            lambda driver: driver.execute_script(
                "return document.readyState") == "complete"
            )
            time.sleep(10)

            if username_el:= self.driver.find_elements(By.CSS_SELECTOR, "input[data-testid='ocfEnterTextTextInput']"):
                username_el[0].send_keys(self.login_username)
                time.sleep(2)
                next_btn_el = self.driver.find_element(By.CSS_SELECTOR, "button[data-testid='ocfEnterTextNextButton']")
                next_btn_el.click()
                WebDriverWait(self.driver, 180).until(
                lambda driver: driver.execute_script(
                    "return document.readyState") == "complete"
                )
                time.sleep(10)


            password_input_el = self.driver.find_element(By.CSS_SELECTOR, "input[type='password']")
            password_input_el.send_keys(self.login_password)
            time.sleep(2)
            if next_btn_el:= self.driver.find_elements(By.CSS_SELECTOR, "button[data-testid='LoginForm_Login_Button']"):
                next_btn_el[0].click()
            else:
                next_btn_el = self.driver.find_element(By.XPATH, "//button[descendant::text()='Next']")
                next_btn_el.click()
            WebDriverWait(self.driver, 180).until(
            lambda driver: driver.execute_script(
                "return document.readyState") == "complete"
            )
            time.sleep(15)

        except Exception as e:
            print(f"=============> login_to_twitter error {e}")


