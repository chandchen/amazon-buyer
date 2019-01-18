# -*- coding: utf-8 -*-
import time

from selenium import webdriver


SITE_URL = 'https://www.amazon.com/'
USERNAME = 'username'
PASSWORD = 'password'
PROXY = '192.168.2.31:8118'
PRODUCTS = 'product_link'
RED_LIST = ''


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
    variation_list = variations.find_elements_by_xpath('ul')
    type_count = []
    for index, ul in enumerate(variation_list):
        type_count.append(0)
        contents = ul.find_elements_by_xpath('li')
        for content in contents:
            # content.click()
            type_count[index] += 1

    offer_list = driver.find_element_by_id('olpOfferList')
    offers = offer_list.find_elements_by_class_name('olpOffer')
    # offers = offer_list.find_elements_by_xpath('//div[@class="olpOffer"]')
    for offer in offers:
        seller_name = offer.find_element_by_class_name('olpSellerName').text
        if seller_name != RED_LIST:
            offer.find_element_by_name('submit.addToCart').click()
            time.sleep(3)
            new_window = driver.current_window_handle
            new_window.find_element_by_id('huc-v2-order-row-buttons')

    driver.quit()


if __name__ == '__main__':
    auto_run_amazon()
