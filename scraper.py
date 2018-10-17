#!/usr/bin/env python3

from io import StringIO
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
import pandas as pd

"""
reference websearcher browser_driver.py
https://github.com/beepscore/websearcher
"""


def get_octable_text(search_string):
    """
    Use browser to request info
    wait for javascript to run and return html for id
    return empty string if timeout or error
    """
    # browser = webdriver.Firefox()
    browser = webdriver.Chrome()

    base_url = "https://www.nseindia.com"
    query_prefix = "/live_market/dynaContent/live_watch/option_chain/optionKeys.jsp?"

    url = base_url + query_prefix + search_string
    browser.get(url)

    try:
        # http://stackoverflow.com/questions/37422832/waiting-for-a-page-to-load-in-selenium-firefox-w-python?lq=1
        # http://stackoverflow.com/questions/5868439/wait-for-page-load-in-selenium
        id_octable = "octable"
        WebDriverWait(browser, 6).until(lambda d: d.find_element_by_id(id_octable).is_displayed())
        octable = browser.find_element_by_id(id_octable)
        return octable.text

    except TimeoutException:
        print("TimeoutException, returning empty string")
        return ""

    except AttributeError:
        # http://stackoverflow.com/questions/9823936/python-how-do-i-know-what-type-of-exception-occured#9824050
        print("AttributeError, returning empty string")
        return ""

    finally:
        browser.quit()


def get_dataframe(search_string):
    """
    :param search_string:
    :return: dataframe
    """

    # avoid duplicate column names
    column_names = ['c_oi', 'c_chng_in_oi', 'c_volume', 'c_iv', 'c_ltp',
                    'c_net_chng', 'c_bid_qty', 'c_bid_price', 'c_ask_price', 'c_ask_qty',
                    'strike price',
                    'p_bid_qty', 'p_bid_price', 'p_ask_price', 'p_ask_qty',
                    'p_net chng', 'p_ltp', 'p_iv', 'p_volume', 'p_chng_in_oi', 'p_oi']

    # read from local data file
    # this can be handy during development
    # df = pd.read_csv('./data/octable.txt', sep=' ', names=column_names, skiprows=10)

    # read from web
    octable_text = get_octable_text(search_string)
    # https://stackoverflow.com/questions/20696479/pandas-read-csv-from-string-or-package-data
    df = pd.read_csv(StringIO(octable_text), dtype=object, sep=' ', names=column_names, skiprows=10)

    return df


if __name__ == '__main__':

    search_string = "segmentLink=17&instrument=OPTIDX&symbol=BANKNIFTY&date=25OCT2018"
    df = get_dataframe(search_string)

    print(df.head())
    """
        c_oi c_chng_in_oi c_volume   ...   p_volume p_chng_in_oi    p_oi
    0      -            -        -   ...        586        5,520  32,760
    1      -            -        -   ...         11          240     760
    2  2,160         -360       18   ...      2,529        3,280  75,960
    3      -            -        -   ...         25          360     640
    4      -            -        -   ...        343       -3,560   7,720
    """

