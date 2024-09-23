import os
import time
import pickle
import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import datetime



"""def click_month_button(browser):
    Click the button to filter sessions by a specific month (e.g., October).
    try:
        # Locate the button for October and click it
        month_button = WebDriverWait(browser, 30).until(
            EC.element_to_be_clickable((By.ID, "ctl00_ContentPlaceHolder1_IBtnM2"))
        )
        month_button.click()
        print("Clicked on the month button to view October sessions.")
    except Exception as e:
        print(f"Error clicking month button: {e}")
        
        """


def get_available_sessions(browser):
    """
    Extracts available sessions from the session table on the CDC website.

    :return: A sorted list of dictionaries, each representing an available session with date, day, session,
     and id.
    """
    available_sessions = []

    try:
        # Get the table rows containing session data
        table_rows = browser.find_elements(By.XPATH, '//*[@id="ctl00_ContentPlaceHolder1_gvLatestav"]/tbody/tr')

        # Iterate through rows and check for available slots
        for row in table_rows[1:]:  # Skip header row
            cells = row.find_elements(By.TAG_NAME, 'td')
            date = cells[0].text.strip()  # Date in dd/MMM/yyyy format (e.g., 04/Oct/2024)
            day = cells[1].text.strip()  # Day (e.g., FRI)

            for i in range(2, len(cells)):
                session_cell = cells[i].find_element(By.TAG_NAME, 'input')
                if session_cell and 'Images1.gif' in session_cell.get_attribute('src'):
                    session_data = {
                        'date': datetime.datetime.strptime(date, '%d/%b/%Y'),
                        'day': day,
                        'session': i - 1,  # Session number (starting from 1)
                        'id': session_cell.get_attribute('id')
                    }
                    available_sessions.append(session_data)

    except Exception as e:
        print(f"Error while fetching available sessions: {e}")

    # Sort the available sessions by date
    sorted_sessions = sort_sessions_by_date(available_sessions)

    return sorted_sessions


def sort_sessions_by_date(sessions):
    """
    Sorts a list of session dictionaries by date.

    :param sessions: A list of dictionaries containing session information.
    :return: A sorted list of dictionaries by date.
    """
    # Sort sessions by date
    sorted_sessions = sorted(sessions, key=lambda x: x['date'])

    # Optionally, convert datetime object back to string for readability
    sorted_sessions_list = [
        {
            'date': session['date'].strftime('%d/%b/%Y'),  # Convert datetime back to string
            'day': session['day'],
            'session': session['session'],
            'id': session['id']
        }
        for session in sorted_sessions
    ]

    return sorted_sessions_list


from selenium.webdriver.common.keys import Keys


def book_earliest_thursday(browser, sessions):
    # Step 1: Filter for the earliest Thursday session
    thursday_sessions = [session for session in sessions if session['day'] == 'THU']

    if not thursday_sessions:
        print("No available Thursday sessions.")
        return

    # Step 2: Sort the sessions by date and get the earliest
    earliest_thursday = thursday_sessions[0]  # Assumes the list is already sorted

    try:
        # Step 3: Click the image button for the earliest Thursday session
        session_button = WebDriverWait(browser, 30).until(
            EC.element_to_be_clickable((By.ID, earliest_thursday['id']))
        )
        session_button.click()
        print(f"Clicked on the session for {earliest_thursday['date']} - Session {earliest_thursday['session']}")

        # Step 4: Simulate pressing the Enter key to confirm the reservation
        session_button.send_keys(Keys.ENTER)
        print("Pressed Enter to confirm reservation.")

        # Step 5: Wait for the image to change (indicating the reservation)
        WebDriverWait(browser, 30).until(
            EC.text_to_be_present_in_element_attribute(
                (By.ID, earliest_thursday['id']), "src", "Images2.gif"
            )
        )
        print("Session reserved successfully (Image changed to 'Images2.gif').")

        # Step 6: Click the 'Next' button to proceed to checkout
        next_button = WebDriverWait(browser, 30).until(
            EC.element_to_be_clickable((By.ID, "ctl00_ContentPlaceHolder1_btnCheckout"))
        )
        next_button.click()
        print("Clicked the 'Next' button to proceed to checkout.")

    except Exception as e:
        print(f"Error during the booking process: {e}")



def logout(browser):
    """Click the Logout button to log out."""
    try:
        # Wait for the Logout link to appear and click it
        logout_link = WebDriverWait(browser, 30).until(
            EC.element_to_be_clickable((By.ID, "ctl00_Menu1_TreeView1t38"))
        )
        logout_link.click()
        print("Logged out successfully.")

    except Exception as e:
        print(f"Error logging out: {e}")


