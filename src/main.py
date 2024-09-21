import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from twocaptcha import TwoCaptcha


# Your 2Captcha API Key
API_KEY = "dbabcc2df0eb91a8a022988d96dfbe06"

class RecaptchaSolver:
    def __init__(self, driver):
        self.driver = driver
        self.solver = TwoCaptcha(apiKey=API_KEY)

    def solve_captcha(self):
        # Step 1: Find the reCAPTCHA site key on the page
        try:
            site_key_element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "[data-sitekey]"))
            )
            site_key = site_key_element.get_attribute("data-sitekey")
            page_url = self.driver.current_url
            print(f"Found site key: {site_key}")

            # Step 2: Use 2Captcha to solve the reCAPTCHA
            result = self.solver.recaptcha(sitekey=site_key, url=page_url)
            print("2Captcha result:", result)

            # Step 3: Inject the CAPTCHA solution into the page
            captcha_solution = result["code"]
            self.driver.execute_script(
                'document.querySelector("[name=g-recaptcha-response]").innerText = "{}";'.format(captcha_solution)
            )
            print("Injected CAPTCHA solution into page.")

            return True
        except Exception as e:
            print(f"An error occurred while solving CAPTCHA: {e}")
            return False


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




        # Click the login button
        #login = WebDriverWait(driver, 30).until(  # Increased timeout to 30 seconds
         #   EC.element_to_be_clickable((By.CLASS_NAME, "BTNSERVICE"))
        #)
        #login.click()
        #print("Login successful")

    except Exception as e:
        print(e)
        print("Error at login")
    finally:
        driver.quit()


cdc_bot()
