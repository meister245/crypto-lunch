import time
from lxml import html
from selenium.common import exceptions
from selenium import webdriver

CHROMEDRIVER_PATH = 'utilities/chromedriver'


class WebScraper:
    def __init__(self):
        pass

    def generate_exchange_page_url(self, exchange_name, tsym=''):
        url = "https://www.cryptocompare.com/exchanges/%s/overview/" % exchange_name.lower()
        return url + tsym if len(tsym) != 0 else url

    def get_exchange_trade_pairs(self, cx_name, cx_pairs):
        """ scrape exchange tsyms from CryptoCompare """
        cx_pairs[cx_name] = {}

        driver = webdriver.Chrome(CHROMEDRIVER_PATH)
        driver.get(self.generate_exchange_page_url(cx_name))

        # get available tsyms for exchange and store them
        tree = html.fromstring(driver.page_source)
        cx_tsyms = \
            tree.xpath(
                "// *[ @ id = \"toolbar-wrapper\"] / div / div[2] / div / ul / li / div / ul / li / a // text()")

        for tsym in cx_tsyms:
            cx_pairs[cx_name][tsym.strip()] = []

        # iterate over tsyms belonging to current exchange and get trade pairs
        for tsym in cx_pairs[cx_name].keys():
            cx_pairs[cx_name][tsym] = self.iterate_exchange_tsyms(cx_name, cx_pairs[cx_name], driver, tsym)

        driver.close()
        return cx_pairs[cx_name]

    def iterate_exchange_tsyms(self, cx_name, cx_tsyms, driver, tsym):
        """ scrape exchange trade pairs from CryptoCompare """
        driver.get(self.generate_exchange_page_url(cx_name, tsym))
        time.sleep(1)

        # click on more button to list all currencies
        try:
            driver.find_element_by_class_name('btn-more-forum').click()
            time.sleep(0.5)
        except exceptions.ElementNotVisibleException:
            pass
        except exceptions.NoSuchElementException:
            driver.refresh()
            driver.find_element_by_class_name('btn-more-forum').click()
            time.sleep(0.5)

        tree = html.fromstring(driver.page_source)
        trade_pairs = \
            tree.xpath(
                "//*[@id=\"col-body\"]/div/div[1]/basic-monitor/div/div/div[3]/table/tbody/tr/td[1]/div[1]/div/span/a/span// text()")

        for t in trade_pairs:
            cx_tsyms[tsym].append(t.split('/')[0])

        return cx_tsyms[tsym]
