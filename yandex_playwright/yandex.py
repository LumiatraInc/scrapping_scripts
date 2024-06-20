import time, math
import random
import asyncio
from playwright.sync_api import (
    sync_playwright,
    Page,
    ElementHandle
)

from utils.types import GetBusinessMode
from utils.convert_to_file import write_to_json_file
from utils.clean_data import clean_data

url = "https://yandex.com/maps"
search_term = "restaurants in Paris"


def get_business_by_category(page: Page):
    categories_titles_els = page.query_selector_all(
        "h3.catalog-grid-view__text")
    categories_titles: list[str] = [title.text_content()
                                    for title in categories_titles_els]

    for index, category_title in enumerate(categories_titles):
        # click on the more button
        more_btn_el = page.query_selector(
            "div._id_more > div.catalog-grid-view__icon")
        more_btn_el.click()

        print(f"category title {category_title}")
        time.sleep(15)
        if categories_els := page.query_selector_all("div.catalog-grid-view__icon"):
            category_el = categories_els[index]
            category_el.click()
            print(f"navigate to {category_title}")
        else:
            print(f"Couldn't find the category {category_title}")

        time.sleep(15)

        print("go back")
        page.goto(url)

def click_overview_tab(element: ElementHandle, page: Page):
    if overview_tab := element.query_selector("div.tabs-select-view__title._name_overview._selected"):
        overview_tab.scroll_into_view_if_needed()
        overview_tab.click()


def scroll_search_result_list(page: Page):
    print("start scrolling")
    number_of_loaded_businesses = 0
    number_of_loading_retries = 0 # retry upto 1
    loop_counts = 0
    while True:
        loaded_business_items_els = page.query_selector_all(
                "li.search-snippet-view")
        number_of_loaded_businesses = len(loaded_business_items_els)
        # Get the initial scroll height of the sidebar
        
        if business_items_els := page.query_selector_all("ul.search-list-view__list > div"):
            last_business_item = business_items_els[math.ceil(len(business_items_els) / 2)]
            last_business_item.scroll_into_view_if_needed()
        else:
            last_business_item = loaded_business_items_els[-1]
            last_business_item.scroll_into_view_if_needed()

        print("scrolling...")
        time.sleep(random.randint(4, 6))


        # stop scrolling when the div div.add-business-view shows on the bottom
        if page.query_selector("div.add-business-view"):
            print("End of list")
            break
        elif number_of_loaded_businesses == len(loaded_business_items_els):
            # if number loading retries gets to 5, we have reached the end of the list
            # otherwise increment loading retries
            if number_of_loading_retries == 5:
                print("End of list")
                break
            else:
                number_of_loading_retries += 1

        elif number_of_loaded_businesses < len(loaded_business_items_els):
            # reset it to 0 because more businesses have been loaded
            number_of_loading_retries = 0

        else:
            continue


def get_business_name(element: ElementHandle) -> (str | None):
    # get the business name with the selector a.card-title-view__title-link::text
    if business_name_el := element.query_selector("a.card-title-view__title-link"):
        return business_name_el.text_content()
    
    
def is_business_verified(element: ElementHandle) -> bool:
    # get if business is verified with selector div.sidebar-view__panel._no-padding 
    if verified_badge_el := element.query_selector("span.business-verified-badge span.business-verified-badge"):
        return True
    else:
        return False
    
def get_business_category(element: ElementHandle) -> bool:
    # get business category with the selector div.business-card-title-view__categories a
    if business_category_el := element.query_selector("div.business-card-title-view__categories a"):
        return business_category_el.text_content()

def get_total_ratings(element: ElementHandle) -> (str | None):
    # get total ratings with the selector div.business-header-rating-view__text._clickable
    if total_rating_el := element.query_selector("div.business-header-rating-view__text._clickable"):
        if total_rating_el.text_content() != "Write review":
            return total_rating_el.text_content()

def get_business_rating(element: ElementHandle) -> (str | None):
    # get the rating with the selector div.business-header-rating-view span.business-rating-badge-view__rating-text
    if business_rating_el := element.query_selector("div.business-header-rating-view span.business-rating-badge-view__rating-text"):
        return business_rating_el.text_content()
    
def get_business_website(element: ElementHandle) -> (str | None):
    # get the business website with selector a.business-urls-view__link
    if website_el := element.query_selector("a.business-urls-view__link"):
        return website_el.get_attribute("href")
    
def get_business_address(element: ElementHandle) -> (str | None):
    # get the address with the selector div.business-contacts-view__address-link
    if business_address_el := element.query_selector("div.business-contacts-view__block div.business-contacts-view__address-link"):
        return business_address_el.text_content()
    
def get_business_phone_number(element: ElementHandle) -> (str | None):
    # get the phonenumber with the selector div.sidebar-view__panel._no-padding span[itemprop="telephone"]
    if business_phone_number_el := element.query_selector("div.business-contacts-view__block span[itemprop='telephone']"):
        return business_phone_number_el.text_content()
    
