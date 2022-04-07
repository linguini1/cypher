# Imports
from .cuScreen import fill_cuScreen
from .email import create_message, send_email, cypher_credentials
from .news import create_news_api_url, get_titles, get_articles, COUNTRY_CODES
from .meet import format_meet_url, MEET_ALERT_SUBJECT, meet_alert_body, DEFAULT_CODE


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
    usr, pswd = cypher_credentials()

    # Send email
    send_email(
        to,
        from_=usr,
        message=message,
        password=pswd,
        is_text=is_text
    )


def google_meet_alert(meet_code: str):

    """Sends a google meet alert."""

    # Check if default code is needed
    if not meet_code:
        meet_code = DEFAULT_CODE

    # Get meeting url'
    url = format_meet_url(meet_code)

    # Send out email
    message = create_message(
        subject=MEET_ALERT_SUBJECT,
        body=format_meet_url(url)
    )

    print(message)

    with open("resources/friend_emails.txt", "r") as file:

        address, password = cypher_credentials()

        for email in file:

            send_email(
                to=email,
                from_=address,
                message=message,
                password=password
            )
