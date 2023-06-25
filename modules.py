import os
import random
import time
import pandas as pd
import urllib3
import requests
from requests import RequestException
from config_names import *

from csl_configloggertime import ConfigLogerTiming
from get_links import get_all_links

# Disable insecure request warnings (for turning verified requests off)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

my_config = ConfigLogerTiming()
logger = my_config.logger


def add_url_with_error(str_url, io_par='a+', file_pth=FILENAME_ERRORS):
    """
    Write the URL with occurred error to the file if there was no previous occurrence.
    :param str_url: URL to write to the file
    :param io_par: Input/output parameter
    :param file_pth: Path to the file
    """

    if io_par == 'a+':
        with open(file_pth, 'a+') as file:
            file.seek(0)  # Move the file pointer to the beginning
            urls = file.read().splitlines()
            if str_url not in urls:
                file.write(str_url + '\n')
                logger.info(f"URL '{str_url}' was written to the file '{file_pth}'")
            else:
                logger.info(f"URL '{str_url}' already exists in the file '{file_pth}'")


def load_data():
    """Load data from a file if it exists, otherwise create a new DataFrame.
    :return: DataFrame"""

    if os.path.isfile(FILENAME_LINKS):
        df = pd.read_csv(FILENAME_LINKS)
        logger.info("Data loaded from file")
        return df
    else:
        df = pd.DataFrame(columns=COLUMN_NAMES)
        df.to_csv(FILENAME_MAIN, index=False)
        return df


def delay(multiplier=1):
    """Sleep for a random amount of time between 1 and 2 seconds.
    :param multiplier: Multiplier for the bounds of the random number
    :return: None"""

    duration = random.uniform(1 * multiplier, 2 * multiplier)
    time.sleep(duration)
    logger.info(f"Waiting {duration.__round__(2)} seconds...")


def request_new(url, image=False):
    """Request with error handling and retrying.
    :param url: URL to request
    :param image: Boolean flag indicating if the request is for an image
    :return: Response object or None"""

    try:
        if image:
            response = requests.head(url, verify=False, timeout=10)
            if response.status_code != 404:
                return response
            else:
                return None
        else:
            response = requests.get(url, verify=False, timeout=10)
            response.raise_for_status()  # Raise an exception if the status code indicates an error
            return response
    except RequestException as e:
        print(f"An error occurred when trying to get {url}: "
              f"Error {e}")
        print("Sleeping for 5-10 minutes before retrying...")
        # Sleep for 5-10 minutes
        minutes = 5
        delay(minutes * 60)
        return request_new(url, image)  # Retry the request after sleeping


def version_io(df, index):
    """Saves a file with a number in the name.
    Deletes the previous file."""

    df.to_csv(FILENAME_MAIN, index=False)
    logger.debug(f"File {FILENAME_MAIN} was saved")


def smart_load():
    """Tries to load data from data.csv file. Checks which index is non-empty for 'Tilda UID' column.
    If there is a NAN value, returns a DataFrame with data from data.csv file and the index of the first empty row.
    If there is no NAN value, returns a DataFrame with data from data.csv file.
    If 'data.csv' doesn't exist, loads data from 'just_links.csv' and returns a DataFrame with links."""

    try:
        df = pd.read_csv(FILENAME_MAIN)
        check_tilda_na = df['Tilda UID'].isna()
        if True in list(check_tilda_na):
            first_na_index = df[check_tilda_na].index[0]
            logger.info(f"Loaded data from 'data.csv' file. Starting from index {first_na_index}.")
            return df, first_na_index
        else:
            logger.info("Loaded data from 'data.csv' file.")
            logger.info("All data was already parsed.")
            return df, 'Ready'

    except FileNotFoundError:
        try:
            df = pd.read_csv(FILENAME_LINKS)
            index = 0
            logger.info(f"Loaded data from '{FILENAME_LINKS}' file.")
            return df, index
        except FileNotFoundError:
            logger.error(f"File '{FILENAME_LINKS}' not found. It means that you haven't parsed the links yet.")
            logger.error("Let's do it now.")
            get_all_links()
