from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import requests
import pandas as pd
from bs4 import BeautifulSoup


def whatsapp_login_and_scrape(phone_number,  name_to_search):
    driver = whatsapp_login(phone_number)

    whatsapp_data = scrape_whatsapp(driver, name_to_search)

    driver.quit()

    return whatsapp_data

def whatsapp_login(phone_number):
    driver = webdriver.Chrome(executable_path="Chrome_Driver_Path")  # Update with the correct path to the ChromeDriver

    driver.get("https://web.whatsapp.com/")
    time.sleep(10)
    link_button = driver.find_element(By.XPATH, "//span[@class='_3iLTh' and text()='Link with phone number']")
    link_button.click()
    
    phone_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//input[@aria-label='Type your phone number.']"))
    )
    phone_input.send_keys(phone_number)

    next_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//div[@class='_1M6AF _3QJHf']//div[text()='Next']"))
    )
    next_button.click()

    return driver

def scrape_whatsapp(driver, search_name):
    time.sleep(60)
    html = driver.page_source
    
    soup = BeautifulSoup(html, 'html.parser')
    search_input = driver.find_element(By.XPATH, "//p[@class='selectable-text copyable-text iq0m558w g0rxnol2']")
    search_input.send_keys(search_name)

    search_result = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//div[@role='gridcell']"))
    )

    search_result.click()

    contact_name_element = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//span[@class='ggj6brxn gfz4du6o r7fjleex g0rxnol2 lhj4utae le5p0ye3 l7jjieqr _11JPr']"))
    )

    contact_name_element.click()

    contact_details_element = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//span[@class='l7jjieqr cw3vfol9 _11JPr selectable-text copyable-text']"))
    )

    contact_name = contact_details_element.text

    try:
        status_element = driver.find_element(By.XPATH, "//span[@title='{}']".format(contact_name))
        status = status_element.get_attribute("title")
    except:
        status = None

    return {'Name': contact_name, 'Status': status, 'Registered': 'Yes'}



data = [
    whatsapp_login_and_scrape('82560011167', 'Yuvhraj')
]

df = pd.DataFrame(data)
print(df)
