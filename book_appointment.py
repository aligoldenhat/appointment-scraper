from random import random
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from CaptchaSolver import solve_it
from users import find_user
from time import sleep
import os, random, datetime
from other import please_note
from testforCM import push_notif
from validate_OTP import fill_things_in_validate_OTD
from timeit import default_timer as timer
import InterceptingRandR

def reserve_available_oppointment(driver, user, refresh_time, count, hard_time, wire):
    useless_class_name =('old disabled day disabled', 'disabled day disabled', 'day not-avl-day disabled',
                            'new day disabled', 'new disabled day disabled', 'day disabled', 'day holiday-day disabled')

    driver.execute_script("window.scrollTo(0, 500)")

    sleep(2)
    WebDriverWait(driver, 30).until(EC.presence_of_all_elements_located((By.XPATH,
                                        "//p[@class='temp-id']//b[@id='sessionwebrefno']")))
    APN = driver.find_element(By.XPATH, "//p[@class='temp-id']//b[@id='sessionwebrefno']").text
    found_user = find_user(APN, user)
    print (f"APN >>> {APN} >> {found_user[0]} > M: {found_user[1]}")
    start = float('inf')

    flag = True
    while flag:
        driver.execute_script("window.scrollTo(0, 700)")
        print (f"trying to reserve oppintment ({count})> {datetime.datetime.now()}  RT[{round(timer()-start, 3)}s]")

        availableday_oppointments = []

        print (f"CHECK>>  {driver.current_url}")

        try:
            WebDriverWait(driver, 13).until(EC.presence_of_all_elements_located((By.XPATH,
                                            '//div[@class="col-sm-6"]//table[@class=" table-condensed"]//tbody')))
        except Exception as e:
            if "book" in driver.current_url:
                start = timer()
                push_notif(f"user-{user} //tbody", "try another REFRESH", 0)
                print (r"Cant found //tbody >> so try another REFRESH")
                driver.refresh()
                please_note(driver)
                continue

            else:
                raise e


        td_s = driver.find_elements(By.XPATH, '//div[@class="col-sm-6"]//table[@class=" table-condensed"]//tbody//tr//td')
        for td in td_s:
            td_class_name = td.get_attribute("class") 

            if not td_class_name in useless_class_name:
                push_notif(f'italy user-{user}', f"{td_class_name} -- {td.text}", -2)
                if 'regular' in td_class_name:
                    push_notif(f"italy user-{user}", f"{td_class_name} -- {td.text}", -1)
                    
                    print (td.text," opened >> ", td_class_name)
                    opened_td_XPATH = f"//td[@class='{td_class_name}'][normalize-space()='{td.text}']"
                    availableday_oppointments.append(opened_td_XPATH)
        
        if wire:
            driver.request_interceptor = InterceptingRandR.mock_response


        if availableday_oppointments:
            availableday_oppointments = change_order(availableday_oppointments, 0)
        for opened_td in availableday_oppointments:
            driver.execute_script("window.scrollTo(0, 700)")
            refind_opened_td = driver.find_element(By.XPATH, opened_td)
            refind_opened_td.click()

            sleep(5)
            #print (InterceptingRandR.get_specific_request_of_session(driver, "/getSlot", 'response_body'))

            if wire:
                del driver.request_interceptor

            is_loading_display_None(driver)


            if find_no_time_slot_option(driver):
                continue

            click_icheck_helper(driver)
            if not check_time_for_Morning(driver, user, td.text):
                print ('Morning baz nist')
                if not check_time_for_Afternoon(driver, user, td.text):
                    print ('Afternoon ham baz nist')
                    
                else:
                    to_be_continue_solve_captcha(driver, hard_time, user)


                    #print (InterceptingRandR.get_specific_request_of_session(driver, "/getSlot", 'response_body'))


                    if check_invalid_captcha(driver):
                        reserve_available_oppointment(driver, user, refresh_time, count)
                    else:
                        fill_things_in_validate_OTD(driver, hard_time, user)
                        
                    flag = False
                    break
            else:
                to_be_continue_solve_captcha(driver, hard_time, user)
                #print (InterceptingRandR.get_specific_request_of_session(driver, "/getSlot", 'response_body'))

                if check_invalid_captcha(driver):
                    reserve_available_oppointment(driver, user, refresh_time, count)
                else:
                    fill_things_in_validate_OTD(driver, hard_time, user)

                flag = False
                break   
        if not flag:
            break
        
        count += 1
        print ('no oppointment available')
        print (f'sleep({refresh_time})')
        sleep(refresh_time)

        start = timer()
        print ("refreshing")
        driver.refresh()
        please_note(driver)

def change_order(list_of_oppointment, HOW):
    if HOW == 0:
        Len = len(list_of_oppointment)
        how_much_remove = Len - (int(Len/2))
        del(list_of_oppointment[how_much_remove:])
        random.shuffle(list_of_oppointment)
        return list_of_oppointment
    
    elif HOW == 1:
        random.shuffle(list_of_oppointment)
        return list_of_oppointment


def find_no_time_slot_option(driver):
    try:
        WebDriverWait(driver, 1).until(EC.presence_of_all_elements_located((By.XPATH,
                                       "//div[@id='timeSlotOptions']//strong[normalize-space()='No Time slot available for this day']")))
        return True
    except:
        return False

def click_icheck_helper(driver):
    driver.execute_script("window.scrollTo(0, 1050)")
    WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.XPATH,
                                        "//div[@class='styled-radio']//ins[@class='iCheck-helper']")))
    driver.find_element(By.XPATH, "//div[@class='styled-radio']//ins[@class='iCheck-helper']").click()

