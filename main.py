from re import T
from time import sleep
import undetected_chromedriver as UC
from selenium import webdriver
import seleniumwire.undetected_chromedriver as SW
from selenium.webdriver.chrome.options import Options
from testforCM import push_notif
from my_account import logging_in_myaccount
from other import is_not_complete, please_note, click_on_cookie_ok
from book_appointment import reserve_available_oppointment
from users import get_user
import sys, traceback
from InterceptingRandR import mock_response

#argv:  [1]T-int, [2]refresh-time, gui, book, hard, error, nocook, break, wire, safe

inputs = sys.argv
argv_user = sys.argv[1]

if len(inputs) > 2:
        if sys.argv[2].isdigit():
                refresh_time = int(sys.argv[2])
        else:
                refresh_time = 300
else:
        refresh_time = 300

showgui = False
if "gui" in inputs:
        showgui = True

book_only = False
if "book" in inputs:
        book_only = True

show_errors = False
if "error" in inputs:
        show_errors = True

hard_mode = False
if "hard" in inputs:
        hard_mode = True

nocook = False
if "nocook" in inputs:
        nocook = True

add_break = False
if "break" in inputs:
        add_break = True

wire = False
if "wire" in inputs:
        wire = True

safe = False
if "safe" in inputs:
        safe = True

print (f"refresh: {refresh_time} | gui: {showgui} | book: {book_only} | error: {show_errors} | hard: {hard_mode} | nocook: {nocook}")
print (f'break: {add_break} | wire: {wire}')

if argv_user.isnumeric() or argv_user == "T":
        which_user = argv_user
        user = get_user(which_user)
else:
        raise ValueError("only int or 'T' are ellow")



driverLocation = "/usr/bin/chromedriver"
binaryLocation = "/usr/bin/google-chrome"

chrome_options = Options()
if not nocook:
        dir = r"/home/ubuntu/.config/google-chrome/Default"
        chrome_options.add_argument(f"--user-data-dir={dir}")
chrome_options.binary_location = binaryLocation

if not showgui:
        chrome_options.add_argument('--headless')

if safe:
        driver = UC.Chrome(executable_path=driverLocation,
                        options=chrome_options)
else:
        driver = SW.Chrome(executable_path=driverLocation,
                        options=chrome_options)

driver.maximize_window()

#driver.request_interceptor = mock_response

if book_only:
        driver.get("https://www.ckgsir.com/book-appointment")
else:
        driver.get("https://www.ckgsir.com/my-account")

def main(user, driver, refresh_time, hard_time, wire):
        print (driver.current_url)

        if not book_only:
                click_on_cookie_ok(driver)
                

                logging_in_myaccount(driver, user[0], user[1], user[2][0], user[2][1]-1, user[2][2])

                is_not_complete(driver)

        sleep(1)
        please_note(driver)

        reserve_available_oppointment(driver, which_user, refresh_time, 0, hard_time, wire)



if __name__ == "__main__":
        if show_errors:
                try:
                        if hard_mode:
                                main(user, driver, refresh_time, True, wire)
                        else:
                                main(user, driver, refresh_time, False, wire)
                except Exception as e:
                        ex_type, ex_value, ex_traceback = sys.exc_info()
                        trace_back = traceback.extract_tb(ex_traceback)
                        stack_trace = list()
                        for trace in trace_back:
                                stack_trace.append(f"File : {trace[0]} , Line : {trace[1]}, Func.Name : {trace[2]}, Message : {trace[3]}")
                        print (f"{ex_type.__name__}: {ex_value}")
                        print (trace_back[-1])

                        print (e)
                        push_notif(f"Error user-{which_user}", e, 2)
                        if add_break and showgui:
                                breakpoint()
        else:
                if hard_mode:
                        main(user, driver, refresh_time, True, wire)
                else:
                        main(user, driver, refresh_time, False, wire)

                        