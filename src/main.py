import os
import time
import pickle
import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from solveRecaptcha import solveRecaptcha
from bookings import logout
import random


def cdc_bot():
    PATH = r"C:/Users/clara/Downloads/chromedriver-win64/chromedriver.exe"
    service = Service(PATH)

    # ensure that code is only executed when the script is run directly,
    # not when it is imported as a module in another script.
    if __name__ == '__main__':
        username = "00792272"
        password = "Driving2243!"

    # Configure Chrome options (non-headless mode)
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument(r'--user-data-dir=C:\Users\clara\AppData\Local\Google\Chrome\User Data\Default')


    # Use the Service object instead of passing PATH directly
    browser = uc.Chrome(service=service, options=chrome_options)

    browser.get("https://www.cdc.com.sg/")  # Replace with the actual URL of the CDC homepage

    cookies = pickle.load(open("cookies.pkl", "rb"))

    if cookies:
        for cookie in cookies:
            cookie['domain'] = ".cdc.com.sg"

            try:
                browser.add_cookie(cookie)

            except Exception as e:
                print(e)
                print("fail to use cookies")

        browser.get('https://bookingportal.cdc.com.sg/NewPortal/Booking/Dashboard.aspx?')

    else:
        try:
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
        except Exception as e:
            print(e)
            print("Error at login")

        try:
            #solve captcha
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


        except Exception as e:
            print(f"An error occurred while solving CAPTCHA: {e}")


        try:
            #Click the login button
            login = WebDriverWait(browser, 30).until(  # Increased timeout to 30 seconds
                EC.element_to_be_clickable((By.CLASS_NAME, "BTNSERVICE"))
            )
            login.click()
            print("Login successful")

        except Exception as e:
            print(e)
            print("Error after captcha")



    #after logging in


    try:
        # Wait until the Practical Lesson button is present and clickable
        # Wait until the Practical Lesson button is present and clickable by ID
        practical_lesson_button = WebDriverWait(browser, 30).until(
            EC.element_to_be_clickable((By.ID, "ctl00_Menu1_TreeView1t6"))
        )

        practical_lesson_button.click()
        print("Clicked on the Practical Lesson button")

        time.sleep(random.uniform(2, 5))  # Random sleep between 2 to 5 seconds


    except Exception as e:
        print(e)
        print("Error clicking practial option")


    try:
        #Interact with the dropdown after it loads
        dropdown = WebDriverWait(browser, 30).until(
            EC.presence_of_element_located((By.ID, "ctl00_ContentPlaceHolder1_ddlCourse"))
        )

        #Select the option "04. Class 3A Motorcar (One Team)" using the Select class
        select = Select(dropdown)
        select.select_by_visible_text("04. Class 3A Motorcar (One Team)")
        print("Selected '04. Class 3A Motorcar (One Team)' from the dropdown")

        time.sleep(random.uniform(2, 5))

    except Exception as e:
        print(e)



    #slot selection

    try:
        no_slots_message = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.ID, "ctl00_ContentPlaceHolder1_lblFullBookMsg"))
        )

        if "No available slots currently" in no_slots_message.text:
            print("No available slots currently. Logging out...")
            logout(browser)  # Assuming logout is a function to handle logging out
            return  # Exit the bot if no slots are available
    except Exception as e:
        print("No full booking message found, continuing slot selection.")




    finally:
        if browser:
            browser.quit()


cdc_bot()
