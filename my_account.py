from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from CaptchaSolver import solve_it
import os
from time import sleep

def fill_all_element(driver, ApplicationReferenceNumber,TravelDocumentNumber, year, month, day):
    driver.execute_script("window.scrollTo(0, 500)") 
    driver.find_element(By.CSS_SELECTOR, "#webReference").send_keys(ApplicationReferenceNumber)

    driver.find_element(By.ID, 'dateOfBirth').click()
    driver.find_element(By.XPATH, '//div[@class="ui-datepicker-title"]//select[@class="ui-datepicker-year"]').click()
    driver.find_element(By.XPATH, f'//div[@class="ui-datepicker-title"]//select[@class="ui-datepicker-year"]//option[@value="{year}"]').click()
    driver.find_element(By.XPATH, '//div[@class="ui-datepicker-title"]//select[@class="ui-datepicker-month"]').click()
    driver.find_element(By.XPATH, f'//div[@class="ui-datepicker-title"]//select[@class="ui-datepicker-month"]//option[@value="{month}"]').click()
    driver.find_element(By.XPATH, f'//div[@id="ui-datepicker-div"]//table[@class="ui-datepicker-calendar"]//a[text()="{day}"]').click()

    driver.find_element(By.NAME, "passportNo").send_keys(TravelDocumentNumber)

    print ("my_account page filled")

    #scroll down
    driver.execute_script("window.scrollTo(0, 700)") 

    sleep(3)

    while True:
        dir = os.path.join(os.path.dirname(__file__), f'./Ss_captcha/captcha_myaccount.png')
        captcha_img = driver.find_element(By.XPATH, '//div[@class="BDC_CaptchaImageDiv"]//img')
        captcha_img.screenshot(dir)

        code = solve_it(f"captcha_myaccount")
        if code == -1:
            driver.find_element(By.XPATH, "//img[@id='LoginCaptcha_ReloadIcon']").click()
        
        else:
            break


    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.ID, "captchaCode")))
    driver.find_element(By.ID, "captchaCode").send_keys(code)
    driver.find_element(By.XPATH, '//div[@class="btn-block"]//div[@class="col-mobi-12"]//button[@id="SubmitButton"]').click()

def found_invalid_captcha(driver):
    try:
        WebDriverWait(driver, 2).until(EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, '#track-widget > div.box-content > div > p')))
        print (driver.find_element(By.CSS_SELECTOR, "#track-widget > div.box-content > div > p").text)
        return True
    except:
        return False

def logging_in_myaccount(driver, ApplicationReferenceNumber, TravelDocumentNumber, year, month, day):
    fill_all_element(driver, ApplicationReferenceNumber,TravelDocumentNumber, year, month, day)
    while True:
        if found_invalid_captcha(driver):
            fill_all_element(driver, ApplicationReferenceNumber,TravelDocumentNumber, year, month, day)
        else:
            break
        

       