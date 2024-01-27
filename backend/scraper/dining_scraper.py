from bs4 import BeautifulSoup
# import requests
from selenium import webdriver
from selenium.webdriver.common.by import By

BASE_URL = 'https://uci.campusdish.com/LocationsAndMenus/'


def scrape_dining_data(eatery_id):
    print("Scraping", BASE_URL + eatery_id)

    browser = webdriver.Firefox()  # uhg ok .. if this doesnt work we can try Chrome
    browser.get(BASE_URL + eatery_id)
    browser.implicitly_wait(0.5)

    scrape_current_source(browser)
    switch_source(browser, 1)


def switch_source(browser, displacement):
    browser.implicitly_wait(5)
    print("Trying to find button...")
    # button = browser.find_element(By.CLASS_NAME, "sc-ikkxIA dVtlOt")
    # button = browser.find_element(By.XPATH, '//button')
    # button = browser.find_element(By.CLASS_NAME, 'sc-empnci kPQgyu DateMealFilterButton')

    # all buttons approach
    buttons = browser.find_elements(By.TAG_NAME, 'button')

    if buttons is None:
        print("no buttons")
    else:
        print(len(buttons), "found")
        xbutton = None
        datebutton = None
        for button in buttons:
            # print("class = \"" + button.get_attribute('class') + "\"")
            if button.get_attribute('class') == "sc-empnci kPQgyu DateMealFilterButton":
                datebutton = button
                print(True)
            elif button.get_attribute('class') == "sc-ikkxIA dVtlOt":
                xbutton = button
                print(True)
            # print()
            # print("\"" + button.text + "\"")
        xbutton.click()
        # datebutton.click()





    # button.click()



def scrape_current_source(browser):
    source = browser.page_source
    soup = BeautifulSoup(source, "html.parser")
    result = soup.find_all("h3", {"class": "sc-fXSgeo htxwrt HeaderItemName"})

    if result is None:
        print("empty")
    else:
        for res in result:
            print(res.text.strip())



def main():
    scrape_dining_data("BrandyWine")
    pass # for testing purposes only


if __name__ == "__main__":
    main()