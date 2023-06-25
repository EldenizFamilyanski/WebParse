from bs4 import BeautifulSoup
from modules import *
from config_names import *
from openai_util import get_gpt_response

# Disable insecure request warnings (for turning verified requests off)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def get_product_info(url):
    """Get info about a product from its page.
    :param url: URL of a product page
    :return: Dictionary with product info"""

    # Preparing the parser
    response = request_new(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Title
    h1_tags = soup.find_all("h1")
    h1_texts = [tag.get_text() for tag in h1_tags][1]
    title = str([h1_texts])

    # Price
    soup = BeautifulSoup(response.text, 'html.parser')
    span_elements = soup.find_all('span', class_=True)
    if len(span_elements) == 0:
        price = "None"
        amount_in_1_pack = "None"
    else:
        data_list = []
        is_it_price = []
        is_it_amount = []
        for span in span_elements:
            data_list.append(span.get_text())
            is_it_price += [".00₽" in span.get_text()]
            is_it_amount += ["шт." in span.get_text()]

        if True in is_it_price and True in is_it_amount:
            if True in is_it_price:
                index_of_price = is_it_price.index(True)
                price = data_list[index_of_price][:-3]
            else:
                price = "None"

            if True in is_it_amount:
                index_of_amount = is_it_amount.index(True)
                amount_in_1_pack = data_list[index_of_amount][:-3]
            else:
                amount_in_1_pack = "None"
        else:
            price = "None"
            amount_in_1_pack = "None"

    # Description
    div_element = soup.find('div', class_='shop-info')
    # Extract the description within the div element
    description1 = div_element.text.strip()

    text = get_gpt_response(DCT_TASKS['text'], description1, url)

    # Photos and SKU
    base_url = url.rsplit("/", 2)[0]  # Extract the base URL
    two_digits = base_url[-4:-2]  # Extract the two digits
    four_digits = base_url[-4:]  # Extract the four digits
    sku = four_digits  # Create the SKU
    photos = ""

    image_url = f"{PHOTOS_URL}{two_digits}/{four_digits}.jpg"
    response = request_new(image_url, True)
    if response is not None:
        photos += image_url
        delay(0.1)
    i = 1

    while True:
        image_url = f"{PHOTOS_URL}{two_digits}/{four_digits}_{i}.jpg"
        response = request_new(image_url, True)
        if response is not None:
            photos += " " + image_url
            i += 1
        else:
            break

    # Return a dictionary with the product info
    return {  # Return a dictionary with the product info
        'Link_to_product_page': url,
        'Title': title[2:-2],
        'Text': text,
        'Photo': photos,
        'SKU': sku,
        'Tilda UID': f"tilda{sku}",
        'Price': price,
        'Amount in 1 pack': amount_in_1_pack
    }


def get_all_products_info():
    """Get info about all products and save it to a file.
    If filename exists, reads it, otherwise parses all pages and saves to a file.
    :return: DataFrame with product info"""

    # prepare dataframe
    df, first_na_ndex = smart_load()
    if first_na_ndex == "Ready":
        return df
    else:
        my_config.pre_scrape(len(df['Link_to_product_page']))
        # Parsing from other pages
        for index, lnk in enumerate(df['Link_to_product_page']):
            if index < first_na_ndex:
                continue
            my_config.iteration_start(index, lnk)
            info = get_product_info(lnk)
            for key, value in info.items():
                logger.debug(f"{key}: {value}")
                df.loc[index, key] = value
            my_config.iteration_end(index)
            version_io(df, index)
        my_config.post_scrape()
        return df


