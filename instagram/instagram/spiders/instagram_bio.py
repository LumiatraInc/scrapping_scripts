import time
import ast
import google.generativeai as genai
from decouple import config
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


from instagram.items import InstagramItem

class InstagramBioSpider(scrapy.Spider):
    name = "instagram_bio"
    allowed_domains = ["instagram.com"]
    start_urls = ["https://www.instagram.com/lego/"]

    def __init__(self, *args, **kwargs):
        options = Options()
        options.add_argument("--headless")  # prevent the browser from opening
        self.driver = webdriver.Chrome()
        self.GEMINI_API_KEY = config("GEMINI_API_KEY", cast=str)
        print(f"{self.GEMINI_API_KEY=}")

    def parse(self, response):
        self.driver.get(response.url)
        WebDriverWait(self.driver, 180).until(
            lambda driver: driver.execute_script(
                "return document.readyState") == "complete"
        )
        time.sleep(20)

        selector = Selector(text=self.driver.page_source)

        header_section = selector.css("header > section")

        print(f"header section {''.join(header_section.getall())}")

        html_snippet = "".join(header_section.getall())
        prompt = self.generate_prompt(html_snippet)
        answer = self.generate_answer(prompt)
        print(f"==========> answer: {answer}")

        profile:dict = ast.literal_eval(answer)

        description = rf'{profile.get("bio_description")}'

        instagram_profile = InstagramItem()

        instagram_profile["profile_name"] = profile.get("full_name")
        instagram_profile["profile_photo"] = profile.get("profile_picture_link")
        instagram_profile["username"] = profile.get("username")
        instagram_profile["is_verified"] = profile.get("is_verified")
        instagram_profile["total_posts"] = profile.get("total_posts")
        instagram_profile["total_followers"] = profile.get("total_followers")
        instagram_profile["total_following"] = profile.get("total_following")
        instagram_profile["bio_description"] = profile.get("bio_description")
        instagram_profile["thread_name"] = profile.get("thread_name")
        instagram_profile["thread_link"] = profile.get("thread_link")
        instagram_profile["source"] = "Instagram"
        instagram_profile["web_link"] = profile.get("website")

        yield instagram_profile

        time.sleep(10)

        self.driver.quit()

    
    def generate_prompt(self, html_snippet: str):
        prompt = f"""
Here is a header section of an instagram profile account.\
Identify the full name , username, profile picture link, account is verified, total posts, thread name, \
thread_link, total followers, bio description, total following and a website link inside this HTML snippet. \

You can get the profile picture link by looking inside an img tag with the alt attribute having a value that contains profile picture. Then extract the value of the images src attribute.
An Example of an img tag that contains the link to the profile picture is below
<img alt="tommyhilfiger's profile picture" class="xpdipgo x11njtxf xh8yej3" crossorigin="anonymous" src="https://instagram.fnbo10-1.fna.fbcdn.net/v/t51.2885-19/275991609_639574667114215_277687374655771022_n.jpg?stp=dst-jpg_s150x150&amp;_nc_ht=instagram.fnbo10-1.fna.fbcdn.net&amp;_nc_cat=1&amp;_nc_ohc=VcfUsJ9Tqh0Q7kNvgEKQlTl&amp;edm=AOQ1c0wBAAAA&amp;ccb=7-5&amp;oh=00_AYC_FuCWSlyyWjuV6eufKjmxJt-Jq4N35Bl1kYFn1gNqCA&amp;oe=665CE419&amp;_nc_sid=8b3546">


Example 1 
The example below is how the output should look like.

{{'full_name': 'Jarib Wetshi', 'username': 'wetshi', \
'profile_picture_link': 'https://instagram.fnbo10-1.fna.fbcdn.net/v/t51.2885-19/275991609_639574667114215_277687374655771022_n.jpg?stp=dst-jpg_s150x150&_nc_ht=instagram.fnbo10-1.fna.fbcdn.net&_nc_cat=1&_nc_ohc=VcfUsJ9Tqh0Q7kNvgEKQlTl&edm=AOQ1c0wBAAAA&ccb=7-5&oh=00_AYC_FuCWSlyyWjuV6eufKjmxJt-Jq4N35Bl1kYFn1gNqCA&oe=665CE419&_nc_sid=8b3546',\
 'is_verified': True, 'total_posts': 891, 'total_followers': 789, 'total_following': 500, \
'bio_description': 'Iconic Fashion.Modern House', 'thread_name': '@wetshi_jarib', 'website': 'https://jarib-wetshi-verceel.org', \
'thread_link': 'https://www.threads.net/@wetshi_jarib?xmt=AQGzPwXa0beXxCwKiLUoFrw9qFkDPogHmN16f03pUDQvO4'}}
HTML SNIPPET:
{html_snippet}
"""
        return prompt
    

    def generate_answer(self, prompt: str) -> str:
        genai.configure(api_key=self.GEMINI_API_KEY)
        model = genai.GenerativeModel()
        answer = model.generate_content(prompt)

        return answer.text

