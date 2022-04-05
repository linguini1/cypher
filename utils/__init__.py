# Imports
from .cuScreen import fill_cuScreen
from .email import create_message, send_email
from .news import create_url, get_titles, get_articles, COUNTRY_CODES


# Functions
def complete_self_assessment(username: str, password: str):

    # Imports
    from selenium import webdriver
    import chromedriver_autoinstaller

    # Check chromedriver install
    chromedriver_autoinstaller.install()

    # Defining browser
    driver = webdriver.Chrome()

    return fill_cuScreen(username, password, driver)


def dispatch(to: str, subject: str = None, body: str = None, is_text: bool = False):

    """Sends the specified email to the specified recipient."""

    # Format message for text or email
    if is_text:
        message = subject
    else:
        message = create_message(subject, body)

    # Get mailer credentials
    with open("./resources/email.txt") as file:
        usr = next(file)
        pswd = next(file)

    # Send email
    send_email(
        to,
        from_=usr,
        message=message,
        password=pswd,
        is_text=is_text
    )

