import time
import pickle
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from bookings import book_session_based_on_criteria
import random
from src.bookings import get_available_sessions
from proxy import get_chromedriver


""" input your preferred day and time for booking
    put None if there is no preference """
# eg 08:30 - 10:10, 10:20 - 12:00, 12:45 - 14:25, 14:35 - 16:15, 16:25 - 18:05, 18:50 - 20:30, 20:40 - 22:20
# eg i want tuesday evenings
preferredTime = ["18:50 - 20:30", "20:40 - 22:20"]
preferredDay = ["TUE"]

def cdc_bot(start_time):
    booking_success = False

    # Use the Service object instead of passing PATH directly
    browser = get_chromedriver(use_proxy=True)

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

    # Retry booking until successful
    while not booking_success:
        try:

            # Check elapsed time
            elapsed_time = time.time() - start_time
            if elapsed_time > 900:
                print(f"Exceeded 15 seconds ({elapsed_time:.2f} seconds). Exiting cdc_bot to restart.")
                browser.quit()
                return


            # Wait until the Practical Lesson button is present and clickable by ID
            practical_lesson_button = WebDriverWait(browser, 30).until(
                EC.element_to_be_clickable((By.ID, "ctl00_Menu1_TreeView1t6"))
            )

            practical_lesson_button.click()
            print("Clicked on the Practical Lesson button")
            time.sleep(random.uniform(2, 5))

            # Interact with the dropdown after it loads
            dropdown = WebDriverWait(browser, 30).until(
                EC.presence_of_element_located((By.ID, "ctl00_ContentPlaceHolder1_ddlCourse"))
            )

            # Select the option "04. Class 3A Motorcar (One Team)" using the Select class
            select = Select(dropdown)
            select.select_by_visible_text("04. Class 3A Motorcar (One Team)")
            print("Selected '04. Class 3A Motorcar (One Team)' from the dropdown")
            time.sleep(random.uniform(2, 5))

            # Check if no slots are available
            try:
                no_slots_message = WebDriverWait(browser, 10).until(
                    EC.presence_of_element_located((By.ID, "ctl00_ContentPlaceHolder1_lblFullBookMsg"))
                )

                if "No available slots currently" in no_slots_message.text:
                    print("No available slots currently. Retrying in 2 minutes ")
                    booking_success = False
                    time.sleep(120)  # Wait 2 minutes before retrying
                    continue

            except Exception as e:
                print("No full booking message found, continuing slot selection.")
                booking_success = False

            if booking_success:
                continue

            # Check if there are available slots
            available_sessions = get_available_sessions(browser)
            print(available_sessions)

            book_slot = book_session_based_on_criteria(browser, available_sessions, preferredDay, preferredTime)

            if book_slot:
                print("Successfully booked a slot!")
                booking_success = True
            else:
                print("Failed to book a slot. Retrying in 2 minutes...")
                booking_success = False
                time.sleep(120)  # Wait 2 minutes before retrying

        except Exception as e:
            print(f"Error during booking process: {e}")
            booking_success = False
            time.sleep(120)  # Wait 2 minutes before retrying

    # Quit the browser only if the booking was successful
    try:
        browser.quit()
    except Exception as e:
        print(f"Error closing the browser: {e}")

    print("Booking completed successfully. Exiting program.")


def run_with_retries():
    while True:
        start_time = time.time()
        cdc_bot(start_time)
        elapsed_time = time.time() - start_time

        # Check if the bot completed within 15 minutes, otherwise wait until the 15 minute mark
        if elapsed_time > 900:
            print(f"Elapsed time is {elapsed_time:.2f} seconds. Restarting the bot immediately.")
            continue  # Restart the bot immediately by continuing the loop


run_with_retries()





