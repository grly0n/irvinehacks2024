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
SHORT_SLEEP = 3
ERRORS = [NoSuchElementException]
DATE_STR_TO_INT = {
    "January"   : 1,
    "February"  : 2,
    "March"     : 3,
    "April"     : 4,
    "May"       : 5,
    "June"      : 6,
    "July"      : 7,
    "August"    : 8,
    "September" : 9,
    "October"   : 10,
    "November"  : 11,
    "December"  : 12,
}


def scrape_dining_data(eatery_id):
    browser = webdriver.Firefox()  # uhg ok .. if this doesnt work we can try Chrome
    browser.get(BASE_URL + eatery_id)

    # main program
    close_popups(browser)
    menus = []
    # scrape_current_source(browser)

    current_date = (1, 27)
    for i in range(0, 25):  # does 25 days in advance as of rn...
        print("scraping", current_date)
        if i > 0:
            switch_page(to=current_date, browser=browser)
        menus.append(scrape_current_source(browser))
        current_date = next_date(current_date)


def next_date(current_date):
    tomorrow_day = current_date[1] + 1
    tomorrow_month = current_date[0]
    if current_date[0] in [4, 6, 9, 11]:  # 30 days
        if tomorrow_day >= 31:
            tomorrow_month += 1
            tomorrow_day = 1
    elif current_date[0] == 2:  # handle february # TODO: handle leap years !!!
        if tomorrow_day >= 29:
            tomorrow_month += 1
            tomorrow_day = 1
    elif current_date[0] in [1, 3, 5, 7, 8, 10, 12]:  # 31 days
        if tomorrow_day >= 32:
            tomorrow_month += 1
            tomorrow_day = 1
    return tomorrow_month, tomorrow_day


# switch page to the next day...
def switch_page(to, browser):
    # first find the "change" button. we might need to scroll down to it.
    open_change_menu(browser)
    open_date_picker(browser)

    # switch dates
    success = change_date(to, browser)  # if this returns False, we're done
    if not success:
        print("Date", to, "was not found.")

    press_done(browser)


# document me
def open_change_menu(browser):
    change = (WebDriverWait(browser, timeout=MAX_TIMEOUT, poll_frequency=POLL_FREQ, ignored_exceptions=ERRORS)
              .until(EC.presence_of_element_located((By.CLASS_NAME, "DateMealFilterButton"))))
    click_elem(change, browser)


# document me
def open_date_picker(browser):
    datepicker = (WebDriverWait(browser, timeout=MAX_TIMEOUT, poll_frequency=POLL_FREQ, ignored_exceptions=ERRORS)
                  .until(EC.presence_of_element_located((By.CLASS_NAME, "DatePickerButton"))))
    click_elem(datepicker, browser)


# requires datepicker to be open. TODO: make this work with years...
def get_current_month(browser):
    date_strs = ((WebDriverWait(browser, timeout=MAX_TIMEOUT, poll_frequency=POLL_FREQ, ignored_exceptions=ERRORS)
                 .until(EC.presence_of_element_located((By.CLASS_NAME, "react-datepicker__current-month"))))
                 .text.strip().split(" "))
    return DATE_STR_TO_INT[date_strs[0]]


def press_done(browser):
    done_button = (WebDriverWait(browser, timeout=MAX_TIMEOUT, poll_frequency=POLL_FREQ, ignored_exceptions=ERRORS)
                   .until(EC.presence_of_element_located((By.CLASS_NAME, "Done"))))
    click_elem(done_button, browser)


def change_date(to, browser, attempt2=False):
    attempts = 0
    while get_current_month(browser) < to[0]:
        if attempts >= 3:
            return False  # date could not be found...
        get_current_month(browser)  # datepicker is open...
        if to[0] < to[1]:
            next_month(browser)
        attempts += 1

    if get_current_month(browser) != to[0]:
        return False  # could not be found...

    # should be on the right mont now...

    (WebDriverWait(browser, timeout=MAX_TIMEOUT, poll_frequency=POLL_FREQ, ignored_exceptions=ERRORS)
     .until(EC.presence_of_element_located((By.CLASS_NAME, "ejvkOn"))))

    dates = browser.find_elements(By.CLASS_NAME, "ejvkOn")
    target = None  # not target int, target date obj
    for date in dates:
        try:
            if int(date.text.strip()) == to[1]:
                target = date
        except ValueError:
            continue

    if target is None:
        return False
    else:
        click_elem(target, browser)

    time.sleep(SHORT_SLEEP)  # short sleep to accommodate load time

    return True  # signifies that we found the date & clicked it


def next_month(browser):
    next_month_button =(WebDriverWait(browser, timeout=MAX_TIMEOUT, poll_frequency=POLL_FREQ, ignored_exceptions=ERRORS)
                        .until(EC.presence_of_element_located((By.CLASS_NAME, "react-datepicker__navigation--next"))))
    click_elem(next_month_button, browser)
    time.sleep(SHORT_SLEEP)


# clicks an element. more reliable than element.click()
def click_elem(which, browser):
    browser.execute_script("arguments[0].click();", which)


# this function does some initial setup once it hits the first page, like clearing
# the cookies preferences and the popup that opens.
# this should only needs to be done once per session.
def close_popups(browser):
    # close out of the popup
    popup_button = (WebDriverWait(browser, timeout=MAX_TIMEOUT, poll_frequency=POLL_FREQ, ignored_exceptions=ERRORS)
                    .until(EC.presence_of_element_located((By.CLASS_NAME, "sc-ikkxIA"))))  # can only search by 1 classname @ a time.. good to know
    click_elem(popup_button, browser)

    # close out of the cookies popup
    cookies_button = (WebDriverWait(browser, timeout=MAX_TIMEOUT, poll_frequency=POLL_FREQ, ignored_exceptions=ERRORS)
                      .until(EC.presence_of_element_located((By.CLASS_NAME, "banner-close-button"))))
    click_elem(cookies_button, browser)

    time.sleep(COOKIES_SLEEP) # big sleep here because there's some sort of JS reload after cookies menu is closed...


def scrape_current_source(browser):
    source = browser.page_source
    soup = BeautifulSoup(source, "html.parser")
    print("Scraping...")

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

    return None


# for testing purposes only
def main():
    scrape_dining_data("BrandyWine")


if __name__ == "__main__":
    main()
