from bs4 import BeautifulSoup
# import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
import time

BASE_URL = 'https://uci.campusdish.com/LocationsAndMenus/'


def scrape_dining_data(eatery_id):
    print("Scraping", BASE_URL + eatery_id)

    browser = webdriver.Firefox()  # uhg ok .. if this doesnt work we can try Chrome
    browser.get(BASE_URL + eatery_id)

    close_popups(browser)
    scrape_current_source(browser)


# switch page to the next day...
def switch_contexts(browser, to):
    pass


# this function does some inital setup once it hits the first page, like clearing
# the cookies preferences and the popup that opens.
# this should only needs to be done once per session.
def close_popups(browser):
    errors = [NoSuchElementException]
    # close out of the popup
    (WebDriverWait(browser, timeout=10, poll_frequency=0.2, ignored_exceptions=errors)
     .until(EC.presence_of_element_located((By.CLASS_NAME, "sc-ikkxIA"))).click())  # can only search by 1 classname @ a time.. good to know
    # close out of the cookies popup
    (WebDriverWait(browser, timeout=10, poll_frequency=1, ignored_exceptions=errors)
     .until(EC.presence_of_element_located((By.CLASS_NAME, "banner-close-button"))).click())


def scrape_current_source(browser):
    source = browser.page_source
    soup = BeautifulSoup(source, "html.parser")

    parentcategories = soup.find_all("div", {"class": "sc-dkmUuB jOJEgu MenuParentCategory"})
    if parentcategories is None:
        print("no parents LOL")

    for parent in parentcategories:
        name = parent.find("h2", {"class": "sc-bDumWk gBTLmS CategoryName"})
        print(name.text.strip())
        contents = parent.find_all("h3", {"class": "sc-fXSgeo htxwrt HeaderItemName"})
        for item in contents:
            print(item.text.strip())
        print("\n")


def main():
    scrape_dining_data("BrandyWine")
    pass  # for testing purposes only


if __name__ == "__main__":
    main()
