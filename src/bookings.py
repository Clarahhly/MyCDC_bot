import os
import time
import pickle
import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from twocaptcha import TwoCaptcha
from selenium.webdriver.support.ui import Select
from solveRecaptcha import solveRecaptcha
import random



def click_month_button(browser):
    """Click the button to filter sessions by a specific month (e.g., October)."""
    try:
        # Locate the button for October and click it
        month_button = WebDriverWait(browser, 30).until(
            EC.element_to_be_clickable((By.ID, "ctl00_ContentPlaceHolder1_IBtnM2"))
        )
        month_button.click()
        print("Clicked on the month button to view October sessions.")
    except Exception as e:
        print(f"Error clicking month button: {e}")


def extract_booked_sessions(browser):
    """Extract upcoming booked sessions from the first table."""
    booked_sessions = []

    # Wait for the booked sessions table to load
    booking_table = WebDriverWait(browser, 30).until(
        EC.presence_of_element_located((By.ID, "ctl00_ContentPlaceHolder1_gvBooked"))
    )

    # Get all rows in the booked sessions table
    rows = booking_table.find_elements(By.TAG_NAME, "tr")

    # Iterate through rows and extract session information
    for row in rows[1:]:  # Skip the header row
        columns = row.find_elements(By.TAG_NAME, "td")
        if len(columns) > 0:
            session_date = columns[0].text
            start_time = columns[2].text
            end_time = columns[3].text

            # Append the session as a tuple (session_date, start_time, end_time)
            booked_sessions.append((session_date, start_time, end_time))

    return booked_sessions


def is_slot_available(booked_sessions, session_date, start_time, end_time):
    """Check if a session slot conflicts with already booked sessions."""
    for booked_session in booked_sessions:
        booked_date, booked_start, booked_end = booked_session

        # Compare the session date and time
        if session_date == booked_date:
            # Check if the time overlaps (basic comparison)
            if not (end_time <= booked_start or start_time >= booked_end):
                return False  # Conflict found

    return True  # No conflict found


def select_available_slot(browser, booked_sessions):
    """Select a slot from the available sessions."""

    # Wait for the available slots table to load
    available_slots_table = WebDriverWait(browser, 30).until(
        EC.presence_of_element_located((By.ID, "ctl00_ContentPlaceHolder1_gvLatestav"))
    )

    # Get all rows in the available slots table
    rows = available_slots_table.find_elements(By.TAG_NAME, "tr")

    # Iterate through rows and extract slot information
    for row in rows[1:]:  # Skip the header row
        columns = row.find_elements(By.TAG_NAME, "td")

        if len(columns) > 0:
            session_date = columns[0].text  # Get the session date
            # Example: start_time and end_time for a session
            start_time = "16:25:00"  # Modify as needed
            end_time = "18:05:00"  # Modify as needed

            # Check if the session is available
            session_button = columns[6].find_element(By.TAG_NAME, "input")  # Adjust index based on the session
            is_available = "Images1.gif" in session_button.get_attribute("src")  # Check if the session is available

            if is_available:
                # Check if this slot conflicts with existing bookings
                if is_slot_available(booked_sessions, session_date, start_time, end_time):
                    session_button.click()  # Click the button to book the session
                    print(f"Booked session on {session_date} from {start_time} to {end_time}")
                    return
                else:
                    print(f"Slot on {session_date} from {start_time} to {end_time} conflicts with existing bookings.")

    print("No available, non-conflicting slots found.")


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


