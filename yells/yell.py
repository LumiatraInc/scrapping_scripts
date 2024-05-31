import time
from playwright.sync_api import (
    sync_playwright, 
    Page, 
    ElementHandle,
)


def get_businesses_by_towns(element: ElementHandle, page: Page):
    towns_el = element.query_selector_all("li div a")

    towns = [f"https://yell.com{link.get_attribute('href')}" for link in towns_el]
    print(f"town {towns[0]}")
    page.goto(towns[0])
    # for town in towns:
    #     town_name = town.inner_text()
    #     category_town_link = town.get_attribute("href")

    #     # click the link
    #     town.click()

    #     businesses_el = page.query_selector_all("div#rightNav div div article")

    #     for business_el in businesses_el:
    #         business_el.click()
    #         get_business_data(page)


def get_business_data(page: Page):
    raise NotImplemented("get_business_data() isn't implemented")

url = "https://www.yell.com/k/popular+searches.html"
with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=False, slow_mo=1000)
    page = browser.new_page()

    page.goto(url)

    search_links_els = page.query_selector_all("ul.findLinks li div.findLinks--item a")
    search_links = [f"https://yell.com{link.get_attribute('href')}" for link in search_links_els]

    print(f"{search_links=}")

    for search_link in search_links:
        # click on link
        page.goto(search_link)

        time.sleep(5)
    
        search_divisions = page.query_selector_all("ul.findLinks")
        if search_divisions:
            town_list = search_divisions[0]
            if town_list:
                town_list.scroll_into_view_if_needed()
                time.sleep(2)
                get_businesses_by_towns(element=town_list, page=page)

        time.sleep(10)
        



    browser.close()

