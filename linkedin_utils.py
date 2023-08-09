from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import mysql.connector as mysql

from selenium.webdriver.common.keys import Keys

from webdriver_manager.chrome import ChromeDriverManager

import random
import undetected_chromedriver as uc
import re
import pycountry
from http_request_randomizer.requests.proxy.requestProxy import RequestProxy

def create_connection():
    try:
        db = mysql.connect(
            host = configuration['db_host'],
            user = configuration['db_username'],
            password = configuration['db_password'],
            database = configuration['db_name']
        )
        cursor = db.cursor()
        print("✔ Database Connection Formed")

        return db, cursor
    except:
        print("Error in Database Connection")


# connection close
def close_connection(db, cur):
    cur.close()
    db.close()
    print("DB Connection Succesfully Closed")

def extract_email(text):
    # Regular expression pattern for email extraction
    pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b'
    
    # Search for email pattern in the text
    matches = re.findall(pattern, text)
    
    if matches:
        return matches[0]  # Return the first email found
    else:
        return None 


def waitandclickelem(locator, selector, t=15):
    if locator == "XPATH":
        element_present = EC.presence_of_element_located((By.XPATH, selector))
        element = WebDriverWait(driver, t).until(element_present)
    elif locator == "CSS":
        element_present = EC.presence_of_element_located((By.CSS_SELECTOR, selector))
        element = WebDriverWait(driver, t).until(element_present)
    else:
        element_present = EC.presence_of_element_located((By.ID, selector))
        element = WebDriverWait(driver, t).until(element_present)

    driver.execute_script("arguments[0].scrollIntoView();", element)
    time.sleep(1)
    driver.execute_script("arguments[0].click();", element)
    time.sleep(2)


def wait_and_click(by, selector, t=20):
    element_present = EC.presence_of_element_located((by, selector))
    element = WebDriverWait(driver, t).until(element_present)
    
    driver.execute_script("arguments[0].scrollIntoView();", element)
    time.sleep(2)
    driver.execute_script("arguments[0].click();", element)
    time.sleep(3)

def waitforelemtobeclickable(by,selector,t=25):
    element_clickable = EC.element_to_be_clickable((by, selector))
    element = WebDriverWait(driver, t).until(element_clickable)

    return element

def checkifelemexists(BY,selector):
    try:
        # return driver.find_element_by_xpath(xpath)
        return driver.find_element(BY,selector)
    except:
        return None


def wait_for_element_to_load(by, selector, t=25):
    try:
        element_present = EC.presence_of_element_located((by, selector))
        element = WebDriverWait(driver, t).until(element_present)

        return element
    except:
        return

def wait_for_elements_to_load(by, selector, t=25):
    element_present = EC.presence_of_all_elements_located((by, selector))
    element_lst = WebDriverWait(driver, t).until(element_present)
    return element_lst

def scroll_to_half():
    driver.execute_script(
        "window.scrollTo({top : Math.ceil(document.body.scrollHeight/2), behavior : 'smooth'});"
    )
    time.sleep(2)
    
    # driver.execute_script(
        # "window.scrollTo(0, Math.ceil(document.body.scrollHeight/2));"
    # )

def scroll_to_top():
    driver.execute_script(
        "window.scrollTo({top:-document.body.scrollHeight,behavior:'smooth'});"
    )
    time.sleep(3)
    # driver.execute_script(
    #     "window.scrollTo(0, 0);"
    # )

def scroll_to_bottom():
    driver.execute_script(
        "window.scrollTo({top:document.body.scrollHeight,behavior:'smooth'});"
    )
    time.sleep(4)

    # driver.execute_script(
    #     "window.scrollTo(0, document.body.scrollHeight);"
    # )

def page_not_found():
    """ function to manage 404 page """
    for _ in range(3):
        if "Page not found" in driver.page_source:
            driver.refresh()
            time.sleep(3)
        else:
            break

def teardown():
    # driver.close()
    driver.quit()
    print("Driver successfully closed")

def click_home():
    waitandclickelem("CSS","nav>ul>li:first-child>a")
    time.sleep(4)

def random_stuff():
    print("- performing some random actions..")
    driver.find_element(By.CSS_SELECTOR,"input[placeholder='Search']").click()
    time.sleep(3)
    driver.find_element(By.CSS_SELECTOR,"input[placeholder='Search']").send_keys(random.choice(queries_01))
    time.sleep(4.5)
    driver.find_element(By.CSS_SELECTOR,"input[placeholder='Search']").send_keys(Keys.ENTER)
    time.sleep(6)

    scroll_to_half()
    scroll_to_bottom()
    scroll_to_top()

    time.sleep(5)


