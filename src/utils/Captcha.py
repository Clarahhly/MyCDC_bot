from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

from solveRecaptcha import solveRecaptcha

PATH = r"C:/Users/clara/Downloads/chromedriver-win64/chromedriver.exe"
service = Service(PATH)


# Configure Chrome options (non-headless mode)
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--start-maximized")

# Use the Service object instead of passing PATH directly
browser = webdriver.Chrome(service=service, options=chrome_options)

browser.get('https://www.google.com/recaptcha/api2/demo')

result = solveRecaptcha(
    "6Le-wvkSAAAAAPBMRTvw0Q4Muexq9bi0DJwx_mJ-",
    "https://www.google.com/recaptcha/api2/demo"
)

code = result['code']

print(code)

WebDriverWait(browser, 10).until(
    EC.presence_of_element_located((By.ID, 'g-recaptcha-response'))
)

browser.execute_script(
    "document.getElementById('g-recaptcha-response').innerHTML = " + "'" + code + "'")

browser.find_element(By.ID, "recaptcha-demo-submit").click()

time.sleep(120)