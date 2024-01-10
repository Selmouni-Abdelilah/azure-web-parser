import azure.functions as func
import logging
import re
import json

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

app = func.FunctionApp()


def get_chrome_driver():
    logging.info("Initializing chrome driver")

    try:
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.198 Safari/537.36 Edg/95.0.1020.30"

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1920x1080")
        chrome_options.add_argument(f"user-agent={user_agent}")

        driver = webdriver.Chrome(options=chrome_options)
        logging.info("Chrome driver initialized successfully")
        return driver
    except:
        logging.error("Error initializing Chrome driver")


def get_page_source(driver, url):
    driver.get(url)

    source = driver.page_source
    logging.info("Amazon page source code: " + driver.page_source)

    return source


def parse_data_for_term(driver, query, pages_to_parse=1):
    data_items = []

    for page_num in range(0, pages_to_parse):
        url = "https://www.amazon.com/s?k=" + query + "&page=" + str(page_num + 1)
        try:
            content = get_page_source(driver, url)
            soup = BeautifulSoup(content, "html.parser")
            all_products = soup.findAll("div", attrs={"class": "s-result-item"})

            for product in all_products:
                asin = product["data-asin"]
                title = ""
                star_rating = ""
                review_count = ""
                price = ""

                if asin != "":
                    try:
                        item = product.find(
                            "a", {"href": re.compile(asin), "class": "a-text-normal"}
                        )
                        title = item.find("span").text.strip()
                        star_rating = (
                            product.find("i", {"class": "a-icon-star-small"})
                            .find("span")
                            .text.strip()
                            .split(" ")[0]
                        )
                        review_count = clean_text(
                            product.find(
                                "a",
                                {
                                    "href": re.compile(asin),
                                    "href": re.compile("Reviews"),
                                },
                            )
                            .find("span")
                            .text.strip()
                            .split(" ")[0]
                        )
                        price = (
                            product.find("span", {"class": "a-price"})
                            .find("span")
                            .text.strip()
                        )
                    except:
                        logging.error("An error has occurred")

                    data_items.append((asin, title, star_rating, review_count, price))
        except Exception as error:
            logging.error(error)
            return (asin, None, None, None)
    return data_items


@app.route(route="SearchAmazonProducts", auth_level=func.AuthLevel.ANONYMOUS)
def SearchAmazonProducts(req: func.HttpRequest) -> func.HttpResponse:
    query = req.params.get("search")
    pages_to_parse = req.params.get("pages")
    pages_to_parse = (
        int(pages_to_parse) if pages_to_parse is None or pages_to_parse is "" else 1
    )

    if query == None or query == "":
        response = {"success": True, "data": None}
        return func.HttpResponse(
            json.dumps(response),
            status_code=200,
        )

    driver = get_chrome_driver()
    asins_data = parse_data_for_term(driver, query, pages_to_parse)
    data_array = list(
        map(
            lambda data: {
                "asin": data[0],
                "title": data[1],
                "rating": data[2],
                "reviewCount": data[3],
                "price": data[4],
            },
            asins_data,
        )
    )
    response = {"success": True, "data": data_array}

    return func.HttpResponse(
        json.dumps(response),
        status_code=200,
        headers={"Content-Type": "application/json"},
    )


def clean_text(str):
    return re.sub("[^A-Za-z0-9]+", "", str)