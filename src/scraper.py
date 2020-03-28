import platform
import re
import sys
import time
from datetime import datetime

from bs4 import BeautifulSoup
from dateutil.parser import parse
from selenium import webdriver

hotel = {}
hotel_address = None
hotel_name = None
total_number_of_reviews = None
lat = None
lng = None
average_score = None

#  TODO: Additional_Number_of_Scoring and Total_Number_of_Reviews_Reviewer_Has_Given


def setup_webdriver_and_url(
    url="https://www.booking.com/hotel/us/holiday-inn-express-columbus-dublin.html",
):
    if platform.system() == "Windows":
        driver = webdriver.Chrome(
            executable_path=r"..\chromedriver.exe", service_log_path=r"chromedriver.log"
        )
    else:
        driver = webdriver.Chrome(service_log_path=r"chromedriver.log")
    try:
        if "https" in sys.argv[1]:
            url = sys.argv[1]
    except IndexError:
        pass
    driver.get(url)
    return driver


def accept_cookies(driver):
    cookie_button = driver.find_elements_by_class_name("cookie-warning-v2__banner-cta")
    if len(cookie_button) > 1:
        cookie_button[0].click()
    time.sleep(4)


def handle_hotel_info(driver):
    hotel["hotel_address"] = __element_text_by_class(
        driver, "hp_address_subtitle"
    ).replace(",", "")
    hotel["hotel_name"] = __element_text_by_class(driver, "hp__hotel-name")

    total_number_of_reviews = __element_text_by_class(driver, "hp_nav_reviews_link")
    lat_lng = driver.find_elements_by_class_name("show_on_map_hp_link")[
        0
    ].get_attribute("data-atlas-latlng")
    lat_lng = lat_lng.split(",")
    hotel["lat"] = lat_lng[0]
    hotel["lng"] = lat_lng[1]
    hotel["total_number_of_reviews"] = re.findall(r"\d+", total_number_of_reviews)[0]


def open_reviews_tab(driver):
    reviews_tab_button = driver.find_element_by_id("show_reviews_tab")
    reviews_tab_button.click()
    time.sleep(4)


def get_reviews_tab(driver):
    hotel["average_score"] = __element_text_by_class(
        driver, "review-score-widget"
    ).split(" ")[0]

    reviews = driver.find_elements_by_class_name("c-review-block")
    file_name = input("Filename? ")
    new_or_old = input("New or old file? ")
    file = open(file_name, "a")

    if new_or_old.lower() == "new":
        file.write(
            "Hotel_Address,Additional_Number_of_Scoring,Review_Date,Average_Score,Hotel_Name,Reviewer_Nationality,Negative_Review,Review_Total_Negative_Word_Counts,Total_Number_of_Reviews,Positive_Review,Review_Total_Positive_Word_Counts,Total_Number_of_Reviews_Reviewer_Has_Given,Reviewer_Score,Tags,days_since_review,lat,lng\n"
        )

    for review in reviews:
        review_list = handle_review_webelement(review)
        write_review_to_file(file, review_list)
    try:
        if sys.argv[1].lower() == "screenshots":
            for i in range(len(reviews)):
                reviews[i].screenshot("review - " + str(i + 1) + ".png")
    except IndexError:
        pass


def handle_review_webelement(review):
    review_list = []
    review_date, days_since_review = __handle_date_and_days_since(review)
    reviewer_nationality = __element_text_by_class(review, "bui-avatar-block__subtitle")
    reviewer_score = __element_text_by_class(review, "bui-review-score__badge")
    blij = review.find_elements_by_class_name("c-review__inner--ltr")
    positive_review = ""
    negative_review = ""
    if len(blij) > 0:
        positive_review = (
            __handle_review_text(blij[0].text, "Liked")
            .strip()
            .replace("\n", "")
            .replace(",", "")
        )
        if len(blij) > 1:
            negative_review = (
                __handle_review_text(blij[1].text, "Disliked")
                .strip()
                .replace("\n", "")
                .replace(",", "")
            )
    review_total_positive_word_counts = len(positive_review.split())
    if review_total_positive_word_counts < 1:
        review_total_positive_word_counts = "No Positive"
    review_total_negative_word_counts = len(negative_review.split())
    if review_total_negative_word_counts < 1:
        review_total_negative_word_counts = "No Negative"
    tags = __build_tags(review)
    review_list = [
        hotel["hotel_address"],
        " ",
        review_date,
        hotel["average_score"],
        hotel["hotel_name"],
        reviewer_nationality,
        negative_review,
        review_total_negative_word_counts,
        total_number_of_reviews,
        positive_review,
        review_total_positive_word_counts,
        " ",
        reviewer_score,
        tags,
        days_since_review,
        hotel["lat"],
        hotel["lng"],
    ]
    return review_list


def write_review_to_file(file, review_list):
    csv_string = ""
    for cell in review_list:
        if cell is None:
            cell = ""
        csv_string += str(cell) + ","
    csv_string = csv_string[:-1]

    file.write(csv_string + "\n")


def __element_text_by_class(element, css_class):
    elements = element.find_elements_by_class_name(css_class)
    if len(elements) > 0:
        return element.find_elements_by_class_name(css_class)[0].text
    else:
        return None


def __handle_date_and_days_since(review):
    review_date = __element_text_by_class(review, "c-review-block__date")
    review_date = review_date.replace("Reviewed: ", "")
    review_date = parse(review_date)
    days_since_review = (datetime.today() - review_date).days
    review_date = review_date.strftime("%m/%d/%Y")
    return review_date, days_since_review


def __handle_review_text(review_text, opinion):
    review_text = review_text.replace(opinion, "")
    review_text = review_text.replace(" · ", "")
    return review_text.strip()


def __build_tags(review):
    tags = []
    room_info = __element_text_by_class(review, "c-review-block__room-info")
    if room_info is not None:
        regex_match = re.search("[0-9]\snight[s]*", room_info)
        if regex_match is not None:
            regex_match = regex_match.group(0)
            tags.append(" Stayed " + regex_match)

    stayed_in = __element_text_by_class(review, "c-review-block__room-info__name")
    if stayed_in is not None:
        tags.append(stayed_in.replace("Stayed in: ", ""))
    if len(tags) > 0:
        tags_string = '"['
        for tag in tags:
            tags_string += "'" + tag.split("\n")[0].replace("\n", "") + " ', "
        tags_string = tags_string[:-2]
        return tags_string + ']"'
    else:
        return ""


if __name__ == "__main__":
    driver = setup_webdriver_and_url()
    try:
        accept_cookies(driver)
        handle_hotel_info(driver)
        open_reviews_tab(driver)
        get_reviews_tab(driver)
    except Exception as e:
        print(e)
    finally:
        driver.quit()
