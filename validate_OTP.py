from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
from CaptchaSolver import solve_it
from testforCM import push_notif



def fill_things_in_validate_OTD(driver, hard_time, user):
    driver.execute_script("window.scrollTo(0, 700)")
    WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.XPATH, "//input[@id='otp_no']")))  
    enter_otp_here = driver.find_element(By.XPATH, "//input[@id='otp_no']")
    
    value_in_otp_no = enter_otp_here.get_attribute('value')
    print ("value is >> " ,value_in_otp_no)

    solve_captcha_section(driver, hard_time, user)


def solve_captcha_section(driver, hard_time, user):
    driver.execute_script("window.scrollTo(0, 800)")
    
    if hard_time == False:
        while True:
            dir = os.path.join(os.path.dirname(__file__), './Ss_captcha/captcha_OTP.png')

            WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.ID, "LoginCaptcha_CaptchaImage"))) 
            captcha_img = driver.find_element(By.ID, "LoginCaptcha_CaptchaImage")
            captcha_img.screenshot(dir)

            code = solve_it("captcha_OTP")
            if code == -1:
                driver.find_element(By.XPATH, "//img[@id='LoginCaptcha_ReloadIcon']").click()
            else:
                break
    else:
        dir = os.path.join(os.path.dirname(__file__), './Ss_captcha/captcha_OTP.png')
        WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.ID, "LoginCaptcha_CaptchaImage"))) 
        captcha_img = driver.find_element(By.ID, "LoginCaptcha_CaptchaImage")
        captcha_img.screenshot(dir)

        push_notif(f'OTP Captcha user-{user}', f"solve OTP Captcha for user-{user}", 1, "captcha_OTP")
        code = input(f"Enter OTP Captcha code for user-{user} : ")




    WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.XPATH, "//input[@id='captchaCode']")))
    driver.find_element(By.XPATH, "//input[@id='captchaCode']").send_keys(code)

    driver.find_element(By.XPATH, "//input[@name='submit']").click()

    check_invalid_captcha(driver)


def check_invalid_captcha(driver):
    driver.execute_script("window.scrollTo(0, 800)")
    try:
        WebDriverWait(driver, 7).until(EC.presence_of_all_elements_located((By.XPATH, "//div[@class='col-sm-12']")))
        invalid_text = driver.find_element(By.XPATH, "//div[@class='col-sm-12']").text
        if "Invalid" in invalid_text:
            click_LoginCaptcha_ReloadIcon(driver)
            solve_captcha_section(driver)
    except:
        return False

def click_LoginCaptcha_ReloadIcon(driver):
    driver.execute_script("window.scrollTo(0, 800)")

    WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.XPATH,
                                                "//a[@id='LoginCaptcha_ReloadLink']")))
    driver.find_element(By.XPATH, "//img[@id='LoginCaptcha_ReloadIcon']").click()

