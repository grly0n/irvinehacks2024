from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common import action_chains as AC
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

BRANDY = "BrandyWine"
ANTEATERY = "TheAnteatery"
DAYS_TO_PULL = 14


# returns the result of the webscraping as a tuple...
# first element is the constructed database
# second element is the time that the scrape started at
def get_info(eatery_id):
    if eatery_id == BRANDY:
        start_time = time.time()
        scrape_result = scrape_dining_data(BRANDY)
        delta = time.time() - start_time
        print(f"scraped brandy in {delta} seconds.")
        return scrape_result, start_time
    elif eatery_id == ANTEATERY:
        start_time = time.time()
        scrape_result = scrape_dining_data(ANTEATERY)
        delta = time.time() - start_time
        print(f"scraped anteatery in {delta} seconds.")
        return scrape_result, start_time
    else:
        print(eatery_id, "invalid.")
        exit(1)


def scrape_dining_data(eatery_id):
    database = {}
    browser = webdriver.Firefox()  # uhg ok .. if this doesnt work we can try Chrome
    browser.get(BASE_URL + eatery_id)
    browser.implicitly_wait(10)

    close_popups(browser)
    open_change_menu(browser)
    open_meal_menu(browser)
    switch_to_brunch(browser)
    press_done(browser)
    print(f"working on {eatery_id}...")
    current_date = (1, 28)
    for days_ahead in range(0, DAYS_TO_PULL):  # does 14 days, starting on ideally a sunday
        meal_map = {}
        if days_ahead > 0:
            switch_page(to=current_date, browser=browser)

        meal_map["Lunch"] = scrape_brandy_source(browser) if eatery_id == BRANDY else scrape_anteatery_source(browser)  # this could be a helper vv
        open_change_menu(browser)
        open_meal_menu(browser)
        switch_to_dinner(browser)
        press_done(browser)
        meal_map["Dinner"] = scrape_brandy_source(browser) if eatery_id == BRANDY else scrape_anteatery_source(browser)

        date_as_str = date_to_string(current_date)
        print(date_as_str, end=" ")
        if date_as_str not in database.keys():
            database[date_as_str] = {}
        database[date_as_str] = meal_map
        current_date = next_date(current_date)
    print()
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


# returns the date tuple as a string
def date_to_string(today):
    return str(today[0]) + '-' + str(today[1])


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
    # meal = (WebDriverWait(browser, timeout=MAX_TIMEOUT, poll_frequency=POLL_FREQ, ignored_exceptions=ERRORS)
    #         .until(EC.presence_of_element_located((By.CLASS_NAME, "select-wrapper-main"))))
    meal = browser.find_element(By.CLASS_NAME, "select-wrapper-main")
    action = AC.ActionChains(browser)
    action.move_to_element_with_offset(meal, 5, 5)
    action.click()
    action.perform()
    time.sleep(1)

    # print(meal.location)
    # click_elem(meal, browser)


def switch_to_brunch(browser):
    brunch = browser.find_element(By.CSS_SELECTOR, ".css-1nmdiq5-menu")
    action = AC.ActionChains(browser)
    action.move_to_element_with_offset(brunch, 0, 0)
    action.click()
    action.perform()
    # time.sleep(1)


def switch_to_dinner(browser):
    dinner = browser.find_element(By.CSS_SELECTOR, ".css-1nmdiq5-menu")
    action = AC.ActionChains(browser)
    action.move_to_element_with_offset(dinner, 5, 35)
    action.click()
    action.perform()


# document me
def open_change_menu(browser):
    change = browser.find_element(By.CLASS_NAME, "DateMealFilterButton")
    click_elem(change, browser)


# document me
def open_date_picker(browser):
    datepicker = browser.find_element(By.CLASS_NAME, "DatePickerButton")
    click_elem(datepicker, browser)


