import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import random
import time



def cdc_bot():
    PATH = r"C:/Users/clara/Downloads/chromedriver-win64/chromedriver.exe"
    service = Service(PATH)

    # Hardcode the username and password
    username = "00792272"
    password = "Driving2243!"

    # Configure Chrome options (non-headless mode)
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--start-maximized")

    # Use the Service object instead of passing PATH directly
    driver = webdriver.Chrome(service=service, options=chrome_options)

    driver.get("https://www.cdc.com.sg/")  # Replace with the actual URL of the CDC homepage

    try:
        # Click the button to go to the login page
        login_button = WebDriverWait(driver, 30).until(  # Increased timeout to 30 seconds
            EC.presence_of_element_located((By.CLASS_NAME, "dipl_modal_trigger_element"))
        )
        login_button.click()
        print("Clicked on the login button")

        # Input username
        usernamebox = WebDriverWait(driver, 30).until(  # Increased timeout to 30 seconds
            EC.presence_of_element_located((By.ID, "userId_4"))
        )
        usernamebox.send_keys(username)

        time.sleep(8)  # Increased sleep time to 8 seconds

        # Input password
        passwordbox = WebDriverWait(driver, 30).until(  # Increased timeout to 30 seconds
            EC.presence_of_element_located((By.ID, "password_4"))
        )
        passwordbox.send_keys(password)

        time.sleep(8)  # Increased sleep time to 8 seconds

        # Instantiate the RecaptchaSolver and solve the CAPTCHA
        recaptcha_solver = RecaptchaSolver(driver)

        try:
            # Perform CAPTCHA solving
            t0 = time.time()
            recaptcha_solver.solveCaptcha()  # This is the correct way to call the method
            print(f"Time to solve the captcha: {time.time() - t0:.2f} seconds")

        except Exception as e:
            print(f"An error occurred: {e}")
            driver.quit()

        # Wait for manual CAPTCHA solving if the image-based CAPTCHA appears
        input("Please solve the CAPTCHA manually and press Enter to continue...")

        # Click the login button
        login = WebDriverWait(driver, 30).until(  # Increased timeout to 30 seconds
            EC.element_to_be_clickable((By.CLASS_NAME, "BTNSERVICE"))
        )
        login.click()
        print("Login successful")
    except Exception as e:
        print(e)
        print("Error at login")
    finally:
        driver.quit()


cdc_bot()
