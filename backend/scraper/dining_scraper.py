from bs4 import BeautifulSoup
# import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
import time


# constants
BASE_URL = 'https://uci.campusdish.com/LocationsAndMenus/'
MAX_TIMEOUT = 10
POLL_FREQ = 0.2
COOKIES_SLEEP = 5


def scrape_dining_data(eatery_id):
    print("Scraping", BASE_URL + eatery_id)

    browser = webdriver.Firefox()  # uhg ok .. if this doesnt work we can try Chrome
    browser.get(BASE_URL + eatery_id)

    close_popups(browser)
    # scrape_current_source(browser)
    switch_page(to=None, browser=browser)


# switch page to the next day...
def switch_page(to, browser):
    # first find the "change" button. we might need to scroll down to it.
    errors = [NoSuchElementException]
    change = (WebDriverWait(browser, timeout=MAX_TIMEOUT, poll_frequency=POLL_FREQ, ignored_exceptions=errors)
              .until(EC.presence_of_element_located((By.CLASS_NAME, "DateMealFilterButton"))))
    print(type(change))
    click_elem(change, browser)


# clicks an element. more reliable than element.click()
def click_elem(elem, browser):
    browser.execute_script("arguments[0].click();", elem)


# this function does some initial setup once it hits the first page, like clearing
# the cookies preferences and the popup that opens.
# this should only needs to be done once per session.
def close_popups(browser):
    errors = [NoSuchElementException]
    # close out of the popup
    (WebDriverWait(browser, timeout=MAX_TIMEOUT, poll_frequency=POLL_FREQ, ignored_exceptions=errors)
     .until(EC.presence_of_element_located((By.CLASS_NAME, "sc-ikkxIA"))).click())  # can only search by 1 classname @ a time.. good to know
    # close out of the cookies popup
    (WebDriverWait(browser, timeout=MAX_TIMEOUT, poll_frequency=POLL_FREQ, ignored_exceptions=errors)
     .until(EC.presence_of_element_located((By.CLASS_NAME, "banner-close-button"))).click())

    time.sleep(COOKIES_SLEEP) # big sleep here because there's some sort of JS reload after cookies menu is closed...


def scrape_current_source(browser):
    source = browser.page_source
    soup = BeautifulSoup(source, "html.parser")

    parent_categories = soup.find_all("div", {"class": "sc-dkmUuB jOJEgu MenuParentCategory"})
    if parent_categories is None:
        print("no parents LOL")

    for parent in parent_categories:
        name = parent.find("h2", {"class": "sc-bDumWk gBTLmS CategoryName"})
        print(name.text.strip())
        contents = parent.find_all("h3", {"class": "sc-fXSgeo htxwrt HeaderItemName"})
        for item in contents:
            print(item.text.strip())
        print("\n")


# for testing purposes only
def main():
    scrape_dining_data("BrandyWine")


if __name__ == "__main__":
    main()
