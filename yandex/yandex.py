from playwright.sync_api import sync_playwright

url = "https://yandex.com/maps"
with sync_playwright() as playwright:
    browser = playwright.chromium.launch()
    page = browser.new_page()

    page.goto(url)

    all_places_btn = page.query_selector("div[title='All places']")
    all_places_btn.click()

    categories = page.query_selector_all("div[aria-label='Quick nearby search'] > div > div > div")

    for category in categories:
        category_name = category.get_attribute("title")


    # TODO! Needs to solve captcha recaptcha
    

