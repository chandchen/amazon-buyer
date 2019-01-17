# -*- coding: utf-8 -*-
# import requests
import time

from selenium import webdriver


SITE_URL = 'https://www.amazon.com/'
USERNAME = 'username'
PASSWORD = 'password'
PROXY = '192.168.2.31:8118'


def webdriver_login(driver, account, passwd):
    driver.find_element_by_id('user_login').send_keys(account)
    driver.find_element_by_id('user_password').send_keys(passwd)
    driver.find_element_by_class_name('btn-save').click()

    title = driver.find_element_by_class_name('shortcuts-activity').text
    try:
        assert title == 'Your projects'
        print('Login Success!')
    except AssertionError as e:
        print('Login Failed!')
    return driver


def auto_ordering():
    # profile = webdriver.FirefoxProfile()
    # profile.set_preference('network.proxy.type', 1)
    # profile.set_preference('network.proxy.http', '192.168.2.31')
    # profile.set_preference('network.proxy.http_port', 8118)
    # profile.set_preference('network.proxy.ssl', '192.168.2.31')
    # profile.set_preference('network.proxy.ssl_port', 8118)
    # profile.update_preferences()
    # driver = webdriver.Firefox(profile)

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--proxy-server=http://{}'.format(PROXY))
    driver = webdriver.Chrome(chrome_options=chrome_options)

    driver.get(SITE_URL)
    driver.maximize_window()
    driver.find_element_by_class_name('nav-action-inner').click()
    driver.find_element_by_class_name('nav-action-inner').click()
    time.sleep(3)

    driver.get("http://httpbin.org/ip")
    time.sleep(3)
    print(driver.page_source)

    # driver = webdriver_login(driver, USERNAME, PASSWORD)

    # driver.quit()


if __name__ == '__main__':
    auto_ordering()
