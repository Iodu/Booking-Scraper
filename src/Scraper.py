import os
import re
import time

import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def setup_webdriver_and_url(
    url="https://www.booking.com/hotel/us/holiday-inn-express-columbus-dublin.html?",
):
    driver = webdriver.Chrome(service_log_path=r"chromedriver.log")
    driver.get(url)
    return driver


def open_reviews_tab(driver):
    reviews_tab_button = driver.find_element_by_id("show_reviews_tab")
    reviews_tab_button.click()
    time.sleep(4)


def get_reviews_tab(driver):
    reviews = driver.find_elements_by_class_name("c-review-block")
    xd = open("xd", "w")

    for review in reviews:
        print(review.get_attribute("OuterHTML"))
        xd.write(review.text)


if __name__ == "__main__":
    driver = setup_webdriver_and_url()
    open_reviews_tab(driver)
    get_reviews_tab(driver)
    driver.quit()
