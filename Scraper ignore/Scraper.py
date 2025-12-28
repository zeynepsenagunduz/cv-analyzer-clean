import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
import time
import pickle
import os 
from  credentials import credentials



def check_cookies():
    try:
        cookies = pickle.load(open("cookies.pkl", "rb"))
        return cookies
    except:
        return False


def check_cookie_is_valid(driver):
    try:
        element_present = EC.presence_of_element_located((By.XPATH,'//*[@id="session_key"]'))
        WebDriverWait(driver, 10).until(element_present)
    except:
        return True
    return False




def login_process(driver):

    print("Login process started...")
    print("Opening Linkedin...")
    driver.get('https://tr.linkedin.com/')
    time.sleep(5)

    print("Clicking login button...")
    # find username input, select it and send username
    element_present = EC.presence_of_element_located((By.XPATH,'//*[@id="session_key"]'))
    WebDriverWait(driver, 60).until(element_present)
    driver.find_element(By.XPATH,'//*[@id="session_key"]').click()
    time.sleep(1)
    element_present = EC.presence_of_element_located((By.XPATH,'//*[@id="session_key"]'))
    WebDriverWait(driver, 60).until(element_present)
    print("Sending username...")
    driver.find_element(By.XPATH,'//*[@id="session_key"]').send_keys(credentials()['username'])
    time.sleep(1)


    print("Clicking password button...")
    # find password input, select it and send password
    element_present = EC.presence_of_element_located((By.XPATH, '//*[@id="session_password"]'))
    WebDriverWait(driver, 60).until(element_present)
    driver.find_element(By.XPATH, '//*[@id="session_password"]').click()
    time.sleep(1)
    print("Sending password...")
    driver.find_element(By.XPATH, '//*[@id="session_password"]').send_keys(credentials()['password'])
    time.sleep(1)

    print("Clicking login button...")
    # click login button
    driver.find_element(By.XPATH,'//button[@data-id="sign-in-form__submit-btn"]').click()

    if(os.listdir().count('cookies.pkl') == 0):
        print("Saving cookies...")
        pickle.dump(driver.get_cookies(), open("cookies.pkl", "wb"))
    else:
        os.remove('cookies.pkl')
        print("Saving cookies...")
        pickle.dump(driver.get_cookies(), open("cookies.pkl", "wb"))
    # confirmation 
    try:
        print("Checking confirmation button...")
        element_present = EC.presence_of_element_located((By.XPATH,'//*[@id="ember26"]/button[1]'))
        WebDriverWait(driver, 15).until(element_present)
        driver.find_element(By.XPATH,'//*[@id="ember26"]/button[1]').click()
    except:
        pass


def keyword_encoder(keyword):
    return keyword.replace(' ','%20')


def collect_job_posts(driver,keyword):
    title_keywords = ['web','software','ui/ux','ui','ux','frontend','front-end','front end','front-end developer','front end developer','frontend developer','front-end engineer','front end engineer','frontend engineer', 'front-end web developer','front end web developer','frontend web developer','front-end web engineer','front end web engineer','frontend web engineer', ]
    driver.get(f'https://www.linkedin.com/jobs/search/?keywords={keyword_encoder(keyword)}')

    element_present = EC.presence_of_element_located((By.CLASS_NAME,'artdeco-pagination__pages'))
    WebDriverWait(driver, 10).until(element_present)

    page_count_ul = driver.find_element(By.CLASS_NAME,'artdeco-pagination__pages')
    time.sleep(2)
    page_count = int(page_count_ul.find_elements(By.TAG_NAME,'li')[-1].get_attribute('data-test-pagination-page-btn'))

    # collect list of job posts
    element_present = EC.presence_of_element_located((By.CLASS_NAME,'scaffold-layout__list-container'))
    WebDriverWait(driver, 60).until(element_present)

    ul = driver.find_element(By.CLASS_NAME,'scaffold-layout__list-container')
    all_li = ul.find_elements(By.TAG_NAME,'li')
    counter = 1
    for li in all_li:
        # job post link 
        try:
            a_text_list = li.find_element(By.TAG_NAME,'a').text.lower().strip().split()
            intersection_count = len(set(a_text_list).intersection(title_keywords))
            if('ember' in li.get_attribute('id') and intersection_count > 0):
                li.click()
                element_present = EC.presence_of_element_located((By.ID,'job-details'))
                WebDriverWait(driver, 20).until(element_present)
                text = driver.find_element(By.ID,'job-details').text
                if(len(text) > 5):
                    # with open(f'{counter}.txt','w') as f:
                    #     f.write(text)
                    # counter += 1 
                    print(f"JOB TEXT: \n {text}")
                    # text icerisindeki \n \t gibi karakterleri sil ve tum texti tek satir haline getir.
                    new_text = text.replace('\n',' ').replace('\t',' ')
                    with open(f'./fetched_data/frontend_data{counter}.txt','a') as f:
                        counter += 1
                        f.write(new_text + '\n')
                time.sleep(5)
        except:
            time.sleep(2)
            pass


    for page in range(1,page_count):
        start_count = page * 25
        driver.get(f'https://www.linkedin.com/jobs/search/?keywords={keyword_encoder(keyword)}&start={start_count}')

        element_present = EC.presence_of_element_located((By.CLASS_NAME,'artdeco-pagination__pages'))
        WebDriverWait(driver, 10).until(element_present)

        page_count_ul = driver.find_element(By.CLASS_NAME,'artdeco-pagination__pages')
        page_count = int(page_count_ul.find_elements(By.TAG_NAME,'li')[-1].get_attribute('data-test-pagination-page-btn'))

        # collect list of job posts
        element_present = EC.presence_of_element_located((By.CLASS_NAME,'scaffold-layout__list-container'))
        WebDriverWait(driver, 60).until(element_present)

        ul = driver.find_element(By.CLASS_NAME,'scaffold-layout__list-container')
        all_li = ul.find_elements(By.TAG_NAME,'li')
        
        for count,li in enumerate(all_li):
            # job post link 
            try:
                if('ember' in li.get_attribute('id')):
                    li.click()
                    element_present = EC.presence_of_element_located((By.ID,'job-details'))
                    WebDriverWait(driver, 20).until(element_present)
                    text = driver.find_element(By.ID,'job-details').text

                    print(f"JOB TEXT: \n {text}")
                    # text icerisindeki \n \t gibi karakterleri sil ve tum texti tek satir haline getir.
                    new_text = text.replace('\n',' ').replace('\t',' ')
                    if(len(text) > 5):
                        with open(f'frontend_data.txt','a') as f:
                            f.write(text)
                    time.sleep(5)
            except:
                time.sleep(2)
                pass


if __name__ == '__main__':
    keyword = "front end developer"

    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    # options.add_argument("--no-sandbox")
    # options.add_argument("--headless")
    # options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36')
    options.add_experimental_option("detach", True)


    driver = webdriver.Chrome(service=Service("./chromedriver"),options=options)

    driver.get("https://www.linkedin.com")
    cookies = check_cookies()
    if(cookies):
        for cookie in cookies:
            driver.add_cookie(cookie)
        driver.refresh()

        valid = check_cookie_is_valid(driver)
        if(valid):
            collect_job_posts(driver,keyword)
        else:
            login_process(driver)
            collect_job_posts(driver,keyword)
    else:
        login_process(driver)
        collect_job_posts(driver,keyword)







        
    

