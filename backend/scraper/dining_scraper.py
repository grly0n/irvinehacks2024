from bs4 import BeautifulSoup
# import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common import action_chains as AC
import time


# constants
BASE_URL = 'https://uci.campusdish.com/LocationsAndMenus/'
MAX_TIMEOUT = 10
POLL_FREQ = 0.2
COOKIES_SLEEP = 5
SHORT_SLEEP = 2.5
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

BRANDY = "BrandyWine"
ANTEATERY = "TheAnteatery"


def scrape_dining_data(eatery_id, database):
    browser = webdriver.Firefox()  # uhg ok .. if this doesnt work we can try Chrome
    browser.get(BASE_URL + eatery_id)

    close_popups(browser)
    open_change_menu(browser)
    open_meal_menu(browser)
    switch_to_brunch(browser)
    press_done(browser)

    current_date = (1, 27)
    for days_ahead in range(0, 15):  # does 25 days in advance as of rn...
        print("scraping", current_date)
        meal_map = {}
        if days_ahead > 0:
            switch_page(to=current_date, browser=browser)
        meal_map["Lunch"] = scrape_current_source(browser)  # this could be a helper vv
        open_change_menu(browser)
        open_meal_menu(browser)
        switch_to_dinner(browser)
        press_done(browser)
        meal_map["Dinner"] = scrape_current_source(browser)
        current_date = next_date(current_date)

        if current_date not in database.keys():
            database[current_date] = {}
        database[current_date][eatery_id] = meal_map
        print(database)

    return database


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

    open_meal_menu(browser)
    switch_to_brunch(browser)

    press_done(browser)


def switch_meal(to, browser):
    open_change_menu(browser)


def open_meal_menu(browser):
    meal = (WebDriverWait(browser, timeout=MAX_TIMEOUT, poll_frequency=POLL_FREQ, ignored_exceptions=ERRORS)
            .until(EC.presence_of_element_located((By.CLASS_NAME, "select-wrapper-main"))))
    action = AC.ActionChains(browser)
    action.move_to_element_with_offset(meal, 5, 5)
    action.click()
    action.perform()
    time.sleep(1)

    # print(meal.location)
    # click_elem(meal, browser)


def switch_to_brunch(browser):
    brunch = (WebDriverWait(browser, timeout=MAX_TIMEOUT, poll_frequency=POLL_FREQ, ignored_exceptions=ERRORS)
              .until(EC.presence_of_element_located((By.CSS_SELECTOR, ".css-1nmdiq5-menu"))))
    print("Switching to brunch...")
    action = AC.ActionChains(browser)
    action.move_to_element_with_offset(brunch, 0, 0)
    action.click()
    action.perform()
    time.sleep(1)


def switch_to_dinner(browser):
    dinner = (WebDriverWait(browser, timeout=MAX_TIMEOUT, poll_frequency=POLL_FREQ, ignored_exceptions=ERRORS)
              .until(EC.presence_of_element_located((By.CSS_SELECTOR, ".css-1nmdiq5-menu"))))
    print("Switching to dinner...")
    action = AC.ActionChains(browser)
    action.move_to_element_with_offset(dinner, 5, 35)
    action.click()
    action.perform()
    time.sleep(1)


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
    time.sleep(SHORT_SLEEP)
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
        current = get_current_month(browser)  # datepicker is open...
        print("current month: " + str(get_current_month(browser)))
        if current < to[0]:  # if current month is < our intended current month...
            next_month(browser)
        attempts += 1

    if get_current_month(browser) != to[0]:
        return False  # could not be found...

    # should be on the right month now...

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

    # time.sleep(SHORT_SLEEP)  # short sleep to accommodate load time

    return True  # signifies that we found the date & clicked it


def next_month(browser):
    next_month_button =(WebDriverWait(browser, timeout=MAX_TIMEOUT, poll_frequency=POLL_FREQ, ignored_exceptions=ERRORS)
                        .until(EC.presence_of_element_located((By.CLASS_NAME, "react-datepicker__navigation--next"))))
    print("next month button @", next_month_button.location)
    click_elem(next_month_button, browser)
    time.sleep(SHORT_SLEEP)


# clicks an element. more reliable than element.click()
def click_elem(which, browser):
    browser.execute_script("arguments[0].click();", which)
    time.sleep(SHORT_SLEEP)


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


# this is just for brandy... TODO: update this function's name...
def scrape_current_source(browser):
    source = browser.page_source
    soup = BeautifulSoup(source, "html.parser")
    stations_dict = dict()
    print("Scraping...")

    stations = soup.find_all("div", {"class": "MenuStation"})

    if stations is None:
        print("no stations found")

    else:
        for station in stations:
            name = station.find("h2", {"class": "StationHeaderTitle"}).text.strip()
            if name not in ["Grubb/ Mainline", "Hearth/Pizza", "Soups", "Crossroads"]:
                continue
            else:  # scrape info from this station
                stations_dict[name] = []
                parent_categories = station.find_all("div", {"class": "sc-dkmUuB jOJEgu MenuParentCategory"})
                if parent_categories is None:
                    print("no parents LOL")
                for parent in parent_categories:
                    # parentname = parent.find("h2", {"class": "sc-bDumWk gBTLmS CategoryName"}).text.strip()
                    contents = parent.find_all("h3", {"class": "sc-fXSgeo htxwrt HeaderItemName"})
                    for item in contents:
                        stations_dict[name].append(item.text.strip())  # TODO: figure out the single-quote conundrum...
        # print(stations_dict)

    return stations_dict


# for testing purposes only
def main():
    # brandy_base = scrape_dining_data(BRANDY, {})
    ant_base    = scrape_dining_data(ANTEATERY, {})

    # print(brandy_base)
    print(ant_base)


if __name__ == "__main__":
    main()
