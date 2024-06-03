import time, re
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
    start_urls = ["https://www.instagram.com/tommyhilfiger/"]

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

        use_ai = False

        if use_ai == False:
            instagram_profile = self.get_instagram_business_data(selector)
        else:
            instagram_profile = self.ai_get_instagram_business_data(selector)

        

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
    
    def ai_get_instagram_business_data(self, element: Selector) -> InstagramItem:
        header_section = element.css("header > section")

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

        return instagram_profile
    
    def get_instagram_business_data(self, element: Selector, isLoggedIn: bool=False) -> InstagramItem:
        instagram_profile = InstagramItem()

        profile_photo: str = None
        username: str = None
        thread_link: str = None
        thread_username: str = None
        total_posts: str = None
        total_followers: str = None
        total_following: str = None
        bio: str = None
        web_link: str = None
        link_name: str = None
        full_name: str = None

        try:
            username = self.driver.current_url.split("/")[-2]
            print(f"username {username}")
        except Exception as e:
            print(f"============> error {e}")
            pass

        if profile_photo_el := element.css(f"header img"):
            profile_photo = profile_photo_el.css("::attr(src)").get()

        if thread_link_el := element.css("a[href*='www.threads.net/@']"):
            thread_link = thread_link_el.css("::attr(href)").get()
            if thread_link:
                thread_username_pattern = r'@([^/\s]+)'
                pattern_match = re.search(thread_username_pattern, thread_link)

                if pattern_match:
                    thread_username = pattern_match.group(1).split("?")[0]

        if follow_post_el := element.css("ul > li > div >  button._acan._ap30"):
            if len(follow_post_el.getall()) == 3:
                for index, btn in enumerate(follow_post_el):
                    if index == 0:
                        if total_post_el := btn.css("span > span"):
                            total_posts = total_post_el.css("::text").get()
                    if index == 1:
                        if total_followers_el := btn.css("span[title]"):
                            total_followers = total_followers_el.css("::attr(title)").get()
                        elif total_followers_el := btn.css("span > span"):
                            total_followers = total_followers_el.css("::text").get()
                    if index == 2:
                        if total_following_el := btn.css("span > span"):
                            total_following = total_following_el.css("::text").get()
        
        if bio_el := element.css("section > div h1"):
            bio = bio_el.get()

        if web_link_el := element.css("a[href*='l.instagram.com']"):
            web_link = web_link_el.css("::attr(href)").get()
            link_name = web_link_el.css("span > span::text").get()
        elif svg_link_icon_el := element.css("svg[aria-label='Link icon']"):
            if button_link_el:= svg_link_icon_el.xpath("/parent::*/parent::*/div"):
                web_link = button_link_el.css("::text").get()
                link_name = web_link


        if full_name_el := element.xpath("//section/div[last()]/div/span"):
            full_name = full_name_el.css("::text").get()

        
        instagram_profile["profile_name"] = full_name
        instagram_profile["profile_photo"] = profile_photo
        instagram_profile["username"] = username
        # instagram_profile["is_verified"] = is_verified
        instagram_profile["total_posts"] = total_posts
        instagram_profile["total_followers"] = total_followers
        instagram_profile["total_following"] = total_following
        instagram_profile["bio_description"] = bio
        instagram_profile["thread_name"] = thread_username
        instagram_profile["thread_link"] = thread_link
        instagram_profile["source"] = "Instagram"
        instagram_profile["web_link"] = web_link
        instagram_profile["link_name"] = link_name

        return instagram_profile
        

