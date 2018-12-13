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


def url(search_string, date_string):
    """
    date_string of the form ddMONyyyy e.g. 25OCT2018, 31JAN2019
    When requesting options, must be in the future.
    Must be a valid option expiration date for that stock.
    return url
    """
    base_url = 'https://www.nseindia.com'
    query_prefix = '/live_market/dynaContent/live_watch/option_chain/optionKeys.jsp?'
    
    date_query = ''
    if date_string is not None:
        date_query = f'&date={date_string}'

    url_string = base_url + query_prefix + search_string + date_query
    return url_string


def get_text(url, css_id):
    """
    Uses browser to request info.
    Waits for javascript to run and return html. Selects by css_id.
    :param url: url to load
    :param css_id: id of page html element to select
    return string. return empty string if timeout or error
    """
    # browser = webdriver.Firefox()
    browser = webdriver.Chrome()

    browser.get(url)

    try:
        # http://stackoverflow.com/questions/37422832/waiting-for-a-page-to-load-in-selenium-firefox-w-python?lq=1
        # http://stackoverflow.com/questions/5868439/wait-for-page-load-in-selenium
        WebDriverWait(browser, 6).until(lambda d: d.find_element_by_id(css_id).is_displayed())
        element = browser.find_element_by_id(css_id)
        return element.text

    except TimeoutException:
        print("TimeoutException, returning empty string")
        return ""

    except AttributeError:
        # http://stackoverflow.com/questions/9823936/python-how-do-i-know-what-type-of-exception-occured#9824050
        print("AttributeError, returning empty string")
        return ""

    finally:
        browser.quit()


def get_dataframe(url, css_id, column_names):
    """
    :param url: url to load
    :param css_id: id of element to select
    :param column_names: column names for dataframe
    :return: dataframe
    """

    # read from local data file
    # this can be handy during development
    # df = pd.read_csv('./data/banknifty_29nov2018_octable.txt', sep=' ', names=column_names, skiprows=10)

    # read from web
    text = get_text(url, css_id)
    # https://stackoverflow.com/questions/20696479/pandas-read-csv-from-string-or-package-data
    df = pd.read_csv(StringIO(text), dtype=object, sep=' ', names=column_names, skiprows=10)

    return df


if __name__ == '__main__':

    search_string = 'segmentLink=17&instrument=OPTIDX&symbol=BANKNIFTY'
    date_string = '31JAN2019'
    url = url(search_string, date_string)
    print(url)
    # https://www.nseindia.com/live_market/dynaContent/live_watch/option_chain/optionKeys.jsp?segmentLink=17&instrument=OPTIDX&symbol=BANKNIFTY&date=29NOV2018

    css_id = "octable"

    # avoid duplicate column names
    column_names = ['c_oi', 'c_chng_in_oi', 'c_volume', 'c_iv', 'c_ltp',
                    'c_net_chng', 'c_bid_qty', 'c_bid_price', 'c_ask_price', 'c_ask_qty',
                    'strike price',
                    'p_bid_qty', 'p_bid_price', 'p_ask_price', 'p_ask_qty',
                    'p_net chng', 'p_ltp', 'p_iv', 'p_volume', 'p_chng_in_oi', 'p_oi']

    df = get_dataframe(url, css_id, column_names)

    print(df.head(10))
    """
    example output
    
         c_oi c_chng_in_oi c_volume   ...    p_volume p_chng_in_oi     p_oi
    0   2,120            -       26   ...          78          -20   38,460
    1       -            -        -   ...          52          540    5,660
    2  18,700           60        7   ...         541        1,160  160,980
    3       -            -        -   ...          40          560   10,380
    4       -            -        -   ...           -            -    5,720
    """

