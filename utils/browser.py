from time import sleep
import os


from selenium import webdriver
from selenium.webdriver.chrome.service import Service


def make_chrome_browser(*options):
    chrome_options = webdriver.ChromeOptions()

    if options is not None:
        for option in options:
            chrome_options.add_argument(option)

    if os.environ.get('SELENIUM_HEADLESS') == '1':
        chrome_options.add_argument('--headless')

    browser = webdriver.Chrome(service=Service(), options=chrome_options)
    return browser


if __name__ == '__main__':
    browser = make_chrome_browser('--headless')
    browser.get('https://www.udemy.com/')
    sleep(5)
    browser.quit()
