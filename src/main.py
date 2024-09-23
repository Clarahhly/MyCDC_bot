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
from bookings import book_earliest_thursday
import random

from src.bookings import get_available_sessions


def cdc_bot():
    PATH = r"PATH TO FIND CHROME DRIVER (eg. C:/Users/clara/Downloads/chromedriver-win64/chromedriver.exe)"
    service = Service(PATH)

    # ensure that code is only executed when the script is run directly,
    # not when it is imported as a module in another script.
    if __name__ == '__main__':
        username = "USERNAME"
        password = "PASSWORD"

    # Configure Chrome options (non-headless mode)
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument(r'--user-data-dir= FIND FROM CHROME VERSION')

    # Use the Service object instead of passing PATH directly
    browser = uc.Chrome(service=service, options=chrome_options)
    browser.get("https://www.cdc.com.sg/")

    cookies = pickle.load(open("cookies.pkl", "rb"))

    for cookie in cookies:
        cookie['domain'] = ".cdc.com.sg"

        try:
            browser.add_cookie(cookie)

        except Exception as e:
            print(e)
            print("fail to use cookies")

    browser.get('https://bookingportal.cdc.com.sg/NewPortal/Booking/Dashboard.aspx?')

    # after logging in
    try:

        theory_lesson_button = WebDriverWait(browser, 30).until(
            EC.element_to_be_clickable((By.ID, "ctl00_Menu1_TreeView1t4"))
        )

        theory_lesson_button.click()
        print("Clicked on the theory Lesson button")

        time.sleep(random.uniform(2, 5))  # Random sleep between 2 to 5 seconds


    except Exception as e:
        print(e)
        print("Error clicking theory option")

    try:
        # Wait until the dropdown is visible and clickable
        dropdown = WebDriverWait(browser, 30).until(
            EC.element_to_be_clickable((By.ID, "ctl00_ContentPlaceHolder1_ddlCourse"))
        )

        # Create a Select object for interacting with the dropdown
        select = Select(dropdown)

        # Select "Basic Theory Lesson A (English)" by visible text
        select.select_by_visible_text("Basic Theory Lesson A (English)")
        print("Selected 'Basic Theory Lesson A (English)' from the dropdown")

        time.sleep(random.uniform(2, 5))  # Optional random sleep to mimic human interaction

    except Exception as e:
        print(f"Error selecting the dropdown option: {e}")

    try:
        # from bookings file
        new_sessions = get_available_sessions(browser)
        print(new_sessions)

        book_slot = book_earliest_thursday(browser, new_sessions)

        if book_slot:
            booked = 1
    finally:
        if browser:
            browser.quit()

    # for practical lessons
    """try:
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

    """


cdc_bot()
