# -*- coding: utf-8 -*-
import time
import pytesseract
import urllib.request

from PIL import Image
from selenium import webdriver

from settings import *


def webdriver_login(driver, account, passwd):
    driver.find_element_by_id('ap_email').send_keys(account)
    driver.find_element_by_id('ap_password').send_keys(passwd)
    driver.find_element_by_id('signInSubmit').click()
    return driver


def robot_check(driver):
    """ Check if current page is robot verification page """
    if driver.title == 'Robot Check':
        time.sleep(1)
        try:
            section = driver.find_element_by_class_name(
                'a-spacing-large').find_element_by_xpath("//img[@src]")
            res = urllib.request.urlopen(section.get_attribute('src')).read()
            image_path = './vcode.jpg'
            f = open(image_path, 'wb')
            f.write(res)
            image = Image.open(image_path)
            vcode = pytesseract.image_to_string(image)
            driver.find_element_by_id('captchacharacters').send_keys(vcode)
            driver.find_element_by_xpath("//button[@type]").click()
            robot_check(driver)
        except Exception as e:
            return
    return


def single_product_ordering(driver):
    """ Ordering for single product page """
    driver.get(PRODUCTS)
    try:
        offers = driver.find_element_by_id(
            'olpOfferList').find_elements_by_class_name('olpOffer')
        for offer in offers:
            seller = offer.find_element_by_class_name(
                'olpSellerName').text
            if seller not in WHITE_LIST:
                offer.find_element_by_name('submit.addToCart').click()
                time.sleep(1)
                driver.find_element_by_id('hlb-ptc-btn-native').click()
                time.sleep(1)
                single_product_ordering(driver)
    except Exception as e:
        return


def multi_type_product_ordering(driver):
    """ Ordering for multiple type of product page """
    driver.get(PRODUCTS)
    try:
        variations = driver.find_element_by_id(
            'variationsTwister').find_elements_by_xpath('ul')
    except Exception as e:
        variations = []
    for size_id, var_type in enumerate(variations):
        try:
            contents = var_type.find_elements_by_xpath('li')
        except Exception as e:
            contents = []
        for color_id, content in enumerate(contents):
            driver.get(DYNAMIC_PRODUCTS.format(color_id, size_id))

            offers = driver.find_element_by_id(
                'olpOfferList').find_elements_by_class_name('olpOffer')
            for offer in offers:
                seller = offer.find_element_by_class_name(
                    'olpSellerName').text
                if seller not in WHITE_LIST:
                    offer.find_element_by_name('submit.addToCart').click()
                    time.sleep(1)
                    driver.find_element_by_id('hlb-ptc-btn-native').click()
                    break


def run_amazon_buyer():
    """ Main function of amazon buyer program """
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--proxy-server=http://{}'.format(PROXY))
    chrome_options.add_argument("--start-maximized")
    driver = webdriver.Chrome(chrome_options=chrome_options)

    driver.get("http://httpbin.org/ip")

    if PROXY_ORIGIN in driver.page_source:
        driver.get(SITE_URL)
        robot_check(driver)
        driver.find_element_by_id('a-autoid-0-announce').click()

        driver = webdriver_login(driver, USERNAME, PASSWORD)
        time.sleep(1)

        # driver.get(PRODUCTS)

        single_product_ordering(driver)

        # multi_type_product_ordering(driver)

    driver.quit()


if __name__ == '__main__':
    run_amazon_buyer()