def search_by_position(position, location):

    driver.find_element(By.CSS_SELECTOR,"input[placeholder='Search']").click()
    time.sleep(3)
    driver.find_element(By.CSS_SELECTOR,"input[placeholder='Search']").send_keys(position)
    time.sleep(4.5)
    driver.find_element(By.CSS_SELECTOR,"input[placeholder='Search']").send_keys(Keys.ENTER)
    time.sleep(6)

    scroll_to_half()
    scroll_to_bottom()
    scroll_to_top()

    time.sleep(5)

    waitforelemtobeclickable(By.XPATH, "//ul[contains(@class,'filter-list')]/li//button[contains(.,'People')]").click()   # select people tab
    time.sleep(4)

    waitforelemtobeclickable(By.XPATH, "//ul[contains(@class,'filter-list')]/li//button[contains(.,'Locations')]").click()   # select location tab
    time.sleep(3)

    driver.find_element(By.XPATH, "//ul[contains(@class,'filter-list')]/li//input[contains(@placeholder,'location')]").send_keys(location)   # send location name
    time.sleep(4)

    waitforelemtobeclickable(By.CSS_SELECTOR, "div[role='listbox'] div[role='option']:first-child").click()    # select 1st suggestion
    time.sleep(3)

    waitforelemtobeclickable(By.XPATH, "//ul[contains(@class,'filter-list')]/li//div[contains(@id,'locations-filter')]//button[contains(.,'Show results')]").click()   # select show results 
    time.sleep(5)

    scroll_to_half()
    scroll_to_bottom()
    scroll_to_top()
    time.sleep(5)

def get_profile_info():
    """ function to get profile information """
    name_elem = wait_for_element_to_load(By.CSS_SELECTOR,"div.relative h1.break-words")
    name_data = name_elem.text.split(" ")
    first_name,last_name = (name_data[0], name_data[-1]) if len(name_data)>1 else (name_data[0],'')
    linkedin_headline = wait_for_element_to_load(By.CSS_SELECTOR, "div.relative div.break-words").text
    location = wait_for_elements_to_load(By.CSS_SELECTOR, "div.relative div>span.break-words")

    about = wait_for_element_to_load(By.XPATH,"((//section[contains(.,'About')])[3]//div[contains(@class,'show-more')]//span)[1]")

    email = extract_email(about.text)

    location = location[-1]
    city, state, country, location_text = (None,None,None,None)
    if location:
        location_text = location.text.strip()
        raw_location = location.text.split(",")
        if len(raw_location) == 3:
            city, state, country = raw_location[0].strip(), raw_location[1].strip(), raw_location[2].strip()
        elif len(raw_location) == 2:
            city, country = raw_location[0].strip(), raw_location[1].strip()
        else:
            country = raw_location[-1].strip() 

    return first_name, last_name, linkedin_headline, city, state, country, location_text,email

