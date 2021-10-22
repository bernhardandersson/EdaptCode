from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from automateTools import find_and_click_elem, option_exists
from random import randint
import time

#Signs into edapt prod using user_name and password
def sign_in_prod(user_name, password, driver):
    driver.get('https://edapt.education/')
    find_and_click_elem(1, "SIGN IN", driver)
    elements = driver.find_elements(By.TAG_NAME, 'input')
    elements[0].send_keys(user_name)
    elements[1].send_keys(password)
    find_and_click_elem(3, 'button', driver)

#Signs into edapt uat using user_name and password
def sign_in_uat(user_name, password, driver):
    driver.get('https://account.edapt.education/#/login-uat')
    elements = driver.find_elements(By.TAG_NAME, 'input')
    elements[0].send_keys(user_name)
    elements[1].send_keys(password)
    find_and_click_elem(3, 'button', driver)

#Navigates to the Intervention v4 page
def navigate_to_interventionsv4(driver):
    find_and_click_elem(2, "To SP", driver)
    find_and_click_elem(2, "Intervention v4", driver)

#Changes school ID
def change_school_to(school_id, driver):
    find_and_click_elem(0, ".fa.fa-cog", driver)

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT, "[new school]")))
    select = Select(driver.find_element(By.ID, 'school_id'))

    if (not option_exists(select, school_id, driver)):
        find_and_click_elem(1, "[new school]", driver)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "input#school_id_new")))
        driver.find_element(By.CSS_SELECTOR, "input#school_id_new").send_keys(school_id)
        find_and_click_elem(1, "[save]", driver)
    else:
        select.select_by_visible_text(school_id)
    
    #time.sleep(1)
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    time.sleep(1)
    find_and_click_elem(0, "button#btn-switch", driver)


#Changes login ID
def change_staff_id_to(staff_id, driver):
    #time.sleep(1)
    find_and_click_elem(0, ".fa.fa-cog", driver)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "input#staff_id")))
    driver.find_element(By.CSS_SELECTOR, "input#staff_id").clear()
    driver.find_element(By.CSS_SELECTOR, "input#staff_id").send_keys(staff_id)
    find_and_click_elem(0, "button#save-setting", driver)

def dashboard_button_test(driver):
    find_and_click_elem(1, "Dashboard", driver)
    try:
        assert driver.current_url == "https://edapt.education/uat/v31/intervention/v4"
    except AssertionError:
        print("Click of dashboard button did not return to dashboard")

def intervention_numbers_test_PROTOTYPE(int_type, driver):
    try:
        find_and_click_elem(1, int_type, driver)
    except StaleElementReferenceException:
        find_and_click_elem(1, int_type, driver)

    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".number.number--completed")))
        cir_num_com = int(driver.find_element(By.CSS_SELECTOR, ".number.number--completed").text)
    except ValueError:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".number.number--completed")))
        cir_num_com = int(driver.find_element(By.CSS_SELECTOR, ".number.number--completed").text)
    int_cnt_com = len(driver.find_elements(By.CLASS_NAME, "intervention-point.number--completed"))

    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".number.number--inprogress")))
        cir_num_prg = int(driver.find_element(By.CSS_SELECTOR, ".number.number--inprogress").text)
    except ValueError:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".number.number--inprogress")))
        cir_num_prg = int(driver.find_element(By.CSS_SELECTOR, ".number.number--inprogress").text)
    int_cnt_prg = len(driver.find_elements(By.CLASS_NAME, "intervention-point.number--inprogress"))

    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".number.number--notstarted")))
        cir_num_nst = int(driver.find_element(By.CSS_SELECTOR, ".number.number--notstarted").text)
    except ValueError:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".number.number--notstarted")))
        cir_num_nst = int(driver.find_element(By.CSS_SELECTOR, ".number.number--notstarted").text)
    int_cnt_nst = len(driver.find_elements(By.CLASS_NAME, "intervention-point.number--notstarted"))

    try:
        assert cir_num_com == int_cnt_com
    except AssertionError:
        print(int_type+ " COMPLETED: Number of interventions in circle is not equal to number of interventions in list")

    try:
        assert cir_num_prg == int_cnt_prg
    except AssertionError:
        print(int_type+" IN PROGRESS: Number of interventions in circle is not equal to number of interventions in list")

    try:
        assert cir_num_nst == int_cnt_nst
    except AssertionError:
        print(int_type+" NOT STARTED: Number of interventions in circle is not equal to number of interventions in list")

def intervention_search_test_PROTOTYPE(int_type, driver):
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT, int_type)))
    driver.find_element(By.LINK_TEXT, int_type).click()
    find_and_click_elem(1, int_type, driver)
    print("\nTESTING INTERVENTION SEARCH FOR "+int_type)
    int_cnt = len(driver.find_elements(By.CLASS_NAME, "intervention-point"))

    cur_intervention = randint(0, int_cnt)