from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException

#Initialises a chrome driver
def start_chrome_driver():
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(service = Service(r"C:\bin\chromedriver.exe"), options=options)
    return driver

#Finds and clicks an element, with arguments by_type: method of finding element, and string: string to search.
#Takes into consideration page loads.
def find_and_click_elem(by_type, string, driver):
    if by_type == 0:
        try:
            WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CSS_SELECTOR, string)))
            driver.find_element(By.CSS_SELECTOR, string).click()
        except StaleElementReferenceException:
            WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CSS_SELECTOR, string)))
            driver.find_element(By.CSS_SELECTOR, string).click()
    elif by_type == 1:
        try:
            WebDriverWait(driver,10).until(EC.presence_of_element_located((By.LINK_TEXT, string)))
            driver.find_element(By.LINK_TEXT, string).click()
        except StaleElementReferenceException:
            WebDriverWait(driver,10).until(EC.presence_of_element_located((By.LINK_TEXT, string)))
            driver.find_element(By.LINK_TEXT, string).click()
    elif by_type == 2:
        try:
            WebDriverWait(driver,10).until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, string)))
            driver.find_element(By.PARTIAL_LINK_TEXT, string).click()
        except StaleElementReferenceException:
            WebDriverWait(driver,10).until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, string)))
            driver.find_element(By.PARTIAL_LINK_TEXT, string).click()
    elif by_type == 3:
        try:
            WebDriverWait(driver,10).until(EC.presence_of_element_located((By.TAG_NAME, string)))
            driver.find_element(By.TAG_NAME, string).click()
        except StaleElementReferenceException:
            WebDriverWait(driver,10).until(EC.presence_of_element_located((By.TAG_NAME, string)))
            driver.find_element(By.TAG_NAME, string).click()
    else:
        print("Invalid by_type.")



#Detects whether drop down option exists (by its text) with selector
def option_exists(selector, option, driver):
    for opt in selector.options:
        if (opt.text == option):
            return True
    return False