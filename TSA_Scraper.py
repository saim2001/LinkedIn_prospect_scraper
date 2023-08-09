from linkedin_utils import *
import pandas as pd
import numpy as np


Industries = ['Airlines and Aviation',
              'Appliances,Electrical and Electronics Manufacturing',
              'Chemical Manufacturing',
              'Computers and Electronics Manufacturing',
              'Food and Beverage Manufacturing',
              'Transportation, Logistics, Supply Chain and Storage']

position = "HR"




def search_profiles(position,location,Indutry,title_keyword):
    # try:
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

    
    try:
        wait_and_click(By.XPATH, "//ul[contains(@class,'filter-list')]/li//button[contains(.,'People')]")   # select people tab
    except:
        page_not_found()
    
    time.sleep(4)

    wait_and_click(By.XPATH, "//ul[contains(@class,'filter-list')]/li//button[contains(.,'Locations')]")  # select location tab
    time.sleep(3)

    driver.find_element(By.XPATH, "//ul[contains(@class,'filter-list')]/li//input[contains(@placeholder,'location')]").send_keys(location)   # send location name
    time.sleep(2)

    wait_and_click(By.CSS_SELECTOR, "div[role='listbox'] div[role='option']:first-child")    # select 1st suggestion
    time.sleep(3)

    wait_and_click(By.XPATH, "//ul[contains(@class,'filter-list')]/li//div[contains(@id,'locations-filter')]//button[contains(.,'Show results')]")   # select show results 
    time.sleep(5)    

    wait_and_click(By.CSS_SELECTOR,"button[class*='all-filters']")
    time.sleep(1)

    wait_and_click(By.XPATH,"//button[contains(.,'Add an industry')]")
    time.sleep(2)
    wait_for_element_to_load(By.XPATH,"(//input[@placeholder='Add an industry'])[1]").send_keys(Indutry)
    time.sleep(1)
    wait_and_click(By.CSS_SELECTOR, "div[role='listbox'] div[role='option']:first-child")
    time.sleep(1)
    wait_for_element_to_load(By.XPATH,"(//label[contains(.,'Title')])[1]//input").send_keys(title_keyword)
    time.sleep(1)
    wait_and_click(By.XPATH,"//ul[contains(@class,'filter-list')]/li//div[contains(@id,'locations-filter')]//button[contains(.,'Show results')]")
    time.sleep(3)

    return 0

def scrape_profiles(filename):
    column = ['linkedin_url']
    profiles = []
    try:
        while True:
            try:

            # all_results = driver.find_elements(By.XPATH, "//ul[contains(@class,'result-list')]/li[@class]//div[contains(@class,'result__item')]")
                all_results = wait_for_elements_to_load(By.XPATH, "//ul[contains(@class,'result-list')]/li[@class]//div[contains(@class,'result__item')]")
            except Exception as e:
                print(e)
                while True:
                    pass
            
            print("-> filtering profiles")
            for result in all_results:
                try:
                    active_profile = result.find_element(By.XPATH, "./div[2]//a[not(contains(.,'LinkedIn Member'))]")
                except:
                    active_profile = None

                if active_profile:
                    profile_url = result.find_element(By.XPATH, "./div[2]//a").get_attribute("href")
                    profiles.append({'linkedin_url':profile_url})
            try:
                scroll_to_bottom()
                time.sleep(1)
                next_btn = driver.find_element(By.XPATH,"//button[@aria-label='Next']")
                if next_btn.is_enabled():
                    next_btn.click()
                    time.sleep(2)
                else:
                    break

                

            except Exception as e:
                print(e)
                pass
        df = pd.DataFrame(profiles,columns=column)
        df.to_csv(filename,index=False)
        return 0
    except Exception as e:
        print(e)
        return 1

    
    keep_open()
def keep_open():
    while True:
        pass




        
def scrape_profiles_info(csv,industry,start,stop):
    columns = ['first_name', 'last_name', 'linkedin_url', 'email','linkedin_headline', 'city', 'state', 'country', 'location_text','position_title', 'company', 'location', 'company_linkedin_url','industry']
    data = []
    df1 = pd.read_csv(csv)

    profiles = df1.loc[start:stop,'linkedin_url']
    # try:
    for profile in profiles:
        try:
            driver.get(profile)
            print(f'=> scraping {profile}')
            time.sleep(3)
            scroll_to_bottom()
            scroll_to_half()
            scroll_to_top()
            time.sleep(3)
            first_name, last_name, linkedin_headline, city, state, country, location_text,email = get_profile_info()
            position_title, company, location, company_linkedin_url = get_experience()
            row = {'first_name' : first_name, 'last_name' : last_name, 'linkedin_url' : profile  , 'email': email, 'linkedin_headline' : linkedin_headline, 'city' : city, 'state' : state, 'country' : country, 'location_text' : location_text,'position_title' : position_title, 'company' : company , 'location' : location, 'company_linkedin_url' : company_linkedin_url, 'industry': industry}
            data.append(row)
        except:
            pass
    df = pd.DataFrame(data,columns=columns)
    df.to_csv('Scraped_profiles_206.csv',index=False)
    return 0
    # except Exception as e:
    #     print(e)
    #     pass

def scrape_comp_profiles_info(csv,industry,start,stop):
    columns = ['first_name', 'last_name', 'linkedin_url', 'email','linkedin_headline', 'city', 'state', 'country', 'location_text','position_title', 'company', 'location', 'company_linkedin_url','industry']
    data = []
    df1 = pd.read_csv(csv)

    profiles = df1.loc[start:stop,'linkedin_url']
    # try:
    for profile in profiles:
        try:
            driver.get(profile)
            print(f'=> scraping {profile}')
            time.sleep(3)
            scroll_to_bottom()
            scroll_to_half()
            scroll_to_top()
            time.sleep(3)
            try:
                wait_and_click(By.XPATH,"//a[contains(@id,'certifications')]")
            except:
                pass
            time.sleep(3)
            comp_urls = wait_for_elements_to_load(By.XPATH,"//section[contains(.,'Licenses & certifications')]//ul[contains(@class,'pvs-list')]//li//a")
            certified = False
            print(comp_urls)
            for i in comp_urls:
                print(i.get_attribute("href"))
                if i.get_attribute("href") == "https://www.linkedin.com/company/6047514/":
                    print('in')
                    certified = True
            time.sleep(3)
            try:
                wait_and_click(By.XPATH,"//button[contains(@aria-label,'Back')]")
            except:
                pass
            time.sleep(3)

            if certified == True:

                print('in2')
                first_name, last_name, linkedin_headline, city, state, country, location_text,email = get_profile_info()
                position_title, company, location, company_linkedin_url = get_experience()
                row = {'first_name' : first_name, 'last_name' : last_name, 'linkedin_url' : profile  , 'email': email, 'linkedin_headline' : linkedin_headline, 'city' : city, 'state' : state, 'country' : country, 'location_text' : location_text,'position_title' : position_title, 'company' : company , 'location' : location, 'company_linkedin_url' : company_linkedin_url, 'industry': industry}
                data.append(row)
                print(row)
        except:
            pass
    print('creating_csv')
    print(data)
    df = pd.DataFrame(data,columns=columns)
    df.to_csv('Scraped_profiles_comp.csv',index=False)
    return 0
    # except Ex
        



# search_profiles(position,'United kingdom',Industries[5],'Training')
# scrape_profiles('scraped_url_205.csv')
# scrape_comp_profiles_info('scraped_urls_404_PE.csv','all',2,3)