def get_business_social_media(element: ElementHandle) -> dict[str, str]:
    social_medias: dict = {}
    # get social media name with selector div.business-contacts-view__social-links div.business-contacts-view__social-button > a::attr(aria-label).split(" ")[-1]
    if social_media_name_els := element.query_selector_all("div.business-contacts-view__social-links div.business-contacts-view__social-button > a"):
        for social_media in social_media_name_els:
            social_media_name = "media"
            social_media_link = None
            if social_media_name_el := social_media.get_attribute("aria-label"):
                social_media_name = social_media_name_el.split(" ")[-1]
            if social_media_link_el := social_media.get_attribute("href"):
                social_media_link = social_media_link_el
        
            social_medias[social_media_name] = social_media_link

        
    return social_medias


def click_feature_tab(element: ElementHandle, page: Page):
    if feature_tab_el := element.query_selector("div.tabs-select-view__title._name_features"):
        feature_tab_el.scroll_into_view_if_needed()
        feature_tab_el.click()

def get_business_services(element: ElementHandle) -> dict[str, list[str]]:
    business_services: dict[str, list] = {}
    if feature_titles_el := element.query_selector_all("div.business-features-view__group-title > div"):
        feature_titles = [title.text_content() for title in feature_titles_el]
        if feature_items_els := element.query_selector_all("div.sidebar-view__panel._no-padding div.features-cut-view div.business-features-view__bool-list"):
            for title, items in zip(feature_titles, feature_items_els):
                if services_el := items.query_selector_all("div.business-features-view__bool-text"):
                    services = [service.text_content() for service in services_el]
                    business_services[title] = services

    return business_services


def get_business_info(element: ElementHandle, page: Page) -> dict[str, (str | int | list | dict | bool)]:
    business_info: dict[str, (str | int | list | dict | bool)] = {}

    business_name = get_business_name(element=element)
    is_verified = is_business_verified(element=element)
    business_category = get_business_category(element=element)
    total_ratings = get_total_ratings(element=element)
    business_rating = get_business_rating(element=element)

    # click on overview tab
    click_overview_tab(element=element, page=page)
    time.sleep(3)

    business_website = get_business_website(element=element)
    business_address = get_business_address(element=element)
    business_phone_number  = get_business_phone_number(element=element)
    social_medias = get_business_social_media(element=element)


    # click on feature tab
    click_feature_tab(element=element, page=page)
    time.sleep(3)
    
    business_services = get_business_services(element=element)

    
    business_info["business_name"] = business_name
    business_info["business_website"] = business_website
    business_info["is_verified"] = is_verified
    business_info["business_category"] = business_category
    business_info["total_ratings"] = total_ratings
    business_info["business_rating"] = business_rating
    business_info["business_address"] = business_address
    business_info["business_phone_number"] = business_phone_number
    business_info["social_medias"] = social_medias
    business_info["business_services"] = business_services

    return business_info


def get_business_by_search(page: Page) -> list [dict]:
    # get search input
    input_el = page.get_by_placeholder("Search places and addresses")
    input_el.fill(search_term)
    page.keyboard.press("Enter")

    page.evaluate("document.body.requestFullscreen()")
    time.sleep(20)

    # scroll the section
    search_result_el = page.query_selector("div.scroll__container")
    # scroll_search_result_list(page=page)

    # get all the businesses
    if businesses_items_els := page.query_selector_all("li.search-snippet-view > div > div > div"):
        # loop through business
        businesses: list[dict] = []
        for business_item_el in businesses_items_els:
            time.sleep(random.randint(3, 10))
            # get business data id through selector div.search-snippet-view__body _type_business::attr(data-object)
            if data_id_el := business_item_el.query_selector("div.search-snippet-view__body _type_business"):
                data_id = data_id_el.get_attribute("data-object")
                print(f"{data_id=}")

            # get business place coordinate through selector div.search-snippet-view__body _type_business::attr(data-coordinates)
            if business_coordinates_el := business_item_el.query_selector("div.search-snippet-view__body _type_business"):
                business_coordinate = business_coordinates_el.get_attribute(
                    "data-coordinates")
                print(f"{business_coordinate=}")

            # click at a business for the sidebar view to show.
            # The container is gotten with the selector div.sidebar-view__panel._no-padding
            try:
                business_item_el.click()
            except Exception as e:
                print(f"==========> Error {e}")
                return None

            time.sleep(10)
            # get the business card
            if business_section_el := page.query_selector("div.sidebar-view__panel._no-padding"):
                business_info = get_business_info(element=business_section_el, page=page)
                businesses.append(business_info)

        return businesses

def main():
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False)
        context = browser.new_context(
            viewport={'width': 1920, 'height': 1080}
        )
        page = context.new_page()

        page.goto(url)
        time.sleep(60)

        get_business_mode = GetBusinessMode.SEARCH

        if get_business_mode == GetBusinessMode.CATEGORY:
            get_business_by_category(page=page)
        else:
            businesses = get_business_by_search(page=page)

        print(f"{businesses=}")
        clean_business = clean_data(data=businesses)
        print(f"{clean_business=}")
        time.sleep(5)
        # write to json file
        write_to_json_file(data=clean_business)

        time.sleep(10)
        browser.close()
        playwright.stop()


main()
