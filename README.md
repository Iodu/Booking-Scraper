> Current state: a scraper of booking reviews and utilizes basic machine learning algorithms.

# Big Data Booking reviews
## Determining whether a review is positive or negative using a machine learning trained model

### Scraping
The scraping makes use of selenium and (chrome's) webdriver.
Scraped reviews are meant to be appended to a [kaggle dataset](https://www.kaggle.com/jiashenliu/515k-hotel-reviews-data-in-europe).

The **Windows** chromedriver **v80** is included in the repo. It will point to this if Windows is detected. On Linux/Mac it just looks for the chromedriver.
Please consult its documentation when an error occurs.