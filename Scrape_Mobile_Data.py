from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

path = "D:\Work\chromedriver-win64\chromedriver-win64\chromedriver.exe"
file = open("mobile_information2.csv", "w")

driver = webdriver.Chrome(path)
driver.get('https://www.amazon.in/')
search = driver.find_element(By.XPATH, "/html/body/div[1]/header/div/div[1]/div[2]/div/form/div[2]/div[1]/input")
search.send_keys("mobile",Keys.ENTER)

last_page = None
count = 0
while last_page != "Next":
    count += 1
    print(count)

    # # model_name = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "a-size-medium a-color-base a-text-normal")))
    # model_name = driver.find_elements_by_xpath("//*[@class='a-size-medium a-color-base a-text-normal']")
    # model_price = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "a-price-whole")))
    # rating = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "a-icon-alt")))
    # # no_of_rating = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "a-size-base s-underline-text")))
    # no_of_rating = driver.find_elements_by_xpath("//*[@class='a-size-base s-underline-text']")
    
    items = driver.find_elements(By.XPATH, '//div[contains(@data-component-type, "s-search-result")]')
    for item in items:
        try:
            name = item.find_element(By.XPATH, './/div[contains(@class, "a-section a-spacing-small a-spacing-top-small")]/div/h2/a/span')
            model_name = name.text
        except:
            model_name = 'NotAvailable'
        try:
            price = item.find_element(By.XPATH, './/span[contains(@class,"a-price-whole")]')
            model_price = price.text
        except:
            model_price = 'NotAvailable'
        try:
            ratings = item.find_elements(By.XPATH, './/div[contains(@class, "a-row a-size-small")]/span')
            model_rating = ratings[0].get_attribute('aria-label')
            model_review = ratings[1].get_attribute('aria-label')
            rating=model_rating
            no_of_review=model_review
        except:
            rating='na'
            review='na'
        mobile_data = f'{model_name},{model_price},{rating},{no_of_review}\n'
        file.write(mobile_data)
        time.sleep(0.2)
    # try:
    #     end_page = driver.find_element(By.XPATH, '//span[@class="s-pagination-item s-pagination-next s-pagination-disabled " and @aria-disabled ="true"]')
    #     last_page = end_page.text
    #     time.sleep(2)
    # except:
    #     driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div[1]/div[1]/div/span[3]/div[2]/div[29]/div/div/span/a[3]").click()
    try:
        next_page = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT, "Next")))
        next_page.click()
    except Exception as E:
        # print(E)
        end_page = driver.find_element(By.XPATH, '//span[@class="s-pagination-item s-pagination-next s-pagination-disabled " and @aria-disabled ="true"]')
        time.sleep(2)
        last_page = end_page.text
       
driver.quit()
