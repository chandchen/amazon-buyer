# -*- coding: utf-8 -*-
import time

from selenium import webdriver


SITE_URL = 'https://www.amazon.com/'
USERNAME = 'username'
PASSWORD = 'password'
PROXY = '192.168.2.31:8118'
PRODUCTS = 'url'
RED_LIST = 'name'


def webdriver_login(driver, account, passwd):
    driver.find_element_by_id('ap_email').send_keys(account)
    driver.find_element_by_id('ap_password').send_keys(passwd)
    driver.find_element_by_id('signInSubmit').click()
    return driver


def auto_run_amazon():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--proxy-server=http://{}'.format(PROXY))
    chrome_options.add_argument("--start-maximized")
    driver = webdriver.Chrome(chrome_options=chrome_options)

    driver.get(SITE_URL)

    # redirect to login page
    driver.find_element_by_id('a-autoid-0-announce').click()

    # re-check proxy here
    # driver.get("http://httpbin.org/ip")
    # time.sleep(1)
    # print(driver.page_source)

    driver = webdriver_login(driver, USERNAME, PASSWORD)
    time.sleep(1)

    driver.get(PRODUCTS)
    variations = driver.find_element_by_id('variationsTwister')
    variations = variations.find_elements_by_xpath('ul')
    for size_id, variation_type in enumerate(variations):
        contents = variation_type.find_elements_by_xpath('li')
        for color_id, content in enumerate(contents):
            url = 'https://www.amazon.com/?mv_color_name={}&mv_size_name=\
                   {}'.format(color_id, size_id)
            driver.get(url)

    offer_list = driver.find_element_by_id('olpOfferList')
    offers = offer_list.find_elements_by_class_name('olpOffer')
    for offer in offers:
        seller_name = offer.find_element_by_class_name('olpSellerName').text
        if seller_name != RED_LIST:
            offer.find_element_by_name('submit.addToCart').click()
            time.sleep(3)
            driver.find_element_by_id('hlb-ptc-btn-native').click()
            time.sleep(3)
            break

    driver.quit()


if __name__ == '__main__':
    auto_run_amazon()
