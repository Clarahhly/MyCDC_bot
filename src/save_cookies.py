import time
import pickle
import random
import undetected_chromedriver as uc
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from solveRecaptcha import solveRecaptcha
from proxy import get_chromedriver

def cookie_bot():
    username = "USERNAME"
    password = "PASSWORD"

    browser = get_chromedriver(use_proxy=True)
    browser.get("https://www.cdc.com.sg/")

    # Click the button to go to the login page
    login_button = WebDriverWait(browser, 30).until(  # Increased timeout to 30 seconds
        EC.presence_of_element_located((By.CLASS_NAME, "dipl_modal_trigger_element"))
    )
    login_button.click()
    print("Clicked on the login button")

    # Input username
    usernamebox = WebDriverWait(browser, 30).until(  # Increased timeout to 30 seconds
         EC.presence_of_element_located((By.ID, "userId_4"))
    )
    usernamebox.send_keys(username)


    # Input password
    passwordbox = WebDriverWait(browser, 30).until(  # Increased timeout to 30 seconds
        EC.presence_of_element_located((By.ID, "password_4"))
    )
    passwordbox.send_keys(password)

    time.sleep(random.uniform(2, 5))  # Random sleep between 2 to 5 seconds


    result = solveRecaptcha(
        "6LePQLQjAAAAALf3ZDUoa4Tu5b2KnXPbaJTNujGw",
        "https://www.cdc.com.sg/"
    )

    code = result['code']

    print(code)

    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, 'g-recaptcha-response'))
    )

    browser.execute_script(
        "document.getElementById('g-recaptcha-response').innerHTML = " + "'" + code + "'")

    time.sleep(random.uniform(2, 5))  # Random sleep between 2 to 5 seconds


    #Click the login button
    login = WebDriverWait(browser, 30).until(  # Increased timeout to 30 seconds
        EC.element_to_be_clickable((By.CLASS_NAME, "BTNSERVICE"))
    )
    login.click()
    print("Login successful")

    time.sleep(random.uniform(2, 5))

    cookies = browser.get_cookies()

    pickle.dump(cookies, open("cookies.pkl", "wb"))

    if browser:
        browser.quit()

cookie_bot()