def get_experience():
    """ function to get experience """
    # try:
    main_list = wait_for_element_to_load(by=By.CSS_SELECTOR, selector="div#experience~div>ul.pvs-list")
    position = main_list.find_element(By.XPATH, "li")

    



    position = position.find_element(By.CLASS_NAME,"pvs-entity")
    company_logo_elem, position_details = position.find_elements(By.XPATH,"*")
    company_linkedin_url = company_logo_elem.find_element(By.XPATH,"*").get_attribute("href")
    # company_linkedin_url = company_logo_elem.find_element_by_xpath("*").get_attribute("href")

    # position details
    # position_details_list = position_details.find_elements_by_xpath("*")
    position_details_list = position_details.find_elements(By.XPATH,"*")
    position_summary_details = position_details_list[0] if len(position_details_list) > 0 else None
    position_summary_text = position_details_list[1] if len(position_details_list) > 1 else None
    outer_positions = position_summary_details.find_element(By.XPATH,"*").find_elements(By.XPATH,"*")
    outer_positions = position_summary_details.find_element(By.XPATH,"*").find_elements(By.XPATH,"*")
    position_hist = True
    try:
        hist = driver.find_element(By.XPATH,"(//section[contains(.,'Experience')]//ul//li//div[@class='pvs-list__outer-container']//ul//li)[1]//span[contains(@class,'node')]")
        
    except:
        position_hist = False
    # print(job_hist)
    position_title, company, location = (None,None,None)
    if position_hist == True:

        

        company_linkedin_url = wait_for_element_to_load(By.XPATH,"//section[contains(.,'Experience')]//ul//li//a").get_attribute("href")
        company = wait_for_element_to_load(By.XPATH,"//section[contains(.,'Experience')]//ul//li//span").text
        postion_hist = wait_for_element_to_load(By.XPATH,"(//section[contains(.,'Experience')]//ul//li//div[@class='pvs-list__outer-container']//ul/li)[1]")
        # li_items = postion_hist.find_elements(By.XPATH,"//ul//li")
        # print(li_items)
        position_title = wait_for_element_to_load(By.XPATH,"(//section[contains(.,'Experience')]//ul//li//div[@class='pvs-list__outer-container']//ul/li)[1]//div[contains(@class,'t-bold')]//span").text
        info = wait_for_elements_to_load(By.XPATH,"(//section[contains(.,'Experience')]//ul//li//div[@class='pvs-list__outer-container']//ul/li)[1]//span[@aria-hidden='true']")
        location = None
        for i in info:
            for country in pycountry.countries:
                if country.name.upper() in i.text.upper():
                    location = i.text

        return position_title, company, location, company_linkedin_url
    
        # # company = outer_positions.find_element(By.XPATH,"div//div//div//div//span").text
        # company = position_summary_details.find_element(By.XPATH,"a//div//div//div//div//span").text
        # # position_list = job_hist.find_elements(By.XPATH,"*")
        # print(position_list)
        # position = position_list[0].find_element(By.XPATH,"(//div)[2]//div//a//div//div//div//div//span").text
        # try:
        #     location = position_list[1].find_element(By.XPATH,"((//div)[2]//div//a//span)[2]").text
        # except:
        #     location = None


    else:
            
        if len(outer_positions) == 4:
            try:
                position_title = outer_positions[0].find_element(By.TAG_NAME,"span").find_element(By.TAG_NAME,"span").text
            except:
                position_title = outer_positions[0].find_element(By.TAG_NAME,"span").text
            company = outer_positions[1].find_element(By.TAG_NAME,"span").text.split("·")[0].strip()
            location = outer_positions[3].find_element(By.TAG_NAME,"span").text

            # location = outer_positions[3].find_element_by_tag_name("span").text
            # company = outer_positions[1].find_element_by_tag_name("span").text.split("·")[0].strip()
            # position_title = outer_positions[0].find_element_by_tag_name("span").find_element_by_tag_name("span").text
            # work_times = outer_positions[2].find_element_by_tag_name("span").text
        elif len(outer_positions) == 3 or len(outer_positions) == 2:
            try:
                position_title = outer_positions[0].find_element(By.TAG_NAME,"span").find_element(By.TAG_NAME,"span").text
            except:
                position_title = outer_positions[0].find_element(By.TAG_NAME,"span").text
            company = outer_positions[1].find_element(By.TAG_NAME,"span").text.split("·")[0].strip()

            # company = outer_positions[1].find_element_by_tag_name("span").text.split("·")[0].strip()
            # position_title = outer_positions[0].find_element_by_tag_name("span").find_element_by_tag_name("span").text

        return position_title, company, location, company_linkedin_url

           
    # except:
    #     print("❌ Error while getting experience data")
    #     position_title, company, location, company_linkedin_url = (None,None,None,None)
    #     return position_title, company, location, company_linkedin_url
    

# config file 
with open("config.json","r") as config:
    configuration = json.load(config)

def rand_proxy():
    random_proxy = random.choice(configuration['proxy_list'])
    return random_proxy
def initiate_driver(URL):
    try:
        proxy = rand_proxy()
        option = uc.ChromeOptions()
        # Set the user data directory and profile directory for Chrome
        option.add_argument("--user-data-dir=C:/Users/saim rao/AppData/Local/Google/Chrome/User Data/")
        option.add_argument("--profile-directory=Profile 5")
        # option.add_argument(f"--proxy-server={proxy}")
        # option.add_argument('--headless')
        # Initialize Chrome driver with the specified options
        try:
            driver = uc.Chrome(service=Service(ChromeDriverManager().install()), options=option)
        except:
            driver = uc.Chrome(options=option)
        
        # Open the specified URL
        driver.get(URL)
        print('\u2713', f'Driver initiated successfully using proxy address {None}')
        time.sleep(5)
        return driver
    except Exception as e:
        print('\u2717', e)
        return None

driver = initiate_driver("https://myexternalip.com/raw")


# //section[contains(.,'Licenses & certifications')]//ul[contains(@class,'pvs-list')]//li//a
# //a[contains(@id,'certifications')]