def check_time_for_Morning(driver, user, regularday):
    useless_classname = 'radio-inline disabled morning'
    driver.execute_script("window.scrollTo(0, 1300)")
    WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.ID, 'Morning')))
    driver.find_element(By.ID, 'Morning').click()

    error_text = driver.find_element(By.XPATH, '//div[@class="select-time-slot"]//div[@class="status-info-box"]//strong')
    if 'slot' in error_text.text:
        return False

    radio_Morning_s = driver.find_elements(By.XPATH, '//div[@id="regular-appointment-cont_185"]//div[@id="avlslot_Morning_185"]//label')
    radio_Morning_s = change_order(radio_Morning_s, 1)

    for radio_Morning in radio_Morning_s:
        radio_Morning_classname = radio_Morning.get_attribute('class')
        if not radio_Morning_classname == useless_classname:
            push_notif(f"italy user-{user}", f"morning opened {regularday}", 2)
            radio_Morning.click()
            return True
    return False
    
def check_time_for_Afternoon(driver, user, regularday):
    useless_classname = 'radio-inline disabled afternoon'
    WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.ID, 'Afternoon')))
    driver.find_element(By.ID, 'Afternoon').click()

    error_text = driver.find_element(By.XPATH, '//div[@class="select-time-slot"]//div[@class="status-info-box"]//strong')
    if 'slot' in error_text.text:
        return False

    radio_Afternoon_s = driver.find_elements(By.XPATH, '//div[@id="regular-appointment-cont_185"]//div[@id="avlslot_Afternoon_185"]//label')
    radio_Afternoon_s = change_order(radio_Afternoon_s, 1)

    for radio_Afternoon in radio_Afternoon_s:
        if not radio_Afternoon.get_attribute("class") == useless_classname:
            push_notif(f"italy user-{user}", f"afternoon opened {regularday}", 2)
            radio_Afternoon.click()
            return True
    return False

def to_be_continue_solve_captcha(driver, hard_time, user):
    driver.execute_script("window.scrollTo(0, 2100)")

    if hard_time == False:
        while True:
            dir = os.path.join(os.path.dirname(__file__), './Ss_captcha/captcha_book.png')
            WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.ID, "LoginCaptcha_CaptchaImage"))) 
            captcha_img = driver.find_element(By.ID, "LoginCaptcha_CaptchaImage")
            captcha_img.screenshot(dir)

            code = solve_it("captcha_book")

            if code == -1:
                driver.find_element(By.XPATH, "//img[@id='LoginCaptcha_ReloadIcon']").click()
            else:
                break
    else:
        dir = os.path.join(os.path.dirname(__file__), './Ss_captcha/captcha_book.png')
        WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.ID, "LoginCaptcha_CaptchaImage"))) 
        captcha_img = driver.find_element(By.ID, "LoginCaptcha_CaptchaImage")
        captcha_img.screenshot(dir)
        
        push_notif(f'BOOK Captcha user-{user}', f"solve book Captcha for user-{user}", 1, "captcha_book")
        code = input(f"Enter book Captcha code for user-{user} : ")


    WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.XPATH, "//input[@id='captchaCode']")))
    driver.find_element(By.XPATH, "//input[@id='captchaCode']").send_keys(code)

    driver.find_element(By.XPATH, '//a[@class="btn btn-primary submit-btn-link book-apointment-btn popup-inline"]').click()

    popup_confirm(driver)

def popup_confirm(driver):
    WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.XPATH,
                                                '//div[@class="btn-container"]//a[@class="btn btn-primary btn-sm confirm-visaapp-hidden"]')))
    driver.find_element(By.XPATH, '//div[@class="btn-container"]//a[@class="btn btn-primary btn-sm confirm-visaapp-hidden"]').click()

def check_invalid_captcha(driver):
    if please_note(driver):
        driver.execute_script("window.scrollTo(0, 1400)")

        text = driver.find_element(By.XPATH, '//div[@class="col-md-7 col-sm-7 col-mobi-12 col-xs-6"]//div[@class="col-sm-12"]').text
        print (text)
        if 'Invalid' in text:
            driver.refresh()
            please_note(driver)

            click_LoginCaptcha_ReloadIcon(driver)
            return True

    else:
        return False

def click_LoginCaptcha_ReloadIcon(driver):
    driver.execute_script("window.scrollTo(0, 1400)")

    WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.XPATH,
                                                "//a[@id='LoginCaptcha_ReloadLink']")))
    driver.find_element(By.XPATH, "//img[@id='LoginCaptcha_ReloadIcon']").click()

def is_loading_display_None(driver):
    try:
        WebDriverWait(driver, 3).until(EC.presence_of_all_elements_located((By.XPATH,
                                                "//div[@id='loading'][@style='display: none;']")))
        return True
    except Exception as e:
        print (e)
        start = timer()
        print ("loading display is BLOCK")
        while True:
            try:
                WebDriverWait(driver, 1).until(EC.presence_of_all_elements_located((By.XPATH,
                                                    "//div[@id='loading'][@style='display: block;']")))
            except:
                WebDriverWait(driver, 2).until(EC.presence_of_all_elements_located((By.XPATH,
                                                "//div[@id='loading'][@style='display: none;']")))
                print (f"loading display is NONE  T[{round(timer() - start, 3)}s]")
                return True
            sleep(1)
            
    

