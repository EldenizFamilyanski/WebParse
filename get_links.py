from urllib.parse import urljoin

import pandas as pd
from bs4 import BeautifulSoup

from config_names import START_URL, FILENAME_LINKS, FILENAME_MAIN
from modules import load_data, logger, delay, request_new


def get_all_links():
    """Get links for all products from all pages and save them to a file.
    If FILENAME_LINKS exists, reads it, otherwise parses all pages and saves to a file.
    :return: List of links to product private pages"""

    df = load_data()
    total_pages = get_total_pages()

    # Parsing from first page
    logger.info(f"Processing page 1/{total_pages}")
    all_links = get_links_from_a_page()

    # Parsing from other pages
    for i in range(2, total_pages + 1):
        logger.info(f"Processing page {i}/{total_pages}")
        delay()
        url = f"{START_URL}/{i}"
        all_links += get_links_from_a_page(url)

    df = pd.concat([df, pd.DataFrame({"Link_to_product_page": value} for value in all_links)],
                   ignore_index=True)
    df.to_csv(FILENAME_LINKS, index=False)
    logger.info(f"Data saved to {FILENAME_MAIN}")

    return df


def get_links_from_a_page(url=None):
    """Get links for all products from a page.
    :param url: URL to parse, if None, uses starting_url
    :return: List of links to product pages"""

    if url is None:
        url = START_URL
    response = request_new(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    links = soup.find_all('a', class_='shop-item-title')
    urls_list = list(urljoin(url, link['href']) for link in links)
    return urls_list


def get_total_pages():
    """Get the total number of pages for pagination.
    :return: Total number of pages"""

    response = request_new(START_URL)
    keyword = '/shop/all/'
    soup = BeautifulSoup(response.content, 'html.parser')
    links = soup.find_all('a', href=lambda href: href and keyword in href)
    total_pages = max([int(link['href'].replace(keyword, '')) for link in links])
    return total_pages
