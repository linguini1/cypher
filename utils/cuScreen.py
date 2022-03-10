# Imports
from selenium.webdriver.common.by import By


# Functions
def login(username: str, password: str, driver):

    """Logs into Thrive health page."""

    # Fill in credentials
    username_field = driver.find_element(By.ID, "userNameInput")
    password_field = driver.find_element(By.ID, "passwordInput")
    login_button = driver.find_element(By.ID, "submitButton")

    username_field.send_keys(username)
    password_field.send_keys(password)
    login_button.click()


def start_assessment(driver):

    """Launch self assessment page."""

    links = driver.find_elements(By.CSS_SELECTOR, "div>div>div>a")
    for link in links:
        if link.text == "Complete your Self-Assessment":
            start_assessment = link

    start_assessment.click()


def respond_no(number_of_questions: int, contingency_runs: int, driver):

    """Responds no to all fields and submits."""

    for _ in range(number_of_questions + contingency_runs):

        response_buttons = driver.find_elements(By.CSS_SELECTOR, "fieldset>label>span")

        for button in response_buttons:
            if button.text == "No":
                button.click()

    # Submit assessment
    submit_button = driver.find_element(By.CSS_SELECTOR, ".MuiBox-root>button")
    submit_button.click()


# Fetching data
def fill_cuScreen(username: str, password: str, driver):

    """Fills out cuScreen self-assessment."""

    URL = "http://cuscreen.carleton.ca/"
    driver.get(URL)

    # Login
    login(username, password, driver)

    # Start assessment
    driver.implicitly_wait(7)  # Long load time
    start_assessment(driver)

    # Click no buttons
    respond_no(6, 5, driver)

    driver.quit()  # End
