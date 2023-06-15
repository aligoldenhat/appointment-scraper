from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os


def is_not_complete(driver):
    WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located(
        (By.XPATH, '//div[@class="btn-container"]//a[@class="btn btn-primary btn-sm confirm-visaapp-hidden"]')))
    driver.find_element(By.XPATH, '//div[@class="btn-container"]//a[@class="btn btn-primary btn-sm confirm-visaapp-hidden"]').click()

def please_note(driver):
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located(
            (By.XPATH, '/html/body/div[2]/div/div/div/button')))
        driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div/button').click()
        return True
    except:
        return False

def click_on_cookie_ok(driver):
    try:
        WebDriverWait(driver, 3).until(EC.presence_of_all_elements_located(
            (By.XPATH, '//div[@class="cookies"]//a[@id="cookieOk"]')))
        driver.find_element(By.XPATH, '//div[@class="cookies"]//a[@id="cookieOk"]').click()
    except:
        print ("cant find cookie button")
        

def take_screenshot_from_weird_popup(driver):
    dir = os.path.join(os.path.dirname(__file__), './Ss_captcha/popup.png')
    captcha_img = driver.find_element(By.XPATH, "//div[@class='popup-box width-md close-btn']")
    captcha_img.screenshot(dir)

def close_weird_popup(driver):
    WebDriverWait(driver, 2).until(EC.presence_of_all_elements_located(
        (By.XPATH, "//button[@title='Close (Esc)']")))
    driver.find_element(By.XPATH, "//button[@title='Close (Esc)']").click()

def start_from_main_page(driver):
    close_weird_popup(driver)

    print (driver.current_url)

    # WebDriverWait(driver, 4).until(EC.presence_of_all_elements_located(
    #     (By.XPATH, '//div[@class="nav-container"]//a[@class="toggleMenu"]')))
    # driver.find_element(By.XPATH, '//div[@class="nav-container"]//a[@class="toggleMenu"]').click()

    # driver.execute_script("window.scrollTo(0, 100)")

    # WebDriverWait(driver, 4).until(EC.presence_of_all_elements_located(
    #     (By.XPATH, "//a[normalize-space()='My Account']")))
    # driver.find_element(By.XPATH, "//a[normalize-space()='My Account']").click()

    driver.get("https://www.ckgsir.com/my-account")

    print (driver.current_url)