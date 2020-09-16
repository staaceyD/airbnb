from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
import time
import requests
from bs4 import BeautifulSoup
import csv
import os


def month_to_num(month):
    month_dict = {
        'January': 1,
        'February': 2,
        'March': 3,
        'April': 4,
        'May': 5,
        'June': 6,
        'July': 7,
        'August': 8,
        'September': 9,
        'October': 10,
        'November': 11,
        'December': 12
    }
    return month_dict[month]


def set_up(site, browser='./chromedriver'):
    global driver
    driver = webdriver.Chrome(browser)
    driver.maximize_window()
    driver.get(site)
    time.sleep(5)


def choose_city(city):

    city_field = driver.find_element_by_class_name("_1xq16jy")
    city_field.send_keys(city)


def choose_check_in_and_out_dates(check_in_date, check_out_date):
    check_in = driver.find_element_by_xpath(
        "//div[contains(text(),'Add dates')]")
    check_in.click()

    current_year_month = time.strftime("%Y-%m")

    arrow = driver.find_element_by_xpath(
        '/html/body/div[4]/div/div/div/div[1]/div[1]/div/header/div/div[2]/div[2]/div/div/div/form/div/div/div[3]/div[4]/section/div/div/div[1]/div/div/div/div[2]/div[1]/div[2]/div/button')

    check_in_month = int(check_in_date[5:7])
    check_out_month = int(check_out_date[5:7])

    current_month = int(current_year_month[-2:])

    from_today_checkin_month = check_in_month - current_month
    trip_lengh = check_out_month - check_in_month

    if check_in_month == check_out_month:
        for _ in range(from_today_checkin_month):
            arrow.click()
            time.sleep(3)

        driver.find_element_by_css_selector(
            f'div[data-testid="datepicker-day-{check_in_date}"]').click()

        driver.find_element_by_css_selector(
            f'div[data-testid="datepicker-day-{check_out_date}"]').click()
    else:
        for _ in range(from_today_checkin_month):
            arrow.click()
            time.sleep(3)
        driver.find_element_by_css_selector(
            f'div[data-testid="datepicker-day-{check_in_date}"]').click()

        for _ in range(trip_lengh):
            arrow.click()
            time.sleep(3)
        driver.find_element_by_css_selector(
            f'div[data-testid="datepicker-day-{check_out_date}"]').click()


def choose_guests_amount(ammount):
    guests = driver.find_element_by_xpath(
        "//div[contains(text(),'Add guests')]")
    guests.click()

    increase_button = driver.find_element_by_css_selector(
        'button[aria-label="increase value"]')

    for _ in range(ammount):
        increase_button.click()


def click_search():
    search = driver.find_element_by_xpath(
        '/html/body/div[4]/div/div/div/div[1]/div[1]/div/header/div/div[2]/div[2]/div/div/div/form/div/div/div[5]/div[4]/button')

    search.click()
    time.sleep(4)


def type_to_xpath(place_type):
    type_dict = {
        'Private': '//*[@id="filter-menu-chip-group"]/div[2]/div/div[2]/div/div/div/div[2]/div/div[1]/div/div[2]/label/span[1]/span',
        'Shared': '//*[@id="filter-menu-chip-group"]/div[2]/div/div[2]/div/div/div/div[2]/div/div[1]/div/div[4]/label/span[1]/span',
        'Entire': '//*[@id="filter-menu-chip-group"]/div[2]/div/div[2]/div/div/div/div[2]/div/div[1]/div/div[1]/label/span[1]/span',
        'Hotel': '//*[@id="filter-menu-chip-group"]/div[2]/div/div[2]/div/div/div/div[2]/div/div[1]/div/div[3]/label/span[1]/span'
    }
    return type_dict[place_type]


def choose_type_of_place(place_type):
    type_of_place = driver.find_element_by_xpath(
        "// span[@class='_36rlri' and text()='Type of place']")

    type_of_place.click()

    time.sleep(2)

    place = driver.find_element_by_xpath(
        type_to_xpath(place_type))
    place.click()
    save_button = driver.find_element_by_id('filter-panel-save-button')
    save_button.click()
    time.sleep(5)


def set_max_price(price):

    price_tab = driver.find_element_by_xpath(
        "// span[@class='_36rlri' and text()='Price']")

    price_tab.click()

    max_price = driver.find_element_by_id('price_filter_max')
    max_price_value = max_price.get_attribute("value")

    for _ in range(len(max_price_value)):
        max_price.send_keys(Keys.BACK_SPACE)
        time.sleep(1)

    max_price.send_keys(price)
    driver.find_element_by_id('filter-panel-save-button').click()
    print(driver.current_url)


def сollect_appartments():
    res = requests.get(driver.current_url)
    soup = BeautifulSoup(res.text, 'html.parser')
    links = soup.find_all("a", class_='_gjfol0')
    prices = soup.select('div._1fwiw8gv span._1p7iugi')

    links_and_prices = []

    for index, item in enumerate(links):
        href = links[index].get('href')
        price = prices[index].get_text()

        links_and_prices.append({'link': href, 'price': price})

    fileEmpty = os.stat('results.csv').st_size == 0
    with open("results.csv", mode="a") as file:

        writer = csv.DictWriter(file, fieldnames=links_and_prices[0].keys())
        if fileEmpty:
            writer.writeheader()
        for data in links_and_prices:
            writer.writerow(data)


def navigate_to_next_page():
    amount = driver.find_element_by_xpath(
        '//*[@id="ExploreLayoutController"]/div[1]/div[2]/div/div/div[1]/nav/ul/li[last()-1]/a').text

    arrow_next = driver.find_element_by_xpath(
        '//*[@id="ExploreLayoutController"]/div[1]/div[2]/div/div/div[1]/nav/ul/li[last()]/a')
    for _ in range(int(amount)):
        сollect_appartments()
        arrow_next.click()
