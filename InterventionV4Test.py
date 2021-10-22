from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException

from random import randint;

import time
import pymysql

user_name ="bernhard.burton"
password = "Bmoskaa1"
hostname = "rds-edapt-uat.cg5bofaurksl.ap-southeast-2.rds.amazonaws.com"
username_db = "edapt-prod"
password_db = "MG3lmJ69Eqnb9EJu"
database = "edapt_ilp"

#Defining connection to Edapt UAT database
def make_EdaptUAT_conn():
    myConnection = pymysql.connect( host=hostname, user=username_db, passwd=password_db, db=database )
    return myConnection

#Closing connection to Edapt UAT database
def close_EdaptUAT_conn():
    myConnection.close()

#Queries query_string to database referred to by connection conn, returns results
def query(query_string, conn):
    cur = conn.cursor()
    cur.execute(query_string)
    return cur.fetchall()

#Returns all combinations of school and staff
def school_staff_query(conn):
    return query("select school_id, staff_id from tbl_school_staff", conn)

#Initialises a chrome driver
def start_chrome_driver():
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(service = Service(r"C:\bin\chromedriver.exe"), options=options)
    return driver

#Finds and clicks an element, with arguments by_type: method of finding element, and string: string to search.
#Takes into consideration page loads.
def find_and_click_elem(by_type, string):
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
def option_exists(selector, option):
    for opt in selector.options:
        if (opt.text == option):
            return True
    return False


#Signs into edapt prod using user_name and password
def sign_in_prod(user_name, password):
    driver.get('https://edapt.education/')
    find_and_click_elem(1, "SIGN IN")
    elements = driver.find_elements(By.TAG_NAME, 'input')
    elements[0].send_keys(user_name)
    elements[1].send_keys(password)
    find_and_click_elem(3, 'button')

#Signs into edapt uat using user_name and password
def sign_in_uat(user_name, password):
    driver.get('https://account.edapt.education/#/login-uat')
    elements = driver.find_elements(By.TAG_NAME, 'input')
    elements[0].send_keys(user_name)
    elements[1].send_keys(password)
    find_and_click_elem(3, 'button')

#Navigates to the Intervention v4 page
def navigate_to_interventionsv4():
    find_and_click_elem(2, "To SP")
    find_and_click_elem(2, "Intervention v4")

#Changes school ID
def change_school_to(school_id):
    #time.sleep(1)
    find_and_click_elem(0, ".fa.fa-cog")

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT, "[new school]")))
    select = Select(driver.find_element(By.ID, 'school_id'))

    if (not option_exists(select, school_id)):
        find_and_click_elem(1, "[new school]")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "input#school_id_new")))
        driver.find_element(By.CSS_SELECTOR, "input#school_id_new").send_keys(school_id)
        find_and_click_elem(1, "[save]")
    else:
        select.select_by_visible_text(school_id)
    
    #time.sleep(1)
    find_and_click_elem(0, "button#btn-switch")


#Changes login ID
def change_staff_id_to(staff_id):
    #time.sleep(1)
    find_and_click_elem(0, ".fa.fa-cog")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "input#staff_id")))
    driver.find_element(By.CSS_SELECTOR, "input#staff_id").clear()
    driver.find_element(By.CSS_SELECTOR, "input#staff_id").send_keys(staff_id)
    find_and_click_elem(0, "button#save-setting")

def dashboard_button_test():
    find_and_click_elem(1, "Dashboard")
    try:
        assert driver.current_url == "https://edapt.education/uat/v31/intervention/v4"
    except AssertionError:
        print("Click of dashboard button did not return to dashboard")

def intervention_numbers_test_PROTOTYPE(int_type):
    try:
        find_and_click_elem(1, int_type)
    except StaleElementReferenceException:
        find_and_click_elem(1, int_type)

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

def intervention_search_test_PROTOTYPE(int_type):
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT, int_type)))
    driver.find_element(By.LINK_TEXT, int_type).click()
    find_and_click_elem(1, int_type)
    print("\nTESTING INTERVENTION SEARCH FOR "+int_type)
    int_cnt = len(driver.find_elements(By.CLASS_NAME, "intervention-point"))

    cur_intervention = randint(0, int_cnt)

#Start up chrome driver
driver = start_chrome_driver()
sign_in_uat(user_name, password)
navigate_to_interventionsv4()

#connect to UAT db
conn = make_EdaptUAT_conn()
school_staff = school_staff_query(conn)

#Prototype to compare intervention numbers and lists for all staff/school combos
cur_school_id = ""
check = False
for element in school_staff:
    if (element[0] != cur_school_id):
        cur_school_id=element[0]
        change_school_to(element[0])
        print("\n\nNOW UPTO SCHOOL: "+element[0]+ "\n**************************************")
        check = True
    change_staff_id_to(element[1])
    print("\nUPTO STAFF: " + element[1]+ "\n----------------------------------------")
    if(check):
        check = False
        intervention_numbers_test_PROTOTYPE("All")
    intervention_numbers_test_PROTOTYPE("Mine")
    intervention_numbers_test_PROTOTYPE("Viewing")


driver.close()