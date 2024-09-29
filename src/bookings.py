from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import datetime


def get_available_sessions(browser):
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

def book_session_based_on_criteria(browser, sessions, preferredDay, preferredTime):
    # Filter sessions based on preferred days and optionally preferred times
    if preferredTime:
        filtered_sessions = [
            session for session in sessions
            if session['day'] in preferredDay and session['session'] in preferredTime
        ]
    else:
        # If no preferred times are provided, filter by day only
        filtered_sessions = [
            session for session in sessions if session['day'] in preferredDay
        ]

    if not filtered_sessions:
        print("No available sessions that match the preferred criteria.")
        return False

    # Sort the sessions by date and get the earliest one
    earliest_session = filtered_sessions[0]  # Assuming the list is already sorted by date

    try:
        # Click the image button for the selected session
        session_button = WebDriverWait(browser, 30).until(
            EC.element_to_be_clickable((By.ID, earliest_session['id']))
        )
        session_button.click()
        print(f"Clicked on the session for {earliest_session['date']} - Session {earliest_session['session']}")

        # Step 4: Simulate pressing the Enter key to confirm the reservation
        session_button.send_keys(Keys.ENTER)
        print("Pressed Enter to confirm reservation.")



    except Exception as e:
        print(f"Error during the booking process: {e}")
        return False


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