# requires datepicker to be open. TODO: make this work with years...
def get_current_month(browser):
    date_strs = browser.find_element(By.CLASS_NAME, "react-datepicker__current-month").text.strip().split(" ")
    return DATE_STR_TO_INT[date_strs[0]]


def press_done(browser):
    done_button = browser.find_element(By.CLASS_NAME, "Done")
    click_elem(done_button, browser)
    time.sleep(SHORT_SLEEP)


def change_date(to, browser, attempt2=False):
    attempts = 0
    while get_current_month(browser) < to[0]:
        if attempts >= 3:
            return False  # date could not be found...
        current = get_current_month(browser)  # datepicker is open...
        if current < to[0]:  # if current month is < our intended current month...
            next_month(browser)
        attempts += 1

    if get_current_month(browser) != to[0]:
        return False  # could not be found...

    # should be on the right month now...

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
    next_month_button = browser.find_element(By.CLASS_NAME, "react-datepicker__navigation--next")
    click_elem(next_month_button, browser)


# clicks an element. more reliable than element.click()
def click_elem(which, browser):
    browser.execute_script("arguments[0].click();", which)


# this function does some initial setup once it hits the first page, like clearing
# the cookies preferences and the popup that opens.
# this should only needs to be done once per session.
def close_popups(browser):
    popup_button = browser.find_element(By.CLASS_NAME, "sc-ikkxIA")
    click_elem(popup_button, browser)

    # close out of the cookies popup
    cookies_button = browser.find_element(By.CLASS_NAME, "banner-close-button")
    click_elem(cookies_button, browser)

    time.sleep(COOKIES_SLEEP) # big sleep here because there's some sort of JS reload after cookies menu is closed...


# this is just for brandy... TODO: update this function's name...
def scrape_brandy_source(browser):
    source = browser.page_source
    soup = BeautifulSoup(source, "html.parser")
    stations_dict = dict()

    stations = soup.find_all("div", {"class": "MenuStation"})

    if stations is None:
        print("no stations found")

    else:
        for station in stations:
            name = station.find("h2", {"class": "StationHeaderTitle"}).text.strip()
            if name not in ["Grubb/ Mainline", "Hearth/Pizza", "Soups", "Crossroads", "Compass"]:
                continue
            else:  # scrape info from this station
                stations_dict[name] = []
                parent_categories = station.find_all("div", {"class": "sc-dkmUuB jOJEgu MenuParentCategory"})
                if parent_categories is None:
                    print("no parents LOL")
                for parent in parent_categories:
                    contents = parent.find_all("h3", {"class": "sc-fXSgeo htxwrt HeaderItemName"})
                    for item in contents:
                        stations_dict[name].append(item.text.strip())  # TODO: figure out the single-quote conundrum...

    return stations_dict


# this only scrapes info from anteatery pages
def scrape_anteatery_source(browser):
    source = browser.page_source
    soup = BeautifulSoup(source, "html.parser")
    stations_dict = dict()

    stations = soup.find_all("div", {"class": "MenuStation_no-categories"})
    if len(stations) == 0:
        print("no stations")

    else:
        for station in stations:
            name = station.find("h2", {"class": "StationHeaderTitle"}).text.strip()
            if name not in ["Home", "Oven", "Vegan", # "Sizzle Grill", "Bakery",
                            "Soups", "Fire And Ice Round Grill", "Fire And Ice Sauté"]:
                continue

            else:  # scrape info from this station
                stations_dict[name] = []
                parent_categories = station.find_all("div", {"class": "MenuItemsDiv"})
                if len(parent_categories) == 0:
                    print("no parents LOL")
                for parent in parent_categories:
                    contents = parent.find_all("h3", {"class": "HeaderItemName"})
                    for item in contents:
                        stations_dict[name].append(item.text.strip())

    return stations_dict


# for testing purposes only
def main():
    print(get_info(BRANDY))
    print(get_info(ANTEATERY))


if __name__ == "__main__":
    main()
